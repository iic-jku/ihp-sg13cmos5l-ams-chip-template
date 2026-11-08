v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 1260 -1780 1200 -1780 {lab=clk}
N 1260 -1730 1200 -1730 {lab=rst_n}
N 1260 -1680 1200 -1680 {lab=sel0}
N 1260 -1630 1200 -1630 {lab=sel1}
N 1260 -1580 1200 -1580 {lab=di_en}
N 1260 -1530 1200 -1530 {lab=IOVDD}
N 1260 -1480 1200 -1480 {lab=GND}
N 1260 -1430 1200 -1430 {lab=VDD}
N 1260 -1380 1200 -1380 {lab=GND}
N 1940 -1780 2000 -1780 {lab=vtune}
N 1940 -1730 2000 -1730 {lab=amp_vin}
N 1940 -1680 2000 -1680 {lab=amp_vout}
N 1940 -1630 2000 -1630 {lab=inv_vin}
N 1940 -1580 2000 -1580 {lab=inv_vout}
N 1940 -1530 2000 -1530 {lab=ro_vout}
N 1940 -1480 2000 -1480 {lab=vdd_ro}
N 1940 -1430 2000 -1430 {lab=vdd_hv}
N 1940 -1380 2000 -1380 {lab=vdd_rf}
N 1360 -1940 1360 -2000 {lab=count0}
N 1420 -1940 1420 -2000 {lab=count1}
N 1480 -1940 1480 -2000 {lab=count2}
N 1540 -1940 1540 -2000 {lab=count3}
N 1600 -1940 1600 -2000 {lab=count4}
N 1660 -1940 1660 -2000 {lab=count5}
N 1720 -1940 1720 -2000 {lab=count6}
N 1780 -1940 1780 -2000 {lab=inv_dout}
N 1840 -1940 1840 -2000 {lab=count7}
N 1570 -1260 1570 -1200 {lab=rf_out_n}
N 1630 -1260 1630 -1200 {lab=rf_out_p}
N 200 -1130 200 -1170 {lab=VDD}
N 200 -1070 200 -1040 {lab=GND}
N 460 -1130 460 -1170 {lab=IOVDD}
N 460 -1070 460 -1040 {lab=GND}
N 720 -1130 720 -1170 {lab=vdd_rf}
N 720 -1070 720 -1040 {lab=GND}
N 980 -1130 980 -1170 {lab=vdd_ro}
N 980 -1070 980 -1040 {lab=GND}
N 1240 -1130 1240 -1170 {lab=vdd_hv}
N 1240 -1070 1240 -1040 {lab=GND}
N 200 -850 200 -890 {lab=clk}
N 200 -790 200 -760 {lab=GND}
N 200 -610 200 -650 {lab=rst_n}
N 200 -550 200 -520 {lab=GND}
N 200 -390 200 -430 {lab=sel1}
N 200 -330 200 -300 {lab=GND}
N 200 -170 200 -210 {lab=sel0}
N 200 -110 200 -80 {lab=GND}
N 720 -850 720 -890 {lab=di_en}
N 720 -790 720 -760 {lab=GND}
N 980 -850 980 -890 {lab=vtune}
N 980 -790 980 -760 {lab=GND}
N 1240 -850 1240 -890 {lab=inv_vin}
N 1240 -790 1240 -760 {lab=GND}
N 1500 -850 1500 -890 {lab=amp_ac}
N 1500 -790 1500 -760 {lab=GND}
N 1770 -880 1760 -880 {lab=amp_ac}
N 1830 -880 1860 -880 {lab=amp_vin}
C {chip_top.sym} 1600 -1600 0 0 {name=x1}
C {devices/lab_wire.sym} 1200 -1780 2 0 {name=p1 sig_type=std_logic lab=clk}
C {devices/lab_wire.sym} 1200 -1730 2 0 {name=p2 sig_type=std_logic lab=rst_n}
C {devices/lab_wire.sym} 1200 -1680 2 0 {name=p3 sig_type=std_logic lab=sel0}
C {devices/lab_wire.sym} 1200 -1630 2 0 {name=p4 sig_type=std_logic lab=sel1}
C {devices/lab_wire.sym} 1200 -1580 2 0 {name=p5 sig_type=std_logic lab=di_en}
C {devices/lab_wire.sym} 1200 -1530 2 0 {name=p6 sig_type=std_logic lab=IOVDD}
C {devices/lab_wire.sym} 1200 -1480 2 0 {name=p7 sig_type=std_logic lab=GND}
C {devices/lab_wire.sym} 1200 -1430 2 0 {name=p8 sig_type=std_logic lab=VDD}
C {devices/lab_wire.sym} 1200 -1380 2 0 {name=p9 sig_type=std_logic lab=GND}
C {devices/lab_wire.sym} 2000 -1780 0 0 {name=p10 sig_type=std_logic lab=vtune}
C {devices/lab_wire.sym} 2000 -1730 0 0 {name=p11 sig_type=std_logic lab=amp_vin}
C {devices/lab_wire.sym} 2000 -1680 0 0 {name=p12 sig_type=std_logic lab=amp_vout}
C {devices/lab_wire.sym} 2000 -1630 0 0 {name=p13 sig_type=std_logic lab=inv_vin}
C {devices/lab_wire.sym} 2000 -1580 0 0 {name=p14 sig_type=std_logic lab=inv_vout}
C {devices/lab_wire.sym} 2000 -1530 0 0 {name=p15 sig_type=std_logic lab=ro_vout}
C {devices/lab_wire.sym} 2000 -1480 0 0 {name=p16 sig_type=std_logic lab=vdd_ro}
C {devices/lab_wire.sym} 2000 -1430 0 0 {name=p17 sig_type=std_logic lab=vdd_hv}
C {devices/lab_wire.sym} 2000 -1380 0 0 {name=p18 sig_type=std_logic lab=vdd_rf}
C {devices/lab_wire.sym} 1360 -2000 3 0 {name=p19 sig_type=std_logic lab=count0}
C {devices/lab_wire.sym} 1420 -2000 3 0 {name=p20 sig_type=std_logic lab=count1}
C {devices/lab_wire.sym} 1480 -2000 3 0 {name=p21 sig_type=std_logic lab=count2}
C {devices/lab_wire.sym} 1540 -2000 3 0 {name=p22 sig_type=std_logic lab=count3}
C {devices/lab_wire.sym} 1600 -2000 3 0 {name=p23 sig_type=std_logic lab=count4}
C {devices/lab_wire.sym} 1660 -2000 3 0 {name=p24 sig_type=std_logic lab=count5}
C {devices/lab_wire.sym} 1720 -2000 3 0 {name=p25 sig_type=std_logic lab=count6}
C {devices/lab_wire.sym} 1780 -2000 3 0 {name=p26 sig_type=std_logic lab=inv_dout}
C {devices/lab_wire.sym} 1840 -2000 3 0 {name=p27 sig_type=std_logic lab=count7}
C {devices/lab_wire.sym} 1570 -1200 1 0 {name=p28 sig_type=std_logic lab=rf_out_n}
C {devices/lab_wire.sym} 1630 -1200 1 0 {name=p29 sig_type=std_logic lab=rf_out_p}
C {devices/vsource.sym} 200 -1100 0 0 {name=Vvdd value="\{VDD\}"}
C {devices/lab_wire.sym} 200 -1170 0 0 {name=p30 sig_type=std_logic lab=VDD}
C {devices/gnd.sym} 200 -1040 0 0 {name=l31 lab=GND}
C {devices/vsource.sym} 460 -1100 0 0 {name=Viovdd value="\{IOVDD\}"}
C {devices/lab_wire.sym} 460 -1170 0 0 {name=p32 sig_type=std_logic lab=IOVDD}
C {devices/gnd.sym} 460 -1040 0 0 {name=l33 lab=GND}
C {devices/vsource.sym} 720 -1100 0 0 {name=Vrf value="\{VDDRF\}"}
C {devices/lab_wire.sym} 720 -1170 0 0 {name=p34 sig_type=std_logic lab=vdd_rf}
C {devices/gnd.sym} 720 -1040 0 0 {name=l35 lab=GND}
C {devices/vsource.sym} 980 -1100 0 0 {name=Vro value="\{VDDRO\}"}
C {devices/lab_wire.sym} 980 -1170 0 0 {name=p36 sig_type=std_logic lab=vdd_ro}
C {devices/gnd.sym} 980 -1040 0 0 {name=l37 lab=GND}
C {devices/vsource.sym} 1240 -1100 0 0 {name=Vhv value="\{VDDHV\}"}
C {devices/lab_wire.sym} 1240 -1170 0 0 {name=p38 sig_type=std_logic lab=vdd_hv}
C {devices/gnd.sym} 1240 -1040 0 0 {name=l39 lab=GND}
C {devices/vsource.sym} 200 -820 0 0 {name=vclk value="pulse(0 \{IOVDD\} 0 100p 100p \{0.5/fclk\} \{1/fclk\})"}
C {devices/lab_wire.sym} 200 -890 0 0 {name=p40 sig_type=std_logic lab=clk}
C {devices/gnd.sym} 200 -760 0 0 {name=l41 lab=GND}
C {devices/vsource.sym} 200 -580 0 0 {name=vrst value="pwl(0 0 200n 0 200.1n \{IOVDD\} 1.4u \{IOVDD\} 1.4001u 0 1.7u 0 1.7001u \{IOVDD\} 2.9u \{IOVDD\} 2.9001u 0 3.2u 0 3.2001u \{IOVDD\} 4.4u \{IOVDD\} 4.4001u 0 4.7u 0 4.7001u \{IOVDD\})"}
C {devices/lab_wire.sym} 200 -650 0 0 {name=p42 sig_type=std_logic lab=rst_n}
C {devices/gnd.sym} 200 -520 0 0 {name=l43 lab=GND}
C {devices/vsource.sym} 200 -360 0 0 {name=vsel1 value="pwl(0 0 1.5u 0 1.5001u \{IOVDD\} 4.5u \{IOVDD\} 4.5001u 0)"}
C {devices/lab_wire.sym} 200 -430 0 0 {name=p44 sig_type=std_logic lab=sel1}
C {devices/gnd.sym} 200 -300 0 0 {name=l45 lab=GND}
C {devices/vsource.sym} 200 -140 0 0 {name=vsel0 value="pwl(0 \{IOVDD\} 1.5u \{IOVDD\} 1.5001u 0 3.0u 0 3.0001u \{IOVDD\} 4.5u \{IOVDD\} 4.5001u 0)"}
C {devices/lab_wire.sym} 200 -210 0 0 {name=p46 sig_type=std_logic lab=sel0}
C {devices/gnd.sym} 200 -80 0 0 {name=l47 lab=GND}
C {devices/vsource.sym} 720 -820 0 0 {name=vdi_en value="0"}
C {devices/lab_wire.sym} 720 -890 0 0 {name=p48 sig_type=std_logic lab=di_en}
C {devices/gnd.sym} 720 -760 0 0 {name=l49 lab=GND}
C {devices/vsource.sym} 980 -820 0 0 {name=vvtune value="\{Vcm\}"}
C {devices/lab_wire.sym} 980 -890 0 0 {name=p50 sig_type=std_logic lab=vtune}
C {devices/gnd.sym} 980 -760 0 0 {name=l51 lab=GND}
C {devices/vsource.sym} 1240 -820 0 0 {name=vinvin value="sin(\{Vcm\} 10m 200k)"}
C {devices/lab_wire.sym} 1240 -890 0 0 {name=p52 sig_type=std_logic lab=inv_vin}
C {devices/gnd.sym} 1240 -760 0 0 {name=l53 lab=GND}
C {devices/vsource.sym} 1500 -820 0 0 {name=vampin value="sin(0 5m 1meg)"}
C {devices/lab_wire.sym} 1500 -890 0 0 {name=p54 sig_type=std_logic lab=amp_ac}
C {devices/gnd.sym} 1500 -760 0 0 {name=l55 lab=GND}
C {devices/capa.sym} 1800 -880 3 0 {name=C1 m=1 value=1n footprint=1206 device="ceramic capacitor"}
C {devices/lab_wire.sym} 1760 -880 0 0 {name=p56 sig_type=std_logic lab=amp_ac}
C {devices/lab_wire.sym} 1860 -880 2 0 {name=p57 sig_type=std_logic lab=amp_vin}
C {devices/code.sym} 200 -2450 0 0 {name=NGSPICE
only_toplevel=true
value="
.include ../../../ip/sg13cmos5l_io_custom/spice/sg13cmos5l_io.spi
.include ../../../macros/counter_lv_ihp/netlist/xspice/counter_lv_ihp_top.xspice
.include ../../../macros/counter_lv_eth/netlist/xspice/counter_lv_eth_top.xspice
* The XSPICE model of the HV counter is built for 3.3 V, so the bench uses its post-layout netlist
.include ../../../macros/counter_hv_kvc/netlist/pex/counter_hv_kvc_top_magic_pex_3.spice
.include ../../../macros/vco/netlist/spice/vco_ind_le.spice
.param IOVDD=3.3
.param VDD=1.2
.param VDDRF=1.5
.param VDDRO=1.2
.param VDDHV=1.2
.param Vcm=0.6
.temp 27
.param fclk=50e6
.csparam fclk=fclk
.param Cload=10p
.param Rload=1k
* Package and instrument loads
Cl0 count0 0 \{Cload\}
Cl1 count1 0 \{Cload\}
Cl2 count2 0 \{Cload\}
Cl3 count3 0 \{Cload\}
Cl4 count4 0 \{Cload\}
Cl5 count5 0 \{Cload\}
Cl6 count6 0 \{Cload\}
Cl7 count7 0 \{Cload\}
Cl8 inv_dout 0 \{Cload\}
Cl9 ro_vout 0 1p
Rl1 amp_vout 0 \{Rload*100\}
Cl10 amp_vout 0 1p
Rl2 inv_vout 0 \{Rload*100\}
Cl11 inv_vout 0 1p
Rrfn rf_out_n 0 50
Rrfp rf_out_p 0 50
.options klu method=gear reltol=3e-3 vntol=1e-5 abstol=1e-11 chgtol=1e-11 cshunt=100f rshunt=1e15
.control

set num_threads=16

save clk rst_n sel1 sel0 di_en count0 count1 count2 count3 count4 count5 count6 count7 inv_dout inv_vin inv_vout amp_vin amp_vout ro_vout rf_out_n rf_out_p i(Vvdd) i(Vhv) i(Vro) i(Vrf) i(Viovdd)

* User Constants
let tstart = 0
let tstop = 5u
let tstep = 100p

* Transient Operating Point Analysis
op
remzerovec
write @schname\\\\.raw
set appendwrite

* Transient Analysis
tran $&tstep $&tstop $&tstart
write @schname\\\\.raw

* Write Data
unset appendwrite
set wr_vecnames
set wr_singlescale
wrdata ../plot_simulations/data/chip_top_tb_tran.txt
+ v(clk) v(rst_n) v(sel1) v(sel0) v(di_en)
+ v(count0) v(count1) v(count2) v(count3) v(count4) v(count5) v(count6) v(count7)
+ v(inv_dout) v(inv_vin) v(inv_vout) v(amp_vin) v(amp_vout) v(ro_vout)
+ i(Vvdd) i(Vhv) i(Vro)
.endc
"}
C {devices/code_shown.sym} 700 -2450 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
.lib cornerMOSlv.lib mos_tt
.lib cornerMOShv.lib mos_tt
.lib cornerRES.lib res_typ
.lib cornerCAP.lib cap_typ
.lib ../models/cornerDIO_custom.lib dio_tt
.include $::env(PDK_ROOT)/$::env(PDK)/libs.ref/sg13cmos5l_stdcell/spice/sg13cmos5l_stdcell.spice
"}
C {devices/title-2.sym} 0 0 0 0 {name=l_title author="Simon Dorrer" rev=1.0 lock=true}
