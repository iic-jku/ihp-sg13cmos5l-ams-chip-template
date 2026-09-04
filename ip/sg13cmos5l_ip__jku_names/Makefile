# SPDX-FileCopyrightText: 2026 Simon Dorrer and Harald Pretl
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1

MAKEFILE_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

# Variables
TOP = sg13cmos5l_ip__jku_names

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

# KLayout DRC level: precheck, macro, or regular (sak-drc.sh -l, only used by klayout-drc; default: macro)
# Override with: make <target> DRC_LEVEL=<precheck|macro|regular>
DRC_LEVEL ?= macro

# Extra options for the sak-open.py file browser (e.g. --all to include build outputs)
# Override with: make open OPEN_ARGS=<options>
OPEN_ARGS ?=

# Folder structure
GDS_DIR     := final/gds
LEF_DIR     := final/lef
LIB_DIR     := final/lib
VH_DIR      := final/vh
DRC_RPT_DIR := verification/drc

# Logo parameters
IMG_FILE    := logo/jku_names.png
BLOCK_SIZE  ?= 100
# Pixel size in microns. Must be >= 0.21 um, the Metal4 minimum space (Mn.b), because single pixels and single-pixel gaps are drawn as is.
PIXEL_SIZE  ?= 0.25

# Layer selection for the logo (IHP SG13CMOS5L)
# Override with: make <target> LAYER=<Metal1|Metal2|Metal3|Metal4|TopMetal1>
# The logo target hands the name to img2lay.py, which resolves it through the PDK layer properties, and the lef target writes it as the OBS layer.
LAYER ?= Metal4

VALID_LAYERS := Metal1 Metal2 Metal3 Metal4 TopMetal1
ifeq ($(filter $(LAYER),$(VALID_LAYERS)),)
$(error Invalid LAYER: '$(LAYER)'. Must be one of $(VALID_LAYERS))
endif


# Help Target
help: ## Show this help message
	@echo 'Usage: make <target> [LAYER=<Metal1|Metal2|Metal3|Metal4|TopMetal1>] [BLOCK_SIZE=<um>] [PIXEL_SIZE=<um>] [CELL=<cellname>] [DRC_LEVEL=<precheck|macro|regular>] [OPEN_ARGS=<options>]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z0-9_.-]+:.*## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*## "}; {printf "  %-20s %s\n", $$1, $$2}'
	@echo ''
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
	rm -rf script/__pycache__
.PHONY: clean
# ================================================================================================


# Build Target
# Logo is drawn on $(LAYER). Override with LAYER=<name>.
# Boundary layers: prBoundary (189/0) and NoMetFiller (160/0).
logo: ## Generate GDS from image using Python script
	mkdir -p $(GDS_DIR)
	python3 script/img2lay.py $(IMG_FILE) $(GDS_DIR)/$(TOP).gds --cellname $(TOP) --invert --merge --pixel-size $(PIXEL_SIZE) --block-size $(BLOCK_SIZE) --foreground $(LAYER) --boundary prBoundary NoMetFiller
.PHONY: logo
# ================================================================================================


# DRC Targets
klayout-drc: ## Run KLayout DRC of the CELL cell (usage: make klayout-drc [CELL=<cellname>] [DRC_LEVEL=<precheck|macro|regular>])
	mkdir -p $(DRC_RPT_DIR)
	sak-drc.sh -d -k -l $(DRC_LEVEL) -w $(DRC_RPT_DIR) $(GDS_DIR)/$(CELL).gds
.PHONY: klayout-drc

magic-drc: ## Run Magic DRC of the CELL cell (usage: make magic-drc [CELL=<cellname>])
	mkdir -p $(DRC_RPT_DIR)
	sak-drc.sh -d -m -f "*" -w $(DRC_RPT_DIR) $(GDS_DIR)/$(CELL).gds
.PHONY: magic-drc
# ================================================================================================


# LEF Target
lef: ## Generate LEF macro definition for the logo
	mkdir -p $(LEF_DIR)
	@printf 'VERSION 5.8 ;\n  NOWIREEXTENSIONATPIN ON ;\n  DIVIDERCHAR "/" ;\n  BUSBITCHARS "[]" ;\nMACRO $(TOP)\n  CLASS BLOCK ;\n  FOREIGN $(TOP) ;\n  ORIGIN 0.000 0.000 ;\n  SIZE $(BLOCK_SIZE) BY $(BLOCK_SIZE) ;\n  OBS\n      LAYER $(LAYER) ;\n        RECT 0.0 0.0 $(BLOCK_SIZE) $(BLOCK_SIZE) ;\n  END\nEND $(TOP)\nEND LIBRARY\n' > $(LEF_DIR)/$(TOP).lef
.PHONY: lef
# ================================================================================================


# LIB Target
lib: ## Generate LIB timing library for the logo
	mkdir -p $(LIB_DIR)
	@printf 'library ($(TOP)) {\n  input_threshold_pct_fall: 50.0;\n  input_threshold_pct_rise: 50.0;\n  output_threshold_pct_fall: 50.0;\n  output_threshold_pct_rise: 50.0;\n  slew_lower_threshold_pct_fall: 20.0;\n  slew_lower_threshold_pct_rise: 20.0;\n  slew_upper_threshold_pct_fall: 80.0;\n  slew_upper_threshold_pct_rise: 80.0;\n  \n  cell ($(TOP)) {\n  }\n}\n' > $(LIB_DIR)/$(TOP).lib
.PHONY: lib
# ================================================================================================


# Verilog Target
verilog: ## Generate a minimal Verilog wrapper for the logo
	mkdir -p $(VH_DIR)
	@printf 'module $(TOP);\nendmodule\n' > $(VH_DIR)/$(TOP).vh
.PHONY: verilog
# ================================================================================================


# Build and Verify All Target
all: ## Build and verify the logo
	$(MAKE) clean
	$(MAKE) logo
	$(MAKE) lef
	$(MAKE) lib
	$(MAKE) verilog
	$(MAKE) klayout-drc
	$(MAKE) magic-drc
.PHONY: all
# ================================================================================================
