// SPDX-FileCopyrightText: 2026 Simon Dorrer and Harald Pretl
// SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
// Description: Top-level chip core.
// Instantiates and connects the digital and analog macros.

`default_nettype none

module chip_core #(
    parameter int unsigned NUM_INPUT_PADS,
    parameter int unsigned NUM_OUTPUT_PADS,
    parameter int unsigned NUM_BIDIR_PADS,
    parameter int unsigned NUM_ANALOG_PADS,
    parameter int unsigned NUM_RF_PADS
)(
    `ifdef USE_POWER_PINS
    inout  wire VDD,
    inout  wire VSS,
    inout  wire vdd_rf,     // VCO supply, from its own analog pad
    inout  wire vdd_ro,     // ring oscillator supply, from its own analog pad
    inout  wire vdd_hv,     // IHP HV counter supply (1.2 V to 1.65 V), from its own analog pad
    `endif

    input  logic clk,       // clock
    input  logic rst_n,     // reset (active low)

    input  logic [NUM_INPUT_PADS-1 :0] input_in,        // Input value
    output logic [NUM_OUTPUT_PADS-1:0] output_out,      // Output value
    input  logic [NUM_BIDIR_PADS-1 :0] bidir_in,        // Bidir input value
    output logic [NUM_BIDIR_PADS-1 :0] bidir_out,       // Bidir output value
    output logic [NUM_BIDIR_PADS-1 :0] bidir_oe,        // Bidir output enable

    inout  wire  [NUM_ANALOG_PADS-1:0] analog_padres,   // Analog (via pad secondary ESD protection)
    inout  wire  [NUM_ANALOG_PADS-1:0] analog_padbare,  // Analog (direct pad connection with primary ESD protection)
    inout  wire  [NUM_RF_PADS-1    :0] rf_padbare       // RF (direct connection to the RF pad)
);

    // ======================================================
    // Input Assignments
    // ======================================================
    logic [1:0] sel;    // counter select: 00 none, 01 IHP LV, 10 IHP HV, 11 ETH LV
    logic       di_en;  // VCO enable (active high)
    assign sel   = input_in[1:0];
    assign di_en = input_in[2];

    // Analog inputs, through the secondary ESD protection of their pads
    wire vtune   = analog_padres[0];
    wire amp_vin = analog_padres[1];
    wire inv_vin = analog_padres[3];

    `ifdef USE_POWER_PINS
    wire vss_tie = VSS;
    `else
    wire vss_tie = 1'b0;
    `endif
    // ======================================================

    // ======================================================
    // Counters (digital macros) behind the counter select
    // ======================================================
    // sel only changes with rst_n low or clk stopped, so the AND gates cannot cut a clock pulse short.
    // Only the selected counter gets a clock, which separates the supply current of each library.
    logic sel_lv_ihp, sel_hv_ihp, sel_lv_eth;
    assign sel_lv_ihp = (sel == 2'b01);
    assign sel_hv_ihp = (sel == 2'b10);
    assign sel_lv_eth = (sel == 2'b11);

    logic clk_lv_ihp, clk_hv_ihp, clk_lv_eth;
    assign clk_lv_ihp = clk & sel_lv_ihp;
    assign clk_hv_ihp = clk & sel_hv_ihp;
    assign clk_lv_eth = clk & sel_lv_eth;

    logic [7:0] count_lv_ihp, count_hv_ihp, count_lv_eth;

    // IHP LV standard cells
    counter_lv_ihp_top counter_lv_ihp (
        `ifdef USE_POWER_PINS
        .VDD(VDD),
        .VSS(VSS),
        `endif
        .clock_i        (clk_lv_ihp),
        .reset_n_i      (rst_n),
        .enable_i       (sel_lv_ihp),
        .counter_value_o(count_lv_ihp)
    );

    // IHP HV standard cells, on their own supply vdd_hv (1.2 V to 1.65 V)
    counter_hv_kvc_top counter_hv_kvc (
        `ifdef USE_POWER_PINS
        .VDD(vdd_hv),
        .VSS(VSS),
        `endif
        .clock_i        (clk_hv_ihp),
        .reset_n_i      (rst_n),
        .enable_i       (sel_hv_ihp),
        .counter_value_o(count_hv_ihp)
    );

    // ETH LV standard cells
    counter_lv_eth_top counter_lv_eth (
        `ifdef USE_POWER_PINS
        .VDD(VDD),
        .VSS(VSS),
        `endif
        .clock_i        (clk_lv_eth),
        .reset_n_i      (rst_n),
        .enable_i       (sel_lv_eth),
        .counter_value_o(count_lv_eth)
    );

    logic [7:0] count;
    always_comb begin
        case (sel)
            2'b01:   count = count_lv_ihp;
            2'b10:   count = count_hv_ihp;
            2'b11:   count = count_lv_eth;
            default: count = 8'h00;
        endcase
    end
    // ======================================================

    // ======================================================
    // Inverter (analog macro)
    // ======================================================
    // Channel 1 is analog, channel 4 is digital and inverts count[7] read back from its bidir pad.
    // The inputs of the unused channels 2 and 3 are tied low, so their outputs drive high and stay open.
    wire inv_din = bidir_in[0];  // vin* are inout ports on inverter_top -> must be wire
    wire inv_vout;
    wire inv_dout;

    inverter_top inverter (
        `ifdef USE_POWER_PINS
        .VDD  (VDD),
        .VSS  (VSS),
        `endif
        .vin1 (inv_vin),
        .vin2 (vss_tie),
        .vin3 (vss_tie),
        .vin4 (inv_din),
        .vout1(inv_vout),
        .vout2(),
        .vout3(),
        .vout4(inv_dout)
    );
    // ======================================================

    // ======================================================
    // Amplifier (analog macro)
    // ======================================================
    wire amp_vout;

    amplifier amplifier (
        `ifdef USE_POWER_PINS
        .VDD (VDD),
        .VSS (VSS),
        `endif
        .vin (amp_vin),
        .vout(amp_vout)
    );
    // ======================================================

    // ======================================================
    // Ring oscillator (analog macro), on its own supply vdd_ro
    // ======================================================
    wire ro_vout;

    ringosc ringosc (
        `ifdef USE_POWER_PINS
        .VDD (vdd_ro),
        .VSS (VSS),
        `endif
        .vout(ro_vout)
    );
    // ======================================================

    // ======================================================
    // VCO (RF macro), on its own supply vdd_rf
    // ======================================================
    wire rf_out_n;
    wire rf_out_p;

    vco_top vco (
        `ifdef USE_POWER_PINS
        .VDD     (vdd_rf),
        .VSS     (VSS),
        `endif
        .di_en   (di_en),
        .vtune   (vtune),
        .rf_out_n(rf_out_n),
        .rf_out_p(rf_out_p)
    );
    // ======================================================

    // ======================================================
    // Output Assignments
    // ======================================================
    // Digital outputs: count[6:0] of the selected counter and the digital inverter channel
    assign output_out[6:0] = count[6:0];
    assign output_out[7]   = inv_dout;

    // Digital bidirectional: count[7], always driven, read back into the digital inverter channel
    assign bidir_out[0] = count[7];
    assign bidir_oe[0]  = 1'b1;

    // Analog outputs
    assign analog_padbare[2] = amp_vout;
    assign analog_padbare[4] = inv_vout;
    assign analog_padbare[5] = ro_vout;

    // RF outputs
    assign rf_padbare[0] = rf_out_n;
    assign rf_padbare[1] = rf_out_p;
    // ======================================================
endmodule

`default_nettype wire
