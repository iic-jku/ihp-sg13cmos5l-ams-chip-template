# Chip Floorplan

This document describes the physical floorplan of the AMS template chip and is the human-readable companion to the macro `instances` blocks in [config.yaml](../flow/librelane/config.yaml).

Related documents:
- Pinout: [pinout.md](pinout.md)
- Specifications: [specifications.md](specifications.md)


## Die / core geometry

| Parameter                | Value                                                |
| ------------------------ | ---------------------------------------------------- |
| `DIE_AREA`               | `[0, 0, 1600, 1600]` µm  (1.6 mm × 1.6 mm)           |
| `CORE_AREA`              | `[365, 365, 1235, 1235]` µm  (870 µm × 870 µm)       |
| Padframe margin per side | 365 µm (between die edge and core)                   |
| `FP_SIZING`              | `absolute`                                           |
| Clock period             | 20 ns (50 MHz)                                       |
| Core supply              | 1.5 V (`VDD` / `VSS`)                                |
| I/O supply               | 3.3 V (`IOVDD` / `IOVSS`)                            |

The 365 µm padframe margin holds the [bondpads](../ip/sg13cmos5l_ip__bondpad_70x70/), [JKU](../ip/sg13cmos5l_ip__jku/) and [names](../ip/sg13cmos5l_ip__jku_names/) logos, IHP IO cells, corner cells, fillers and the top-level power ring (Metal4 vertical + TopMetal1 horizontal, 15 µm wide, 5 µm spacing, see [config.yaml](../flow/librelane/config.yaml) and [pdn_cfg.tcl](../flow/librelane/pdn_cfg.tcl)).

SG13CMOS5L routes on Metal1 to Metal4 plus TopMetal1. There is no Metal5 and no TopMetal2, so the two top-level PDN layers are Metal4 (vertical) and TopMetal1 (horizontal), one thin metal and one thick metal, instead of the two thick metals a SG13G2 chip uses. Several of the choices below follow from that.

Each side of the padframe offers 960 µm between the corner cells for 8 IO cells of 80 µm width, which leaves 320 µm of fill. `PAD_SPACING_MULTIPLE: 2` in [config.yaml](../flow/librelane/config.yaml) makes `OpenROAD.PadRing` floor the pad-to-pad gap to 34 µm, so the 41 µm left at each row end lands on the 1 µm IO site grid. The default multiple of 1 µm gives 35 µm gaps, 37.5 µm at the ends, and an off-grid error.


## Hard macros

Five hard macros are placed inside the core:

| Macro instance              | Cell                                  | Size (W × H)       | Lower-left (x, y) | Upper-right (x, y) | Orientation |
| --------------------------- | ------------------------------------- | ------------------ | ----------------- | ------------------ | ----------- |
| `i_chip_core.sram_0`        | `RM_IHPSG13_1P_1024x32_c2_bm_bist`    | 416.64 × 336.46 µm | (435, 495)        | (851.64, 831.46)   | N           |
| `i_chip_core.counter1`      | `counter_top`                         | 200 × 100 µm       | (935, 995)        | (1135, 1095)       | N           |
| `i_chip_core.counter2`      | `counter_top`                         | 200 × 100 µm       | (935, 495)        | (1135, 595)        | FS          |
| `i_chip_core.inverter1`     | `inverter_top`                        | 54.18 × 81.92 µm   | (1080.00, 850.08) | (1134.18, 932.00)  | N           |
| `i_chip_core.inverter2`     | `inverter_top`                        | 54.18 × 81.92 µm   | (1080.00, 658.14) | (1134.18, 740.06)  | N           |

The values are kept in the `instances` blocks of [config.yaml](../flow/librelane/config.yaml). The `inverter_top` coordinates are tied to the routing grid: `X` is a multiple of 0.48 µm, the Metal2 / Metal4 track pitch that carries the `vin1..vin4` pin face, and `Y` is a multiple of 0.42 µm, the Metal1 / Metal3 track pitch that carries the `vout1..vout4` pin face. See the [LibreLane cheatsheet](librelane/librelane_cheatsheet.md) for the track pitches of the whole stack and for the meaning of the orientation codes.


## Macro placement (top view)

With the current `CORE_AREA` `[365,365,1235,1235]`, the macros occupy the right-hand side of the core: SRAM and `counter2` in the lower half, `counter1` and both inverter instances in the upper half.

```text
y=1235 ┌───────────────────────────────────────────────┐
       │                                               │
       │                                  ┌─counter1─┐ │
 1095  │                                  │(935,995) │ │
       │                                  └──────────┘ │
       │                                               │
  932  │                                   ┌inv1────┐  │
       │                                   │(1080,  │  │
       │                                   │ 850.08)│  │
  740  │                                   └inv2────┘  │
       │                                   ┌────────┐  │
       │                                   │(1080,  │  │
  658  │                                   │ 658.14)│  │
       │ ┌─sram_0───────────────────────┐  └────────┘  │
       │ │ (435,495) → (851.64, 831.46) │              │
  595  │ │                              │ ┌counter2──┐ │
       │ │                              │ │(935,495) │ │
  495  │ └──────────────────────────────┘ └──────────┘ │
       │                                               │
y= 365 └───────────────────────────────────────────────┘
       x=365         906       935          1080      1235
```

Pad order (away from origin) on each side (see [pinout.md](pinout.md) for the full per-pad breakdown):

| Side  | Pad order                                                                             |
| ----- | ------------------------------------------------------------------------------------- |
| West  | SRAM_out, VSS, VDD, IOVSS, IOVDD, enable, rst_n, clk                  (bottom → top)  |
| North | counter1[3:0] (4 outputs), counter1[7:4] / inv1.vin (4 bidir)         (left → right)  |
| South | counter2[7:0] (8 outputs)                                             (left → right)  |
| East  | inverter2 ch1/ch2 analog (4 pads), inverter1.vout1..vout4 (4 outputs) (bottom → top)  |


## Power-distribution network (PDN)

The PDN is generated by [pdn_cfg.tcl](../flow/librelane/pdn_cfg.tcl) on top of the chip top-level grid that LibreLane builds from the `PDN_*` keys in [config.yaml](../flow/librelane/config.yaml). The PDK defaults in `libs.tech/librelane/config.tcl` set the vertical PDN layer to Metal4 and the horizontal one to TopMetal1.

| Domain / macro         | Stripes                                                          | Connect            |
| ---------------------- | ---------------------------------------------------------------- | ------------------ |
| Chip core              | Metal4 vertical + TopMetal1 horizontal                           | Metal4 ↔ TopMetal1 |
| Core ring              | Metal4 + TopMetal1, 15 µm wide, 5 µm spacing, `-connect_to_pads` | core ring ↔ pads   |
| `sram_0` (custom)      | none added, the macro's own Metal4 pins act as the stripes        | Metal4 ↔ TopMetal1 |
| `inverter1/2` (custom) | none added, relies on the chip top-level stripes                  | Metal4 ↔ TopMetal1 |
| Default macro grid     | Metal4 ↔ TopMetal1 (used by counter1 / counter2)                 | Metal4 ↔ TopMetal1 |

Two of these grids look the way they do only because of the metal stack:

- **SRAM.** The macro exposes `VDD!`, `VDDARRAY!` and `VSS!` as vertical Metal4 stripes, 2.81 µm wide on an 11.24 µm pitch. On SG13G2 those pins are reached through a dedicated Metal5 stripe pattern that is bridged up to TopMetal1 and down to Metal4. Here Metal4 is already the top-level vertical PDN layer, so no bridging stripes are added: the top-level TopMetal1 stripes that cross the macro drop TopVia1 stacks onto every pin of the same net. `VSS!` and one group of `VDD!` pins span the full macro height and `VDDARRAY!` spans it from 45 µm up, so every horizontal stripe pair over the macro reaches all three pin groups. The grid is independent of the instance orientation, which is why there is one `sram` grid here and an `sram_NS` / `sram_WE` pair on SG13G2.
- **Inverter.** Each `inverter_top` instance carries its own supply ring, with the two horizontal segments on Metal3 and the two vertical segments on Metal4, joined by a 4 × 5 Via3 array at each of the eight corners. [inverter_top.lef](../macros/inverter/final/lef/inverter_top.lef) therefore lists four `PORT`s per supply pin, two on `Metal3` and two on `Metal4`, one per ring segment. TopMetal1 stays out of the macro entirely, so the top-level TopMetal1 stripes cross the ring and a single Metal4 to TopMetal1 connect feeds it from both stripe directions. A ring that also occupied TopMetal1 would make `pdngen` cut every top-level stripe at the macro and leave the ring unfed, which is an IR-drop failure (`PSM-0069`), not a routing warning.

The SRAM has a secondary `VDDARRAY!` supply pin in its LEF in addition to `VDD!`/`VSS!`. The two `PDN_MACRO_CONNECTIONS` lines in [config.yaml](../flow/librelane/config.yaml) bind both pin sets to the chip top-level `VDD` / `VSS` nets.


## Logos

Two decorative IPs sit in the upper corners of the die (outside the core, between the core ring and the seal ring):

| Instance     | Cell                       | Size         | Location                                                                        |
| ------------ | -------------------------- | ------------ | ------------------------------------------------------------------------------- |
| `jku_logo`   | `sg13cmos5l_ip__jku`       | 100 × 100 µm | `($DIE_AREA[0] + 36.4 + 20.4, $DIE_AREA[3] - 36.4 - 120.4)` = (56.8, 1443.2)    |
| `jku_names`  | `sg13cmos5l_ip__jku_names` | 100 × 100 µm | `($DIE_AREA[2] - 36.4 - 120.4, $DIE_AREA[3] - 36.4 - 120.4)` = (1443.2, 1443.2) |

Both logos are listed as `IGNORE_DISCONNECTED_MODULES` in [config.yaml](../flow/librelane/config.yaml) so LibreLane does not flag them as floating logic. Their pixels are drawn on Metal4, the top thin metal of this stack, where the SG13G2 logos use Metal5.

The third logo, the chip logo in [flow/logo/](../flow/logo/), is not a macro. It is merged into the final GDS after the LibreLane run by [add_logo_fill.sh](../scripts/add_logo_fill.sh), on TopMetal1, together with the TopMetal1 filler.


## Constraints when editing the floorplan

For every macro `M` placed at `(X, Y)` with size `W × H`:

1. **Inside the core:** `X ≥ 365`, `Y ≥ 365`, `X + W ≤ 1235`, `Y + H ≤ 1235`.
2. **No overlap** with any other macro rectangle (RePlAce will diverge with `[GPL-0305]` otherwise).
3. **Aligned to the routing grid:** the `inverter_top` macro additionally requires `X` to be a multiple of 0.48 µm and `Y` a multiple of 0.42 µm.
4. **Clear of the IO ring:** routing inside the bondpad area is reserved for the padframe.
5. **Keep a macro supply ring off one of the two PDN layers.** A ring that occupies Metal4 *and* TopMetal1 blocks both top-level stripe directions at once. `inverter_top` keeps its ring on Metal3 and Metal4, so TopMetal1 stays free.
