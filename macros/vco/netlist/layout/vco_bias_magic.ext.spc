* NGSPICE file created from vco_bias.ext - technology: ihp-sg13cmos5l

.subckt vco_bias di_en ibias_100u vbn_buf vbg_buf VSS VDD
X0 a_4745_n10428# di_en VDD VDD sg13_lv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.13u
X1 a_4745_n10428# di_en VSS VSS sg13_lv_nmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=0.13u
X2 ibias_100u ibias_100u VSS VSS sg13_lv_nmos ad=0.85p pd=5.68u as=0.85p ps=5.68u w=2.5u l=0.5u
X3 VSS vbn_buf VSS VSS sg13_lv_nmos ad=1.52p pd=8.38u as=0.5193n ps=2.49026m w=8u l=10u
X4 VSS vbn_buf VSS VSS sg13_lv_nmos ad=1.52p pd=8.38u as=0 ps=0 w=8u l=10u
X5 VSS vbg_buf VSS VSS sg13_lv_nmos ad=1.52p pd=8.38u as=0 ps=0 w=8u l=10u
X6 VSS vbg_buf VSS VSS sg13_lv_nmos ad=1.52p pd=8.38u as=0 ps=0 w=8u l=10u
X7 a_5408_n8844# a_5408_n8844# VDD VDD sg13_lv_pmos ad=1.7p pd=10.68u as=1.7p ps=10.68u w=5u l=0.5u
X8 VDD VDD VDD VDD sg13_lv_pmos ad=1.7p pd=10.68u as=45.026p ps=0.22748m w=5u l=0.5u
X9 vbn_buf ibias_100u VSS rhigh l=32u w=0.5u
X10 VSS VSS VSS VSS sg13_lv_nmos ad=0.85p pd=5.68u as=0 ps=0 w=2.5u l=0.5u
X11 VDD VDD VDD VDD sg13_lv_pmos ad=1.7p pd=10.68u as=0 ps=0 w=5u l=0.5u
X12 VSS VSS VSS VSS sg13_lv_nmos ad=0.85p pd=5.68u as=0 ps=0 w=2.5u l=0.5u
X13 VSS vbn_buf VSS VSS sg13_lv_nmos ad=1.52p pd=8.38u as=0 ps=0 w=8u l=10u
X14 a_5408_n8844# ibias_100u VSS VSS sg13_lv_nmos ad=0.85p pd=5.68u as=0.85p ps=5.68u w=2.5u l=0.5u
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
X27 a_4788_n10564# a_4745_n10428# VDD VDD sg13_lv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.13u
X28 vbn_buf a_4745_n10428# VSS VSS sg13_lv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.13u
X29 a_4788_n10564# a_4745_n10428# VSS VSS sg13_lv_nmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=0.13u
X30 vbg_buf a_4400_n9272# VSS rhigh l=32u w=0.5u
X31 VSS vbn_buf VSS VSS sg13_lv_nmos ad=2.72p pd=16.68u as=0 ps=0 w=8u l=10u
X32 VSS vbg_buf VSS VSS sg13_lv_nmos ad=2.72p pd=16.68u as=0 ps=0 w=8u l=10u
X33 ibias_100u a_4745_n10428# VSS VSS sg13_lv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.13u
X34 VSS vbn_buf VSS VSS sg13_lv_nmos ad=1.52p pd=8.38u as=0 ps=0 w=8u l=10u
X35 VSS vbn_buf VSS VSS sg13_lv_nmos ad=1.52p pd=8.38u as=0 ps=0 w=8u l=10u
X36 a_4400_n9272# a_5408_n8844# VDD VDD sg13_lv_pmos ad=1.7p pd=10.68u as=1.7p ps=10.68u w=5u l=0.5u
X37 VSS vbn_buf VSS VSS sg13_lv_nmos ad=2.72p pd=16.68u as=0 ps=0 w=8u l=10u
X38 VSS vbg_buf VSS VSS sg13_lv_nmos ad=1.52p pd=8.38u as=0 ps=0 w=8u l=10u
X39 VSS vbg_buf VSS VSS sg13_lv_nmos ad=1.52p pd=8.38u as=0 ps=0 w=8u l=10u
X40 VDD VDD VDD VDD sg13_lv_pmos ad=0.34p pd=2.68u as=0 ps=0 w=1u l=0.13u
.ends

