# Chip Floorplan

This document describes the physical floorplan of this chip and is the human-readable companion to the macro `instances` blocks in [config.yaml](../flow/librelane/config.yaml).

Related documents:
- Pinout: [pinout.md](pinout.md)
- Specifications: [specifications.md](specifications.md)


## Die / core geometry

| Parameter                | Value                                                |
| ------------------------ | ---------------------------------------------------- |
| `DIE_AREA`               | `[0, 0, 1600, 1600]` µm  (1.6 mm × 1.6 mm)           |
| `CORE_AREA`              | `[365, 365, 1235, 1235]` µm  (870 µm × 870 µm), snapped to (365.28, 366.66) to (1234.56, 1232.28) |
| Padframe margin per side | 365 µm (between die edge and core)                   |
| `FP_SIZING`              | `absolute`                                           |
| Clock period             | 20 ns (50 MHz)                                       |
| Core supply              | 1.2 V (`VDD` / `VSS`)                                |
| I/O supply               | 3.3 V (`IOVDD` / `IOVSS`)                            |

The 365 µm padframe margin holds the [bondpads](../ip/sg13cmos5l_ip__bondpad_70x70/), the [RF pads](../ip/sg13cmos5l_ip__rfpad_70x70/), the [JKU](../ip/sg13cmos5l_ip__jku/) and [names](../ip/sg13cmos5l_ip__jku_names/) logos, IHP IO cells, corner cells, fillers and the top-level power ring (Metal4 vertical + TopMetal1 horizontal).

SG13CMOS5L routes on Metal1 to Metal4 plus TopMetal1. There is no Metal5 and no TopMetal2, so the two top-level PDN layers are Metal4 (vertical) and TopMetal1 (horizontal), one thin metal and one thick metal, instead of the two thick metals a SG13G2 chip uses.

Each side of the padframe offers 960 µm between the corner cells for 8 IO cells of 80 µm width, which leaves 320 µm of fill. `PAD_SPACING_MULTIPLE: 20` in [config.yaml](../flow/librelane/config.yaml) makes `OpenROAD.PadRing` floor the pad-to-pad gap to 20 µm, so the pads sit on a 100 µm pitch with their centers at 450 to 1150 µm. Every side needs its 8 pads for that pitch.

The RF pads carry their own bond pad and are 80 × 250 µm. [pad_cfg.tcl](../flow/librelane/pad_cfg.tcl) is LibreLane's script with one added block that moves them outward by the 70 µm bondpad depth, so that their rail bands abut the neighbouring pads.


## Hard macros

Seven hard macros are placed inside the core:

| Macro instance               | Cell                 | Size (W × H)      | Lower-left (x, y) | Upper-right (x, y) | Orientation |
| ---------------------------- | -------------------- | ----------------- | ----------------- | ------------------ | ----------- |
| `i_chip_core.counter_lv_ihp` | `counter_lv_ihp_top` | 200 × 100 µm      | (440, 1095)       | (640, 1195)        | N           |
| `i_chip_core.counter_lv_eth` | `counter_lv_eth_top` | 200 × 100 µm      | (700, 1095)       | (900, 1195)        | N           |
| `i_chip_core.counter_hv_kvc` | `counter_hv_kvc_top` | 200 × 100 µm      | (960, 1095)       | (1160, 1195)       | N           |
| `i_chip_core.ringosc`        | `ringosc`            | 133.52 × 15.28 µm | (1075, 929.88)    | (1208.52, 945.16)  | N           |
| `i_chip_core.inverter`       | `inverter_top`       | 54.18 × 81.92 µm  | (1080, 684.18)    | (1134.18, 766.10)  | N           |
| `i_chip_core.amplifier`      | `amplifier`          | 35.38 × 18.24 µm  | (1148.90, 487.04) | (1184.28, 505.28)  | N           |
| `i_chip_core.vco`            | `vco_top`            | 143 × 176.90 µm   | (728.64, 385.14)  | (871.64, 562.04)   | N           |

The values are kept in the `instances` blocks of [config.yaml](../flow/librelane/config.yaml). The counter row is x-centered on the die with 60 µm between the macros. The amplifier is placed by its cell origin at (1150, 490), its `rhigh` resistor reaches 1.1 µm left of and 2.96 µm below that origin. The ring oscillator's `y` of 929.88 µm is a row boundary. [prep-ic/chip_top.json](prep-ic/chip_top.json) holds the same floorplan as a PREP-IC project.


## Macro placement (top view)

```text
y=1235 ┌───────────────────────────────────────────────┐
 1195  │ ┌counter_lv_ihp┐ ┌counter_lv_eth┐ ┌counter_hv┐ │
 1095  │ └──────────────┘ └──────────────┘ └──────────┘ │
       │                                                │
  945  │                               ┌──ringosc───┐   │
  930  │                               └────────────┘   │
       │                                                │
  766  │                                ┌inverter┐      │
  684  │                                └────────┘      │
       │              ┌──vco──┐                         │
  562  │              │ coil  │                         │
       │              │       │              ┌amp┐      │
  490  │              │       │              └───┘      │
  385  │              └───────┘                         │
y= 365 └───────────────────────────────────────────────┘
       x=365    440        729   872     1080       1235
```

Pad order (away from origin) on each side (see [pinout.md](pinout.md) for the full per-pad breakdown):

| Side  | Pad order                                                                                   |
| ----- | ------------------------------------------------------------------------------------------- |
| West  | VSS, VDD, IOVSS, IOVDD, sel[0], sel[1], rst_n, clk                          (bottom → top)  |
| North | count[0] to count[7]                                                        (left → right)  |
| South | di_en, vtune, VSS, rf_out_n, rf_out_p, VSS, vdd_rf, VSS                     (left → right)  |
| East  | amp_vin, amp_vout, inv_vin, inv_vout, inv_dout, vdd_ro, ro_vout, vdd_hv     (bottom → top)  |


## Power-distribution network (PDN)

The PDN is generated by [pdn_cfg.tcl](../flow/librelane/pdn_cfg.tcl) on top of the chip top-level grid that LibreLane builds from the `PDN_*` keys in [config.yaml](../flow/librelane/config.yaml). The PDK defaults in `libs.tech/librelane/config.tcl` set the stripes: Metal4 1 µm wide and TopMetal1 2 µm wide, both on a 50 µm pitch with a 10 µm offset. The offset places the stripe centers.

| Domain / macro            | Stripes                                                          | Connect             |
| ------------------------- | ---------------------------------------------------------------- | ------------------- |
| Chip core                 | Metal4 vertical + TopMetal1 horizontal                           | Metal4 ↔ TopMetal1  |
| Core ring                 | Metal4 + TopMetal1, 15 µm wide, 5 µm spacing, `-connect_to_pads` | core ring ↔ pads    |
| Counters (`macro` grid)   | none added, the macro's own Metal4 pins act as the stripes       | Metal4 ↔ TopMetal1  |
| `inverter` (custom)       | none added, relies on the chip top-level stripes                 | Metal4 ↔ TopMetal1  |
| `amplifier` (custom)      | none added, the Metal4 stripes cross its Metal3 supply strips    | Metal3 ↔ Metal4     |
| `vco`, `ringosc`          | no grid, drawn straps                                            | see below           |

The inverter carries its own supply ring, with the two horizontal segments on Metal3 and the two vertical segments on Metal4, so TopMetal1 stays free and the top-level TopMetal1 stripes feed it.

### Supplies of their own and the RF lines

The VCO, the ring oscillator and the IHP HV counter run from analog pads of their own, not from the ring's `VDD`. `PDN_MACRO_CONNECTIONS` puts each macro's `VDD` pin on a power net of its own, and [pdn_cfg.tcl](../flow/librelane/pdn_cfg.tcl) moves the `padbare` of its pad onto the same net. The router leaves power nets alone, so `pdn_cfg.tcl` draws those connections, the `VSS` pins of the VCO and the ring oscillator, and the two RF lines, which it marks special so that the router leaves them alone too. The straps are added right after `pdngen`, which would otherwise cut its stripes around them.

| Net        | From                                      | Route                                                                                | To                                                  |
| ---------- | ----------------------------------------- | ------------------------------------------------------------------------------------ | --------------------------------------------------- |
| `vdd_rf`   | `vdd_rf_pad`, Metal3 at y 320             | Metal3 north under the core ring, TopMetal1 west along the strip below the VCO       | VCO `VDD` pin at its lower-left corner              |
| VCO `VSS`  | VCO `VSS` pin at its left edge            | TopMetal1 west, TopVia1                                                              | Metal4 `VSS` stripes at x 628.28 and 678.28         |
| `vdd_hv`   | `vdd_hv_pad`, Metal3 at x 1280            | Metal3 west under the core ring, TopMetal1 over the counter                          | four Metal4 `VDD` stripes of the IHP HV counter     |
| `vdd_ro`   | `vdd_ro_pad`, Metal3 at x 1280            | Metal3 west under the core ring, TopMetal1 over the ring oscillator                  | via stack on its `VDD` pin at the top edge          |
| ring oscillator `VSS` | its `VSS` pin at the bottom edge | Metal3 south, Via3 and TopVia1                                                       | TopMetal1 `VSS` stripe at y 882.66                  |
| `rf_out_n`, `rf_out_p` | RF pad, TopMetal1 at y 320   | TopVia1 and Via3 below the core ring, 4 µm of Metal3 north                           | VCO RF pins at its bottom edge                      |

`PDN_OBSTRUCTIONS` keeps the stripes off the VCO coil and the ring oscillator, and keeps the TopMetal1 stripes out of the strip below the VCO where `vdd_rf` and the VCO `VSS` run.

The coordinates in `pdn_cfg.tcl` follow from the pad pitch, the core area, the macro locations and the stripe grid, so recheck them when any of these move. Three rules came out of building them:

- **A Metal3 strap must not cross a Metal4 stripe inside the core.** The via stacks from the stripes down to the Metal1 rails have Metal3 pads, so the strap would short to `VDD` and `VSS`. The `vdd_hv` and `vdd_ro` straps step up to TopMetal1 east of the last stripes for that reason.
- **A strap on the macro's own pin layer ends at the macro edge.** Reaching into the macro's obstructions fails the blocked layers check of the detailed placer (`DPL-0033`), and touching shapes connect anyway.
- **That check also rejects a same-layer strap at the top edge of a macro,** so the ring oscillator's top pin takes a via stack from above. Straps from below and from the left pass.

Each macro's `VSS` stays on the chip `VSS`.


## Logos

Two decorative IPs sit in the upper corners of the die (outside the core, between the core ring and the seal ring):

| Instance     | Cell                       | Size         | Location                                                                        |
| ------------ | -------------------------- | ------------ | ------------------------------------------------------------------------------- |
| `jku_logo`   | `sg13cmos5l_ip__jku`       | 100 × 100 µm | `($DIE_AREA[0] + 36.4 + 20.4, $DIE_AREA[3] - 36.4 - 120.4)` = (56.8, 1443.2)    |
| `jku_names`  | `sg13cmos5l_ip__jku_names` | 100 × 100 µm | `($DIE_AREA[2] - 36.4 - 120.4, $DIE_AREA[3] - 36.4 - 120.4)` = (1443.2, 1443.2) |
| `template_name` | `sg13cmos5l_ip__template_name` | 100 × 100 µm | (56.8, 56.8), placed by `scripts/add_logo_fill.sh` |
| `mpw_date`   | `sg13cmos5l_ip__mpw_date`  | 100 × 100 µm | (1443.2, 56.8), placed by `scripts/add_logo_fill.sh` |

`scripts/add_logo_fill.sh` also draws five NWell strips along the row edges beside the amplifier, inverter and VCO halos, which remove the `NW.d` markers at the row ends, and a TopMetal1 bridge from the VSS strap of the VCO to the VSS rail at y = 382.66 µm with six TopVia1 cuts onto one more Metal4 stripe. Their coordinates follow the placement, so recheck them after a new LibreLane run.

Both logos are listed as `IGNORE_DISCONNECTED_MODULES` in [config.yaml](../flow/librelane/config.yaml) so LibreLane does not flag them as floating logic. Their pixels are drawn on Metal4, the top thin metal of this stack, where the SG13G2 logos use Metal5.

The third logo, the chip logo in [flow/logo/](../flow/logo/), is not a macro. It is merged into the final GDS after the LibreLane run by [add_logo_fill.sh](../scripts/add_logo_fill.sh), on TopMetal1, together with the TopMetal1 filler.


## Constraints when editing the floorplan

For every macro `M` placed at `(X, Y)` with size `W × H`:

1. **Inside the core:** `X ≥ 365`, `Y ≥ 365`, `X + W ≤ 1235`, `Y + H ≤ 1235`.
2. **No overlap** with any other macro rectangle (RePlAce will diverge with `[GPL-0305]` otherwise).
3. **Aligned to the routing grid:** the `inverter_top` macro additionally requires `X` to be a multiple of 0.48 µm and `Y` a multiple of 0.42 µm.
4. **Clear of the IO ring:** routing inside the bondpad area is reserved for the padframe.
5. **Keep a macro supply ring off one of the two PDN layers.** A ring that occupies Metal4 *and* TopMetal1 blocks both top-level stripe directions at once. `inverter_top` keeps its ring on Metal3 and Metal4, so TopMetal1 stays free.
6. **Move the drawn straps with the macro.** The straps in `pdn_cfg.tcl` hold absolute coordinates of the VCO, the ring oscillator, the IHP HV counter and their pads.
