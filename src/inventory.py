"""Validate the authoritative classroom material inventory; no LCA coefficients."""
import csv
import math
from pathlib import Path

EXPECTED_G = {'Kettle': 723.0, 'Packaging': 137.8}

def load_bom(path):
    with Path(path).open(encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != ['material','finished_mass_g','scope']:
            raise ValueError('Unexpected classroom BOM schema')
        rows = list(reader)
    if len(rows) != 12:
        raise ValueError('Expected the 12 classroom BOM entries')
    seen=set()
    for r in rows:
        if not r['material'] or r['material'] in seen:
            raise ValueError('Empty or duplicate material')
        seen.add(r['material'])
        mass=float(r['finished_mass_g'])
        if not math.isfinite(mass) or mass <= 0:
            raise ValueError('Physical mass must be finite and positive')
        if r['scope'] not in EXPECTED_G:
            raise ValueError('Unknown scope')
    totals={scope:sum(float(r['finished_mass_g']) for r in rows if r['scope']==scope)
            for scope in EXPECTED_G}
    for scope, expected in EXPECTED_G.items():
        if not math.isclose(totals[scope],expected,rel_tol=0,abs_tol=1e-6):
            raise ValueError(f'{scope} mass does not match assignment')
    return rows, dict(totals, Total=sum(totals.values()))

def write_si(rows, destination):
    with Path(destination).open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f,lineterminator="\n")
        w.writerow(['item_id','material','quantity','unit','scope','source_id','quantity_kind'])
        for i,r in enumerate(rows,1):
            w.writerow([f'BOM-{i:02d}',r['material'],float(r['finished_mass_g'])/1000,
                        'kg',r['scope'],'classroom-bom','finished_mass'])
