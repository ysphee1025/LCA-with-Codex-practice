# BC1 1 L Electric Kettle — Independent Cradle-to-Gate LCA

**Status: Phase 1/2 scaffold. No baseline, numerical GWP100, contribution, sensitivity or environmental-impact figures have been calculated.**

This restarted project follows the classroom instructions in [docs/codex_prompt.md](docs/codex_prompt.md). Existing earlier work is preserved in Git history and an external local archive; the former material-factor calculator is not the chosen new architecture.

## 1. Model and run identification
Product: BC1 simple plastic kettle, a representative base case. This branch is `classroom-restart`. Access probes use unique UTC run IDs under `data/provenance/`; these are not LCA result runs. No baseline commit exists yet. The exact ten website README requirements could not be retrieved; these ten sections are provisional.

## 2. Goal, functional unit and system boundary
Functional unit as assigned: **one packaged nominal 1 L electric kettle, ready to leave the manufacturing facility**. Include raw materials, component manufacture, assembly and packaging. Resolve upstream energy, transport and production losses/waste. Exclude customer delivery, consumer use/boiling electricity and end of life. Final gate is after kettle assembly and packaging, not an upstream material supplier gate.

## 3. Foreground inventory and sources
Authoritative assignment totals: product 723.00 g, packaging 137.80 g, total 860.80 g. `data/input/classroom_bom_supplied.csv` retains the classroom BOM supplied by the student; it is not a newly estimated product BOM. The requested original URL is tested by the retrieval script. A successful downloaded CSV is retained separately and validated before adoption. `data/processed/bom_si.csv` converts grams to kg. Finished masses do not establish gross manufacturing inputs or component allocation. Sources and file hashes are in `data/provenance/source_registry.json`.

## 4. Database exploration and matching
Required: TianGong and USLCI/Federal LCA Commons. Neither background database version is selected. TianGong CLI 0.1.27 is installed; process search requires authorized OAuth login. The exact USLCI dataset portal is probed. No datasets, UUIDs or providers have been selected or invented. All 24 material/database searches are tracked as pending in `data/mapping/search_plan.csv`. Candidate decisions will be appended to `candidate_history.csv`, not replaced. Inspect reference units, geography/year, scope, energy inclusion, allocation and upstream suppliers before choosing providers. No ecoinvent or generic factors are used.

## 5. Calculation method and scientific review
Planned process-based Python calculation: **A s = f; g = B s; h = C g**, including normalization to reference production quantities and explicit supplier links. It is not implemented yet. GWP100 method edition and factor version remain unresolved. Phase 4 must diagnose supplier gaps, flow mismatches and uncharacterized flows before complete cradle-to-gate claims. Details: [methodology](docs/phase1-methodology.md).

## 6. Environment and installation
Verified Python 3.12.14, Node 24.19.0, TianGong CLI 0.1.27. Current Python scripts require no third-party packages. From the checkout:

```sh
python3 -m unittest discover -s tests -v
python3 src/access.py
```

Cloud CLI installation and writable session configuration:

```sh
npm --cache /tmp/lca-npm-cache install --prefix /workspace/lca-tools --no-audit --no-fund --save-exact @tiangong-lca/cli@0.1.27
export XDG_STATE_HOME=/workspace/lca-tools/state
export XDG_CONFIG_HOME=/workspace/lca-tools/config
/workspace/lca-tools/node_modules/.bin/tiangong-lca auth status --json
```

Use the official CLI's browser authorization in a trusted terminal. A login on a local computer does not authenticate this cloud machine automatically. Never send passwords/tokens in chat or commit sessions. Authorized non-secret exports can be supplied after checking redistribution rights. `src/access.py --cli PATH` supports an installed CLI elsewhere.

## 7. Reproducibility and data rights
The public repository reproduces BOM/mass/unit checks and read-only access probes only. Background datasets, factors and LCA results are absent. Each probe preserves its own report; downloaded original BOM and search outputs are saved per access run. Raw datasets/search responses must be reviewed for licensing and secrets before publication. Existing provider mappings must not be confused with completed database exploration.

## 8. Actual results and completeness
Only inventory validation results exist in `results/inventory_checks.json`. There is no total GWP, hotspot/top-three ranking, contribution analysis, baseline, revised result or LCIA figure. Absence is not zero impact. The principal blockers are authenticated data acquisition, full upstream linking, manufacturing foreground data and compatible characterization factors.

## 9. Uncertainty and revised model
Unspecified nylon grade, production losses, assembly electricity, manufacturing location and transport remain unresolved. No arbitrary numeric ranges or confidence intervals are reported. After a verified independent baseline, select one meaningful alternative with the student, record expected direction before recalculation and retain baseline/revision inputs, outputs and full Git SHAs.

## 10. Human decisions and references
Human decisions: [decision log](docs/human_decisions.csv). Scientifically material provider/boundary alternatives require human input once real candidates are available.

- Classroom: https://tiangong-lca-decision-lab.ecodino73.chatgpt.site/
- Original BOM: https://tiangong-lca-decision-lab.ecodino73.chatgpt.site/classroom/kettle-bom.csv
- Official CLI: https://github.com/tiangong-lca/cli
- USLCI portal: https://www.lcacommons.gov/lca-collaboration/National_Renewable_Energy_Laboratory/USLCI_Database_Public/datasets
- Assignment screenshot cites EU Electric Kettles preparatory study (2020), Task 4, Tables 4-3, 4-4 and 4-8; primary report not yet independently verified.
