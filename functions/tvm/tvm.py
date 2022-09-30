import numpy_financial as npf

def tvm(inputs: dict) -> float:
    fv = inputs['fv']
    pmt = inputs['pmt']
    pv = inputs['pv']
    rate = inputs['rate']
    nper = inputs['nper']
    if nper == '':
        return npf.nper(pmt= pmt, rate= rate, pv= pv, fv= fv)
    elif rate == '':
        return npf.rate(nper= nper, pmt= pmt, pv= pv, fv= fv)
    elif pmt == '':
        return npf.pmt(nper= nper, rate= rate, pv= pv, fv= fv)
    elif pv == '':
        return npf.pv(nper= nper, pmt= pmt, rate= rate, fv= fv)
    elif fv == '':
        return npf.fv(nper= nper, pmt= pmt, rate= rate, pv= pv)


if __name__=='__main__':
    inputs = {
        'fv': '',
        'pmt': -3_000,
        'pv': 0,
        'rate': 0.06 / 12,
        'nper': 12 * 20
    }
    result = tvm(inputs)
    print(result)
