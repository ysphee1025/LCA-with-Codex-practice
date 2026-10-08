# Phase 1 methodological design

## Confirmed requirements
The supplied classroom prompt, earlier screenshots and BOM establish BC1, one packaged nominal 1 L kettle, 723 g product and 137.8 g packaging. Include materials, component manufacture, assembly and packaging through final manufacturing-facility gate. Exclude downstream distribution, customer delivery, use and end of life. Principal indicator: GWP100, kg CO2-eq per packaged kettle. Explore TianGong and USLCI for every BOM entry; preserve candidate history, an independent baseline and one revised modeling choice.

## Unverified website content
The website and original CSV remain subject to access checks. The exact ten README rules have not been independently read. The headings in README are provisional coverage, not a claim to know those rules. The primary EU study has not been independently inspected.

## Proposed method and architecture
Separate foreground finished masses, gross production inputs, conversion services and assembly/packaging energy. Do not add arbitrary components or assume a PCB. No allocation from material totals to components is established. A supplier's material gate is not the final kettle assembly gate.

Prefer a normalized process export with exact reference-flow quantities and units, unique dataset ID/version, supplier-linked technosphere inputs and elementary flows. For production-positive, input-negative A columns and elementary-emission B columns, solve A s = f, then g = B s and h = C g. Convert all exchanges to consistent reference units before solving; preserve allocation and sign conventions. Missing suppliers, unresolved mappings and incompatible/uncharacterized climate flows must be diagnosed before a complete GWP claim. Direct emissions alone are not cumulative impacts.

A matrix implementation is planned for Phase 4, not implemented in Phase 1/2. Select a dated/versioned GWP100 method only after checking available inventories and characterization factors; GWP100 does not itself identify an IPCC edition. No factors, numerical LCIA or assumed zero burdens are currently used.

## Missing critical inputs and decisions
Actual datasets, database versions and rights; supplier closure; reference flows/units; compatible GWP factors; manufacturing geography/year; conversion processes; material yields/losses; assembly energy; packaging operations; inbound transport; manufacturing waste handling. Nylon grade is unspecified. These are not filled with numerical guesses. Materially different provider or boundary choices will be presented for human scientific decision after candidates are available.

## Baseline and revision protocol
No baseline has yet been calculated. Phase 1/2 Git commits are setup commits, not baseline commits. Once verified, record full 40-character baseline SHA and immutable model/run IDs and outputs. Before changing one choice, record expected direction and rationale. Save revised results under another run ID and preserve baseline files. Do not substitute statistically interpreted intervals for sensitivity scenarios.
