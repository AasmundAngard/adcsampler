import subprocess
import numpy as np
import os

from utilities.raspi_import import raspi_import
from utilities.findTheta import angleOfAttack


# Kode for retningsbestemmelse av lud
# Kjører 3 ADC-er og lagrer resultatet
# Finner tidsforsinkelsen mellom signalene
# Beregner innfallsvinkel til lyden


while True:
    angleToTest = input("Hvilken vinkel vil du teste: ")

    if angleToTest in ["q","quit","close","end"]:
        break

    # Finn ubrukt filnavn for målinger
    toFileName =None
    tempName = "measure"+angleToTest+".bin"
    if os.path.isfile(tempName):
        for i in range(10):
            tempName = "measure"+angleToTest+""+i+".bin"
            if not (os.path.isfile(tempName)):
                toFileName = tempName
                break
    else:
        toFileName = tempName
        
    del tempName

    if toFileName == None:
        break

    # Kjør adc_sampler med 1 sekund sampling, og skriv til filnavn. Blokkerer til ferdig kjørt
    subprocess.run(["./adc_sampler", 31250, toFileName], check=True)


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
    print("theta: ",theta)
