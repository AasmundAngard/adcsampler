import numpy as np

def angleOfAttack(n21,n31,n32):
    """nxy: Forsinkelsen FRA y TIL x, retur i rad"""

    y = n31 + n21
    x = n31 - n21 + 2*n32

    
    theta = np.arctan(np.sqrt(3)*y/x)

    if (x<0):
        theta += np.pi


    return theta