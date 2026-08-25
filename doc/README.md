# Documentation

Reference material for this chip and for the IHP SG13CMOS5L Open-PDK it is built on.

## This chip

| Document | Contents |
| --- | --- |
| [specifications.md](specifications.md) | Top-level specifications: technology, supplies, clock, corner list, macro inventory, functional behaviour of every block. |
| [pinout.md](pinout.md) | The full 32-pad table per side, with the `chip_top` port and the role each pad carries inside `chip_core`. |
| [floorplan.md](floorplan.md) | Die and core geometry, hard-macro placement coordinates, the PDN strategy and the floorplan diagram. |

The three are cross-linked and are written against the design files, not the other way round. If you change a number in [flow/librelane/config.yaml](../flow/librelane/config.yaml), [rtl/](../rtl/) or [packaging/config.yaml](../packaging/config.yaml), mirror it here.

## Tools

| Document | Contents |
| --- | --- |
| [klayout/klayout_cheatsheet.md](klayout/klayout_cheatsheet.md) | KLayout for this PDK: shortcuts, the `SG13_dev` PCell list, layer roles, padframe components, the DRC and LVS menu entries. |
| [librelane/librelane_cheatsheet.md](librelane/librelane_cheatsheet.md) | LibreLane `final/` directory anatomy, non-default routing rules, the complete SG13CMOS5L via and metal-stack tables, the eight LEF/DEF orientations. |
| [verilog/](verilog/) | Verilog and SystemVerilog cheatsheets (external documents, PDK-independent). |

## PDK

| Document | Contents |
| --- | --- |
| [ihp-sg13cmos5l-Open-PDK/sg13cmos5l_os_layout_rules.pdf](ihp-sg13cmos5l-Open-PDK/sg13cmos5l_os_layout_rules.pdf) | The IHP layout rules. The authoritative source when a tool deck and a datasheet disagree. |
| [ihp-sg13cmos5l-Open-PDK/sg13cmos5l_os_process_spec.pdf](ihp-sg13cmos5l-Open-PDK/sg13cmos5l_os_process_spec.pdf) | The IHP process specification. |
| [ihp-sg13cmos5l-Open-PDK/sg13cmos5l_os_layout_cheatsheet.xlsx](ihp-sg13cmos5l-Open-PDK/sg13cmos5l_os_layout_cheatsheet.xlsx) | One sheet of formulas for wire resistance, parasitic capacitance and DC current limits. Read the caveats below before using it. |
| [ihp-sg13cmos5l-Open-PDK/sg13cmos5l_ngspice_mc_mm_guide.md](ihp-sg13cmos5l-Open-PDK/sg13cmos5l_ngspice_mc_mm_guide.md) | How the ngspice model files fit together, what `mm_ok` and `num_sigmas` do, and which corner, Monte Carlo and mismatch runs are possible per device family. |
| [sizing/](sizing/) | gm/ID techsweep plot overviews for the LV and HV MOS devices, the data behind the sizing notebooks in [macros/inverter/scripts/sizing/](../macros/inverter/scripts/sizing/). |

## Other

[ihp-structure-proposals/](ihp-structure-proposals/) holds four proposed submission-repo layouts for IHP shuttle chips (an ADC, an LNA, an MCU and an op-amp), contributed to the discussion around a common directory structure. They are PDK-independent and are kept here verbatim from the SG13G2 template. The generator script that produced them, `gen_structure.py`, is deliberately not tracked (see [.gitignore](../.gitignore)).

## Provenance and caveats

The two PDK PDFs are copied unchanged out of `libs.doc/doc/` of the SG13CMOS5L PDK (`ihp-sg13cmos5l @ ff32f48`, the PDK in the IIC-OSIC-TOOLS 2026.08 image), renamed to lower case to match the folder convention: layout rules **Rev. 0.1 (2025-12-08)**, process specification **Rev. 0.2 (2025-12-15)**. The revision is on the title page of each document. A repo copy of a PDK document ages silently, so check that stamp against `$PDK_ROOT/$PDK/libs.doc/doc/` before letting one of these decide a rule.

Three items are carried over from the SG13G2 sibling of this template and are worth knowing about:

- **The layout cheatsheet is the SG13G2 sheet.** It is byte-identical to `sg13g2_os_layout_cheatsheet.xlsx`, so its layer list still contains `M5`, `TM2` and `TV2`, which do not exist on this stack. The `M1`..`M4`, `TM1`, `Contact`, `Via 1/2/3` and `TV1` rows apply here unchanged, ignore the rest. Two further columns are wrong on both PDKs: the resistance columns use bulk-aluminium resistivity and are optimistic by roughly a factor of two against the tech LEF, and the "min. Width" column lists 0.42 µm for TopMetal1 where the LEF says 1.64 µm. Take widths from the DRC deck, resistance from the tech LEF or from PEX, and current limits from the [LibreLane cheatsheet](librelane/librelane_cheatsheet.md) tables, which are read out of `sg13cmos5l_tech.lef`.
- **The gm/ID techsweep plots are the SG13G2 sweep.** The LV and HV MOS ngspice models of this PDK are symbolic links into `ihp-sg13g2/libs.tech/ngspice/models/`, so the devices are the same devices and the curves are the same curves. The `.mat` lookup tables under [macros/inverter/scripts/sizing/data/](../macros/inverter/scripts/sizing/data/) are likewise byte-identical to the SG13G2 ones under a SG13CMOS5L name. The figure captions inside the PDFs still read "SG13G2". They will be regenerated when a SG13CMOS5L-specific sweep exists.
- **The Verilog and SystemVerilog cheatsheets** are external documents with no PDK content at all.

Nothing in `doc/` is generated by a make target. It is all hand-maintained.
