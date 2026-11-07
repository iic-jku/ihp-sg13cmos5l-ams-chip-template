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
T {Template Testbench for transient analysis - Ring Oscillator} 470 -1720 0 0 1.2 1.2 {}
T {Free-Running Oscillation (fosc, Idd)} 180 -1210 0 0 0.4 0.4 {}
N 840 -720 840 -680 {lab=VDD}
N 840 -620 840 -580 {lab=GND}
N 1020 -620 1020 -580 {
lab=GND}
N 1020 -720 1020 -680 {
lab=VSS}
N 600 -890 640 -890 {lab=vout}
N 440 -970 440 -950 {lab=VDD}
N 440 -830 440 -770 {lab=GND}
N 560 -890 600 -890 {lab=vout}
N 600 -890 600 -850 {lab=vout}
N 600 -790 600 -770 {lab=GND}
C {devices/code_shown.sym} 1220 -1070 0 0 {name=NGSPICE
simulator=ngspice
only_toplevel=false
value="
.include CACE\{DUT_path\}
.temp CACE\{temp\}
.options klu method=gear reltol=1e-4 abstol=1e-15 gmin=1e-15 SEED=CACE[CACE\{seed=12345\} + CACE\{iterations=0\}]
* Flag unsafe operating conditions (exceeds models' specified limits)
.option warn=1
* Start-up: the operating point holds vosc low, so the ring does not wait at its mid-rail point for numerical noise
.ic v(x1.vosc)=0
.control

save v(vout) i(VDD)

* CACE already runs one ngspice per core
set num_threads=1

* Transient Analysis
tran 10p 200n 0 20p

* Measurements, without two crossings of VDD/2 fosc stays 0 and fails its minimum
let vmid = CACE\{vdd\}/2
let t_start = 0
let t_stop = 0
let fosc = 0
let Idd = 0
* Skip the start-up, average over 20 periods
meas tran t_start when v(vout)=vmid rise=10
meas tran t_stop when v(vout)=vmid rise=30
if t_stop > t_start
  let fosc = 20/(t_stop-t_start)
  meas tran Idd_avg avg i(VDD) from=$&t_start to=$&t_stop
  let Idd = -Idd_avg
end

echo $&fosc $&Idd > CACE\{simpath\}/CACE\{filename\}_CACE\{N\}.data

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
C {ringosc.sym} 440 -890 0 0 {name=x1}
