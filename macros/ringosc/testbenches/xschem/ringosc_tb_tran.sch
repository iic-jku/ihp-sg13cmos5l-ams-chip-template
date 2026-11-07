v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
B 2 1640 -1240 2440 -840 {flags=graph
y1=-0.024
y2=0.019
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=2.5400448e-06
x2=2.55e-06
divx=5
subdivx=1
xlabmag=1.0
ylabmag=1.0


dataset=-1
unitx=1
logx=0
logy=0
linewidth_mult=3
color=4
node=i(VDD)}
B 2 1640 -820 2440 -420 {flags=graph
y1=-0.086
y2=1.6
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=2.5400448e-06
x2=2.55e-06
divx=5
subdivx=1
xlabmag=1.0
ylabmag=1.0
node="x1.vosc
vout"
color="4 7"
dataset=-1
unitx=1
logx=0
logy=0
linewidth_mult=3
autoload=0
}
T {Testbench for transient analysis - Ring Oscillator} 570 -1730 0 0 1 1 {}
N 1380 -1080 1380 -1040 {lab=VDD}
N 1380 -980 1380 -940 {lab=GND}
N 1380 -840 1460 -840 {lab=vout}
N 1260 -840 1260 -820 {lab=vout}
N 1380 -840 1380 -820 {lab=vout}
N 1260 -840 1380 -840 {lab=vout}
N 1260 -760 1260 -740 {lab=GND}
N 1380 -760 1380 -740 {lab=GND}
N 1100 -940 1100 -900 {lab=VDD}
N 1100 -780 1100 -740 {lab=GND}
N 1220 -840 1260 -840 {lab=vout}
C {devices/code_shown.sym} 80 -1370 0 0 {name=NGSPICE
only_toplevel=true 
value="
.include ../../../netlist/pex/ringosc_magic_pex_3.spice
.param VDD=1.5
.csparam VDD=VDD
.param Vcm=VDD/2
.csparam Vcm=Vcm
.temp 27
.param Cload=100f
.param Rload=1k
.options savecurrents reltol=1e-3 abstol=1e-12 gmin=1e-15
.control

save all

* Operating Point Analysis
op
remzerovec
write @schname\\\\.raw
set appendwrite

* Transient Analysis
*tran 100p 5u 2u
tran 100p 2.55u 2.54u
write @schname\\\\.raw

* Plotting
plot vout
plot i(VDD)

* Measurements
* Oscillation frequency from two consecutive rising crossings of the mid-level Vcm.
* The stored transient window has to contain at least two rising edges.
meas tran t_rise1 when v(vout)=Vcm rise=1
meas tran t_rise2 when v(vout)=Vcm rise=2
let T_osc = t_rise2 - t_rise1
let f_osc = 1/T_osc
print T_osc
print f_osc

* Stage delay of the three-stage ring, T_osc = 2 * N * t_d with N = 3
let t_d = T_osc/6
print t_d

* Output swing
meas tran vout_max MAX v(vout)
meas tran vout_min MIN v(vout)
let vout_pp = vout_max - vout_min
print vout_pp

* Write Data
unset appendwrite
set wr_vecnames
set wr_singlescale
wrdata ../plot_simulations/data/@schname\\\\.txt v(vout)

*quit
.endc
"}
C {devices/launcher.sym} 1700 -1410 0 0 {name=h2
descr="Simulate" 
tclcommand="xschem save; xschem netlist; file mkdir $netlist_dir; write_data [save_params] $netlist_dir/[file rootname [file tail [xschem get current_name]]].save; xschem simulate"
}
C {title-3.sym} 0 0 0 0 {name=l2 author="Simon Dorrer" rev=1.0 lock=true}
C {devices/launcher.sym} 1700 -1290 0 0 {name=h1
descr="Load waves" 
tclcommand="xschem raw_read $netlist_dir/[file rootname [file tail [xschem get current_name]]].raw tran"
}
C {devices/launcher.sym} 1700 -1350 0 0 {name=h3
descr="Annotate OP" 
tclcommand="set show_hidden_texts 1; xschem annotate_op"
}
C {devices/vsource.sym} 1380 -1010 0 0 {name=VDD value=\{VDD\}}
C {devices/gnd.sym} 1380 -940 0 0 {name=l3 lab=GND}
C {vdd.sym} 1380 -1080 0 0 {name=l7 lab=VDD}
C {devices/lab_pin.sym} 1460 -840 0 1 {name=l12 sig_type=std_logic lab=vout}
C {devices/code_shown.sym} 1960 -1410 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
.lib cornerMOSlv.lib mos_tt
.lib cornerMOShv.lib mos_tt
.lib cornerRES.lib res_typ
.lib cornerDIO.lib dio_tt
"}
C {devices/gnd.sym} 1100 -740 0 0 {name=l1 lab=GND}
C {vdd.sym} 1100 -940 0 0 {name=l4 lab=VDD}
C {capa.sym} 1260 -790 0 0 {name=C1
m=1
value=\{Cload\}
footprint=1206
device="ceramic capacitor"
}
C {res.sym} 1380 -790 0 0 {name=R1
value=\{Rload\}
footprint=1206
device=resistor
m=1
spice_ignore=true}
C {devices/gnd.sym} 1260 -740 0 0 {name=l5 lab=GND}
C {devices/gnd.sym} 1380 -740 0 0 {name=l6 lab=GND}
C {ringosc.sym} 1100 -1260 0 0 {name=x2
spice_ignore=true}
C {ringosc_pex.sym} 1380 -1260 0 0 {name=x3
spice_ignore=true}
C {ringosc.sym} 1100 -840 0 0 {name=x1
}
C {devices/code_shown.sym} 1640 -1500 0 0 {name=SAVE only_toplevel=true
format="tcleval( @value )"
value="
.include [file rootname [file tail [xschem get schname]]].save
"}
