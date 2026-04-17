import subprocess
import numpy as np
import os

from utilities.raspi_import import raspi_import
from utilities.doppler import dopplershiftToSpeed
from utilities.myfft import myFFT


# Kode for måling av radar
# Formål: Å gi standardiserte filnavn automatisk
# Kjører 2 ADC-er tilkoblet PI og lagrer resultatet
# Resultat: 2 tidsserier med reell (I-kanal) og 
# imaginær (Q-kanal) radardata.

# Spesifikt til forsøket:
# Velg tre farter mot radar, og en fra radar.
# Gjennomfør fire målinger med radar på hver fart
# speed1 - speed3 er mot radar
# speed4 er fra radar


# Måletid i sekund
measurementDuration = 2
MEASUREMENT_FREQUENCY = 31250





while True:
    speedToTest = input("Hvilken fart (1-4) vil du teste: ")

    if speedToTest in ["q","quit","close","end"]:
        break

    # Finn ubrukt filnavn for målinger
    toFileName =None
    tempName = "speed"+str(speedToTest)+".bin"

    # Finn ledig fil-index for farten speedToTest
    for i in range(10):
        tempName = "speed"+str(speedToTest)+"_"+str(i)+".bin"
        if not (os.path.isfile(tempName)):
            toFileName = tempName
            break
        
    del tempName

    if toFileName == None:
        break

    # Kjør adc_sampler med 10 sekund sampling, og skriv til filnavn. Blokkerer til ferdig kjørt
    subprocess.run(["./adc_sampler", str(MEASUREMENT_FREQUENCY*measurementDuration), toFileName], check=True)

    samplePeriod, data = raspi_import(toFileName,2)
    fft, frequency, maxIndex = myFFT(samplePeriod,data[0]+1j*data[1],1)

    speed = dopplershiftToSpeed(frequency[maxIndex])
    print("fart: ",speed)