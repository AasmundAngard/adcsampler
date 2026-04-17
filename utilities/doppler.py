import numpy as np
import matplotlib.pyplot as plt


def speedToDopplershift(vr:float,f0,c=3e8) -> float:
    # fD = 2*vr*f0 / c
    return 2*vr*f0/c

def dopplershiftToSpeed(fD,f0,c=3e8) -> float:
    # vr = fD*c/(2*f0)
    return fD*c/(2*f0)




