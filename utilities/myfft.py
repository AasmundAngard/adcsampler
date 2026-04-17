import numpy as np
from raspi_import import raspi_import
from scipy.fft import fft

sample_period,data = raspi_import("målinger/speed1-1.bin",2)


fft = fft(data)



def myFFT(samplePeriod:int,data:np.ndarray,nKanaler:int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    # fft-beregning:
    # -Gi spektrumet
    # -Gi frekvensakse
    # -Gi maks-indeks

    # Lengde av datavektorer og fft
    numSamples = data.shape[0]
    fftLength = numSamples

    completedFFT = np.ndarray()
    for n in range(nKanaler):
        nColumnData = data[:,n]
        completedFFT = np.append(completedFFT,fft(nColumnData))

    frequencyAxis = np.arange(fftLength)/fftLength * (1/samplePeriod)

    maxIndex = np.ndarray()
    # For å finne indeks med høyest verdi
    for n in range(len(completedFFT)):
        maxIndex[n] = np.argmax(np.abs(completedFFT[n]))


    print("Indeks for maksverdi:")
    for index in maxIndex:
        print(index)

    print("Maks-verdi:")
    for index in maxIndex:
        print(np.abs(completedFFT[maxIndex]))


    return completedFFT, frequencyAxis, maxIndex



