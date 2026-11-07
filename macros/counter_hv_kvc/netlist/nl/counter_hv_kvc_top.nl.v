module counter_hv_kvc_top (clock_i,
    enable_i,
    reset_n_i,
    counter_value_o);
 input clock_i;
 input enable_i;
 input reset_n_i;
 output [7:0] counter_value_o;

 wire _00_;
 wire _01_;
 wire _02_;
 wire _03_;
 wire _04_;
 wire _05_;
 wire _06_;
 wire _07_;
 wire _08_;
 wire _09_;
 wire _10_;
 wire _11_;
 wire _12_;
 wire _13_;
 wire _14_;
 wire _15_;
 wire _16_;
 wire _17_;
 wire _18_;
 wire _19_;
 wire _20_;
 wire _21_;
 wire _22_;
 wire _23_;
 wire _24_;
 wire _25_;
 wire _26_;
 wire _27_;
 wire _28_;
 wire _29_;
 wire _30_;
 wire net11;
 wire net12;
 wire net13;
 wire net14;
 wire net15;
 wire net16;
 wire net17;
 wire clknet_0_clock_i;
 wire net3;
 wire net4;
 wire net5;
 wire net6;
 wire net7;
 wire net8;
 wire net9;
 wire net10;
 wire net1;
 wire net2;
 wire net;
 wire clknet_1_0__leaf_clock_i;
 wire clknet_1_1__leaf_clock_i;

 sg13g2_hv_fill_8 FILLER_0_107 ();
 sg13g2_hv_fill_8 FILLER_0_115 ();
 sg13g2_hv_fill_8 FILLER_0_123 ();
 sg13g2_hv_fill_8 FILLER_0_131 ();
 sg13g2_hv_fill_8 FILLER_0_139 ();
 sg13g2_hv_fill_8 FILLER_0_14 ();
 sg13g2_hv_fill_8 FILLER_0_147 ();
 sg13g2_hv_fill_8 FILLER_0_155 ();
 sg13g2_hv_fill_2 FILLER_0_163 ();
 sg13g2_hv_fill_8 FILLER_0_169 ();
 sg13g2_hv_fill_8 FILLER_0_177 ();
 sg13g2_hv_fill_8 FILLER_0_185 ();
 sg13g2_hv_fill_8 FILLER_0_193 ();
 sg13g2_hv_fill_8 FILLER_0_201 ();
 sg13g2_hv_fill_8 FILLER_0_209 ();
 sg13g2_hv_fill_8 FILLER_0_217 ();
 sg13g2_hv_fill_8 FILLER_0_22 ();
 sg13g2_hv_fill_8 FILLER_0_225 ();
 sg13g2_hv_fill_8 FILLER_0_233 ();
 sg13g2_hv_fill_8 FILLER_0_241 ();
 sg13g2_hv_fill_8 FILLER_0_249 ();
 sg13g2_hv_fill_8 FILLER_0_257 ();
 sg13g2_hv_fill_8 FILLER_0_265 ();
 sg13g2_hv_fill_8 FILLER_0_273 ();
 sg13g2_hv_fill_8 FILLER_0_281 ();
 sg13g2_hv_fill_8 FILLER_0_289 ();
 sg13g2_hv_fill_8 FILLER_0_297 ();
 sg13g2_hv_fill_8 FILLER_0_30 ();
 sg13g2_hv_fill_8 FILLER_0_305 ();
 sg13g2_hv_fill_8 FILLER_0_313 ();
 sg13g2_hv_fill_8 FILLER_0_321 ();
 sg13g2_hv_fill_8 FILLER_0_329 ();
 sg13g2_hv_fill_8 FILLER_0_337 ();
 sg13g2_hv_fill_8 FILLER_0_345 ();
 sg13g2_hv_fill_8 FILLER_0_353 ();
 sg13g2_hv_fill_8 FILLER_0_361 ();
 sg13g2_hv_fill_8 FILLER_0_369 ();
 sg13g2_hv_fill_8 FILLER_0_377 ();
 sg13g2_hv_fill_8 FILLER_0_38 ();
 sg13g2_hv_decap_8 FILLER_0_385 ();
 sg13g2_hv_fill_8 FILLER_0_46 ();
 sg13g2_hv_fill_8 FILLER_0_54 ();
 sg13g2_hv_fill_8 FILLER_0_6 ();
 sg13g2_hv_fill_1 FILLER_0_62 ();
 sg13g2_hv_fill_8 FILLER_0_67 ();
 sg13g2_hv_fill_8 FILLER_0_75 ();
 sg13g2_hv_fill_8 FILLER_0_83 ();
 sg13g2_hv_fill_8 FILLER_0_91 ();
 sg13g2_hv_fill_8 FILLER_0_99 ();
 sg13g2_hv_fill_8 FILLER_1_0 ();
 sg13g2_hv_fill_8 FILLER_1_106 ();
 sg13g2_hv_fill_8 FILLER_1_114 ();
 sg13g2_hv_fill_8 FILLER_1_122 ();
 sg13g2_hv_decap_4 FILLER_1_130 ();
 sg13g2_hv_fill_2 FILLER_1_134 ();
 sg13g2_hv_fill_2 FILLER_1_154 ();
 sg13g2_hv_fill_1 FILLER_1_156 ();
 sg13g2_hv_fill_8 FILLER_1_16 ();
 sg13g2_hv_fill_2 FILLER_1_200 ();
 sg13g2_hv_fill_1 FILLER_1_202 ();
 sg13g2_hv_fill_8 FILLER_1_228 ();
 sg13g2_hv_decap_4 FILLER_1_236 ();
 sg13g2_hv_fill_8 FILLER_1_24 ();
 sg13g2_hv_fill_1 FILLER_1_240 ();
 sg13g2_hv_fill_8 FILLER_1_288 ();
 sg13g2_hv_fill_8 FILLER_1_296 ();
 sg13g2_hv_fill_8 FILLER_1_304 ();
 sg13g2_hv_fill_8 FILLER_1_312 ();
 sg13g2_hv_fill_2 FILLER_1_32 ();
 sg13g2_hv_fill_8 FILLER_1_320 ();
 sg13g2_hv_fill_8 FILLER_1_328 ();
 sg13g2_hv_fill_8 FILLER_1_336 ();
 sg13g2_hv_fill_8 FILLER_1_344 ();
 sg13g2_hv_fill_8 FILLER_1_352 ();
 sg13g2_hv_fill_8 FILLER_1_360 ();
 sg13g2_hv_fill_8 FILLER_1_368 ();
 sg13g2_hv_fill_8 FILLER_1_376 ();
 sg13g2_hv_fill_8 FILLER_1_384 ();
 sg13g2_hv_fill_8 FILLER_1_8 ();
 sg13g2_hv_fill_8 FILLER_1_98 ();
 sg13g2_hv_fill_8 FILLER_2_0 ();
 sg13g2_hv_fill_8 FILLER_2_101 ();
 sg13g2_hv_fill_8 FILLER_2_109 ();
 sg13g2_hv_fill_8 FILLER_2_117 ();
 sg13g2_hv_fill_8 FILLER_2_125 ();
 sg13g2_hv_fill_8 FILLER_2_133 ();
 sg13g2_hv_decap_4 FILLER_2_141 ();
 sg13g2_hv_fill_2 FILLER_2_145 ();
 sg13g2_hv_fill_8 FILLER_2_154 ();
 sg13g2_hv_fill_8 FILLER_2_162 ();
 sg13g2_hv_fill_8 FILLER_2_170 ();
 sg13g2_hv_fill_8 FILLER_2_178 ();
 sg13g2_hv_fill_8 FILLER_2_186 ();
 sg13g2_hv_fill_8 FILLER_2_194 ();
 sg13g2_hv_fill_2 FILLER_2_202 ();
 sg13g2_hv_fill_8 FILLER_2_21 ();
 sg13g2_hv_fill_2 FILLER_2_210 ();
 sg13g2_hv_fill_1 FILLER_2_212 ();
 sg13g2_hv_fill_8 FILLER_2_220 ();
 sg13g2_hv_decap_4 FILLER_2_228 ();
 sg13g2_hv_fill_8 FILLER_2_250 ();
 sg13g2_hv_fill_8 FILLER_2_258 ();
 sg13g2_hv_fill_8 FILLER_2_266 ();
 sg13g2_hv_fill_2 FILLER_2_274 ();
 sg13g2_hv_fill_8 FILLER_2_29 ();
 sg13g2_hv_fill_8 FILLER_2_319 ();
 sg13g2_hv_fill_8 FILLER_2_327 ();
 sg13g2_hv_fill_8 FILLER_2_335 ();
 sg13g2_hv_fill_8 FILLER_2_343 ();
 sg13g2_hv_fill_8 FILLER_2_351 ();
 sg13g2_hv_fill_8 FILLER_2_359 ();
 sg13g2_hv_fill_8 FILLER_2_367 ();
 sg13g2_hv_fill_8 FILLER_2_37 ();
 sg13g2_hv_fill_8 FILLER_2_375 ();
 sg13g2_hv_fill_8 FILLER_2_383 ();
 sg13g2_hv_fill_1 FILLER_2_391 ();
 sg13g2_hv_fill_8 FILLER_2_45 ();
 sg13g2_hv_fill_8 FILLER_2_53 ();
 sg13g2_hv_fill_8 FILLER_2_61 ();
 sg13g2_hv_fill_8 FILLER_2_69 ();
 sg13g2_hv_fill_8 FILLER_2_77 ();
 sg13g2_hv_decap_8 FILLER_2_8 ();
 sg13g2_hv_fill_8 FILLER_2_85 ();
 sg13g2_hv_fill_8 FILLER_2_93 ();
 sg13g2_hv_fill_8 FILLER_3_132 ();
 sg13g2_hv_fill_8 FILLER_3_140 ();
 sg13g2_hv_fill_2 FILLER_3_148 ();
 sg13g2_hv_fill_1 FILLER_3_150 ();
 sg13g2_hv_decap_4 FILLER_3_161 ();
 sg13g2_hv_fill_1 FILLER_3_165 ();
 sg13g2_hv_fill_8 FILLER_3_206 ();
 sg13g2_hv_fill_8 FILLER_3_214 ();
 sg13g2_hv_fill_8 FILLER_3_222 ();
 sg13g2_hv_fill_2 FILLER_3_230 ();
 sg13g2_hv_decap_4 FILLER_3_279 ();
 sg13g2_hv_fill_1 FILLER_3_283 ();
 sg13g2_hv_fill_8 FILLER_3_288 ();
 sg13g2_hv_fill_8 FILLER_3_29 ();
 sg13g2_hv_fill_8 FILLER_3_296 ();
 sg13g2_hv_fill_8 FILLER_3_304 ();
 sg13g2_hv_fill_8 FILLER_3_312 ();
 sg13g2_hv_fill_8 FILLER_3_320 ();
 sg13g2_hv_fill_8 FILLER_3_328 ();
 sg13g2_hv_fill_8 FILLER_3_336 ();
 sg13g2_hv_fill_8 FILLER_3_344 ();
 sg13g2_hv_fill_8 FILLER_3_352 ();
 sg13g2_hv_fill_8 FILLER_3_360 ();
 sg13g2_hv_fill_8 FILLER_3_368 ();
 sg13g2_hv_fill_8 FILLER_3_37 ();
 sg13g2_hv_fill_8 FILLER_3_376 ();
 sg13g2_hv_fill_8 FILLER_3_384 ();
 sg13g2_hv_fill_8 FILLER_3_45 ();
 sg13g2_hv_fill_8 FILLER_3_53 ();
 sg13g2_hv_fill_1 FILLER_3_65 ();
 sg13g2_hv_decap_4 FILLER_3_73 ();
 sg13g2_hv_fill_8 FILLER_3_84 ();
 sg13g2_hv_fill_8 FILLER_4_0 ();
 sg13g2_hv_fill_1 FILLER_4_12 ();
 sg13g2_hv_fill_2 FILLER_4_143 ();
 sg13g2_hv_fill_1 FILLER_4_145 ();
 sg13g2_hv_decap_4 FILLER_4_160 ();
 sg13g2_hv_fill_8 FILLER_4_207 ();
 sg13g2_hv_fill_2 FILLER_4_215 ();
 sg13g2_hv_fill_2 FILLER_4_226 ();
 sg13g2_hv_fill_8 FILLER_4_253 ();
 sg13g2_hv_fill_8 FILLER_4_261 ();
 sg13g2_hv_fill_2 FILLER_4_269 ();
 sg13g2_hv_fill_1 FILLER_4_271 ();
 sg13g2_hv_fill_8 FILLER_4_315 ();
 sg13g2_hv_fill_8 FILLER_4_323 ();
 sg13g2_hv_fill_8 FILLER_4_331 ();
 sg13g2_hv_fill_8 FILLER_4_339 ();
 sg13g2_hv_fill_8 FILLER_4_347 ();
 sg13g2_hv_fill_8 FILLER_4_355 ();
 sg13g2_hv_fill_8 FILLER_4_363 ();
 sg13g2_hv_fill_8 FILLER_4_371 ();
 sg13g2_hv_fill_8 FILLER_4_379 ();
 sg13g2_hv_decap_4 FILLER_4_387 ();
 sg13g2_hv_fill_1 FILLER_4_391 ();
 sg13g2_hv_decap_4 FILLER_4_56 ();
 sg13g2_hv_fill_2 FILLER_4_60 ();
 sg13g2_hv_decap_4 FILLER_4_8 ();
 sg13g2_hv_fill_2 FILLER_4_87 ();
 sg13g2_hv_fill_8 FILLER_5_0 ();
 sg13g2_hv_fill_8 FILLER_5_103 ();
 sg13g2_hv_decap_4 FILLER_5_111 ();
 sg13g2_hv_fill_2 FILLER_5_115 ();
 sg13g2_hv_fill_1 FILLER_5_12 ();
 sg13g2_hv_fill_8 FILLER_5_123 ();
 sg13g2_hv_fill_8 FILLER_5_131 ();
 sg13g2_hv_fill_8 FILLER_5_139 ();
 sg13g2_hv_fill_8 FILLER_5_147 ();
 sg13g2_hv_fill_8 FILLER_5_155 ();
 sg13g2_hv_decap_4 FILLER_5_163 ();
 sg13g2_hv_fill_2 FILLER_5_167 ();
 sg13g2_hv_fill_8 FILLER_5_179 ();
 sg13g2_hv_fill_8 FILLER_5_187 ();
 sg13g2_hv_fill_2 FILLER_5_19 ();
 sg13g2_hv_fill_8 FILLER_5_195 ();
 sg13g2_hv_fill_8 FILLER_5_203 ();
 sg13g2_hv_fill_1 FILLER_5_21 ();
 sg13g2_hv_fill_8 FILLER_5_211 ();
 sg13g2_hv_fill_2 FILLER_5_219 ();
 sg13g2_hv_fill_8 FILLER_5_227 ();
 sg13g2_hv_fill_8 FILLER_5_235 ();
 sg13g2_hv_fill_8 FILLER_5_243 ();
 sg13g2_hv_fill_8 FILLER_5_251 ();
 sg13g2_hv_fill_8 FILLER_5_259 ();
 sg13g2_hv_fill_8 FILLER_5_26 ();
 sg13g2_hv_decap_4 FILLER_5_267 ();
 sg13g2_hv_fill_2 FILLER_5_271 ();
 sg13g2_hv_fill_1 FILLER_5_279 ();
 sg13g2_hv_fill_8 FILLER_5_284 ();
 sg13g2_hv_fill_8 FILLER_5_292 ();
 sg13g2_hv_fill_8 FILLER_5_300 ();
 sg13g2_hv_fill_8 FILLER_5_308 ();
 sg13g2_hv_fill_8 FILLER_5_316 ();
 sg13g2_hv_fill_1 FILLER_5_324 ();
 sg13g2_hv_fill_8 FILLER_5_331 ();
 sg13g2_hv_fill_8 FILLER_5_339 ();
 sg13g2_hv_fill_8 FILLER_5_34 ();
 sg13g2_hv_fill_8 FILLER_5_347 ();
 sg13g2_hv_fill_8 FILLER_5_355 ();
 sg13g2_hv_fill_8 FILLER_5_363 ();
 sg13g2_hv_decap_4 FILLER_5_371 ();
 sg13g2_hv_fill_2 FILLER_5_375 ();
 sg13g2_hv_fill_8 FILLER_5_383 ();
 sg13g2_hv_fill_1 FILLER_5_391 ();
 sg13g2_hv_fill_8 FILLER_5_42 ();
 sg13g2_hv_fill_8 FILLER_5_50 ();
 sg13g2_hv_decap_8 FILLER_5_58 ();
 sg13g2_hv_fill_8 FILLER_5_71 ();
 sg13g2_hv_fill_8 FILLER_5_79 ();
 sg13g2_hv_decap_4 FILLER_5_8 ();
 sg13g2_hv_fill_8 FILLER_5_87 ();
 sg13g2_hv_fill_8 FILLER_5_95 ();
 sg13g2_hv_nand3_1 _39_ (.B(net4),
    .C(net1),
    .A(net3),
    .Y(_08_));
 sg13g2_hv_xnor2_1 _40_ (.Y(_09_),
    .A(net5),
    .B(_08_));
 sg13g2_hv_or3_1 _41_ (.A(net9),
    .B(_13_),
    .C(_14_),
    .X(_16_));
 sg13g2_hv_inv_1 _42_ (.Y(_17_),
    .A(net2));
 sg13g2_hv_a21oi_1 _43_ (.A1(_15_),
    .A2(_16_),
    .Y(_05_),
    .B1(_17_));
 sg13g2_hv_nand2b_1 _44_ (.Y(_18_),
    .B(net3),
    .A_N(net1));
 sg13g2_hv_nand2b_1 _45_ (.Y(_19_),
    .B(net1),
    .A_N(net3));
 sg13g2_hv_a21oi_1 _46_ (.A1(_18_),
    .A2(_19_),
    .Y(_04_),
    .B1(_17_));
 sg13g2_hv_nand2_1 _47_ (.Y(_20_),
    .A(net6),
    .B(_13_));
 sg13g2_hv_inv_1 _48_ (.Y(_21_),
    .A(net6));
 sg13g2_hv_nand2b_1 _49_ (.Y(_22_),
    .B(_21_),
    .A_N(_13_));
 sg13g2_hv_a21oi_1 _50_ (.A1(_20_),
    .A2(_22_),
    .Y(_03_),
    .B1(_17_));
 sg13g2_hv_and2_1 _51_ (.A(net2),
    .B(_09_),
    .X(_07_));
 sg13g2_hv_nand4_1 _52_ (.B(net7),
    .C(net8),
    .A(net6),
    .Y(_23_),
    .D(net9));
 sg13g2_hv_o21ai_1 _53_ (.B1(net10),
    .Y(_24_),
    .A1(_13_),
    .A2(_23_));
 sg13g2_hv_or3_1 _54_ (.A(net10),
    .B(_13_),
    .C(_23_),
    .X(_25_));
 sg13g2_hv_a21oi_1 _55_ (.A1(_24_),
    .A2(_25_),
    .Y(_02_),
    .B1(_17_));
 sg13g2_hv_o21ai_1 _56_ (.B1(net7),
    .Y(_26_),
    .A1(_21_),
    .A2(_13_));
 sg13g2_hv_or3_1 _57_ (.A(_21_),
    .B(net7),
    .C(_13_),
    .X(_27_));
 sg13g2_hv_a21oi_1 _58_ (.A1(_26_),
    .A2(_27_),
    .Y(_01_),
    .B1(_17_));
 sg13g2_hv_nand2_1 _59_ (.Y(_28_),
    .A(net6),
    .B(net7));
 sg13g2_hv_o21ai_1 _60_ (.B1(net8),
    .Y(_29_),
    .A1(_13_),
    .A2(_28_));
 sg13g2_hv_or3_1 _61_ (.A(net8),
    .B(_13_),
    .C(_28_),
    .X(_30_));
 sg13g2_hv_nand2_1 _62_ (.Y(_10_),
    .A(net3),
    .B(net1));
 sg13g2_hv_a21oi_1 _63_ (.A1(_29_),
    .A2(_30_),
    .Y(_00_),
    .B1(_17_));
 sg13g2_hv_xnor2_1 _64_ (.Y(_11_),
    .A(net4),
    .B(_10_));
 sg13g2_hv_and2_1 _65_ (.A(net2),
    .B(_11_),
    .X(_06_));
 sg13g2_hv_nand4_1 _66_ (.B(net4),
    .C(net5),
    .A(net3),
    .Y(_12_),
    .D(net1));
 sg13g2_hv_buf_2 _67_ (.A(_12_),
    .X(_13_));
 sg13g2_hv_nand3_1 _68_ (.B(net7),
    .C(net8),
    .A(net6),
    .Y(_14_));
 sg13g2_hv_o21ai_1 _69_ (.B1(net9),
    .Y(_15_),
    .A1(_13_),
    .A2(_14_));
 sg13g2_hv_dfrbpq_1 _70_ (.RESET_B(net16),
    .D(_04_),
    .Q(net3),
    .CLK(clknet_1_0__leaf_clock_i));
 sg13g2_hv_tiehi _70__17 (.L_HI(net16));
 sg13g2_hv_dfrbpq_1 _71_ (.RESET_B(net13),
    .D(_06_),
    .Q(net4),
    .CLK(clknet_1_0__leaf_clock_i));
 sg13g2_hv_tiehi _71__14 (.L_HI(net13));
 sg13g2_hv_dfrbpq_1 _72_ (.RESET_B(net15),
    .D(_07_),
    .Q(net5),
    .CLK(clknet_1_0__leaf_clock_i));
 sg13g2_hv_tiehi _72__16 (.L_HI(net15));
 sg13g2_hv_dfrbpq_1 _73_ (.RESET_B(net12),
    .D(_03_),
    .Q(net6),
    .CLK(clknet_1_1__leaf_clock_i));
 sg13g2_hv_tiehi _73__13 (.L_HI(net12));
 sg13g2_hv_dfrbpq_1 _74_ (.RESET_B(net),
    .D(_01_),
    .Q(net7),
    .CLK(clknet_1_0__leaf_clock_i));
 sg13g2_hv_tiehi _74__11 (.L_HI(net));
 sg13g2_hv_dfrbpq_1 _75_ (.RESET_B(net17),
    .D(_00_),
    .Q(net8),
    .CLK(clknet_1_1__leaf_clock_i));
 sg13g2_hv_tiehi _75__18 (.L_HI(net17));
 sg13g2_hv_dfrbpq_1 _76_ (.RESET_B(net11),
    .D(_05_),
    .Q(net9),
    .CLK(clknet_1_1__leaf_clock_i));
 sg13g2_hv_tiehi _76__12 (.L_HI(net11));
 sg13g2_hv_dfrbpq_1 _77_ (.RESET_B(net14),
    .D(_02_),
    .Q(net10),
    .CLK(clknet_1_1__leaf_clock_i));
 sg13g2_hv_tiehi _77__15 (.L_HI(net14));
 sg13g2_hv_buf_16 clkbuf_0_clock_i (.X(clknet_0_clock_i),
    .A(clock_i));
 sg13g2_hv_buf_16 clkbuf_1_0__f_clock_i (.X(clknet_1_0__leaf_clock_i),
    .A(clknet_0_clock_i));
 sg13g2_hv_buf_16 clkbuf_1_1__f_clock_i (.X(clknet_1_1__leaf_clock_i),
    .A(clknet_0_clock_i));
 sg13g2_hv_buf_1 input1 (.A(enable_i),
    .X(net1));
 sg13g2_hv_buf_1 input2 (.A(reset_n_i),
    .X(net2));
 sg13g2_hv_buf_1 output10 (.A(net10),
    .X(counter_value_o[7]));
 sg13g2_hv_buf_1 output3 (.A(net3),
    .X(counter_value_o[0]));
 sg13g2_hv_buf_1 output4 (.A(net4),
    .X(counter_value_o[1]));
 sg13g2_hv_buf_1 output5 (.A(net5),
    .X(counter_value_o[2]));
 sg13g2_hv_buf_1 output6 (.A(net6),
    .X(counter_value_o[3]));
 sg13g2_hv_buf_1 output7 (.A(net7),
    .X(counter_value_o[4]));
 sg13g2_hv_buf_1 output8 (.A(net8),
    .X(counter_value_o[5]));
 sg13g2_hv_buf_1 output9 (.A(net9),
    .X(counter_value_o[6]));
endmodule
