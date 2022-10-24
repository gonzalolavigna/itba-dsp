## Makefile

# Defaults
SIM ?= ghdl
TOPLEVEL_LANG ?= vhdl

# Sources
VHDL_SOURCES += $(PWD)/hdl/mult_by_constant.vhd

TOPLEVEL = mult_by_constant
MODULE = test_fxp

SIM_ARGS+=--vcd=wave.vcd

include $(shell cocotb-config --makefiles)/Makefile.sim