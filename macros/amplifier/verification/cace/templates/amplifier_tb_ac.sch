v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
B 4 180 -1180 740 -560 {fill = false
dash = 8}
P 4 1 180 -1180 {}
T {Capacitive Load} 550 -740 0 0 0.25 0.25 {}
T {Template Testbench for AC analysis - Amplifier} 470 -1720 0 0 1.2 1.2 {}
T {Self-Biased Amplifier, AC Coupled Input (Av, fcu)} 180 -1210 0 0 0.4 0.4 {}
N 840 -720 840 -680 {lab=VDD}
N 840 -620 840 -580 {lab=GND}
N 1020 -620 1020 -580 {
lab=GND}
N 1020 -720 1020 -680 {
lab=VSS}
N 600 -890 640 -890 {lab=vout}
N 440 -970 440 -950 {lab=VDD}
N 230 -890 270 -890 {lab=vs}
N 230 -890 230 -850 {lab=vs}
N 230 -790 230 -770 {lab=GND}
N 330 -890 380 -890 {lab=vin}
N 440 -830 440 -770 {lab=GND}
N 520 -890 600 -890 {lab=vout}
N 600 -890 600 -850 {lab=vout}
N 600 -790 600 -770 {lab=GND}
C {devices/code_shown.sym} 1220 -1070 0 0 {name=NGSPICE
simulator=ngspice
only_toplevel=false
value="
.include CACE\{DUT_path\}
.temp CACE\{temp\}
.options savecurrents klu method=gear reltol=1e-4 abstol=1e-15 gmin=1e-15 SEED=CACE[CACE\{seed=12345\} + CACE\{iterations=0\}]
* Flag unsafe operating conditions (exceeds models' specified limits)
.option warn=1
.control

save all

* CACE already runs one ngspice per core
set num_threads=1

* AC Analysis
ac dec 101 1 1G

* Voltage gain between the macro pins. Cc leaves the DC point to the feedback rhigh, and vout/vin does not depend on what drives vin
let Av=v(vout)/v(vin)
let Av_mag_dB = vdb(Av)

* Measurements
* 10Hz voltage gain
meas ac Av_dB find Av_mag_dB when frequency = 10

* Upper 3dB cut-off frequency
let Amag_fc = Av_dB-3
meas ac fcu find frequency when Av_mag_dB = Amag_fc FALL=1

echo $&Av_dB $&fcu > CACE\{simpath\}/CACE\{filename\}_CACE\{N\}.data

.endc
"}
C {devices/capa.sym} 600 -820 0 0 {name=C2
m=1
value=CACE\{cload\}
footprint=1206
device="ceramic capacitor"}
C {devices/vsource.sym} 840 -650 0 0 {name=VDD value=CACE\{vdd\}}
C {devices/lab_pin.sym} 640 -890 0 1 {name=l12 sig_type=std_logic lab=vout}
C {devices/vsource.sym} 1020 -650 0 0 {name=VSS value=0 savecurrent=false}
C {devices/gnd.sym} 1020 -580 0 0 {name=l16 lab=GND}
C {devices/lab_wire.sym} 1020 -720 0 0 {name=p1 sig_type=std_logic lab=VSS}
C {devices/gnd.sym} 840 -580 0 0 {name=l2 lab=GND}
C {devices/gnd.sym} 600 -770 0 0 {name=l7 lab=GND}
C {vdd.sym} 840 -720 0 0 {name=l21 lab=VDD}
C {title-3.sym} 0 0 0 0 {name=l67 author="Simon Dorrer" rev=1.0 lock=true}
C {devices/gnd.sym} 440 -770 0 0 {name=l5 lab=GND}
C {vdd.sym} 440 -970 0 0 {name=l9 lab=VDD}
C {devices/code_shown.sym} 1220 -1250 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
.lib cornerMOSlv.lib mos_CACE\{corner_mos\}
.lib cornerMOShv.lib mos_CACE\{corner_mos\}
.lib cornerRES.lib res_CACE\{corner_r\}
"}
C {devices/lab_pin.sym} 230 -890 0 0 {name=l18 sig_type=std_logic lab=vs}
C {devices/lab_wire.sym} 355 -890 0 0 {name=p2 sig_type=std_logic lab=vin}
C {devices/gnd.sym} 230 -770 0 0 {name=l57 lab=GND}
C {devices/capa.sym} 300 -890 1 0 {name=Cc
m=1
value=1u
footprint=1206
device="ceramic capacitor"}
C {amplifier.sym} 440 -890 0 0 {name=x1}
C {devices/vsource.sym} 230 -820 0 1 {name=vs spice_ignore=False value="dc 0 ac 1"
}
