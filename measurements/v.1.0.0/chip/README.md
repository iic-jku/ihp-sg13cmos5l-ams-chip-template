# Chip Bring-Up

The die photo and the checks before and at the first power-up of each sample. The pad ring and the supplies are described in [`doc/pinout.md`][pinout] and [`doc/specifications.md`][spec] of `ef8524f`.


## Die Photo

A photo of a bare die goes into `figures/`, at the orientation of the layout render [`chip_top_white.png`][render] of `ef8524f`.

| Sample | Microscope and objective | Figure |
| --- | --- | --- |
| TBD | TBD | TBD |


## Pad Check

Unpowered, every signal pad against `VSS` and against `IOVSS`, to find shorts and opens before the first power-up. The ESD diodes of the pads show as forward-biased diodes.

| Sample | Pads checked | Short or open | Measured |
| --- | --- | --- | --- |
| TBD | TBD | TBD | TBD |


## Quiescent Supply Currents

Power up in the order of the [operating rules](../README.md#operating-rules), with `sel[1:0]` = `00`, `clk` stopped, `rst_n` low and `di_en` low. Each supply has its own source meter. `vdd_ro` (pin 22) stays at 0 V, which keeps the ring oscillator off.

| Supply | Pin | Voltage | Simulated | Source | Measured |
| --- | --- | --- | --- | --- | --- |
| `IOVDD` | 5 | 3.3 V | not simulated | | TBD |
| `VDD` | 7 | 1.2 V | not simulated | | TBD |
| `vdd_rf` | 15 | 1.5 V | 9 nA, VCO alone, post-layout, TT, 27 °C | [VCO][vco] | TBD |
| `vdd_hv` | 24 | 1.2 V | not simulated | | TBD |

[pinout]: https://github.com/iic-jku/ihp-sg13cmos5l-ams-chip-template/blob/ef8524f81b8355548f01540cfba7907767346396/doc/pinout.md
[spec]: https://github.com/iic-jku/ihp-sg13cmos5l-ams-chip-template/blob/ef8524f81b8355548f01540cfba7907767346396/doc/specifications.md
[render]: https://github.com/iic-jku/ihp-sg13cmos5l-ams-chip-template/blob/ef8524f81b8355548f01540cfba7907767346396/render/img/chip_top_white.png
[vco]: https://github.com/iic-jku/ihp-sg13cmos5l-ams-chip-template/blob/ef8524f81b8355548f01540cfba7907767346396/macros/vco/README.md#power-up-and-enable
