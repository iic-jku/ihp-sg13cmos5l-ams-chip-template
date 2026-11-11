* NGSPICE file created from vco_bias.ext - technology: ihp-sg13cmos5l

.subckt vco_bias di_en en_b vbn_buf vbg_buf VSS VDD
X0 en_b di_en VDD VDD sg13_lv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.13u
X1 en_b di_en VSS VSS sg13_lv_nmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=0.13u
X2 a_3900_n11978# a_3900_n11978# VSS VSS sg13_lv_nmos ad=0.85p pd=5.68u as=0.85p ps=5.68u w=2.5u l=0.5u
X3 VSS vbn_buf VSS VSS sg13_lv_nmos ad=1.52p pd=8.38u as=0.50971n ps=2.36652m w=8u l=10u
X4 VSS vbn_buf VSS VSS sg13_lv_nmos ad=1.52p pd=8.38u as=0 ps=0 w=8u l=10u
X5 VSS vbg_buf VSS VSS sg13_lv_nmos ad=1.52p pd=8.38u as=0 ps=0 w=8u l=10u
X6 VSS vbg_buf VSS VSS sg13_lv_nmos ad=1.52p pd=8.38u as=0 ps=0 w=8u l=10u
X7 a_3900_n9272# en_b VDD VDD sg13_lv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.13u
X8 a_5408_n8844# a_5408_n8844# VDD VDD sg13_lv_pmos ad=1.7p pd=10.68u as=1.7p ps=10.68u w=5u l=0.5u
X9 VDD VDD VDD VDD sg13_lv_pmos ad=1.7p pd=10.68u as=41.581p ps=0.19678m w=5u l=0.5u
X10 vbn_buf a_3900_n11978# VSS rhigh l=32u w=0.5u
X11 VSS VSS VSS VSS sg13_lv_nmos ad=0.85p pd=5.68u as=0 ps=0 w=2.5u l=0.5u
X12 VSS VSS VSS VSS sg13_lv_nmos ad=0.85p pd=5.68u as=0 ps=0 w=2.5u l=0.5u
X13 VSS vbn_buf VSS VSS sg13_lv_nmos ad=1.52p pd=8.38u as=0 ps=0 w=8u l=10u
X14 a_5408_n8844# a_3900_n11978# VSS VSS sg13_lv_nmos ad=0.85p pd=5.68u as=0.85p ps=5.68u w=2.5u l=0.5u
X15 VSS vbn_buf VSS VSS sg13_lv_nmos ad=1.52p pd=8.38u as=0 ps=0 w=8u l=10u
X16 VSS vbg_buf VSS VSS sg13_lv_nmos ad=2.72p pd=16.68u as=0 ps=0 w=8u l=10u
X17 a_5408_n8844# a_4788_n10564# VDD VDD sg13_lv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.13u
X18 VSS vbg_buf VSS VSS sg13_lv_nmos ad=1.52p pd=8.38u as=0 ps=0 w=8u l=10u
X19 VSS vbg_buf VSS VSS sg13_lv_nmos ad=1.52p pd=8.38u as=0 ps=0 w=8u l=10u
X20 VSS vbg_buf VSS VSS sg13_lv_nmos ad=1.52p pd=8.38u as=0 ps=0 w=8u l=10u
X21 VSS vbg_buf VSS VSS sg13_lv_nmos ad=1.52p pd=8.38u as=0 ps=0 w=8u l=10u
X22 a_4400_n9272# a_4400_n11058# VSS rppd l=8.5u w=0.5u
X23 VDD VDD VDD VDD sg13_lv_pmos ad=1.7p pd=10.68u as=0 ps=0 w=5u l=0.5u
X24 VSS vbn_buf VSS VSS sg13_lv_nmos ad=1.52p pd=8.38u as=0 ps=0 w=8u l=10u
X25 VSS vbn_buf VSS VSS sg13_lv_nmos ad=1.52p pd=8.38u as=0 ps=0 w=8u l=10u
X26 a_4400_n11058# a_4400_n11058# VSS VSS sg13_lv_nmos ad=0.85p pd=5.68u as=0.85p ps=5.68u w=2.5u l=0.5u
X27 a_4788_n10564# en_b VDD VDD sg13_lv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.13u
X28 vbn_buf en_b VSS VSS sg13_lv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.13u
X29 a_4788_n10564# en_b VSS VSS sg13_lv_nmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=0.13u
X30 vbg_buf a_4400_n9272# VSS rhigh l=32u w=0.5u
X31 VSS vbn_buf VSS VSS sg13_lv_nmos ad=2.72p pd=16.68u as=0 ps=0 w=8u l=10u
X32 VSS vbg_buf VSS VSS sg13_lv_nmos ad=2.72p pd=16.68u as=0 ps=0 w=8u l=10u
X33 a_3900_n11978# en_b VSS VSS sg13_lv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.13u
X34 VSS vbn_buf VSS VSS sg13_lv_nmos ad=1.52p pd=8.38u as=0 ps=0 w=8u l=10u
X35 VSS vbn_buf VSS VSS sg13_lv_nmos ad=1.52p pd=8.38u as=0 ps=0 w=8u l=10u
X36 a_3900_n9272# a_3900_n11978# VSS rppd l=13.1u w=0.5u
X37 a_4400_n9272# a_5408_n8844# VDD VDD sg13_lv_pmos ad=1.7p pd=10.68u as=1.7p ps=10.68u w=5u l=0.5u
X38 VSS vbn_buf VSS VSS sg13_lv_nmos ad=2.72p pd=16.68u as=0 ps=0 w=8u l=10u
X39 VSS vbg_buf VSS VSS sg13_lv_nmos ad=1.52p pd=8.38u as=0 ps=0 w=8u l=10u
X40 VSS vbg_buf VSS VSS sg13_lv_nmos ad=1.52p pd=8.38u as=0 ps=0 w=8u l=10u
X41 VDD VDD VDD VDD sg13_lv_pmos ad=0.34p pd=2.68u as=0 ps=0 w=1u l=0.13u
.ends

