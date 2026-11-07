module ringosc (
`ifdef USE_POWER_PINS
    inout VDD,
    inout VSS,
`endif
    inout vout
);
endmodule
