v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {Self-Biased Single-Ended Inverter Amplifier} 690 -1680 0 0 1 1 {}
N 1160 -920 1160 -900 {lab=VDD}
N 1160 -820 1160 -800 {lab=VSS}
N 1020 -860 1100 -860 {lab=vin}
N 1240 -860 1320 -860 {lab=vout}
N 1200 -1040 1320 -1040 {lab=vout}
N 1320 -1040 1320 -860 {lab=vout}
N 1320 -860 1400 -860 {lab=vout}
N 940 -860 1020 -860 {lab=vin}
N 1020 -1040 1140 -1040 {lab=vin}
N 1020 -1040 1020 -860 {lab=vin}
C {title-3.sym} 0 0 0 0 {name=l1 author="Simon Dorrer" rev=1.0 lock=true}
C {devices/ipin.sym} 940 -860 0 0 {name=p10 lab=vin}
C {devices/iopin.sym} 1160 -920 3 0 {name=p11 lab=VDD}
C {devices/iopin.sym} 1160 -800 1 0 {name=p1 lab=VSS}
C {devices/iopin.sym} 1400 -860 0 0 {name=p6 lab=vout}
C {inverter.sym} 1160 -860 0 0 {name=x1}
C {sg13cmos5l_pr/rhigh.sym} 1170 -1040 3 0 {name=R1
w=0.5e-6
l=25e-6
model=rhigh
body=VSS
spiceprefix=X
b=0
 m=1
  mm_ok=1
value="expr_eng(  ( 1.6e-4 / @w + 1360.0 * ( (@b + 1)* @l + ( 1.081*( @w - 0.04e-6 ) + 0.18e-6 )*@b ) / ( @w - 0.04e-6 ) ) / @m  )"
}
