# VCO

The 20 GHz LC VCO [`vco_top`][macro] of `ef8524f` on its own supply `vdd_rf`, measured on-wafer: the bond wires of the package are 1.3 mm to 1.7 mm long. Each output has a 50 Ohm resistor to `vdd_rf` on chip, so the load has to be AC-coupled.


## Connections

| Pin | Signal | Path | Connect to |
| --- | --- | --- | --- |
| 9 | `di_en`, enable, active high | digital input pad, 3.3 V levels | DC probe |
| 10 | `vtune`, 0 V to 1.5 V | `padres` | DC probe, source meter |
| 11 to 14 | `VSS`, `rf_out_n`, `rf_out_p`, `VSS` | RF pads on `padbare` | GSSG probe, 100 µm pitch, DC blocks before the instruments |
| 15 | `vdd_rf`, 1.5 V | `padbare` | DC probe, source meter |
| 5 to 8 | `IOVDD`, `IOVSS`, `VDD`, `VSS` | west side | DC probes, `VDD` at 1.5 V |


## Conditions

`VDD` and `vdd_rf` both at 1.5 V, so that `di_en` reaches the VCO at 1.5 V, `sel[1:0]` at `00` and `clk` stopped, so that no digital pad switches. The ETH LV counter stays deselected at this `VDD`.

The simulated values are of the macro alone, without the RF pads and the lines from the macro to them: post-layout at TT, 27 °C, typical resistors and 1.5 V unless stated, with the coil model fitted to its EM simulation. The macro README expects the silicon about 0.2 GHz higher, because the coil model's inductance is about 2 % above the EM result.


## Results

| Parameter | Condition | Simulated | Source | Measured |
| --- | --- | --- | --- | --- |
| Supply current, `vdd_rf` | `di_en` high, `vtune` 0.75 V | 10.8 mA. 9.6 mA to 11.9 mA over the MOS corners from -40 °C to 85 °C at both ends of the tuning range | [Corners][corners] | TBD |
| Supply current, `vdd_rf`, disabled | `di_en` low | 9 nA | [Power-Up and Enable][powerup] | TBD |
| Output power per output into 50 Ohm | `vtune` 0.75 V | -10.2 dBm from the peak-to-peak swing, which counts the harmonics and reads up to about 1 dB high. -8.3 dBm at the fundamental in the schematic (PSS) | [Specification][spec] | TBD |
| Second harmonic at `rf_out_p` | `vtune` 0.75 V | -16.8 dBc. It is common mode, -50.2 dBc between the outputs in the schematic | [Limitations][limits] | TBD |
| Third harmonic at `rf_out_p` | `vtune` 0.75 V | -28.1 dBc | [Limitations][limits] | TBD |
| Frequency against `vdd_rf` | `vtune` 0.75 V, `VDD` and `vdd_rf` from 1.35 V to 1.65 V | not simulated at TT alone, the corner runs combine the supply with the resistor corners | [Corners][corners] | TBD |
| Output settling after `di_en` rises | `vtune` 0.75 V | 99 % of the final swing after 4.8 µs, 5.6 µs at worst over the corners | [Power-Up and Enable][powerup] | TBD |


### Tuning Curve

| `vtune` | Frequency, simulated | `K_VCO`, simulated | Frequency, measured | Output power, measured |
| --- | --- | --- | --- | --- |
| 0 V | 19.40 GHz | 0.49 GHz/V | TBD | TBD |
| 0.25 V | 19.53 GHz | 0.67 GHz/V | TBD | TBD |
| 0.5 V | 19.74 GHz | 1.12 GHz/V | TBD | TBD |
| 0.75 V | 20.09 GHz | 1.59 GHz/V | TBD | TBD |
| 1 V | 20.54 GHz | 1.78 GHz/V | TBD | TBD |
| 1.25 V | 20.98 GHz | 1.63 GHz/V | TBD | TBD |
| 1.5 V | 21.35 GHz | 1.47 GHz/V | TBD | TBD |

From [Tuning Curve][tuning]. Over all 162 post-layout corner runs, with the resistor corners and the supply from 1.35 V to 1.65 V, the VCO runs from 19.07 GHz to 21.59 GHz.


### Phase Noise

At `vtune` 0.75 V, simulated by transient noise of the post-layout netlist over 8 seeds.

| Offset | Simulated | Measured |
| --- | --- | --- |
| 1 MHz | -101.6 dBc/Hz | TBD |
| 3 MHz | -113.9 dBc/Hz | TBD |
| 10 MHz | -123.8 dBc/Hz | TBD |
| 30 MHz | -133.9 dBc/Hz | TBD |
| 100 MHz | -144.4 dBc/Hz | TBD |

From [Phase Noise][pn]. `vdd_rf` reaches the tank through the center-tap resistor: about 30 nV/rtHz on `vdd_rf` at 1 MHz equals the oscillator's own phase noise ([Limitations][limits]), so the noise of the supply source matters.


## Setup

| Item | Value |
| --- | --- |
| Samples | TBD |
| Probe station, GSSG probe and DC probes | TBD |
| DC blocks, cables, and their loss at 20 GHz | TBD |
| Spectrum analyzer or phase noise analyzer | TBD |
| Supplies of `VDD`, `vdd_rf` and `vtune` | TBD |
| Temperature | TBD |

[macro]: https://github.com/iic-jku/ihp-sg13cmos5l-ams-chip-template/blob/ef8524f81b8355548f01540cfba7907767346396/macros/vco/README.md
[spec]: https://github.com/iic-jku/ihp-sg13cmos5l-ams-chip-template/blob/ef8524f81b8355548f01540cfba7907767346396/macros/vco/README.md#specification
[tuning]: https://github.com/iic-jku/ihp-sg13cmos5l-ams-chip-template/blob/ef8524f81b8355548f01540cfba7907767346396/macros/vco/README.md#tuning-curve
[corners]: https://github.com/iic-jku/ihp-sg13cmos5l-ams-chip-template/blob/ef8524f81b8355548f01540cfba7907767346396/macros/vco/README.md#corners
[powerup]: https://github.com/iic-jku/ihp-sg13cmos5l-ams-chip-template/blob/ef8524f81b8355548f01540cfba7907767346396/macros/vco/README.md#power-up-and-enable
[pn]: https://github.com/iic-jku/ihp-sg13cmos5l-ams-chip-template/blob/ef8524f81b8355548f01540cfba7907767346396/macros/vco/README.md#phase-noise
[limits]: https://github.com/iic-jku/ihp-sg13cmos5l-ams-chip-template/blob/ef8524f81b8355548f01540cfba7907767346396/macros/vco/README.md#limitations
