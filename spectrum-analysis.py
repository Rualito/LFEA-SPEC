import PyGnuplot as gp
import numpy as np
import Spectrum

import time

from os import listdir
from os.path import isfile, join, splitext
from decimal import Decimal

def isNaN(num):
    return num != num

def getTxtFileArray(filename, n=0, concat=False):
    file = open(filename, "r")

    lines = file.readlines()
    file.close()

    arr = []
    if n == 0:
        n = len(lines[1].split())

    if not concat:
        for i in range(n):
            arr.append([])
    else:
        arr = [[], []]

    for i in range(len(lines)):
        vals = []
        try:
            strVal = lines[i].split()

            for str0 in strVal:
                # converting all the strings into values, with the try checking for any incompatible value
                vals.append(float(str0))

            if concat:

                med = 0
                cnt = 0
                for j in range(1, n):
                    if not isNaN(vals[j]):
                        med += vals[j]
                        cnt += 1
                if cnt != 0:
                    arr[0].append(vals[0])
                    arr[1].append(med/cnt)
            else:
                for j in range(n):
                    # loading the values onto the array
                    arr[j].append(vals[j])
        except ValueError:
            print("Getting ValueError on entry " + str(i))
            continue

    return arr

def xryToTxt(filename):
    name, ext = splitext(filename)

    if ext != ".xry":
        print("Wrong file extension, returning ", name, ext)
        return False

    fileR = open(filename, "r")

    lines = fileR.readlines()
    fileR.close()

    sAng = Decimal(lines[4].split()[0])
    step = Decimal(lines[4].split()[3])

    sL = 18
    fL = sL+int(lines[17].split()[1])

    fileW = open(name+".txt", "w")

    for i in range(fL-sL):
        fileW.write(str(sAng+i*step) + " " + ' '.join(lines[sL+i].split())+"\n")

    fileW.close()
    return True

def convertXRYDirToTxt(dir):
    xryNames = [f for f in listdir(dir) if isfile(join(dir, f)) and splitext(join(dir, f))[1]=='.xry']

    fullPathNames = [join(dir, name) for name in xryNames]
    [xryToTxt(fullName) for fullName in fullPathNames]

# this is wrong, I cant blindly join files like this
def getDataArray(dir:str, crystal:str):
    # from the file names gets the full data into an array, for display and analysis

    crystalFiles = [join(dir, fname) for fname in listdir(dir) if crystal.casefold() in fname.casefold() and splitext(fname)[1]==".txt" ]

    arrTot = [getTxtFileArray(fname) for fname in crystalFiles]

    dictTotal = dict()
    for fileID in range(len(arrTot)):

        angVec = arrTot[fileID][0]
        rateVec = arrTot[fileID][1:]

        # for each angle on the angle vector, it updated the rate for that point
        # using the average of all the rates
        for i in range(len(angVec)):

            currentRate = 0
            cnt = 0
            for j in range(len(rateVec)):
                rate = rateVec[j][i]
                if not isNaN(rate):
                    cnt += 1
                    currentRate += rate

            if dictTotal.__contains__(angVec[i]):
                currentRate += dictTotal[angVec[i]]
                cnt += 1

            dictTotal[angVec[i]] = currentRate/cnt
    #dictTotal = sorted(dictTotal, key= lambda input: input.)
    data0 = sorted(dictTotal.items(), key=lambda item: item[0])

    data1 = [[], []]

    for i in range(len(data0)):
        data1[0].append(data0[i][0])
        data1[1].append(data0[i][1])

    return data1

def convertAll():
    convertXRYDirToTxt("SPEC\\2D\\2D data files")
    convertXRYDirToTxt("SPEC\\3D\\3D data files\\1seccao")
    convertXRYDirToTxt("SPEC\\3D\\3D data files\\2seccao")
    convertXRYDirToTxt("SPEC\\4D\\4D data files")
    convertXRYDirToTxt("SPEC\\5D\\5D data files")

crystalNames = ["NaCl","Al", "Si", "LiF", "direto", "misterio"]

def printFileParameters(file):
    arr = getTxtFileArray(file, 0, True)

    min0 = arr[0][0]
    max0 = arr[0][-1]
    step = arr[0][1]-min0

    return "\t"+str(min0) + "\t" + str(max0) + "\t" + "%0.2f"%step


crystalFitParameters = \
    {"NaCl": [
        {"m": -500./3, "b": 1800, "A": [200, 800], "mu": [6.4, 7.4], "sig": [0.1, 0.1], "range": [5.5, 8.3]},
        {"m": -500./3, "b": 1800, "A": [10, 20], "mu": [13, 14.5], "sig": [0.1, 0.1], "range": [12, 16]},
        {"m": -500./3, "b": 1800, "A": [10, 20], "mu": [19.5, 22.2], "sig": [0.1, 0.1], "range": [18.6, 23.4]},
        {"m": -500./3, "b": 1800, "A": [1, 2], "mu": [26.6], "sig": [0.1], "range": [25.8, 28]},
        {"m": -5./3, "b": 80, "A": [3], "mu": [30.3], "sig": [0.1], "range": [28, 31]}
    ],
    "Al": [
        {"m": -500./3, "b": 1800, "A": [20, 50], "mu": [8.5, 9.9], "sig": [0.2, 0.2], "range": [7, 11.6]},
        {"m": -500./3, "b": 1800, "A": [5, 32], "mu": [18, 20.3], "sig": [0.2, 0.2], "range": [16.6, 21.5]},
        {"m": -500./3, "b": 1800, "A": [1], "mu": [27], "sig": [0.1], "range": [25.6, 28.5]},
        {"m": -500./3, "b": 1800, "A": [1], "mu": [31], "sig": [0.1], "range": [29.6, 32.5]}],
    "Si": [
        {"m": -500./3, "b": 1800, "A": [200, 500], "mu": [13.3, 15], "sig": [0.2, 0.2], "range": [12, 16.2]},
        {"m": -500./3, "b": 1800, "A": [3, 5], "mu": [27.5, 31.2], "sig": [0.2, 0.2], "range": [26.5, 33]},
        {"m": -5./3, "b": 18, "A": [0.5], "mu": [44.2], "sig": [0.1], "range": [42.9, 45.5]},
        {"m": -5./3, "b": 18, "A": [1], "mu": [51.7], "sig": [0.1], "range": [50.5, 53]}],
    "LiF": [
        {"m": -500./3, "b": 1800, "A": [200, 500], "mu": [8.9, 10], "sig": [0.2, 0.2], "range":[8, 11]},
        {"m": -500./3, "b": 1800, "A": [30], "mu": [18.1], "sig": [0.2], "range": [17, 19.3]},
        {"m": -500./3, "b": 1800, "A": [60], "mu": [20.5], "sig": [0.2], "range":[19.5, 21.5]},
        {"m": -500./3, "b": 1800, "A": [5], "mu": [28], "sig": [0.1], "range":[27, 29.5]},
        {"m": -5./3, "b": 1800, "A": [10], "mu": [31.7], "sig": [0.1], "range":[30.5, 33]}]
    }


def customizeGraph(type=""):
    gp.c("reset")
    gp.c("set grid")

    gp.c("set termoption enhanced")

    gp.c("set xlabel '{/Symbol b} [º]'")
    gp.c("set ylabel 'R'")

    if type == "log":
        gp.c("set logscale y")


def crystalFit(spec: Spectrum, crystal: str, index: int, fname: str):
    specificPars = crystalFitParameters[crystal][index]
    spec.setBaseLinePars(specificPars["m"],  specificPars["b"])

    for i in range(len(specificPars["mu"])):
        spec.addGaussianParameters(specificPars["A"][i], specificPars["mu"][i], specificPars["sig"][i])

    customizeGraph()
    return spec.fitData(specificPars["range"][0], specificPars["range"][1], fname)

currentCrystal = "NaCl"
index = 0

crystalFileNames = {"NaCl": "SPEC\\4D\\4D data files\\NaCl_2.txt",
                    "Al":"SPEC\\4D\\4D data files\\Al.txt",
                    "Si": "SPEC\\4D\\4D data files\\Si.txt",
                    "LiF": "SPEC\\4D\\4D data files\\LiF.txt"}

def __main__():
    convertAll()

    spec = Spectrum.Spectrum(getTxtFileArray(crystalFileNames[currentCrystal], 0, True))

    cpars = crystalFitParameters[currentCrystal][index]
    print(cpars)

    fitpars = crystalFit(spec, currentCrystal, index, currentCrystal+" fit "+str(cpars["range"][0]) + " - " + str(cpars["range"][1]) + ".pdf")

    print(currentCrystal+" fit "+str(cpars["range"][0]) + " - " + str(cpars["range"][1]) + ".pdf")
    print("chi2\t", fitpars[0])
    for i in range(len(fitpars[1])):
        print(fitpars[1][i], "\t", fitpars[2][i], "\t", fitpars[3][i])

def __fitClassExample__():
    data = getTxtFileArray("SPEC\\2D\\2D data files\\05-NaCl1-4ordema-01-25s.txt", 0, True)
    spec = Spectrum.Spectrum(data)

    spec.setBaseLinePars(-500. / 3, 1800)
    spec.addGaussianParameters(100, 30, 0.1)


    customizeGraph()
    fitpars = spec.fitData(30, 31, "test.pdf")

    print("chi2: ", fitpars[0])
    for i in range(len(fitpars[1])):
        print(fitpars[1][i], ": ", fitpars[2][i], " +/-", fitpars[3][i])


def plotFile(filename: str, xmin=0, xmax=0):
    customizeGraph()
    Spectrum.Spectrum(getTxtFileArray(filename)).plotData(xmin, xmax)


def __plotDataExample__():
    # crystalFileNames[currentCrystal]
    data = getTxtFileArray("SPEC\\2D\\2D data files\\05-NaCl1-4ordema-01-25s.txt", 0, True)

    spec = Spectrum.Spectrum(data)
    cpars = crystalFitParameters[currentCrystal][index]

    customizeGraph()
    spec.plotData()


# __main__()
# __plotDataExample__()
__fitClassExample__()



def __fitExample__():

    customizeGraph()
    gp.s([ [1,2,3], [4, 7, 13], [1,1,1]])
    gp.c("m = 1")
    gp.c("b = 1")
    gp.c("f(x) = m*x+b")
    gp.c("fit f(x) 'tmp.dat' u 1:2:3 yerrors via m,b")
    gp.c("set xrange [0:4]")
    gp.c("plot 'tmp.dat' u 1:2:3 w yerrorbars, f(x)")


#
# crystal = crystalNames[5]
# directory = "SPEC\\4D\\4D data files"
# crystalFiles = [join(directory, fname) for fname in listdir(directory)
#                 if crystal.casefold() in fname.casefold() and splitext(fname)[1] == ".txt"]
#
# crystalFilesname = [fname for fname in listdir(directory)
#                 if crystal.casefold() in fname.casefold() and splitext(fname)[1] == ".txt"]
# for i in range(len(crystalFiles)):
#     print(crystalFilesname[i], printFileParameters(crystalFiles[i]))