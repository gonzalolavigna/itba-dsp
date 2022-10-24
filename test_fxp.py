import numpy as np
from lib import conversions
import cocotb
from cocotb.triggers import Timer
from cocotb.triggers import RisingEdge, FallingEdge, Timer

from typing import Iterable, List, Sequence, Optional
import os
import fxpmath

#async def feed_samples( dut , samples: Iterable[float], dtype: str = "S16.16"):
#    for sample in samples:
#        dut.data_i.value = conversions.float_to_fixed(sample, dtype)
#        await FallingEdge(dut.clk_i)
#    dut.data_i.value = 0

output_data_dir = "output"

f_s = 100e6
f_a = 1e6
n   = 100

signal_input = 0.25*np.sin(2 * np.pi * f_a * np.arange(n) / f_s)
abs_path = lambda f: str(os.path.join(output_data_dir, f))
np.save(abs_path("signal_input"), signal_input, allow_pickle=True)

data_type = "S16.16"
#Convert to fixed point
fxp_real_list = []
for sample in signal_input:
  sample_fxp_real = fxpmath.Fxp(sample,True, 16, 8,overflow='saturate')
  fxp_real_list.append(sample_fxp_real.get_val())

print("{:2.2f}".format(fxp_real_list[0]))
print("{:2.2f}".format(fxp_real_list[25]))
print("{:2.2f}".format(fxp_real_list[50]))
print("{:2.2f}".format(fxp_real_list[75]))
print("{:2.2f}".format(fxp_real_list[99]))


signal_fixed_point = np.asarray(sample_fxp_real)
np.save(abs_path("signal_fxp"), fxp_real_list, allow_pickle=True)


async def reset_dut(dut):
    dut.reset_ni.value = 0
    await Timer(1, units="us")  # type: ignore
    dut.reset_ni.value = 1
    await Timer(1, units="us")  # type: ignore

async def generate_clock(dut):
    while True:
        dut.clk_i.value = 0
        await Timer(1, units="ns")  # type: ignore
        dut.clk_i.value = 1
        await Timer(1, units="ns")  # type: ignore

async def feed_samples(dut,samples,dtype ):
    for sample in samples:
        dut.data_i.value = conversions.float_to_fixed(sample, dtype)
        await FallingEdge(dut.clk_i)
    dut.data_i.value = 0

async def capture_output(dut, arr, dtype: str = "S32.32"):
    await RisingEdge(dut.clk_i)  # Don't capture unil fist compute completes.
    while True:
        await FallingEdge(dut.clk_i)
        arr.append(conversions.fxp_binary_value_to_float(dut.data_o, dtype))
    


@cocotb.test()
async def test_multiplication(dut):
    # Reset pulse.    
    output: List[float] = list()
    
    await reset_dut(dut)
    
    await Timer(1, units="us")  # Make some delay here
    
    await cocotb.start(generate_clock(dut))
    await cocotb.start(feed_samples(dut, signal_input,dtype="S0.16"))   
    await cocotb.start(capture_output(dut, output, dtype="S0.32")) 
    await Timer(2, units="us")  # Make some delay here
    
    # Getting DUT output.
    output_ndarray = np.array(output)
    if output_data_dir is not None:
      abs_path = lambda f: str(os.path.join(output_data_dir, f))
      np.save(abs_path("signal_output"), output_ndarray, allow_pickle=True)