module counter_hv_kvc_top (clock_i,
    enable_i,
    reset_n_i,
    VDD,
    VSS,
    counter_value_o);
 input clock_i;
 input enable_i;
 input reset_n_i;
 inout VDD;
 inout VSS;
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

 sg13g2_hv_fill_8 FILLER_0_107 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_0_115 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_0_123 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_0_131 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_0_139 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_0_14 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_0_147 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_0_155 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_2 FILLER_0_163 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_0_169 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_0_177 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_0_185 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_0_193 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_0_201 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_0_209 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_0_217 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_0_22 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_0_225 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_0_233 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_0_241 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_0_249 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_0_257 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_0_265 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_0_273 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_0_281 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_0_289 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_0_297 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_0_30 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_0_305 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_0_313 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_0_321 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_0_329 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_0_337 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_0_345 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_0_353 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_0_361 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_0_369 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_0_377 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_0_38 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_decap_8 FILLER_0_385 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_0_46 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_0_54 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_0_6 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_1 FILLER_0_62 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_0_67 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_0_75 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_0_83 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_0_91 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_0_99 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_1_0 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_1_106 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_1_114 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_1_122 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_decap_4 FILLER_1_130 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_2 FILLER_1_134 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_2 FILLER_1_154 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_1 FILLER_1_156 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_1_16 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_2 FILLER_1_200 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_1 FILLER_1_202 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_1_228 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_decap_4 FILLER_1_236 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_1_24 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_1 FILLER_1_240 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_1_288 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_1_296 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_1_304 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_1_312 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_2 FILLER_1_32 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_1_320 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_1_328 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_1_336 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_1_344 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_1_352 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_1_360 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_1_368 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_1_376 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_1_384 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_1_8 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_1_98 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_2_0 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_2_101 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_2_109 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_2_117 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_2_125 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_2_133 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_decap_4 FILLER_2_141 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_2 FILLER_2_145 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_2_154 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_2_162 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_2_170 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_2_178 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_2_186 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_2_194 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_2 FILLER_2_202 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_2_21 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_2 FILLER_2_210 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_1 FILLER_2_212 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_2_220 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_decap_4 FILLER_2_228 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_2_250 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_2_258 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_2_266 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_2 FILLER_2_274 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_2_29 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_2_319 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_2_327 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_2_335 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_2_343 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_2_351 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_2_359 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_2_367 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_2_37 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_2_375 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_2_383 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_1 FILLER_2_391 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_2_45 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_2_53 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_2_61 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_2_69 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_2_77 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_decap_8 FILLER_2_8 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_2_85 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_2_93 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_3_132 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_3_140 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_2 FILLER_3_148 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_1 FILLER_3_150 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_decap_4 FILLER_3_161 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_1 FILLER_3_165 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_3_206 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_3_214 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_3_222 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_2 FILLER_3_230 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_decap_4 FILLER_3_279 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_1 FILLER_3_283 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_3_288 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_3_29 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_3_296 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_3_304 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_3_312 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_3_320 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_3_328 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_3_336 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_3_344 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_3_352 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_3_360 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_3_368 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_3_37 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_3_376 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_3_384 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_3_45 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_3_53 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_1 FILLER_3_65 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_decap_4 FILLER_3_73 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_3_84 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_4_0 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_1 FILLER_4_12 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_2 FILLER_4_143 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_1 FILLER_4_145 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_decap_4 FILLER_4_160 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_4_207 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_2 FILLER_4_215 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_2 FILLER_4_226 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_4_253 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_4_261 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_2 FILLER_4_269 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_1 FILLER_4_271 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_4_315 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_4_323 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_4_331 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_4_339 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_4_347 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_4_355 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_4_363 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_4_371 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_4_379 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_decap_4 FILLER_4_387 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_1 FILLER_4_391 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_decap_4 FILLER_4_56 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_2 FILLER_4_60 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_decap_4 FILLER_4_8 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_2 FILLER_4_87 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_5_0 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_5_103 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_decap_4 FILLER_5_111 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_2 FILLER_5_115 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_1 FILLER_5_12 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_5_123 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_5_131 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_5_139 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_5_147 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_5_155 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_decap_4 FILLER_5_163 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_2 FILLER_5_167 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_5_179 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_5_187 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_2 FILLER_5_19 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_5_195 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_5_203 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_1 FILLER_5_21 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_5_211 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_2 FILLER_5_219 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_5_227 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_5_235 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_5_243 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_5_251 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_5_259 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_5_26 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_decap_4 FILLER_5_267 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_2 FILLER_5_271 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_1 FILLER_5_279 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_5_284 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_5_292 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_5_300 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_5_308 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_5_316 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_1 FILLER_5_324 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_5_331 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_5_339 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_5_34 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_5_347 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_5_355 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_5_363 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_decap_4 FILLER_5_371 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_2 FILLER_5_375 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_5_383 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_1 FILLER_5_391 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_5_42 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_5_50 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_decap_8 FILLER_5_58 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_5_71 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_5_79 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_decap_4 FILLER_5_8 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_5_87 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_fill_8 FILLER_5_95 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_nand3_1 _39_ (.B(net4),
    .C(net1),
    .A(net3),
    .Y(_08_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_xnor2_1 _40_ (.Y(_09_),
    .A(net5),
    .B(_08_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_or3_1 _41_ (.A(net9),
    .B(_13_),
    .C(_14_),
    .X(_16_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_inv_1 _42_ (.VDD(VDD),
    .Y(_17_),
    .A(net2),
    .VSS(VSS));
 sg13g2_hv_a21oi_1 _43_ (.VSS(VSS),
    .VDD(VDD),
    .A1(_15_),
    .A2(_16_),
    .Y(_05_),
    .B1(_17_));
 sg13g2_hv_nand2b_1 _44_ (.Y(_18_),
    .B(net3),
    .A_N(net1),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_nand2b_1 _45_ (.Y(_19_),
    .B(net1),
    .A_N(net3),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_a21oi_1 _46_ (.VSS(VSS),
    .VDD(VDD),
    .A1(_18_),
    .A2(_19_),
    .Y(_04_),
    .B1(_17_));
 sg13g2_hv_nand2_1 _47_ (.Y(_20_),
    .A(net6),
    .B(_13_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_inv_1 _48_ (.VDD(VDD),
    .Y(_21_),
    .A(net6),
    .VSS(VSS));
 sg13g2_hv_nand2b_1 _49_ (.Y(_22_),
    .B(_21_),
    .A_N(_13_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_a21oi_1 _50_ (.VSS(VSS),
    .VDD(VDD),
    .A1(_20_),
    .A2(_22_),
    .Y(_03_),
    .B1(_17_));
 sg13g2_hv_and2_1 _51_ (.A(net2),
    .B(_09_),
    .X(_07_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_nand4_1 _52_ (.B(net7),
    .C(net8),
    .A(net6),
    .Y(_23_),
    .VDD(VDD),
    .VSS(VSS),
    .D(net9));
 sg13g2_hv_o21ai_1 _53_ (.B1(net10),
    .VDD(VDD),
    .Y(_24_),
    .VSS(VSS),
    .A1(_13_),
    .A2(_23_));
 sg13g2_hv_or3_1 _54_ (.A(net10),
    .B(_13_),
    .C(_23_),
    .X(_25_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_a21oi_1 _55_ (.VSS(VSS),
    .VDD(VDD),
    .A1(_24_),
    .A2(_25_),
    .Y(_02_),
    .B1(_17_));
 sg13g2_hv_o21ai_1 _56_ (.B1(net7),
    .VDD(VDD),
    .Y(_26_),
    .VSS(VSS),
    .A1(_21_),
    .A2(_13_));
 sg13g2_hv_or3_1 _57_ (.A(_21_),
    .B(net7),
    .C(_13_),
    .X(_27_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_a21oi_1 _58_ (.VSS(VSS),
    .VDD(VDD),
    .A1(_26_),
    .A2(_27_),
    .Y(_01_),
    .B1(_17_));
 sg13g2_hv_nand2_1 _59_ (.Y(_28_),
    .A(net6),
    .B(net7),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_o21ai_1 _60_ (.B1(net8),
    .VDD(VDD),
    .Y(_29_),
    .VSS(VSS),
    .A1(_13_),
    .A2(_28_));
 sg13g2_hv_or3_1 _61_ (.A(net8),
    .B(_13_),
    .C(_28_),
    .X(_30_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_nand2_1 _62_ (.Y(_10_),
    .A(net3),
    .B(net1),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_a21oi_1 _63_ (.VSS(VSS),
    .VDD(VDD),
    .A1(_29_),
    .A2(_30_),
    .Y(_00_),
    .B1(_17_));
 sg13g2_hv_xnor2_1 _64_ (.Y(_11_),
    .A(net4),
    .B(_10_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_and2_1 _65_ (.A(net2),
    .B(_11_),
    .X(_06_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_nand4_1 _66_ (.B(net4),
    .C(net5),
    .A(net3),
    .Y(_12_),
    .VDD(VDD),
    .VSS(VSS),
    .D(net1));
 sg13g2_hv_buf_2 _67_ (.A(_12_),
    .X(_13_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_nand3_1 _68_ (.B(net7),
    .C(net8),
    .A(net6),
    .Y(_14_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_o21ai_1 _69_ (.B1(net9),
    .VDD(VDD),
    .Y(_15_),
    .VSS(VSS),
    .A1(_13_),
    .A2(_14_));
 sg13g2_hv_dfrbpq_1 _70_ (.RESET_B(net16),
    .VSS(VSS),
    .VDD(VDD),
    .D(_04_),
    .Q(net3),
    .CLK(clknet_1_0__leaf_clock_i));
 sg13g2_hv_tiehi _70__17 (.VDD(VDD),
    .VSS(VSS),
    .L_HI(net16));
 sg13g2_hv_dfrbpq_1 _71_ (.RESET_B(net13),
    .VSS(VSS),
    .VDD(VDD),
    .D(_06_),
    .Q(net4),
    .CLK(clknet_1_0__leaf_clock_i));
 sg13g2_hv_tiehi _71__14 (.VDD(VDD),
    .VSS(VSS),
    .L_HI(net13));
 sg13g2_hv_dfrbpq_1 _72_ (.RESET_B(net15),
    .VSS(VSS),
    .VDD(VDD),
    .D(_07_),
    .Q(net5),
    .CLK(clknet_1_0__leaf_clock_i));
 sg13g2_hv_tiehi _72__16 (.VDD(VDD),
    .VSS(VSS),
    .L_HI(net15));
 sg13g2_hv_dfrbpq_1 _73_ (.RESET_B(net12),
    .VSS(VSS),
    .VDD(VDD),
    .D(_03_),
    .Q(net6),
    .CLK(clknet_1_1__leaf_clock_i));
 sg13g2_hv_tiehi _73__13 (.VDD(VDD),
    .VSS(VSS),
    .L_HI(net12));
 sg13g2_hv_dfrbpq_1 _74_ (.RESET_B(net),
    .VSS(VSS),
    .VDD(VDD),
    .D(_01_),
    .Q(net7),
    .CLK(clknet_1_0__leaf_clock_i));
 sg13g2_hv_tiehi _74__11 (.VDD(VDD),
    .VSS(VSS),
    .L_HI(net));
 sg13g2_hv_dfrbpq_1 _75_ (.RESET_B(net17),
    .VSS(VSS),
    .VDD(VDD),
    .D(_00_),
    .Q(net8),
    .CLK(clknet_1_1__leaf_clock_i));
 sg13g2_hv_tiehi _75__18 (.VDD(VDD),
    .VSS(VSS),
    .L_HI(net17));
 sg13g2_hv_dfrbpq_1 _76_ (.RESET_B(net11),
    .VSS(VSS),
    .VDD(VDD),
    .D(_05_),
    .Q(net9),
    .CLK(clknet_1_1__leaf_clock_i));
 sg13g2_hv_tiehi _76__12 (.VDD(VDD),
    .VSS(VSS),
    .L_HI(net11));
 sg13g2_hv_dfrbpq_1 _77_ (.RESET_B(net14),
    .VSS(VSS),
    .VDD(VDD),
    .D(_02_),
    .Q(net10),
    .CLK(clknet_1_1__leaf_clock_i));
 sg13g2_hv_tiehi _77__15 (.VDD(VDD),
    .VSS(VSS),
    .L_HI(net14));
 sg13g2_hv_buf_16 clkbuf_0_clock_i (.X(clknet_0_clock_i),
    .A(clock_i),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_buf_16 clkbuf_1_0__f_clock_i (.X(clknet_1_0__leaf_clock_i),
    .A(clknet_0_clock_i),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_buf_16 clkbuf_1_1__f_clock_i (.X(clknet_1_1__leaf_clock_i),
    .A(clknet_0_clock_i),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_buf_1 input1 (.A(enable_i),
    .X(net1),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_buf_1 input2 (.A(reset_n_i),
    .X(net2),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_buf_1 output10 (.A(net10),
    .X(counter_value_o[7]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_buf_1 output3 (.A(net3),
    .X(counter_value_o[0]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_buf_1 output4 (.A(net4),
    .X(counter_value_o[1]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_buf_1 output5 (.A(net5),
    .X(counter_value_o[2]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_buf_1 output6 (.A(net6),
    .X(counter_value_o[3]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_buf_1 output7 (.A(net7),
    .X(counter_value_o[4]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_buf_1 output8 (.A(net8),
    .X(counter_value_o[5]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_hv_buf_1 output9 (.A(net9),
    .X(counter_value_o[6]),
    .VDD(VDD),
    .VSS(VSS));
endmodule
