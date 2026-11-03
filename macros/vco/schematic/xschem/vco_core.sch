v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {VCO Core, Voltage-Biased NMOS Cross-Coupled Pair} 300 -1740 0 0 1 1 {}
T {After Jung and Park, Electronics Letters 44(10), 2008: no current source,
the center tap of the coil sits on its own supply vdd_core (0.78 V, own pad).
The tank common mode is vdd_core, so vtune from 0 V to VDD sweeps the
accumulation-mode varactors across their C-V transition at 0 V gate-to-well.
Each tank node swings from about 0.11 V to 1.53 V, 0.21 V to 1.32 V post-layout.
The pair draws 4.8 mA at Vgs = vdd_core. Cct1 and Cct2, six cap_cmomf units
(3.8 pF by the model, 3.7 pF in the extraction), decouple vdd_core
at the center tap.} 1440 -1440 0 0 0.3 0.3 {}
N 1120 -280 1340 -280 {lab=VSS}
N 880 -1260 880 -1220 {lab=vdd_core}
N 880 -1260 1120 -1260 {lab=vdd_core}
N 1120 -1260 1420 -1260 {lab=vdd_core}
N 700 -1160 780 -1160 {lab=rf_p}
N 980 -1160 1060 -1160 {lab=rf_n}
N 700 -880 780 -880 {lab=rf_p}
N 980 -880 1060 -880 {lab=rf_n}
N 880 -980 880 -940 {lab=vtune}
N 520 -980 880 -980 {lab=vtune}
N 700 -1160 700 -880 {lab=rf_p}
N 700 -880 700 -660 {lab=rf_p}
N 700 -660 700 -600 {lab=rf_p}
N 700 -600 700 -490 {lab=rf_p}
N 1060 -1160 1060 -880 {lab=rf_n}
N 1060 -880 1060 -660 {lab=rf_n}
N 1060 -660 1060 -600 {lab=rf_n}
N 1060 -600 1060 -490 {lab=rf_n}
N 740 -460 780 -460 {lab=rf_n}
N 780 -460 980 -600 {lab=rf_n}
N 980 -600 1060 -600 {lab=rf_n}
N 980 -460 1020 -460 {lab=rf_p}
N 780 -600 980 -460 {lab=rf_p}
N 700 -600 780 -600 {lab=rf_p}
N 700 -430 700 -280 {lab=VSS}
N 1060 -430 1060 -280 {lab=VSS}
N 640 -460 700 -460 {lab=VSS}
N 640 -460 640 -280 {lab=VSS}
N 1060 -460 1120 -460 {lab=VSS}
N 1120 -460 1120 -280 {lab=VSS}
N 520 -660 700 -660 {lab=rf_p}
N 1060 -660 1240 -660 {lab=rf_n}
N 420 -1460 880 -1460 {lab=vdd_core}
N 880 -1460 880 -1260 {lab=vdd_core}
N 640 -280 700 -280 {lab=VSS}
N 700 -280 1060 -280 {lab=VSS}
N 420 -280 640 -280 {lab=VSS}
N 1060 -280 1120 -280 {lab=VSS}
C {title-3.sym} 0 0 0 0 {name=l1 author="Simon Dorrer" rev=1.0 lock=true}
C {devices/iopin.sym} 420 -1460 0 1 {name=p1 lab=vdd_core}
C {devices/iopin.sym} 420 -280 0 1 {name=p2 lab=VSS}
T {The tank coil sits beside the core in vco_top: the LVS deck extracts it in the top cell of a run.} 700 -1180 0 0 0.25 0.25 {}
C {sg13cmos5l_pr/cap_cmomf.sym} 1120 -1230 0 0 {name=Cct1a[1..2]
model=cap_cmomf
w=19e-6
l=26e-6
mmin=1
mmax=4
subblock=0
m=1
mm_ok=1
spiceprefix=X}
C {devices/lab_pin.sym} 1120 -1200 1 0 {name=l1 sig_type=std_logic lab=VSS}
C {vco_var.sym} 800 -840 0 0 {name=xvar}
C {devices/ipin.sym} 520 -980 0 0 {name=p4 lab=vtune}
C {devices/lab_pin.sym} 920 -820 1 0 {name=l4 sig_type=std_logic lab=VSS}
C {sg13cmos5l_pr/sg13_lv_nmos.sym} 720 -460 0 1 {name=M1
l=0.13u
w=20u
ng=10
m=1
model=sg13_lv_nmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_lv_nmos.sym} 1040 -460 0 0 {name=M2
l=0.13u
w=20u
ng=10
m=1
model=sg13_lv_nmos
spiceprefix=X}
C {devices/iopin.sym} 520 -660 0 1 {name=p5 lab=rf_p}
C {devices/iopin.sym} 1240 -660 0 0 {name=p6 lab=rf_n}
C {sg13cmos5l_pr/cap_cmomf.sym} 1220 -1230 0 0 {name=Cct2a
model=cap_cmomf
w=25.5e-6
l=19e-6
mmin=1
mmax=4
subblock=0
m=1
mm_ok=1
spiceprefix=X}
C {devices/lab_pin.sym} 1220 -1200 1 0 {name=l3 sig_type=std_logic lab=VSS}
C {sg13cmos5l_pr/cap_cmomf.sym} 1320 -1230 2 0 {name=Cct1b[1..2]
model=cap_cmomf
w=19e-6
l=26e-6
mmin=1
mmax=4
subblock=0
m=1
mm_ok=1
spiceprefix=X}
C {devices/lab_pin.sym} 1320 -1200 1 0 {name=l20 sig_type=std_logic lab=VSS}
C {sg13cmos5l_pr/cap_cmomf.sym} 1420 -1230 2 0 {name=Cct2b
model=cap_cmomf
w=25.5e-6
l=19e-6
mmin=1
mmax=4
subblock=0
m=1
mm_ok=1
spiceprefix=X}
C {devices/lab_pin.sym} 1420 -1200 1 0 {name=l21 sig_type=std_logic lab=VSS}
