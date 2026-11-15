# Counters

Three 8-bit synchronous up-counters, the same RTL hardened on three standard cell libraries: [`counter_lv_ihp`][lv-ihp], [`counter_lv_eth`][lv-eth] and [`counter_hv_kvc`][hv-kvc] of `ef8524f`. `sel[1:0]` selects one of them. Only the selected counter gets a clock, and its value appears on `count[7:0]`.

| `sel[1:0]` | Counter | Library | Supply |
| --- | --- | --- | --- |
| `00` | none, `count` held at 0 | | |
| `01` | IHP LV | `sg13cmos5l_stdcell` | `VDD` |
| `10` | IHP HV | `sg13cmos5l_stdcell_hv` | `vdd_hv` |
| `11` | ETH LV | `ez130_8t` | `VDD` |


## Connections

| Pin | Signal | Connect to |
| --- | --- | --- |
| 1 | `clk` | clock source, 3.3 V levels |
| 2 | `rst_n` | bench output, active low |
| 3, 4 | `sel[1]`, `sel[0]` | bench outputs |
| 7 | `VDD` | source meter, supply current of the IHP LV and ETH LV counters |
| 24 | `vdd_hv` | source meter, supply current of the IHP HV counter |
| 25 | `count[7]` | logic analyzer. Also drives inverter channel 4 |
| 26 to 32 | `count[6]` to `count[0]` | logic analyzer |


## Procedure

1. Hold `rst_n` low, set `sel[1:0]`, and give at least one rising clock edge: the reset is synchronous. A counter that is not selected gets no clock and keeps its state through a reset.
2. Release `rst_n`. `count` increments on every rising clock edge and wraps from 255 to 0, so `count[7]` runs at the clock frequency divided by 256, 195.3 kHz at 50 MHz.
3. Change `sel[1:0]` only with `rst_n` low or `clk` stopped.

The power of a counter is the rise of its supply current against `sel[1:0]` = `00` at the same clock frequency, times the supply voltage. On `VDD` this includes the select multiplexer. `vdd_hv` feeds the IHP HV counter alone, so only its leakage can be measured apart from the rest of the chip.


## Results

| Parameter | Counter | Condition | Simulated | Source | Measured |
| --- | --- | --- | --- | --- | --- |
| Counts through the wrap | IHP LV | `VDD` 1.2 V, 50 MHz | no setup or hold violation in the six corners of chip STA | [chip STA][sta] | TBD |
| Counts through the wrap | ETH LV | `VDD` 1.2 V, 50 MHz | as IHP LV. Its Liberty ends at 1.32 V, so the corners above reuse the nearest one | [chip STA][sta] | TBD |
| Counts through the wrap | IHP HV | `vdd_hv` 1.2 V to 1.65 V, 50 MHz | 7 of 7 post-layout cases pass, with 50 MHz in each corner from ss 125 °C at 1.2 V to ff -40 °C at 1.65 V | [HV counter][hv-low-vdd] | TBD |
| Highest clock frequency | IHP LV | `VDD` 1.08 V, 1.2 V, 1.32 V | not simulated, chip STA ran at 50 MHz | | TBD |
| Highest clock frequency | ETH LV | `VDD` 1.08 V, 1.2 V, 1.32 V | not simulated | | TBD |
| Highest clock frequency | IHP HV | `vdd_hv` 1.2 V, 1.35 V, 1.5 V, 1.65 V | not simulated | | TBD |
| Power | IHP LV | `VDD` 1.2 V, 50 MHz | 53.2 µW, macro alone, `nom_typ_1p20V_25C` | [power report][lv-ihp-power] | TBD |
| Power | ETH LV | `VDD` 1.2 V, 50 MHz | 30.0 µW, macro alone, `nom_typ_1p20V_25C` | [power report][lv-eth-power] | TBD |
| Power | IHP HV | `vdd_hv` 1.2 V, 50 MHz | none: the Liberty of the library has no dynamic power data and starts at 3.0 V | [HV counter][hv-kvc] | TBD |
| Leakage | IHP HV | `vdd_hv` 1.2 V and 1.65 V, deselected | not simulated | | TBD |


## Setup

| Item | Value |
| --- | --- |
| Samples | TBD |
| Clock source | TBD |
| Logic analyzer | TBD |
| Source meters | TBD |
| Temperature | TBD |

[lv-ihp]: https://github.com/iic-jku/ihp-sg13cmos5l-ams-chip-template/blob/ef8524f81b8355548f01540cfba7907767346396/macros/counter_lv_ihp/README.md
[lv-eth]: https://github.com/iic-jku/ihp-sg13cmos5l-ams-chip-template/blob/ef8524f81b8355548f01540cfba7907767346396/macros/counter_lv_eth/README.md
[hv-kvc]: https://github.com/iic-jku/ihp-sg13cmos5l-ams-chip-template/blob/ef8524f81b8355548f01540cfba7907767346396/macros/counter_hv_kvc/README.md
[hv-low-vdd]: https://github.com/iic-jku/ihp-sg13cmos5l-ams-chip-template/tree/ef8524f81b8355548f01540cfba7907767346396/macros/counter_hv_kvc/testbenches/ngspice/data
[sta]: https://github.com/iic-jku/ihp-sg13cmos5l-ams-chip-template/blob/ef8524f81b8355548f01540cfba7907767346396/verification/reports/stapostpnr_summary.rpt
[lv-ihp-power]: https://github.com/iic-jku/ihp-sg13cmos5l-ams-chip-template/blob/ef8524f81b8355548f01540cfba7907767346396/macros/counter_lv_ihp/verification/stapostpnr_nom_typ_1p20V_25C_power.rpt
[lv-eth-power]: https://github.com/iic-jku/ihp-sg13cmos5l-ams-chip-template/blob/ef8524f81b8355548f01540cfba7907767346396/macros/counter_lv_eth/verification/stapostpnr_nom_typ_1p20V_25C_power.rpt
