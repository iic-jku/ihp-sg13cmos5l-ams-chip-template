# SPDX-FileCopyrightText: 2026 Simon Dorrer and Harald Pretl
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1

MAKEFILE_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

# Variables
TOP = sg13cmos5l_ip__bondpad_70x70
RF_TOP = sg13cmos5l_ip__rfpad_70x70

.DEFAULT_GOAL := help

# PDK Guard
# Override with: make <target> REQUIRED_PDK=<pdk>, an empty value skips the check
REQUIRED_PDK ?= ihp-sg13cmos5l

# Goals that do not read the PDK
PDK_FREE_GOALS = help clean

ifneq ($(REQUIRED_PDK),)
ifneq ($(filter-out $(PDK_FREE_GOALS),$(or $(MAKECMDGOALS),$(.DEFAULT_GOAL))),)
ifneq ($(PDK),$(REQUIRED_PDK))
$(error PDK is "$(PDK)", but this IP needs "$(REQUIRED_PDK)". Run `sak-pdk $(REQUIRED_PDK)` in this shell and retry, or pass REQUIRED_PDK= to skip this check)
endif
endif
endif
# ================================================================================================


# Cell name for verification targets (default: top-level cell)
# Override with: make <target> CELL=<cellname>
CELL ?= $(TOP)

# KLayout/gdscheck DRC level: precheck, macro, or regular (sak-drc.sh -l, only used by klayout-drc and gdscheck-drc; default: macro)
# Override with: make <target> DRC_LEVEL=<precheck|macro|regular>
DRC_LEVEL ?= macro

# gdscheck suite, replaces the one DRC_LEVEL selects (sak-drc.sh -s, only used by gdscheck-drc; default: empty = precheck runs precheck, macro core, regular main)
# Override with: make <target> GDSCHECK_SUITE=<precheck|core|main|density|antenna|recommended>
GDSCHECK_SUITE ?=

# gdscheck rule decks instead of a suite, comma-separated (sak-drc.sh -D, only used by gdscheck-drc, not together with GDSCHECK_SUITE; default: empty = run the suite)
# Override with: make <target> GDSCHECK_DECKS=<deck>[,<deck>...]
GDSCHECK_DECKS ?=

# Parallel DRC jobs, the KLayout processes and gdscheck threads (sak-drc.sh -j, only used by klayout-drc and gdscheck-drc; default: empty = 4 KLayout processes or fewer, gdscheck on every CPU)
# Override with: make <target> DRC_JOBS=<n>
DRC_JOBS ?=

# sak-drc.sh options for the three variables above, left out when empty so that the script defaults apply
_GDSCHECK_SUITE_OPT = $(if $(GDSCHECK_SUITE),-s "$(GDSCHECK_SUITE)")
_GDSCHECK_DECKS_OPT = $(if $(GDSCHECK_DECKS),-D "$(GDSCHECK_DECKS)")
_DRC_JOBS_OPT = $(if $(DRC_JOBS),-j $(DRC_JOBS))

# Extra options for the sak-open.py file browser (e.g. --all to include build outputs)
# Override with: make open OPEN_ARGS=<options>
OPEN_ARGS ?=

# Folder structure
GDS_DIR   	:= final/gds
LEF_DIR   	:= final/lef
LIB_DIR   	:= final/lib
VH_DIR    	:= final/vh
DRC_RPT_DIR := verification/drc
LVS_RPT_DIR := verification/lvs
XSCHEM_SCH_DIR := schematic/xschem
NET_SCH_DIR := netlist/schematic
NET_LAY_DIR := netlist/layout

# Bondpad parameters
DIAMETER     ?= 70.0
SHAPE        ?= square
BOTTOM_METAL ?= 3


# Help Target
help: ## Show this help message
	@echo 'Usage: make <target> [DIAMETER=<um>] [SHAPE=<square|octagon|circle>] [BOTTOM_METAL=<1-4>] [CELL=<cellname>]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z0-9_.-]+:.*## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*## "}; {printf "  %-20s %s\n", $$1, $$2}'
	@echo ''
	@echo 'DIAMETER defaults to $(DIAMETER) (µm).'
	@echo 'SHAPE defaults to $(SHAPE). Allowed: square, octagon, circle.'
	@echo 'BOTTOM_METAL defaults to $(BOTTOM_METAL) (1=Metal1 .. 4=Metal4). Top is fixed to TopMetal1.'
	@echo 'CELL defaults to $(TOP). Override to verify other cells, $(RF_TOP) is the RF pad.'
	@echo 'REQUIRED_PDK defaults to $(REQUIRED_PDK). Every target except help and clean aborts if $$PDK differs.'
.PHONY: help
# ================================================================================================


# Open Target
open: ## Open the design files of this folder in the sak-open.py file browser (needs the VNC/X11 desktop)
	sak-open.py $(OPEN_ARGS) .
.PHONY: open
# ================================================================================================


# Clean Target
clean: ## Remove generated outputs and reports
	rm -rf $(GDS_DIR)
	rm -rf $(LEF_DIR)
	rm -rf $(LIB_DIR)
	rm -rf $(VH_DIR)
	rm -rf $(DRC_RPT_DIR)
	rm -rf $(LVS_RPT_DIR)
	rm -rf $(NET_SCH_DIR)
	rm -rf $(NET_LAY_DIR)
	rm -rf script/__pycache__
.PHONY: clean
# ================================================================================================


# Build Target
bondpad: ## Generate bondpad GDS and LEF (usage: make bondpad [DIAMETER=<um>] [SHAPE=<square|octagon|circle>] [BOTTOM_METAL=<1-4>])
	KLAYOUT_PATH=$(PDK_ROOT)/$(PDK)/libs.tech/klayout:$(PDK_ROOT)/$(PDK)/libs.tech/klayout/tech klayout -n sg13cmos5l -zz -r script/bondpad.py -rd diameter=$(DIAMETER) -rd shape=$(SHAPE) -rd bottom_metal=$(BOTTOM_METAL) -rd gds_output=$(GDS_DIR)/$(TOP).gds -rd lef_output=$(LEF_DIR)/$(TOP).lef
.PHONY: bondpad

rfpad: ## Generate the RF pad GDS, LEF and Liberty, the script stops on a broken geometry or connectivity
	KLAYOUT_PATH=$(PDK_ROOT)/$(PDK)/libs.tech/klayout:$(PDK_ROOT)/$(PDK)/libs.tech/klayout/tech klayout -n sg13cmos5l -zz -r script/bondpad.py -rd pad_type=rf -rd gds_output=$(GDS_DIR)/$(RF_TOP).gds -rd lef_output=$(LEF_DIR)/$(RF_TOP).lef -rd lib_output=$(LIB_DIR)/$(RF_TOP).lib
.PHONY: rfpad
# ================================================================================================


# DRC Targets
klayout-drc: ## Run KLayout DRC of the CELL cell (usage: make klayout-drc [CELL=<cellname>] [DRC_LEVEL=<precheck|macro|regular>] [DRC_JOBS=<n>])
	mkdir -p $(DRC_RPT_DIR)
	sak-drc.sh -d -k -l $(DRC_LEVEL) $(_DRC_JOBS_OPT) -w $(DRC_RPT_DIR) $(GDS_DIR)/$(CELL).gds
.PHONY: klayout-drc

magic-drc: ## Run Magic DRC of the CELL cell (usage: make magic-drc [CELL=<cellname>])
	mkdir -p $(DRC_RPT_DIR)
	sak-drc.sh -d -m -w $(DRC_RPT_DIR) $(GDS_DIR)/$(CELL).gds
.PHONY: magic-drc

gdscheck-drc: ## Run gdscheck DRC of the CELL cell (usage: make gdscheck-drc [CELL=<cellname>] [DRC_LEVEL=<precheck|macro|regular>] [GDSCHECK_SUITE=<suite>|GDSCHECK_DECKS=<decks>] [DRC_JOBS=<n>])
	mkdir -p $(DRC_RPT_DIR)
	sak-drc.sh -d -g -l $(DRC_LEVEL) $(_GDSCHECK_SUITE_OPT) $(_GDSCHECK_DECKS_OPT) $(_DRC_JOBS_OPT) -w $(DRC_RPT_DIR) $(GDS_DIR)/$(CELL).gds
.PHONY: gdscheck-drc

# Pad.fR_M1 asks for 7 um of Metal1 past dfpad. The Metal1 crossing dfpad is the RF shield's 3 um collar, a ground plane that exits nowhere, and the 80 um cell leaves 5 um a side.
# Without the collar the pad's rim field lands on the substrate, so exactly these markers are waived and anything else fails.
_RF_DRC_REPORTS = $(DRC_RPT_DIR)/$(RF_TOP).klayout.drc/*.lyrdb

rfpad-klayout-drc: ## Run KLayout DRC of the RF pad at macro level, passes only with exactly the 7 waived Pad.fR_M1 markers (usage: make rfpad-klayout-drc [DRC_JOBS=<n>])
	mkdir -p $(DRC_RPT_DIR)
	rm -f $(_RF_DRC_REPORTS)
	sak-drc.sh -d -k -l macro $(_DRC_JOBS_OPT) -w $(DRC_RPT_DIR) $(GDS_DIR)/$(RF_TOP).gds || true
	@total=$$(cat $(_RF_DRC_REPORTS) | grep -c '<category>.*</category>'); \
	waived=$$(cat $(_RF_DRC_REPORTS) | grep -c "<category>'Pad.fR_M1'</category>"); \
	echo "rfpad-klayout-drc: $$total markers, $$waived of them the waived Pad.fR_M1"; \
	test "$$total" -eq 7 && test "$$waived" -eq 7
.PHONY: rfpad-klayout-drc
# ================================================================================================


# LVS Targets
rfpad-lvs-netlist: ## Export the CDL schematic netlist of the RF pad from Xschem for KLayout LVS
	mkdir -p $(NET_SCH_DIR)
	xschem -s -r -x -q --rcfile $(XSCHEM_SCH_DIR)/xschemrc --command ' \
		set spiceprefix 1; \
		set lvs_netlist 1; \
		set top_is_subckt 1; \
		set lvs_ignore 1; \
		set netlist_dir $(NET_SCH_DIR); \
		xschem set netlist_name [file tail [file rootname [xschem get current_name]]]_klayout.cdl; \
		xschem netlist \
	' $(XSCHEM_SCH_DIR)/$(RF_TOP).sch
.PHONY: rfpad-lvs-netlist

rfpad-lvs: ## Run KLayout LVS of the RF pad against its schematic
	$(MAKE) rfpad-lvs-netlist
	mkdir -p $(LVS_RPT_DIR)
	mkdir -p $(NET_LAY_DIR)
	sak-lvs.sh -d -k -w $(LVS_RPT_DIR) -s $(NET_SCH_DIR)/$(RF_TOP)_klayout.cdl -l $(GDS_DIR)/$(RF_TOP).gds -c $(RF_TOP)
	mv $(LVS_RPT_DIR)/$(RF_TOP).klayout.lvs/$(RF_TOP)_extracted.cir $(NET_LAY_DIR)/$(RF_TOP)_klayout.cir
.PHONY: rfpad-lvs
# ================================================================================================


# Verilog Target
verilog: ## Generate minimal Verilog wrappers for the bondpad and the RF pad
	mkdir -p $(VH_DIR)
	@printf 'module $(TOP) (\n    inout pad\n);\nendmodule\n' > $(VH_DIR)/$(TOP).vh
	@printf '(* blackbox *)\nmodule $(RF_TOP) (\n    inout vss,\n    inout vdd,\n    inout iovss,\n    inout iovdd,\n    inout pad,\n    inout padbare\n);\nendmodule\n' > $(VH_DIR)/$(RF_TOP).vh
.PHONY: verilog
# ================================================================================================


# Build and Verify All Target
all: ## Build and verify the bondpad and the RF pad
	$(MAKE) clean
	$(MAKE) bondpad
	$(MAKE) rfpad
	$(MAKE) verilog
	$(MAKE) klayout-drc
	$(MAKE) gdscheck-drc
	$(MAKE) rfpad-klayout-drc
	$(MAKE) gdscheck-drc CELL=$(RF_TOP)
	$(MAKE) rfpad-lvs
# The flows leave the Magic DRC out until the foundry cells are clean in it, make magic-drc still runs it
#	$(MAKE) magic-drc
.PHONY: all
# ================================================================================================