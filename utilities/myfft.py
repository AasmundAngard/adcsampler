import numpy as np
from scipy.fft import fft

# sample_period,data = raspi_import("målinger/speed1-1.bin",2)


# fft = fft(data)



def myFFT(samplePeriod:int,data:np.ndarray,nKanaler:int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    # fft-beregning:
    # -Gi spektrumet
    # -Gi frekvensakse
    # -Gi maks-indeks

    # Lengde av datavektorer og fft
    numSamples = data.shape[0]
    fftLength = numSamples

    completedFFT = []
    if nKanaler == 1:
        completedFFT = fft(data)
    else:
        for n in range(nKanaler):
            nColumnData = data[:, n]
            completedFFT.append(fft(nColumnData))

    completedFFT = np.array(completedFFT).T

    frequencyAxis = np.arange(fftLength)/fftLength * (1/samplePeriod)

    maxIndex = [0]
    # For å finne indeks med høyest verdi
    if nKanaler == 1:
        maxIndex[0] = np.argmax(np.abs(completedFFT))
    else:
        for n in range(len(completedFFT)):
            maxIndex.append(np.argmax(np.abs(completedFFT[n])))

    maxIndex = np.array(maxIndex)

    print("Indeks for maksverdi:")
    for index in maxIndex:
        print(index)

    print("Maks-verdi:")
    for index in maxIndex:
        print(np.abs(completedFFT[maxIndex]))


    return completedFFT, frequencyAxis, maxIndex



