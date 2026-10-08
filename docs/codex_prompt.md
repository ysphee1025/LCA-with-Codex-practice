# Codex Classroom — Electric Kettle LCA

You are my LCA research and software development assistant.

We will build an independent, reproducible cradle-to-gate LCA calculation tool for one packaged BC1 1 L electric kettle, following the assignment at:

https://tiangong-lca-decision-lab.ecodino73.chatgpt.site/

## Assignment requirements

Use the provided classroom BOM as the authoritative foreground material inventory.

Product mass: 723.00 g
Packaging mass: 137.80 g
Total mass: 860.80 g

Retrieve the original BOM CSV from:
https://tiangong-lca-decision-lab.ecodino73.chatgpt.site/classroom/kettle-bom.csv

Do not replace these quantities with a newly estimated product BOM.

The system boundary is cradle-to-factory-gate.

Include materials, component manufacturing, assembly, and packaging. Exclude customer delivery, consumer use, and end-of-life.

The principal impact indicator is GWP100, expressed in kg CO2-eq per packaged kettle.

## Primary objective

Build our own transparent LCA calculation tool using process datasets from:

1. TianGong LCA
   https://github.com/tiangong-lca/cli

2. USLCI / Federal LCA Commons
   https://www.lcacommons.gov/lca-collaboration/National_Renewable_Energy_Laboratory/USLCI_Database_Public/datasets

Explore both databases. Do not default to ecoinvent or generic emission factors as substitutes for the required database exploration.

Use the official TianGong CLI and authorized USLCI data interfaces or downloads where feasible.

Document the exact data-access methods, software versions, and any authentication requirements.

Never invent a dataset, UUID, upstream provider, emission factor, or characterization factor.

## Technical requirements

Implement a reproducible Python-based LCA tool.

Prefer an explicit process-based matrix calculation where feasible:

A × s = f
g = B × s
h = C × g

where:
- A represents technosphere exchanges
- s represents process activity levels
- f represents final demand
- B represents elementary flows
- g represents the life cycle inventory
- C represents characterization factors
- h represents LCIA results

Implement proper units, process reference-flow scaling, supplier linking, and upstream burden calculation.

Do not mistake direct unit-process emissions for cumulative life cycle impacts.

Where provider chains cannot be fully resolved, explicitly report the missing providers and prevent unsupported claims of complete cradle-to-gate coverage.

## Data matching and scientific review

For every BOM entry:

1. Search TianGong and USLCI for potential matching processes.
2. Record dataset names, UUIDs, versions, reference units, geographies, and years.
3. Compare relevant candidate processes.
4. Select and justify a preferred provider.
5. Document any proxy, transformation, conversion process, or data gap.
6. Check whether upstream manufacturing energy and material production are included.
7. Avoid double counting.
8. Preserve the full matching and decision history.

Investigate unspecified nylon grade, manufacturing losses, conversion services, assembly electricity, and transportation assumptions.

Distinguish sourced inputs from engineering estimates.

Do not invent numerical assumptions without labeling and justification.

## Calculation and verification

Calculate GWP100 per packaged kettle when suitable inventories and characterization factors are available.

Produce:
- Total GWP100
- Material-level contributions
- Component or process-level contributions
- Manufacturing and packaging contributions
- Top three contributors
- Data-coverage and completeness diagnostics
- Mass and unit checks
- Contribution-sum checks
- Supplier-closure checks
- Uncharacterized-flow diagnostics

Do not silently substitute zero for missing information.

Distinguish independently calculated results from approximations and incomplete screening estimates.

## Repository and documentation

Create a public-GitHub-ready repository with:

- Source code
- Input BOM
- Data retrieval and process mapping scripts
- Dataset manifest and provenance records
- LCIA calculation scripts
- Results and figures
- Automated tests
- README.md
- Codex prompt and human decision log

Follow all ten README requirements provided on the classroom website, including model/run identification, data matching, calculation methods, reproducibility, results, uncertainty, and human decisions.

Avoid publishing secrets, credentials, or datasets without redistribution permission.

## Independent and revised results

First complete and preserve an independent baseline calculation.

Do not overwrite baseline outputs.

Record the baseline Git commit and full 40-character SHA.

After the baseline is verified, change one scientifically meaningful modeling choice.

Before recalculating, record the expected direction of impact.

Calculate and document the revised result, difference from baseline, and explanation.

Preserve both versions for class comparison.

## Workflow

Work through these phases:

Phase 1 — Confirm requirements and set up repository
Phase 2 — Retrieve BOM and inspect TianGong/USLCI access
Phase 3 — Search, evaluate, and map background processes
Phase 4 — Implement the inventory and LCIA solver
Phase 5 — Validate and calculate baseline results
Phase 6 — Create README and freeze baseline commit
Phase 7 — Test one changed choice and prepare revised commit

Start with Phase 1 and Phase 2.

Inspect the available environment, retrieve the required materials, verify database access, and build the project scaffold.

Report the actual findings and unresolved access problems before proceeding to numerical LCA calculations.

Continue autonomously with clearly supported implementation tasks, but request my scientific decision if alternative dataset selections or system-boundary choices would materially change the result.