* NGSPICE file created from amplifier.ext - technology: ihp-sg13cmos5l

.subckt amplifier vin VDD VSS vout
X0 vout vin VDD VDD sg13_lv_pmos ad=1.14p pd=6.38u as=1.14p ps=6.38u w=6u l=1u
X1 VDD vin vout VDD sg13_lv_pmos ad=1.14p pd=6.38u as=1.14p ps=6.38u w=6u l=1u
X2 vout vin VDD VDD sg13_lv_pmos ad=1.14p pd=6.38u as=1.14p ps=6.38u w=6u l=1u
X3 vout vin VSS VSS sg13_lv_nmos ad=0.19p pd=1.38u as=0.19p ps=1.38u w=1u l=1u
X4 vout vin VSS VSS sg13_lv_nmos ad=0.19p pd=1.38u as=0.19p ps=1.38u w=1u l=1u
X5 VSS VSS VSS VSS sg13_lv_nmos ad=0.34p pd=2.68u as=0.12329n ps=0.24456m w=1u l=1u
X6 VSS vin vout VSS sg13_lv_nmos ad=0.19p pd=1.38u as=0.19p ps=1.38u w=1u l=1u
X7 vout vin VDD VDD sg13_lv_pmos ad=1.14p pd=6.38u as=1.14p ps=6.38u w=6u l=1u
X8 VDD vin vout VDD sg13_lv_pmos ad=1.14p pd=6.38u as=1.14p ps=6.38u w=6u l=1u
X9 vout vin VSS VSS sg13_lv_nmos ad=0.19p pd=1.38u as=0.19p ps=1.38u w=1u l=1u
X10 vout vin VDD VDD sg13_lv_pmos ad=1.14p pd=6.38u as=1.14p ps=6.38u w=6u l=1u
X11 VSS vin vout VSS sg13_lv_nmos ad=0.19p pd=1.38u as=0.19p ps=1.38u w=1u l=1u
X12 VSS vin vout VSS sg13_lv_nmos ad=0.19p pd=1.38u as=0.19p ps=1.38u w=1u l=1u
X13 vin vout VSS rhigh l=25u w=0.5u
X14 VDD vin vout VDD sg13_lv_pmos ad=1.14p pd=6.38u as=1.14p ps=6.38u w=6u l=1u
X15 vout vin VDD VDD sg13_lv_pmos ad=1.14p pd=6.38u as=1.14p ps=6.38u w=6u l=1u
X16 VDD vin vout VDD sg13_lv_pmos ad=1.14p pd=6.38u as=1.14p ps=6.38u w=6u l=1u
X17 vout vin VDD VDD sg13_lv_pmos ad=1.14p pd=6.38u as=1.14p ps=6.38u w=6u l=1u
X18 vout vin VSS VSS sg13_lv_nmos ad=0.19p pd=1.38u as=0.19p ps=1.38u w=1u l=1u
X19 VSS vin vout VSS sg13_lv_nmos ad=0.19p pd=1.38u as=0.19p ps=1.38u w=1u l=1u
X20 VDD vin vout VDD sg13_lv_pmos ad=1.14p pd=6.38u as=1.14p ps=6.38u w=6u l=1u
X21 vout vin VDD VDD sg13_lv_pmos ad=1.14p pd=6.38u as=1.14p ps=6.38u w=6u l=1u
X22 VDD VDD VDD VDD sg13_lv_pmos ad=2.04p pd=12.68u as=0.14199n ps=0.28418m w=6u l=1u
X23 vout vin VSS VSS sg13_lv_nmos ad=0.19p pd=1.38u as=0.19p ps=1.38u w=1u l=1u
X24 VSS vin vout VSS sg13_lv_nmos ad=0.19p pd=1.38u as=0.19p ps=1.38u w=1u l=1u
X25 VDD vin vout VDD sg13_lv_pmos ad=1.14p pd=6.38u as=1.14p ps=6.38u w=6u l=1u
X26 VDD vin vout VDD sg13_lv_pmos ad=1.14p pd=6.38u as=1.14p ps=6.38u w=6u l=1u
X27 VSS vin vout VSS sg13_lv_nmos ad=0.19p pd=1.38u as=0.19p ps=1.38u w=1u l=1u
X28 vout vin VDD VDD sg13_lv_pmos ad=1.14p pd=6.38u as=1.14p ps=6.38u w=6u l=1u
X29 VSS vin vout VSS sg13_lv_nmos ad=0.19p pd=1.38u as=0.19p ps=1.38u w=1u l=1u
X30 vout vin VSS VSS sg13_lv_nmos ad=0.19p pd=1.38u as=0.19p ps=1.38u w=1u l=1u
X31 VSS vin vout VSS sg13_lv_nmos ad=0.19p pd=1.38u as=0.19p ps=1.38u w=1u l=1u
X32 vout vin VSS VSS sg13_lv_nmos ad=0.19p pd=1.38u as=0.19p ps=1.38u w=1u l=1u
X33 VDD vin vout VDD sg13_lv_pmos ad=1.14p pd=6.38u as=1.14p ps=6.38u w=6u l=1u
X34 vout vin VSS VSS sg13_lv_nmos ad=0.19p pd=1.38u as=0.19p ps=1.38u w=1u l=1u
X35 vout vin VDD VDD sg13_lv_pmos ad=1.14p pd=6.38u as=1.14p ps=6.38u w=6u l=1u
X36 VSS vin vout VSS sg13_lv_nmos ad=0.19p pd=1.38u as=0.19p ps=1.38u w=1u l=1u
X37 VDD vin vout VDD sg13_lv_pmos ad=1.14p pd=6.38u as=1.14p ps=6.38u w=6u l=1u
X38 VDD VDD VDD VDD sg13_lv_pmos ad=1.14p pd=6.38u as=0 ps=0 w=6u l=1u
X39 VDD vin vout VDD sg13_lv_pmos ad=1.14p pd=6.38u as=1.14p ps=6.38u w=6u l=1u
X40 vout vin VSS VSS sg13_lv_nmos ad=0.19p pd=1.38u as=0.19p ps=1.38u w=1u l=1u
X41 vout vin VSS VSS sg13_lv_nmos ad=0.19p pd=1.38u as=0.19p ps=1.38u w=1u l=1u
X42 vout vin VDD VDD sg13_lv_pmos ad=1.14p pd=6.38u as=1.14p ps=6.38u w=6u l=1u
X43 VSS vin vout VSS sg13_lv_nmos ad=0.19p pd=1.38u as=0.19p ps=1.38u w=1u l=1u
X44 VSS VSS VSS VSS sg13_lv_nmos ad=0.19p pd=1.38u as=0 ps=0 w=1u l=1u
.ends

