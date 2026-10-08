# BC1 electric kettle cradle-to-gate LCA

## Status
Work in progress: BOM validation and a tested material-only LCIA calculation scaffold are implemented. **No environmental impact results have been calculated.** TianGong process search requires an authenticated session. Dataset selection, supplier-chain closure, component manufacture, assembly, and full LCIA remain outstanding. This repository is not yet a completed LCA submission.

## Goal and scope
Declared unit: **one packaged 1 L electric kettle (BC1 simple plastic kettle), at the factory gate**. BC1 represents a base case, not a named commercial product.

Include material production, component manufacture, assembly and packaging. Account for inbound transport and production waste explicitly where relevant. Exclude customer delivery, use and end of life, including disposal of packaging by the customer. The gate is after packaging at the manufacturing factory, not at the resin supplier.

Before calculation, PP is a predicted contributor because it has the largest mass; stainless steel is another candidate. This is a hypothesis, not a measured finding.

## Inventory and provenance
`data/bom.csv` transcribes the assignment BOM supplied by the student. Source cited by the assignment: EU Electric Kettles preparatory study (2020), Task 4, Tables 4-3, 4-4 and 4-8, printed pp. 26, 27 and 30. The primary report has not yet been independently checked.

- Kettle: 723.00 g
- Packaging: 137.80 g
- Total: 860.80 g

These are finished masses, not gross production inputs. Do not silently assume zero processing loss. Nylon grade and factory assembly electricity are unspecified. `data/assumptions.csv` separates unresolved choices from supplied facts.

## Run locally
Python 3.12 or later; the current Python tools use only the standard library.

```sh
python3 src/lca.py inventory --output results/inventory_summary.json
python3 -m unittest discover -s tests -v
python3 src/lca.py materials
```

The last command intentionally exits with an error until reviewed factors are supplied. It computes **material-only** impacts and cannot establish the full packaged-kettle footprint. It accepts aggregate cradle-to-material-gate LCIA factors per kg, not raw exchanges from an unlinked unit process. Negative factors are permitted for documented credits; nonfinite values, missing materials, mixed methods, duplicate factors and incompatible boundaries are rejected.

## TianGong search
Official CLI: https://github.com/tiangong-lca/cli

The current environment uses Node 24.19.0 and published CLI 0.1.27. Install outside the project to keep tool dependencies separate:

```sh
npm --cache /tmp/lca-npm-cache install --prefix /workspace/lca-tools --no-audit --no-fund --save-exact @tiangong-lca/cli@0.1.27
export XDG_STATE_HOME=/workspace/lca-tools/state
export XDG_CONFIG_HOME=/workspace/lca-tools/config
/workspace/lca-tools/node_modules/.bin/tiangong-lca auth status --json
```

In a trusted terminal on your own machine, install the same CLI and follow its official `auth login` flow. Browser loopback login on a local computer does not automatically authenticate this cloud machine. Never commit sessions, tokens, `.env` files, or put credentials in chat. If cloud login is unavailable, perform searches locally and provide non-secret dataset exports and source metadata, subject to licensing.

After authentication, from this checkout:

```sh
/workspace/lca-tools/node_modules/.bin/tiangong-lca search process --input search_requests/04.json --json
```

The 12 request files are search starting points, not matches. Search **both TianGong and USLCI** for each relevant input. Verify the installed CLI's supported source filter and source identifiers before filtering; do not assume USLCI is covered by an unfiltered search. Record rejected candidates as well as chosen matches.

For each selected dataset record ID, version, database, geography, reference flow/unit, boundary, allocation/recycled content, included conversion processes, upstream suppliers, license, and selection rationale. Use `data/dataset_mapping.csv` as the initial mapping register. Check silicone rubber versus silicon, nylon PA6 versus PA66, stainless alloy grade and cardboard type.

## Completing LCIA
1. Verify available data exports, upstream supplier closure and elementary-flow identities on a PP pilot.
2. Select and freeze one compatible LCIA method/version. Apply it consistently to TianGong and USLCI inventory; never combine incompatible precomputed methods.
3. Obtain material impacts through a linked supply-chain solver or verified aggregated LCI/LCIA. Individual unit-process direct emissions alone omit upstream burdens.
4. Add component conversion, assembly electricity, packaging conversion, inbound transport and production-waste treatment with documented quantities and units. Inspect dataset scope first to avoid double counting.
5. Extend the calculation to those foreground activities and validate full cradle-to-gate totals and category-specific contributions.
6. Compare one changed choice, preferably PA6 versus PA66 if both are available; keep all other settings and the declared unit constant.
7. Write category results, hotspots, limitations and scenario differences here. Document exclusions and data gaps explicitly; missing data is not zero impact.

The empty `data/impact_factors.csv` defines the input schema for the material-only calculator. Do not fill it with guessed environmental coefficients. Raw database exports are ignored until their redistribution license is checked. Public reproducibility must include permitted data or precise retrieval instructions, pinned dataset versions, method and required access.

## Current checks
Seven unit tests passed in the cloud environment, covering assignment mass, kg conversion, absent data, missing coverage, inconsistent methods, duplicate/nonfinite factors and incompatible boundaries. Inventory results are in `results/inventory_summary.json`. These checks validate the scaffold, not LCA results.

## References
- Assignment: https://tiangong-lca-decision-lab.ecodino73.chatgpt.site/#resources (cloud access blocked; supplied screenshots/BOM used).
- CLI documentation: https://github.com/tiangong-lca/cli
- TianGong repositories: https://github.com/orgs/tiangong-lca/repositories
