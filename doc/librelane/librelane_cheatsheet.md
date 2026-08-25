# LibreLane Cheatsheet

## LibreLane Final Directory Structure Explanation

The `final` directory in a LibreLane (or OpenLane-based) ASIC design flow contains the "golden" output files produced after the hardening process. These files represent various views of the design, from logical netlists to the final physical layout ready for manufacturing.

### 1. Physical Layout
* **`gds/`**: Contains the **GDSII** (.gds) file. This is the industry-standard binary format for the final integrated circuit layout, used for "tape out" and sent to the foundry for fabrication.
* **`mag/`**: Contains **Magic** layout files (.mag). These are native to the Magic VLSI tool, used for DRC (Design Rule Checking) and GDS generation.
* **`mag_gds/`**: Contains GDS files specifically generated or processed by the Magic tool.
* **`klayout_gds/`**: Contains GDS files optimized or generated for **KLayout**, often including extra metadata for easier visual debugging.

### 2. Design Exchange & Abstraction
* **`lef/`**: Contains **Library Exchange Format** files. These are "abstract" views containing pin locations and blockages used by placement and routing tools without revealing internal transistor geometry.
* **`def/`**: Contains **Design Exchange Format** files. A text-based representation of the physical design, including cell placement, power grids, and routing.

### 3. Netlists & Circuit Views
* **`nl/`**: Stands for **Netlist**. Contains the gate-level Verilog netlist produced after synthesis.
* **`pnl/`**: Stands for **Powered Netlist**. A Verilog netlist that includes explicit connections for power ($V_{DD}$) and ground ($V_{SS}$), critical for LVS (Layout vs. Schematic) checks.
* **`vh/`**: Contains **Verilog Headers**. Structural Verilog files used for hierarchy management or inclusion in other simulation environments.
* **`spice/`**: Contains **SPICE** netlists (.spice). Used for transistor-level simulations and as the primary reference for LVS to ensure the layout matches the electrical circuit.
* **`json_h/`**: Contains **Yosys JSON Headers**. A machine-readable version of the netlist used by internal LibreLane Python scripts for analysis.

### 4. Timing, Parasitics & Constraints
* **`sdc/`**: Contains **Synopsys Design Constraints** (.sdc). Defines timing requirements like clock periods, input/output delays, and false paths.
* **`spef/`**: Contains **Standard Parasitic Exchange Format** files. Represents the resistance and capacitance (parasitics) of the metal wires extracted from the layout.
* **`sdf/`**: Contains **Standard Delay Format** files. Used in gate-level simulations to annotate exact timing delays.
* **`lib/`**: Contains **Liberty** timing files (.lib). Provides timing, power, and area models for the design, treating it as a "macro" for higher-level integration.

### 5. Databases & Metrics
* **`odb/`**: Contains **OpenDB** (.odb) files. The internal binary database format for **OpenROAD**, combining LEF and DEF data for tool efficiency.
* **`metrics.json`**: A comprehensive summary of results (cell count, area, power, timing slack, DRC/LVS violations) in JSON format.
* **`metrics.csv`**: A spreadsheet-compatible version of the design metrics for tracking and comparison.


## Non-Default Rules (NDR)

Introduced in [PR #869](https://github.com/librelane/librelane/pull/869). Useful for routing non-critical analog nets with wider widths/spacings.

### 1. `NON_DEFAULT_RULES`

**Step:** `OpenROAD.DetailedRouting`  
**Type:** `Optional[dict[str, NDR]]`

Defines one or more non-default rules. Each rule (keyed by its name) has three fields:

| Field | Type | Description |
|---|---|---|
| `width` | `List[str]` | Wire width. Can be a **single value** (applies to all layers), a **multiplier** like `*3` (multiplies default width by 3), or **layer/value pairs** like `[Metal1, 0.42, Metal2, 0.42, ...]`. |
| `spacing` | `List[str]` | Wire spacing. Same format as `width`: single value, multiplier (`*3`), or layer/value pairs. |
| `via` | `Optional[List[str]]` | Allowed vias for this rule, e.g. `[Cont, Via1, Via2, TopVia1]`. If omitted or set to `None`, default vias are used. |

#### Example

```yaml
NON_DEFAULT_RULES:
  ndr_2x:
    width: "*2"
    spacing: "*2"
  ndr_custom:
    width: [Metal1, "0.42", Metal2, "0.42", Metal3, "0.9"]
    spacing: [Metal1, "0.51", Metal2, "0.42", Metal3, "0.9"]
    via: [Cont, Via1, Via2]
```

### 2. `DRT_ASSIGN_NDR`

**Step:** `OpenROAD.DetailedRouting`  
**Type:** `Optional[dict[str, str]]`

Assigns nets to previously defined non-default rules. The net name is matched as a **regular expression**. Use `^name$` for exact matching.

#### Example

```yaml
DRT_ASSIGN_NDR:
  "^clk$": ndr_2x
  "analog_.*": ndr_custom
```

### 3. `CTS_APPLY_NDR`

**Step:** `OpenROAD.CTS`  
**Type:** `Literal["none", "root_only", "half", "full"]`  
**Default:** `"half"`

Controls automatic 2x-spacing NDR application to clock nets. Passed directly to OpenROAD's `clock_tree_synthesis -apply_ndr` flag.

| Value | Behavior |
|---|---|
| `none` | No NDR applied to clock nets. |
| `root_only` | NDR applied only to the root of the clock tree. |
| `half` | NDR applied to the upper half of the clock tree (excluding leaf-level nets). **This is the default.** |
| `full` | NDR applied to all clock tree nets except leaf-level nets. |

#### Example

```yaml
CTS_APPLY_NDR: full
```

### Important Notes

> **Note:** NDR cannot block routing on a specific layer. By omitting a specific layer (e.g. Metal1), default rules apply there. The router may still use this specific layer for short connections.

### Via Types in IHP SG13CMOS5L

The IHP SG13CMOS5L technology LEF (`libs.ref/sg13cmos5l_stdcell/lef/sg13cmos5l_tech.lef`) defines three categories of vias: **cut layers**, **fixed via definitions**, and **GENERATE via rules** (for automatic arrays).

The stack is shorter than the SG13G2 one: five routing metals (Metal1 to Metal4 plus TopMetal1) and four cut layers above `Cont`. There is no `Via4`, no `Metal5`, no `TopVia2` and no `TopMetal2`, so every table below stops one transition earlier than its SG13G2 counterpart.

#### Via Overview (Quick Reference)

The technology provides **52 fixed vias** plus **4 `GENERATE` array rules**, across four layer transitions. Only the three inter-metal transitions (`Via1`–`Via3`) offer a choice of variants (17 each), the top-metal transition has a single symmetric via.

| Transition | Cut layer | Fixed variants | GENERATE rule | Composition |
|---|---|---|---|---|
| Metal1 → Metal2 | `Via1` | 17 | `via1Array` | 9 single-cut + 8 double-cut |
| Metal2 → Metal3 | `Via2` | 17 | `via2Array` | 9 single-cut + 8 double-cut |
| Metal3 → Metal4 | `Via3` | 17 | `via3Array` | 9 single-cut + 8 double-cut |
| Metal4 → TopMetal1 | `TopVia1` | 1 (`TopVia1EWNS`) | `viaTop1Array` | symmetric only |

**Naming key**: fixed vias are named `<transition>_<variant>`:

- `ViaN_XX` / `XY` / `YX` / `YY`: **single-cut**, and the two letters are the enclosure orientation of the metal **below** then **above** (`X` = horizontal / east–west, `Y` = vertical / north–south). Pick the one whose two orientations match the wire directions on each side.
- `ViaN_..._s` and `ViaN_s`: single-cut with a **wider** metal enclosure (`ViaN_s` is a square/symmetric enclosure).
- `ViaN_DC{1,2}{B,T,L,R}`: **double-cut** (two cuts → ~2× current capacity and cut redundancy). `1`/`2` = above-metal enclosure aligned / perpendicular to the cut pair, `B/T/L/R` = direction the second cut is placed (`B`=+Y, `T`=−Y, `L`=+X, `R`=−X).
- `TopVia1EWNS`: symmetric enclosure on all four sides (**E**ast-**W**est-**N**orth-**S**outh), so it is orientation-independent and the only variant needed for the top metal.

> **Choosing vias for a wide analog NDR:** prefer the **double-cut** (`DC*`) variants for reliability, and add the single-cut orientations (`XX/XY/YX/YY`) so the router can still place a via in tight spots. The Metal4 → TopMetal1 transition only has the one `EWNS` via. If you omit the `via` field entirely, the router falls back to the `GENERATE` array rules and automatically sizes a multi-cut array to the wire width. The chip top level of this template uses `["Via1_DC1B", "Via2_DC1B", "Via3_DC1B"]` for its `NDR_analog` rule, see [flow/librelane/config.yaml](../../flow/librelane/config.yaml).

#### Metal Stack

| Layer | Direction | Min Width | Pitch | Thickness | Sheet R | DC Current Density |
|---|---|---|---|---|---|---|
| Metal1 | Horizontal | 0.16 µm | 0.42 µm | 0.40 µm | 135 mΩ/□ | 1 mA/µm |
| Metal2 | Vertical | 0.20 µm | 0.48 µm | 0.45 µm | 103 mΩ/□ | 2 mA/µm |
| Metal3 | Horizontal | 0.20 µm | 0.42 µm | 0.45 µm | 103 mΩ/□ | 2 mA/µm |
| Metal4 | Vertical | 0.20 µm | 0.48 µm | 0.45 µm | 103 mΩ/□ | 2 mA/µm |
| TopMetal1 | Horizontal | 1.64 µm | 3.28 µm | 2.0 µm | 21 mΩ/□ | 15 mA/µm |

`Pitch` is the LEF pitch perpendicular to the layer's preferred direction, i.e. the wire-to-wire pitch of the routing grid. `Sheet R` is the LEF `RESISTANCE RPERSQ` value. `Metal1` and `Metal2` additionally declare `MAXWIDTH 30`, and the layout rules cap unslotted metal at 30 µm on the whole stack, which is why the chip's 15 µm PDN ring needs no slotting.

Note the two differences to SG13G2 that bite when a design is ported: **TopMetal1 is horizontal here** (it is vertical on SG13G2), and it is the only thick metal, so a chip-level PDN pairs it with a thin Metal4 rather than with a second thick metal.

Two more per-layer numbers worth knowing:

- LibreLane's own track file, `libs.tech/librelane/sg13cmos5l_stdcell/tracks.info`, gives `Metal1` and `Metal3` a 0.42 µm pitch on **both** axes (the LEF says 0.48 µm in X), and `TopMetal1` a track pitch of **2.28 µm**. With `WIDTH 1.64` and `SPACING 1.64` in the same LEF, 3.28 µm is the smallest pitch two minimum-width TopMetal1 wires can legally hold, so treat 2.28 µm as a routing grid and not as a legal wire pitch.
- The PDK's `LAYERS_RC` dictionary in `libs.tech/librelane/config.tcl` is empty, so the OpenROAD repair passes see no per-layer RC and cannot estimate wire delay. Take resistance from the table above or from PEX.

#### Cut Layer Properties

| Cut Layer | Connects | Cut Size | Min Spacing | Resistance | DC Current (per cut) |
|---|---|---|---|---|---|
| Cont | GatPoly → Metal1 | 0.16 µm | 0.18 µm | 22 Ω | n/a |
| Via1 | Metal1 → Metal2 | 0.19 µm | 0.22 µm | 20 Ω | 0.4 mA |
| Via2 | Metal2 → Metal3 | 0.19 µm | 0.22 µm | 20 Ω | 0.4 mA |
| Via3 | Metal3 → Metal4 | 0.19 µm | 0.22 µm | 20 Ω | 0.4 mA |
| TopVia1 | Metal4 → TopMetal1 | 0.42 µm | 0.42 µm | 4 Ω | 1.4 mA |

`Cont` has no `DCCURRENTDENSITY` entry in the tech LEF. The layout cheatsheet in [doc/ihp-sg13cmos5l-Open-PDK/](../ihp-sg13cmos5l-Open-PDK/) gives it 0.3 mA per cut.

#### Fixed Via Definitions

Fixed vias have pre-defined geometry (metal enclosures and cut positions). They are used by the NDR `via` field and as fallback when GENERATE rules cannot be applied.

##### Single-Cut Vias (Via1–Via3)

Each via layer (Via1 through Via3) has 9 single-cut variants with different metal enclosure orientations.

**Naming convention:** `ViaN_AB[_s]`

- `N` = via layer number (1–3)
- `A` = enclosure direction of the metal **below** (`X` = horizontal, `Y` = vertical)
- `B` = enclosure direction of the metal **above** (`X` = horizontal, `Y` = vertical)
- `_s` = wider (symmetric) enclosure on the metal above

| Via | Below Encl. | Above Encl. | Notes |
|---|---|---|---|
| `ViaN_XX` | Horizontal | Horizontal | Both metals extend in X |
| `ViaN_XX_s` | Horizontal | Horizontal (wide) | Wider above-metal enclosure |
| `ViaN_XY` | Horizontal | Vertical | Cross-direction transition |
| `ViaN_XY_s` | Horizontal | Vertical (wide) | Wider above-metal enclosure |
| `ViaN_YX` | Vertical | Horizontal | Cross-direction transition |
| `ViaN_YX_s` | Vertical | Horizontal (wide) | Wider above-metal enclosure |
| `ViaN_YY` | Vertical | Vertical | Both metals extend in Y |
| `ViaN_YY_s` | Vertical | Vertical (wide) | Wider above-metal enclosure |
| `ViaN_s` | Symmetric | Symmetric | Equal enclosure in all directions |

Example: `Via1_XY`. Metal1 enclosure extends horizontally, Metal2 enclosure extends vertically. Useful when routing transitions from horizontal Metal1 to vertical Metal2.

##### Double-Cut Vias (Via1–Via3)

Double-cut vias contain **two cut rectangles** in a single via instance, providing **2× current capacity** compared to single-cut vias and improved reliability.

**Naming convention:** `ViaN_DCVarDir`

- `DC` = Double Cut
- `Var` = enclosure variant (`1` or `2`):
  - `1` = above-metal enclosure aligned with the double-cut direction
  - `2` = above-metal enclosure perpendicular to the double-cut direction
- `Dir` = direction of the second cut relative to center:
  - `B` = second cut placed above (+Y)
  - `T` = second cut placed below (−Y)
  - `L` = second cut placed to the right (+X)
  - `R` = second cut placed to the left (−X)

| Via | Arrangement | Above-Metal Alignment | Notes |
|---|---|---|---|
| `ViaN_DC1B` | Vertical (+Y) | Aligned (tall) | Second cut above center |
| `ViaN_DC1T` | Vertical (−Y) | Aligned (tall) | Second cut below center |
| `ViaN_DC1L` | Horizontal (+X) | Aligned (wide) | Second cut right of center |
| `ViaN_DC1R` | Horizontal (−X) | Aligned (wide) | Second cut left of center |
| `ViaN_DC2B` | Vertical (+Y) | Perpendicular | Second cut above center |
| `ViaN_DC2T` | Vertical (−Y) | Perpendicular | Second cut below center |
| `ViaN_DC2L` | Horizontal (+X) | Perpendicular | Second cut right of center |
| `ViaN_DC2R` | Horizontal (−X) | Perpendicular | Second cut left of center |

Example: `Via1_DC1B`. Two Via1 cuts arranged vertically (second cut at +Y), Metal2 enclosure tall/narrow (aligned with the vertical arrangement). Provides 0.8 mA DC current capacity.

##### TopVia Fixed Via

| Via | Connects | Cut Size | Enclosure | Resistance |
|---|---|---|---|---|
| `TopVia1EWNS` | Metal4 → TopMetal1 | 0.42 µm | Metal4: 0.31 µm, TopMetal1: 0.75 µm | 4 Ω |

`EWNS` = East-West-North-South, symmetric enclosure in all four directions. It is the only fixed via variant for the top metal transition because TopMetal1 has a large minimum width that inherently requires a symmetric enclosure. On SG13G2 the same via sits between Metal5 and TopMetal1, here it lands directly on the Metal4 routing layer.

#### GENERATE Via Rules (Automatic Arrays)

GENERATE rules allow the router to automatically create via **arrays** sized to match the wire width. Wider wires produce more cuts, lowering resistance and increasing current capacity.

| Rule | Cut Layer | Cut Spacing | Enclosure (Below) | Enclosure (Above) |
|---|---|---|---|---|
| `via1Array` | Via1 | 0.48 µm × 0.48 µm | Metal1: 0.05/0.01 µm | Metal2: 0.05/0.005 µm |
| `via2Array` | Via2 | 0.48 µm × 0.48 µm | Metal2: 0.05/0.005 µm | Metal3: 0.05/0.005 µm |
| `via3Array` | Via3 | 0.48 µm × 0.48 µm | Metal3: 0.05/0.005 µm | Metal4: 0.05/0.005 µm |
| `viaTop1Array` | TopVia1 | 0.84 µm × 0.84 µm | Metal4: 0.1/0.1 µm | TopMetal1: 0.42/0.42 µm |

The router uses GENERATE rules when no specific fixed vias are mandated by NDR rules. When NDR `via` specifies fixed via types (e.g., `Via1_DC1B`), the router uses those fixed definitions instead.

#### Current Capacity Example (10 mA)

To carry 10 mA through a via transition:

| Cut Layer | Current per Cut | Cuts Needed | Notes |
|---|---|---|---|
| Via1–Via3 | 0.4 mA | 25 | With double-cut vias: 13 instances |
| TopVia1 | 1.4 mA | 8 | With `viaTop1Array` on a 5 µm wire: ~25 cuts |

With a 5 µm wide NDR wire and GENERATE via array rules, the router can fit approximately $\lfloor 5.0 / 0.48 \rfloor ^2 \approx 100$ cuts for Via1–Via3, far exceeding the 25 needed for 10 mA. When using fixed double-cut vias (e.g., `Via1_DC1B`), the router places multiple instances as space permits.

There is no `TopVia2` on this stack, so 10 mA off-chip has to leave through TopVia1 arrays. A single-cut top via is not enough the way `TopVia2EWNS` would be on SG13G2.

#### Summary of All Via Names

**Via1 (Metal1 → Metal2):** `Via1_XX`, `Via1_XX_s`, `Via1_XY`, `Via1_XY_s`, `Via1_YX`, `Via1_YX_s`, `Via1_YY`, `Via1_YY_s`, `Via1_s`, `Via1_DC1B`, `Via1_DC1T`, `Via1_DC1L`, `Via1_DC1R`, `Via1_DC2B`, `Via1_DC2T`, `Via1_DC2L`, `Via1_DC2R`

**Via2 (Metal2 → Metal3):** `Via2_XX`, `Via2_XX_s`, `Via2_XY`, `Via2_XY_s`, `Via2_YX`, `Via2_YX_s`, `Via2_YY`, `Via2_YY_s`, `Via2_s`, `Via2_DC1B`, `Via2_DC1T`, `Via2_DC1L`, `Via2_DC1R`, `Via2_DC2B`, `Via2_DC2T`, `Via2_DC2L`, `Via2_DC2R`

**Via3 (Metal3 → Metal4):** `Via3_XX`, `Via3_XX_s`, `Via3_XY`, `Via3_XY_s`, `Via3_YX`, `Via3_YX_s`, `Via3_YY`, `Via3_YY_s`, `Via3_s`, `Via3_DC1B`, `Via3_DC1T`, `Via3_DC1L`, `Via3_DC1R`, `Via3_DC2B`, `Via3_DC2T`, `Via3_DC2L`, `Via3_DC2R`

**TopVia1 (Metal4 → TopMetal1):** `TopVia1EWNS`

### How It Works

NDRs are created and assigned in `drt.tcl` right before detailed routing runs:

1. **NDR creation:** If `NON_DEFAULT_RULES` is set, the script iterates over each rule, extracts `width`, `spacing`, and `via`, and calls OpenROAD's `create_ndr`.
2. **NDR assignment:** If `DRT_ASSIGN_NDR` is set, the script iterates over all nets in the design, matches each net name against the provided regex patterns, and calls `assign_ndr` for matches.

This ensures the router respects the wider widths/spacings during detailed routing.

## The Eight LEF/DEF Orientations

LEF/DEF uses eight orientation codes to describe macro placement. All rotations are counter-clockwise.

| Code | Name | Rotation | Mirror | Description |
|---|---|---|---|---|
| `N` | North | 0° | None | Default orientation. Placed exactly as drawn. |
| `W` | West | 90° CCW | None | Original top edge becomes the left edge. |
| `S` | South | 180° CCW | None | Original top-right corner becomes bottom-left corner. |
| `E` | East | 270° CCW | None | Original top edge becomes the right edge. |
| `FN` | Flipped North | 0° | Y-axis | Mirrored horizontally. Left becomes right, top/bottom unchanged. |
| `FW` | Flipped West | 90° CCW | Y-axis | Mirrored horizontally, then rotated 90° CCW. Equivalent to mirroring across the diagonal axis. |
| `FS` | Flipped South | 0° | X-axis | Mirrored vertically. Top becomes bottom, left/right unchanged. |
| `FE` | Flipped East | 270° CCW | Y-axis | Mirrored horizontally, then rotated 270° CCW. |

A rotation is not a free transform for a hard macro: its pin faces have to keep the layer that runs along them. Rotating an `N` macro to `W` turns a Metal3 (horizontal) pin face into an edge that a horizontal layer can no longer leave, so the macro has to be re-hardened rather than re-oriented. The two `counter_top` instances of this template are placed `N` and `FS`. Both are unrotated, so every layer keeps its direction, and `FS` only mirrors the macro about the X axis, which swaps its top and bottom pin edges.
