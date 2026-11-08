# SPDX-FileCopyrightText: 2026 Simon Dorrer and Harald Pretl
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
# Description: Netgen setup for the Magic LVS of cells with cap_cmomf: the PDK setup, and the MoM caps left out.
#
# Magic's ihp-sg13cmos5l tech draws cap_cmomf but extracts no device for it, so its combs come out as plain metal and
# the schematic's caps have no counterpart. KLayout LVS extracts them, and scripts/check_mom.py checks their size and
# stack, so Netgen compares the rest of the cell without them.

source $::env(PDK_ROOT)/$::env(PDK)/libs.tech/netgen/$::env(PDK)_setup.tcl
ignore class "-circuit2 cap_cmomf"
