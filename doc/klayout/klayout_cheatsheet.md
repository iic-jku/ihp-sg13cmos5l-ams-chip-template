# KLayout IHP SG13CMOS5L Cheat Sheet

## Plugins

- **Productivity Suite** by Martin Köhler:

  <https://github.com/iic-jku/klayout-productivity-suite>

---

## Layout Tips

- Layout an inverter first and go through all the design steps and get used to KLayout.
- Place dummy resistors with minimum length above and below the actual resistor.
- Use alternating metal layers for horizontal (M1/M3/TM1) and vertical (M2/M4) connections to minimize coupling. This stack has five routing metals in total: Metal1 to Metal4 plus TopMetal1, no Metal5 and no TopMetal2.
- Restrict routing within the sub-circuit to lower metal layers: M1-M3
- Route sensitive signals first.
- Avoid the shadowing effect (orient the bias transistor in the same direction as the mirror transistor).
- Use self-made decoupling capacitors with NMOS capacitors at the bottom (for low-Q decoupling) and metal capacitors between each layer with alternating (vertical and horizontal) VIA contacts.
  - This fixes ringing that would otherwise occur when bond-wire inductance and high-Q metal capacitors resonate.
  - Example stack: NMOS (VDD) → M1 (VSS) → M2 (VDD), again alternating vertical and horizontal.
  - Alternative: Use PMOS instead of NMOS, as this often is recommended for better ESD robustness.
- **RF decoupling:** Add an additional RC circuit in series with the supply voltage.

---

## Project Start

1. Open KLayout in edit mode with `klayout -e` (or `ke`). In this repository, `make open` gives one button per design file, and `make librelane-klayout` opens the last LibreLane run.
2. **File → New Layout**:
    - Choose top cell name
    - Set **Data Base Unit (DBU)** to **0.001 µm** → IMPORTANT for IHP Open-PDK*
3. **File → Open** a hierarchical layout (`.klay.gds`), which allows sub-cells / sub-cell trees.
4. Hide empty layers.
5. Place instances by selecting and dragging them in.

\* If the DBU has been set wrong (e.g. to **0.005 µm**), change the DBU and scale the layout accordingly afterwards:
- **File → Layout Properties** → set DBU = `0.001 µm`
- **Edit → Layout → Scale** → enter `5.0` → press **OK** only (not *Apply + OK*, otherwise it scales 25 times → reported KLayout bug)
---

## Add Shortcuts

1. **File → Setup**
2. Customize Menu
3. Search for function and enter shortcut

The PDK's own macros ship with an empty `<shortcut/>`, so the `F9` to `F12` keys used below for DRC and LVS are the ones you assign here, not defaults.

---

## Net Tracer

1. **Tools → Trace Net**
2. Configure: tick `Halo`, `line width` = 3pixel, 90% `intensity increase`
3. Search for function and enter shortcut

---

## Enable Layer Numbers

1. **File → Setup**
2. Layer Properties
3. Tick *Always show layer source in layer list*

---

## Libraries (`.klib` File, Hierarchical Layout Only)

- Add entries in the `.klib` file:
  - Manually directly to the `.klib` file
  - In the GUI via "File / Cell Library Manager Map"
- Works for both `.gds` and `.klay.gds`.
- Build the cell tree bottom-up.

The two PCell libraries keep the names they have on SG13G2, `SG13_dev` and `SG13_native_pcell_lib`, but the device list is the SG13CMOS5L one. Every PCell is registered under the name of its `<name>_code.py` file in `libs.tech/klayout/python/sg13cmos5l_pycell_lib/ihp/`.

Common `SG13_dev` PCells:

- Transistors: `nmos`, `pmos` (low-voltage, 1.5 V) and `nmosHV`, `pmosHV` (high-voltage, 3.3 V), plus the RF variants `rfnmos`, `rfpmos`, `rfnmosHV`, `rfpmosHV`
- Resistors: `rppd`, `rsil`, `rhigh`
- Capacitors: `cap_cmomi` (interdigitated metal-oxide-metal), `cap_cmomf` (metal fringe), `moscap_n`, `moscap_p`
  - SG13CMOS5L has **no MIM capacitor**. `cmim` / `rfcmim` need the MIM layer, which this process does not offer, so use the MoM or MOS capacitors instead.
- Varactor: `SVaricap`
- Bipolar: `pnpMPA`. There are **no HBTs** (`npn13G2` and friends do not exist here).
- Antenna diodes: `dantenna`, `dpantenna`. ESD devices: `esd`
- Well/substrate contacts: `guard_ring`, `ntap1`, `ptap1`
- Pads and seal ring: `bondpad`, `sealring`
- Filler exclusion: `NoFillerStack`
- Vias:
  - `via_stack` from `SG13_dev`
  - `Via` from the `SG13_native_pcell_lib` library
- etc.

The `bondpad` PCell has a smaller parameter space here than on SG13G2: `topMetal` is fixed to `TM1` and `bottomMetal` accepts `1` to `4` only. Selecting `TM1` as the bottom metal crashes the PCell code.

---

## Layer Roles

- `MetalX.drawing`: actual connections
- `MetalX.pin`: input, output, inout pins placement
- `MetalX.text`: label of the pins
- Use filler layers later for final density closure.

---

## Padframe

| Component      | Notes                                           |
| -------------- | ----------------------------------------------- |
| Seal ring      | Place at origin with `Shift + O` (25 µm offset) |
| IHP Pads       | `sg13cmos5l_io`, 80 µm × 180 µm per cell        |
| RF Pads        | add VIA ring for robustness                     |
| IO Pads        | 3.3 V                                           |
| VDD / VSS Pads | 1.5 V                                           |
| Bond Pads      | 70 µm x 70 µm                                   |

---

## Shortcuts

### General Editing

| Shortcut    | Action                                           |
| ----------- | ------------------------------------------------ |
| `Q`         | Properties of selected objects/pcells            |
| `P`         | Path / drawing tool (double-click to finish)     |
| `U`         | Undo                                             |
| `Shift + U` | Redo                                             |
| `F`         | Zoom full                                        |
| `R`         | Draw rectangle                                   |
| `A`         | Align tool: click on dot (middle / corner / edge)     |
| `C`         | Copy object                                      |
| `M`         | Move quickly (connections & movements: diagonal) |
| `T`         | Place text                                       |
| `K`         | Ruler+                                           |
| `Shift + K` | Clear all Ruler+s                                |
| `Shift + C` | Toggle Crosshair Cursor                          |

### Pins & VIAs

| Shortcut    | Action                                                             |
| ----------- | ------------------------------------------------------------------ |
| `Shift + P` | Set pin (input, output, …) for LVS                                 |
| `O`         | Place VIAs during routing (pathmode)                               |
|             | Manual VIA stack via IHP Pcells → drag out → `Q` → set layer input |

### Instance Manipulation

| Shortcut    | Action                     |
| ----------- | -------------------------- |
| `E`         | Descend into instance      |
| `Ctrl + E`  | Ascend from instance       |
| Middle Mouse Button | Show As New Top	   |
| `Shift + R` | Rotate instance by 90°     |
| `Shift + H` | Flip instance horizontally |
| `Shift + V` | Flip instance vertically   |
| `Shift + O` | Set origin                 |

### Hierarchy Visibility

| Shortcut    | Action                                 |
| ----------- | -------------------------------------- |
| `Ctrl + F`  | Hide all instances per hierarchy level |
| `Shift + F` | Show all instances per hierarchy level |

### Layer Visibility

| Key | Layer Focus                  |
| --- | ---------------------------- |
| `0` | Show default layers          |
| `,` | Hide default layers          |
| `1` | 1st metal and related VIAs   |
| `2` | 2nd metal and related VIAs   |
| `3` | 3rd metal and related VIAs   |
| `4` | 4th metal and related VIAs   |
| `5` | 5th metal and related VIAs   |
| `6` | 6th metal and related VIAs   |
| `7` | 7th metal and related VIAs   |
| `8` | Gate poly and related layers |
| `9` | Diffusion and related layers |
| `Shift+1`      | Extend the focus to include 1st metal and related vias   |
| `Shift+2`      | Extend the focus to include 2nd metal and related vias   |
| `Shift+3`      | Extend the focus to include 3rd metal and related vias   |
| `Shift+4`      | Extend the focus to include 4th metal and related vias   |
| `Shift+5`      | Extend the focus to include 5th metal and related vias   |
| `Shift+6`      | Extend the focus to include 6th metal and related vias   |
| `Shift+7`      | Extend the focus to include 7th metal and related vias   |
| `Shift+8`      | Extend the focus to include Gate Poly and related vias   |
| `Shift+9`      | Extend the focus to include Diffusion and related vias   |

The table is the plugin's, not the PDK's. SG13CMOS5L has five routing metals (Metal1 to Metal4, then TopMetal1 as the fifth), so keys `6` and `7` have nothing to show here.

---

## LVS (Layout vs. Schematic)

- Open-Source Tool Check
  - Xschem:
    - **Simulation → LVS → untick "Use 'spiceprefix' attribute"**
    - **Simulation → LVS → tick "LVS netlist + Top level is a .subckt" and "Upper case .SUBCKT and .ENDS"**
    - **Simulation → "Set top level netlist name" → enter top level netlist name (equals file name + `.cdl` or `.spice`)**
    - **Right top corner → click on "create netlist" → creates a `.cdl` or `.spice` file**
  - KLayout:
    - Rename the cell to match the LVS netlist name
    - **SG13CMOS5L PDK → SG13CMOS5L LVS Options (`F12`) → set "Netlist Path"**
    - **SG13CMOS5L PDK → Run Klayout LVS (`F11`)**

The same run is available headless as `make klayout-lvs CELL=<cellname>` in a macro folder, with `make klayout-lvs-netlist` exporting the schematic netlist from Xschem first.

---

## DRC (Design Rule Check)

- Open-Source Tool Check
  - KLayout:
    - **SG13CMOS5L PDK → SG13CMOS5L DRC Options (`F10`)**
      - *Basic* tab: leave "Disable FEOL Checks", "Disable BEOL Checks" and "Disable Extra Rule Set" unticked.
      - *Advanced* tab:
        - "Disable Density Checks" is ticked by default, keep it that way only at the beginning.
        - Tick "Enable Antenna Checks".
    - **SG13CMOS5L PDK → Run Klayout DRC (`F9`)**

Headless equivalent: `make klayout-drc CELL=<cellname> DRC_LEVEL=<precheck|macro|regular>`.

---

## Makefiles

- Every macro folder contains Makefile targets for common verification and extraction flows, including DRC, LVS, and PEX with KLayout or Magic & Netgen.
- `kpex` does not support `ihp-sg13cmos5l` yet, so `make klayout-pex` fails on this PDK. Use `make magic-pex` for parasitic extraction until that lands.

---
