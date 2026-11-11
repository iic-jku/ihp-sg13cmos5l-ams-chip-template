* NGSPICE file created from vco_buf.ext - technology: ihp-sg13cmos5l

.subckt vco_buf VSS VDD vbn_buf rf_out_n rf_out_p vbg_buf rf_p rf_n
X0 a_n2502_n1000# vbn_buf VSS VSS sg13_lv_nmos ad=0.95p pd=5.38u as=0.95p ps=5.38u w=5u l=0.5u
X1 a_n2502_n1000# vbn_buf VSS VSS sg13_lv_nmos ad=0.95p pd=5.38u as=0.95p ps=5.38u w=5u l=0.5u
X2 VSS vbn_buf a_n2502_n1000# VSS sg13_lv_nmos ad=0.95p pd=5.38u as=0.95p ps=5.38u w=5u l=0.5u
X3 VSS vbn_buf a_n2502_n1000# VSS sg13_lv_nmos ad=0.95p pd=5.38u as=0.95p ps=5.38u w=5u l=0.5u
X4 a_n2502_n1000# a_n4900_2020# rf_out_n VSS sg13_lv_nmos ad=0.38p pd=2.38u as=0.38p ps=2.38u w=2u l=0.13u
X5 a_n2502_n1000# vbn_buf VSS VSS sg13_lv_nmos ad=0.95p pd=5.38u as=0.95p ps=5.38u w=5u l=0.5u
X6 a_n2502_n1000# a_n4900_2020# rf_out_n VSS sg13_lv_nmos ad=0.38p pd=2.38u as=0.38p ps=2.38u w=2u l=0.13u
X7 rf_out_n a_n4900_2020# a_n2502_n1000# VSS sg13_lv_nmos ad=0.38p pd=2.38u as=0.38p ps=2.38u w=2u l=0.13u
X8 VSS vbn_buf a_n2502_n1000# VSS sg13_lv_nmos ad=0.95p pd=5.38u as=0.95p ps=5.38u w=5u l=0.5u
X9 a_n2502_n1000# vbn_buf VSS VSS sg13_lv_nmos ad=0.95p pd=5.38u as=0.95p ps=5.38u w=5u l=0.5u
X10 a_n2502_n1000# vbn_buf VSS VSS sg13_lv_nmos ad=0.95p pd=5.38u as=0.95p ps=5.38u w=5u l=0.5u
X11 rf_out_n a_n4900_2020# a_n2502_n1000# VSS sg13_lv_nmos ad=0.38p pd=2.38u as=0.38p ps=2.38u w=2u l=0.13u
X12 rf_out_p a_368_464# a_n2502_n1000# VSS sg13_lv_nmos ad=0.38p pd=2.38u as=0.68p ps=4.68u w=2u l=0.13u
X13 rf_out_n a_n4900_2020# a_n2502_n1000# VSS sg13_lv_nmos ad=0.38p pd=2.38u as=0.38p ps=2.38u w=2u l=0.13u
X14 a_n2502_n1000# a_n4900_2020# rf_out_n VSS sg13_lv_nmos ad=0.38p pd=2.38u as=0.38p ps=2.38u w=2u l=0.13u
X15 a_n2502_n1000# a_368_464# rf_out_p VSS sg13_lv_nmos ad=0.38p pd=2.38u as=0.38p ps=2.38u w=2u l=0.13u
X16 a_n2502_n1000# vbn_buf VSS VSS sg13_lv_nmos ad=0.95p pd=5.38u as=0.95p ps=5.38u w=5u l=0.5u
X17 VSS vbn_buf a_n2502_n1000# VSS sg13_lv_nmos ad=0.95p pd=5.38u as=0.95p ps=5.38u w=5u l=0.5u
X18 VSS vbn_buf a_n2502_n1000# VSS sg13_lv_nmos ad=0.95p pd=5.38u as=0.95p ps=5.38u w=5u l=0.5u
X19 a_n2502_n1000# a_n4900_2020# rf_out_n VSS sg13_lv_nmos ad=0.38p pd=2.38u as=0.38p ps=2.38u w=2u l=0.13u
X20 rf_out_p a_368_464# a_n2502_n1000# VSS sg13_lv_nmos ad=0.38p pd=2.38u as=0.38p ps=2.38u w=2u l=0.13u
X21 a_n2502_n1000# a_368_464# rf_out_p VSS sg13_lv_nmos ad=0.38p pd=2.38u as=0.38p ps=2.38u w=2u l=0.13u
X22 a_n2502_n1000# vbn_buf VSS VSS sg13_lv_nmos ad=0.95p pd=5.38u as=0.95p ps=5.38u w=5u l=0.5u
X23 rf_out_n a_n4900_2020# a_n2502_n1000# VSS sg13_lv_nmos ad=0.38p pd=2.38u as=0.68p ps=4.68u w=2u l=0.13u
X24 a_n2502_n1000# vbn_buf VSS VSS sg13_lv_nmos ad=0.95p pd=5.38u as=0.95p ps=5.38u w=5u l=0.5u
X25 a_n2502_n1000# vbn_buf VSS VSS sg13_lv_nmos ad=0.95p pd=5.38u as=0.95p ps=5.38u w=5u l=0.5u
X26 rf_out_p a_368_464# a_n2502_n1000# VSS sg13_lv_nmos ad=0.38p pd=2.38u as=0.38p ps=2.38u w=2u l=0.13u
X27 vbg_buf a_n4900_2020# VSS rhigh l=8u w=0.5u
X28 vbg_buf a_368_464# VSS rhigh l=8u w=0.5u
X29 VDD rf_out_p VSS rppd l=1.65u w=10u
X30 a_n2502_n1000# a_368_464# rf_out_p VSS sg13_lv_nmos ad=0.38p pd=2.38u as=0.38p ps=2.38u w=2u l=0.13u
X31 VDD rf_out_n VSS rppd l=1.65u w=10u
X32 rf_out_p a_368_464# a_n2502_n1000# VSS sg13_lv_nmos ad=0.38p pd=2.38u as=0.38p ps=2.38u w=2u l=0.13u
X33 VSS vbn_buf a_n2502_n1000# VSS sg13_lv_nmos ad=0.95p pd=5.38u as=0.95p ps=5.38u w=5u l=0.5u
X34 a_n2502_n1000# vbn_buf VSS VSS sg13_lv_nmos ad=0.95p pd=5.38u as=0.95p ps=5.38u w=5u l=0.5u
X35 VSS vbn_buf a_n2502_n1000# VSS sg13_lv_nmos ad=0.95p pd=5.38u as=0.95p ps=5.38u w=5u l=0.5u
X36 a_n2502_n1000# vbn_buf VSS VSS sg13_lv_nmos ad=0.95p pd=5.38u as=0.95p ps=5.38u w=5u l=0.5u
X37 a_n2502_n1000# vbn_buf VSS VSS sg13_lv_nmos ad=0.95p pd=5.38u as=0.95p ps=5.38u w=5u l=0.5u
X38 a_n2502_n1000# a_n4900_2020# rf_out_n VSS sg13_lv_nmos ad=0.68p pd=4.68u as=0.38p ps=2.38u w=2u l=0.13u
X39 a_n2502_n1000# a_368_464# rf_out_p VSS sg13_lv_nmos ad=0.38p pd=2.38u as=0.38p ps=2.38u w=2u l=0.13u
X40 a_n2502_n1000# vbn_buf VSS VSS sg13_lv_nmos ad=0.95p pd=5.38u as=0.95p ps=5.38u w=5u l=0.5u
X41 rf_out_n a_n4900_2020# a_n2502_n1000# VSS sg13_lv_nmos ad=0.38p pd=2.38u as=0.38p ps=2.38u w=2u l=0.13u
X42 rf_out_p a_368_464# a_n2502_n1000# VSS sg13_lv_nmos ad=0.38p pd=2.38u as=0.38p ps=2.38u w=2u l=0.13u
X43 VSS vbn_buf a_n2502_n1000# VSS sg13_lv_nmos ad=0.95p pd=5.38u as=0.95p ps=5.38u w=5u l=0.5u
X44 VSS vbn_buf a_n2502_n1000# VSS sg13_lv_nmos ad=0.95p pd=5.38u as=0.95p ps=5.38u w=5u l=0.5u
X45 VSS vbn_buf a_n2502_n1000# VSS sg13_lv_nmos ad=0.95p pd=5.38u as=0.95p ps=5.38u w=5u l=0.5u
X46 VSS vbn_buf a_n2502_n1000# VSS sg13_lv_nmos ad=0.95p pd=5.38u as=0.95p ps=5.38u w=5u l=0.5u
X47 a_n2502_n1000# vbn_buf VSS VSS sg13_lv_nmos ad=0.95p pd=5.38u as=0.95p ps=5.38u w=5u l=0.5u
X48 a_n2502_n1000# a_n4900_2020# rf_out_n VSS sg13_lv_nmos ad=0.38p pd=2.38u as=0.38p ps=2.38u w=2u l=0.13u
X49 a_n2502_n1000# a_368_464# rf_out_p VSS sg13_lv_nmos ad=0.38p pd=2.38u as=0.38p ps=2.38u w=2u l=0.13u
X50 rf_out_n a_n4900_2020# a_n2502_n1000# VSS sg13_lv_nmos ad=0.38p pd=2.38u as=0.38p ps=2.38u w=2u l=0.13u
X51 rf_out_p a_368_464# a_n2502_n1000# VSS sg13_lv_nmos ad=0.38p pd=2.38u as=0.38p ps=2.38u w=2u l=0.13u
X52 a_n2502_n1000# a_368_464# rf_out_p VSS sg13_lv_nmos ad=0.68p pd=4.68u as=0.38p ps=2.38u w=2u l=0.13u
X53 VSS vbn_buf a_n2502_n1000# VSS sg13_lv_nmos ad=0.95p pd=5.38u as=0.95p ps=5.38u w=5u l=0.5u
X54 VSS vbn_buf a_n2502_n1000# VSS sg13_lv_nmos ad=0.95p pd=5.38u as=0.95p ps=5.38u w=5u l=0.5u
X55 a_n2502_n1000# vbn_buf VSS VSS sg13_lv_nmos ad=0.95p pd=5.38u as=1.7p ps=10.68u w=5u l=0.5u
X56 VSS vbn_buf a_n2502_n1000# VSS sg13_lv_nmos ad=0.95p pd=5.38u as=0.95p ps=5.38u w=5u l=0.5u
X57 VSS vbn_buf a_n2502_n1000# VSS sg13_lv_nmos ad=1.7p pd=10.68u as=0.95p ps=5.38u w=5u l=0.5u
.ends

