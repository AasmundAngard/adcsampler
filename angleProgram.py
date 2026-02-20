import subprocess
import numpy as np
import os

from utilities.raspi_import import raspi_import
from utilities.findTheta import angleOfAttack,findTheta


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
            tempName = "measure"+angleToTest+"_"+i+".bin"
            if not (os.path.isfile(tempName)):
                toFileName = tempName
                break
    else:
        toFileName = tempName
        
    del tempName

    if toFileName == None:
        break

    # Kjør adc_sampler med 1 sekund sampling, og skriv til filnavn. Blokkerer til ferdig kjørt
    subprocess.run(["./adc_sampler", "31250", toFileName], check=True)


    theta = findTheta(toFileName)
    print("theta: ",theta)
