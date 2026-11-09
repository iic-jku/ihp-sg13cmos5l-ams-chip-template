# SPDX-FileCopyrightText: 2020-2022 Efabless Corporation, 2025 LibreLane Contributors
# SPDX-License-Identifier: Apache-2.0
#
# Copyright 2025 LibreLane Contributors
#
# Adapted from OpenLane
#
# Copyright 2020-2022 Efabless Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

source $::env(SCRIPTS_DIR)/openroad/common/io.tcl
source $::env(SCRIPTS_DIR)/openroad/common/set_global_connections.tcl
set_global_connections

set secondary []
foreach vdd $::env(VDD_NETS) gnd $::env(GND_NETS) {
    if { $vdd != $::env(VDD_NET)} {
        lappend secondary $vdd

        set db_net [[ord::get_db_block] findNet $vdd]
        if {$db_net == "NULL"} {
            set net [odb::dbNet_create [ord::get_db_block] $vdd]
            $net setSpecial
            $net setSigType "POWER"
        }
    }

    if { $gnd != $::env(GND_NET)} {
        lappend secondary $gnd

        set db_net [[ord::get_db_block] findNet $gnd]
        if {$db_net == "NULL"} {
            set net [odb::dbNet_create [ord::get_db_block] $gnd]
            $net setSpecial
            $net setSigType "GROUND"
        }
    }
}

set_voltage_domain -name CORE -power $::env(VDD_NET) -ground $::env(GND_NET) \
    -secondary_power $secondary



if { $::env(PDN_MULTILAYER) == 1 } {

    set arg_list [list]
    if { $::env(PDN_ENABLE_PINS) } {
        lappend arg_list -pins "$::env(PDN_VERTICAL_LAYER) $::env(PDN_HORIZONTAL_LAYER)"
    }

    define_pdn_grid \
        -name stdcell_grid \
        -starts_with POWER \
        -voltage_domain CORE \
        {*}$arg_list

    set arg_list [list]
    append_if_equals arg_list PDN_EXTEND_TO "core_ring" -extend_to_core_ring
    append_if_equals arg_list PDN_EXTEND_TO "boundary" -extend_to_boundary

    add_pdn_stripe \
        -grid stdcell_grid \
        -layer $::env(PDN_VERTICAL_LAYER) \
        -width $::env(PDN_VWIDTH) \
        -pitch $::env(PDN_VPITCH) \
        -offset $::env(PDN_VOFFSET) \
        -spacing $::env(PDN_VSPACING) \
        -starts_with POWER \
        {*}$arg_list

    add_pdn_stripe \
        -grid stdcell_grid \
        -layer $::env(PDN_HORIZONTAL_LAYER) \
        -width $::env(PDN_HWIDTH) \
        -pitch $::env(PDN_HPITCH) \
        -offset $::env(PDN_HOFFSET) \
        -spacing $::env(PDN_HSPACING) \
        -starts_with POWER \
        {*}$arg_list

    add_pdn_connect \
        -grid stdcell_grid \
        -layers "$::env(PDN_VERTICAL_LAYER) $::env(PDN_HORIZONTAL_LAYER)"
} else {

    set arg_list [list]
    if { $::env(PDN_ENABLE_PINS) } {
        lappend arg_list -pins "$::env(PDN_VERTICAL_LAYER)"
    }

    define_pdn_grid \
        -name stdcell_grid \
        -starts_with POWER \
        -voltage_domain CORE \
        {*}$arg_list

    set arg_list [list]
    append_if_equals arg_list PDN_EXTEND_TO "core_ring" -extend_to_core_ring
    append_if_equals arg_list PDN_EXTEND_TO "boundary" -extend_to_boundary

    add_pdn_stripe \
        -grid stdcell_grid \
        -layer $::env(PDN_VERTICAL_LAYER) \
        -width $::env(PDN_VWIDTH) \
        -pitch $::env(PDN_VPITCH) \
        -offset $::env(PDN_VOFFSET) \
        -spacing $::env(PDN_VSPACING) \
        -starts_with POWER \
        {*}$arg_list
}

# Adds the standard cell rails if enabled.
if { $::env(PDN_ENABLE_RAILS) == 1 } {
    add_pdn_stripe \
        -grid stdcell_grid \
        -layer $::env(PDN_RAIL_LAYER) \
        -width $::env(PDN_RAIL_WIDTH) \
        -followpins

    add_pdn_connect \
        -grid stdcell_grid \
        -layers "$::env(PDN_RAIL_LAYER) $::env(PDN_VERTICAL_LAYER)"
}


# Adds the core ring if enabled.
if { $::env(PDN_CORE_RING) == 1 } {
    if { $::env(PDN_MULTILAYER) == 1 } {
        set arg_list [list]
        append_if_flag arg_list PDN_CORE_RING_ALLOW_OUT_OF_DIE -allow_out_of_die
        append_if_flag arg_list PDN_CORE_RING_CONNECT_TO_PADS -connect_to_pads
        append_if_equals arg_list PDN_EXTEND_TO "boundary" -extend_to_boundary

        set pdn_core_vertical_layer $::env(PDN_VERTICAL_LAYER)
        set pdn_core_horizontal_layer $::env(PDN_HORIZONTAL_LAYER)

        if { [info exists ::env(PDN_CORE_VERTICAL_LAYER)] } {
            set pdn_core_vertical_layer $::env(PDN_CORE_VERTICAL_LAYER)
        }

        if { [info exists ::env(PDN_CORE_HORIZONTAL_LAYER)] } {
            set pdn_core_horizontal_layer $::env(PDN_CORE_HORIZONTAL_LAYER)
        }

        add_pdn_ring \
            -grid stdcell_grid \
            -layers "$pdn_core_vertical_layer $pdn_core_horizontal_layer" \
            -widths "$::env(PDN_CORE_RING_VWIDTH) $::env(PDN_CORE_RING_HWIDTH)" \
            -spacings "$::env(PDN_CORE_RING_VSPACING) $::env(PDN_CORE_RING_HSPACING)" \
            -core_offset "$::env(PDN_CORE_RING_VOFFSET) $::env(PDN_CORE_RING_HOFFSET)" \
            {*}$arg_list

        if { [info exists ::env(PDN_CORE_VERTICAL_LAYER)] } {
            add_pdn_connect \
                -grid stdcell_grid \
                -layers "$::env(PDN_CORE_VERTICAL_LAYER) $::env(PDN_HORIZONTAL_LAYER)"
        }

        if { [info exists ::env(PDN_CORE_HORIZONTAL_LAYER)] } {
            add_pdn_connect \
                -grid stdcell_grid \
                -layers "$::env(PDN_CORE_HORIZONTAL_LAYER) $::env(PDN_VERTICAL_LAYER)"
        }

        if { [info exists ::env(PDN_CORE_VERTICAL_LAYER)] && [info exists ::env(PDN_CORE_HORIZONTAL_LAYER)] } {
            add_pdn_connect \
                -grid stdcell_grid \
                -layers "$::env(PDN_CORE_VERTICAL_LAYER) $::env(PDN_CORE_HORIZONTAL_LAYER)"
        }

    } else {
        throw APPLICATION "PDN_CORE_RING cannot be used when PDN_MULTILAYER is set to false."
    }
}

# Grid for the three counters: the top-level TopMetal1 stripes cross them and drop TopVia1 onto their Metal4 supply stripes.
# Pins on a supply of its own (vdd_hv of the IHP HV counter) get no via from the VDD stripes, see the straps at the end.
# The VCO and the ring oscillator have no grid, their pins sit off the stripe grid and the straps below connect them.
define_pdn_grid \
    -macro \
    -instances "i_chip_core.counter_lv_ihp i_chip_core.counter_lv_eth i_chip_core.counter_hv_kvc" \
    -name macro \
    -starts_with POWER \
    -halo "$::env(PDN_HORIZONTAL_HALO) $::env(PDN_VERTICAL_HALO)"

add_pdn_connect \
    -grid macro \
    -layers "$::env(PDN_VERTICAL_LAYER) $::env(PDN_HORIZONTAL_LAYER)"

# Custom connect for the amplifier macro.
# Its VDD and VSS pins are horizontal Metal2 and Metal3 strips with no Metal4 above, so the top-level Metal4 stripes cross
# them and one Metal4 to Metal3 connect lands on each strip of the same net.
define_pdn_grid \
    -macro \
    -instances "i_chip_core.amplifier" \
    -name amplifier \
    -starts_with POWER \
    -halo "$::env(PDN_HORIZONTAL_HALO) $::env(PDN_VERTICAL_HALO)"

add_pdn_connect \
    -grid amplifier \
    -layers "Metal3 $::env(PDN_VERTICAL_LAYER)"


# Custom connect for the inverter macro.
# The top-level PDN is on Metal4 (vertical) and TopMetal1 (horizontal).
# The inverter has its own power ring with the horizontal segments on Metal3 and the vertical segments on Metal4, so TopMetal1 stays free.
# The top-level TopMetal1 stripes therefore cross the macro and one Metal4 to TopMetal1 connect feeds the ring.
# A ring that occupied both PDN layers would make pdngen cut every top-level stripe at the macro and leave the ring unfed (PSM-0069).
# Note: within an inverter's power ring no top-level Metal4 or TopMetal1 power rails are routed.
define_pdn_grid \
    -macro \
    -instances "i_chip_core.inverter" \
    -name inverter_top \
    -starts_with POWER \
    -halo "$::env(PDN_HORIZONTAL_HALO) $::env(PDN_VERTICAL_HALO)"

add_pdn_connect \
    -grid inverter_top \
    -layers "$::env(PDN_VERTICAL_LAYER) $::env(PDN_HORIZONTAL_LAYER)"


# ================================================================================================
# Straps to the pins the stripe grid cannot reach
# ================================================================================================
# The VCO, the ring oscillator and the IHP HV counter run from supplies of their own: analog pads whose padbare shares a
# power net with the macro supply pin (PDN_MACRO_CONNECTIONS). The router leaves power nets alone, so these straps are drawn
# here, as are the VSS pins of the VCO and the ring oscillator and the two RF lines, which must not be router wires.
# The coordinates follow from the pad pitch, the core area, the macro locations in config.yaml and the stripe grid
# (PDN_VOFFSET and PDN_HOFFSET 10 um, pitch 50 um), so recheck them when any of these move.
# PDN_OBSTRUCTIONS keeps the TopMetal1 stripes out of the strip below the VCO, where vdd_rf and the VCO VSS run.
# This file is sourced inside a procedure, so the helpers use global variables.
set ::pdn_block [ord::get_db_block]
set ::pdn_tech  [[ord::get_db] getTech]
set ::pdn_dbu   [$::pdn_block getDefUnits]

proc pdn_net {name} {
    set net [$::pdn_block findNet $name]
    if { $net == "NULL" || $net eq "" } {
        puts stderr "\[ERROR\] Net $name of a drawn strap not found."
        exit 1
    }
    return $net
}

# The padbare of a supply pad sits on the signal net the netlist gives it, and add_global_connection skips a pin that is
# already connected. Move it onto the power net of its macro, which Odb.SetPowerConnections named after the RTL.
foreach {pad net} {vdd_rf_pad i_chip_core.vdd_rf vdd_ro_pad i_chip_core.vdd_ro vdd_hv_pad i_chip_core.vdd_hv} {
    set iterm [[$::pdn_block findInst $pad] findITerm padbare]
    $iterm connect [pdn_net $net]
}

# One rectangle of metal, coordinates in um
proc strap {net layer x1 y1 x2 y2} {
    set sw [odb::dbSWire_create $net ROUTED]
    odb::dbSBox_create $sw [$::pdn_tech findLayer $layer] \
        [expr {round($x1 * $::pdn_dbu)}] [expr {round($y1 * $::pdn_dbu)}] \
        [expr {round($x2 * $::pdn_dbu)}] [expr {round($y2 * $::pdn_dbu)}] STRIPE
}

# Single-cut tech vias filling a rectangle in um, the via centers inset from its edges by cut half width plus enclosure
proc via_array {net via x1 y1 x2 y2 pitch inset_x inset_y} {
    set sw [odb::dbSWire_create $net ROUTED]
    set v [$::pdn_tech findVia $via]
    for {set x [expr {$x1 + $inset_x}]} {$x <= $x2 - $inset_x + 1e-6} {set x [expr {$x + $pitch}]} {
        for {set y [expr {$y1 + $inset_y}]} {$y <= $y2 - $inset_y + 1e-6} {set y [expr {$y + $pitch}]} {
            odb::dbSBox_create $sw $v [expr {round($x * $::pdn_dbu)}] [expr {round($y * $::pdn_dbu)}] STRIPE
        }
    }
}

# A connection into a macro whose obstructions cover its pins ends at the macro edge, on the pin: touching shapes connect,
# and a strap reaching into the obstruction fails the blocked layers check of the detailed placer (DPL-0033).
# That check also rejects a same-layer strap at the top edge of a macro, so a pin there takes a via stack from above.
proc draw_straps {} {
# Via3: 0.19 um cut, 0.29 um spacing between adjacent cuts. TopVia1: 0.42 um cut and spacing, 1.5 um wide on TopMetal1,
# so a center 0.75 um from the strap edge keeps that rectangle inside the strap.
set via3_pitch 0.48
set via3_inset 0.3
set topvia1_pitch 0.84
set topvia1_inset 0.75

# vdd_rf, 10.8 mA: padbare of vdd_rf_pad (Metal3 at y 320, x 1036.1 to 1060.9) -> Metal3 north under the core ring ->
# TopMetal1 west along the strip below the VCO -> the VCO VDD pin (TopMetal1, x 728.64 to 730.64, y 385.14 to 386.78)
set n [pdn_net i_chip_core.vdd_rf]
strap $n Metal3 1039 319.71 1058 380
strap $n Metal4 1039 368 1058 380
via_array $n Via3_XX 1039 368 1058 380 $via3_pitch $via3_inset $via3_inset
strap $n TopMetal1 726 370 1058 380
via_array $n TopVia1EWNS 1039 370 1058 380 $topvia1_pitch $topvia1_inset $topvia1_inset
strap $n TopMetal1 728.64 380 730.64 385.14

# VCO VSS: its VSS pin (TopMetal1, x 728.64 to 731.91, y 388.42 to 390.06) -> TopMetal1 west -> TopVia1 onto the Metal4
# VSS stripes centered at x 628.28 and 678.28 (pdngen offsets the stripe centers), 16 cuts for the 10.8 mA of the VCO
set n [pdn_net VSS]
strap $n TopMetal1 620 388.42 726 396
strap $n TopMetal1 726 388.42 728.64 390.06
foreach x {627.78 677.78} {
    via_array $n TopVia1EWNS $x 388.42 [expr {$x + $::env(PDN_VWIDTH)}] 396 $topvia1_pitch 0.5 $topvia1_inset
}

# vdd_hv: padbare of vdd_hv_pad (Metal3 at x 1280, y 1136.1 to 1160.9) -> Metal3 west under the core ring ->
# TopMetal1 over the IHP HV counter between the stripes -> TopVia1 onto its four Metal4 VDD stripes.
# The step up to TopMetal1 sits east of the last Metal4 stripes (x 1225 and 1228): the via stacks from those stripes to the
# rails have Metal3 pads, so a Metal3 strap crossing them would short it to VDD and VSS.
set n [pdn_net i_chip_core.vdd_hv]
strap $n Metal3 1230.5 1140 1280.29 1158
strap $n Metal4 1230.5 1140 1235 1158
via_array $n Via3_XX 1230.5 1140 1235 1158 $via3_pitch $via3_inset $via3_inset
via_array $n TopVia1EWNS 1230.5 1140 1235 1158 $topvia1_pitch $topvia1_inset $topvia1_inset
strap $n TopMetal1 968 1140 1235 1158
foreach x {975.26 1025.26 1075.26 1125.26} {
    via_array $n TopVia1EWNS $x 1140 [expr {$x + 1.0}] 1158 $topvia1_pitch 0.5 $topvia1_inset
}

# vdd_ro, up to 4 mA: padbare of vdd_ro_pad (Metal3 at x 1280, y 936.1 to 960.9) -> Metal3 west under the core ring ->
# TopMetal1 over the ring oscillator -> via stack onto its VDD pin at the top edge (Metal3, x 1140.955 to 1142.565, y 943.66 to 945.16).
# The stack is tech vias on a Metal4 patch over the pin: 9 Via3 cuts carry 3.6 mA and 4 TopVia1 cuts 5.6 mA.
set n [pdn_net i_chip_core.vdd_ro]
strap $n Metal3 1230.5 939 1280.29 950
strap $n Metal4 1230.5 939 1235 950
via_array $n Via3_XX 1230.5 939 1235 950 $via3_pitch $via3_inset $via3_inset
via_array $n TopVia1EWNS 1230.5 939 1235 950 $topvia1_pitch $topvia1_inset $topvia1_inset
strap $n TopMetal1 1136 939 1235 950
strap $n Metal4 1140.955 943.66 1142.565 945.16
via_array $n Via3_XX 1140.955 943.66 1142.565 945.16 $via3_pitch 0.325 0.27
via_array $n TopVia1EWNS 1140.955 943.66 1142.565 945.16 $topvia1_pitch 0.315 0.31

# Ring oscillator VSS: its VSS pin at the bottom edge (Metal3, x 1140.955 to 1142.565, y 929.88 to 931.38) -> Metal3 south ->
# Via3 and TopVia1 onto the TopMetal1 VSS stripe centered at y 882.66 (y 881.66 to 883.66)
set n [pdn_net VSS]
strap $n Metal3 1140.955 927.88 1142.565 929.88
strap $n Metal3 1138 880 1146 928.38
strap $n Metal4 1138 880 1146 887
via_array $n Via3_XX 1138 880 1146 887 $via3_pitch $via3_inset $via3_inset
via_array $n TopVia1EWNS 1138 881.66 1146 883.66 $topvia1_pitch $topvia1_inset 1.0

# RF lines, marked special so that the router leaves them alone: padbare of the RF pad (TopMetal1 at y 320) ->
# TopVia1 and Via3 below the core ring -> 4 um of Metal3 north -> the VCO pin (Metal3, 0.6 um wide, at y 385.14)
foreach {name pad_x vco_x} {i_chip_core.rf_out_n 749.18 787.84 i_chip_core.rf_out_p 849.18 811.84} {
    set n [pdn_net $name]
    $n setSpecial
    set line_x1 [expr {$vco_x + 0.3 - 2.0}]
    set line_x2 [expr {$vco_x + 0.3 + 2.0}]
    strap $n TopMetal1 $pad_x 314 [expr {$pad_x + 1.64}] 326
    strap $n Metal4 [expr {$pad_x - 0.68}] 320.5 [expr {$pad_x + 2.32}] 326.5
    via_array $n TopVia1EWNS $pad_x 320.5 [expr {$pad_x + 1.64}] 326 $topvia1_pitch 0.82 $topvia1_inset
    via_array $n Via3_XX [expr {$pad_x - 0.68}] 320.5 [expr {$pad_x + 2.32}] 326.5 $via3_pitch $via3_inset $via3_inset
    strap $n Metal3 [expr {min($pad_x - 0.68, $line_x1)}] 320.5 [expr {max($pad_x + 2.32, $line_x2)}] 326.5
    strap $n Metal3 $line_x1 320.5 $line_x2 384
    strap $n Metal3 $vco_x 383 [expr {$vco_x + 0.6}] 385.14
}
}

# LibreLane calls pdngen right after sourcing this file. pdngen cuts its stripes around shapes that already exist, which
# would open the ring oscillator's VSS stripe, so the straps go in right after it.
rename pdngen pdngen_stock
proc pdngen {args} {
    pdngen_stock {*}$args
    draw_straps
}