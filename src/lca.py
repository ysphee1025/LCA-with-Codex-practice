"""BOM validation and material-only LCIA using reviewed aggregate impact factors.

This module does not solve unlinked unit-process supply chains. Factors must be
cradle-to-material-gate results from one consistent LCIA method/version.
"""
import argparse
import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read_bom(path):
    with open(path, newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise ValueError('Empty BOM')
    seen = set()
    for row in rows:
        mass = float(row['finished_mass_g'])
        if not math.isfinite(mass) or mass <= 0:
            raise ValueError('Mass must be finite and positive')
        if row['material'] in seen or row['scope'] not in {'Kettle', 'Packaging'}:
            raise ValueError('Duplicate material or invalid scope')
        seen.add(row['material'])
    return rows

def inventory_summary(rows):
    sums = {scope: sum(float(r['finished_mass_g']) for r in rows if r['scope'] == scope)
            for scope in ('Kettle', 'Packaging')}
    return {'materials': len(rows), 'kettle_g': sums['Kettle'],
            'packaging_g': sums['Packaging'], 'total_g': sum(sums.values())}

def material_lcia(rows, factors):
    if not factors:
        raise ValueError('No impact factors: retrieve and review database results first')
    methods = {(f['method'], f['method_version']) for f in factors}
    if len(methods) != 1 or any(not x for m in methods for x in m):
        raise ValueError('Use exactly one named LCIA method and version')
    lookup = {}
    units = {}
    materials = {r['material'] for r in rows}
    for f in factors:
        if f['material'] not in materials:
            raise ValueError('Factor for unknown material')
        if not all(f[k].strip() for k in ('category', 'impact_unit', 'dataset_id', 'source')):
            raise ValueError('Missing factor provenance or category')
        if f['boundary'] != 'cradle-to-material-gate':
            raise ValueError('Factor boundary must be cradle-to-material-gate')
        value = float(f['factor_per_kg'])
        if not math.isfinite(value):
            raise ValueError('Nonfinite factor')
        key = (f['material'], f['category'])
        if key in lookup:
            raise ValueError('Duplicate factor')
        if f['category'] in units and units[f['category']] != f['impact_unit']:
            raise ValueError('Inconsistent impact units')
        units[f['category']] = f['impact_unit']
        lookup[key] = value
    output = []
    for row in rows:
        for category, unit in sorted(units.items()):
            key = (row['material'], category)
            if key not in lookup:
                raise ValueError(f'Missing factor for {key}')
            output.append({'material': row['material'], 'scope': row['scope'],
                           'category': category, 'impact_unit': unit,
                           'impact': float(row['finished_mass_g']) / 1000 * lookup[key]})
    return output

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['inventory', 'materials'])
    parser.add_argument('--bom', type=Path, default=ROOT/'data/bom.csv')
    parser.add_argument('--factors', type=Path, default=ROOT/'data/impact_factors.csv')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    try:
        rows = read_bom(args.bom)
        if args.command == 'inventory':
            result = inventory_summary(rows)
        else:
            with args.factors.open(newline='') as f:
                factors = list(csv.DictReader(f))
            contributions = material_lcia(rows, factors)
            result = {'status': 'material-only; not complete kettle cradle-to-gate LCIA',
                      'contributions': contributions}
        text = json.dumps(result, indent=2, allow_nan=False)+'\n'
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(text)
        else:
            print(text, end='')
    except (ValueError, KeyError, OSError) as exc:
        parser.exit(1, f'Error: {exc}\n')

if __name__ == '__main__':
    main()
