import numpy as np
from raspi_import import raspi_import

def findTheta(toFileName):
    # Les fra fil, og beregn theta

    
    skipSpike = 100 
    numSamples = 31250
    # numSamples = 100
    resolution = 4096
    max_voltage = 3.3
    # Les fra fil
    sample_period,data = raspi_import(toFileName,3)
    timeaxis = np.arange(numSamples)*sample_period

    # Fjern DC
    c1_avg = np.sum(data[:,0])/data.shape[0]
    c2_avg = np.sum(data[:,1])/data.shape[0]
    c3_avg = np.sum(data[:,2])/data.shape[0]

    # Hent ut data
    c1 = (data[skipSpike:skipSpike+numSamples,0]-c1_avg)/resolution*max_voltage
    c2 = (data[skipSpike:skipSpike+numSamples,1]-c2_avg)/resolution*max_voltage
    c3 = (data[skipSpike:skipSpike+numSamples,2]-c3_avg)/resolution*max_voltage

    # Beregn korrelasjon
    korr21 = np.correlate(c2,c1,mode="full")
    korr31 = np.correlate(c3,c1,mode="full")
    korr32 = np.correlate(c3,c2,mode="full")

    # Høyeste peak sier tiden fra y til x (korrxy)
    delay21 = np.argmax(korr21) - numSamples + 1
    delay31 = np.argmax(korr31) - numSamples + 1
    delay32 = np.argmax(korr32) - numSamples + 1

    print("antall knepp forsinkelse 1 til 2/ 1 foran 2: ",delay21)
    print("1 foran 3: ",delay31)
    print("2 foran 3: ",delay32)

    # Beregn theta fra figur 4
    theta = angleOfAttack(delay21,delay31,delay32)/np.pi * 180

    return theta



def angleOfAttack(n21,n31,n32):
    """nxy: Forsinkelsen FRA y TIL x, retur i rad"""

    y = n31 + n21
    x = n31 - n21 + 2*n32

    
    theta = np.arctan(np.sqrt(3)*y/x)

    if (x<0):
        theta += np.pi


    return theta