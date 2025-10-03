from datetime import datetime
from functions.op_pyxl.op_pyxl import op_pyxl as xl
from functions.yh_fnce.yh_fnce import yh_fnce as yf

current_time = datetime.now().strftime("%d-%b-%y %I:%M %p")
# path = ("/Users/minipotus/Dropbox/Personal.xlsm") # old path for old mac
path = ("/Users/ssl/Dropbox/Personal.xlsm")
tbl_name = "rPF_Budget"
mywb = xl(path)

def updatemktdata():
    USDCAD = yf.lastclose("CAD=X")
    SGDCAD = yf.lastclose("SGDUSD=X")*USDCAD
    USDMMK = yf.lastclose("MMK=X")
    MMKCAD = USDCAD/USDMMK
    EURCAD = yf.lastclose("EURCAD=X")
    HKDCAD = yf.lastclose("HKDCAD=X")
    GLEPA = yf.lastclose("GLE.PA")
    mywb.update_rng_val("USDCAD",USDCAD)
    mywb.update_rng_val("SGDCAD",SGDCAD)
    mywb.update_rng_val("MMKCAD",MMKCAD)
    mywb.update_rng_val("EURCAD", EURCAD)
    mywb.update_rng_val("HKDCAD", HKDCAD)
    mywb.update_rng_val("rPF_SGStockPrice",GLEPA)
    mywb.update_rng_val("rPF_TS_Py",current_time)

updatemktdata()