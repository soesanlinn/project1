Test github with my first project.

tvm.py
This function will ask user to enter all but one input that he/ she needs to know and generate the result.

----------------------------------------------------------------
from tvm.tvm import tvm
fv = ''
pmt = -3_000
pv = 0
rate = 0.06/12
nper = 12*20
result = tvm(nper=nper, pmt=pmt, rate= rate, pv=pv, fv=fv)
print(result) # print out fv
