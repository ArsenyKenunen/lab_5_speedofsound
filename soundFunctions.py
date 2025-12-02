import numpy as np

def speedOfSound(temperature, h2oX, co2Max):
    T = 273.15 + temperature
    R = 8.314

    airMu = 28.97
    airCp = 1.0036
    airCv = 0.7166

    h2oMu = 18.01
    h2oCp = 1.863
    h2oCv = 1.403

    co2Mu = 44.01
    co2Cp = 0.838
    co2Cv = 0.649

    co2X = np.linspace(0, co2Max / 100, 100)
    airX = 1 - h2oX - co2X

    Cp = airMu * airCp * airX + h2oMu * h2oCp * h2oX + co2Mu * co2Cp * co2X
    Cv = airMu * airCv * airX + h2oMu * h2oCv * h2oX + co2Mu * co2Cv * co2X

    gamma = Cp / Cv
    mu = airMu * airX + h2oMu * h2oX + co2Mu * co2X

    soundSpeed = np.sqrt(gamma * R * T / (mu / 1000))

    return co2X * 100, soundSpeed