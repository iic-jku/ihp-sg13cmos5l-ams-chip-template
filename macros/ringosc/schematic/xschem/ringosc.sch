v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {Three-Stage Ring Oscillator with Output Buffer} 610 -1700 0 0 1 1 {}
N 900 -900 980 -900 {lab=#net1}
N 1120 -900 1200 -900 {lab=#net2}
N 1420 -900 1500 -900 {lab=vosc}
N 1640 -900 1720 -900 {lab=vout}
N 820 -980 820 -940 {lab=VDD}
N 820 -860 820 -820 {lab=VSS}
N 1040 -980 1040 -940 {lab=VDD}
N 1040 -860 1040 -820 {lab=VSS}
N 1260 -860 1260 -820 {lab=VSS}
N 1260 -980 1260 -940 {lab=VDD}
N 1560 -980 1560 -940 {lab=VDD}
N 1560 -860 1560 -820 {lab=VSS}
N 680 -900 760 -900 {lab=vosc}
N 680 -1080 680 -900 {lab=vosc}
N 680 -1080 1420 -1080 {lab=vosc}
N 1420 -1080 1420 -900 {lab=vosc}
N 1340 -900 1420 -900 {lab=vosc}
C {title-3.sym} 0 0 0 0 {name=l1 author="Simon Dorrer" rev=1.0 lock=true}
C {inverter.sym} 820 -900 0 0 {name=x1}
C {inverter.sym} 1040 -900 0 0 {name=x2}
C {inverter.sym} 1260 -900 0 0 {name=x3}
C {inverter.sym} 1560 -900 0 0 {name=x4}
C {lab_pin.sym} 1040 -980 1 0 {name=p3 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 1420 -900 2 1 {name=p4 sig_type=std_logic lab=vosc}
C {lab_pin.sym} 1260 -980 1 0 {name=p7 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 1560 -980 1 0 {name=p8 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 1040 -820 3 0 {name=p9 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 1260 -820 3 0 {name=p10 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 1560 -820 3 0 {name=p11 sig_type=std_logic lab=VSS}
C {devices/iopin.sym} 820 -980 3 0 {name=p1 lab=VDD}
C {devices/iopin.sym} 820 -820 1 0 {name=p5 lab=VSS}
C {devices/opin.sym} 1720 -900 0 0 {name=p6 lab=vout}
