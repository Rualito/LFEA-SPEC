import Spectrum
from os import listdir
from os.path import isfile, join, splitext
from decimal import Decimal
import PyGnuplot as gp
import time

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

def customizeGraph(type=""):
    gp.c("reset")
    gp.c("set grid")

    gp.c("set termoption enhanced")

    gp.c("set xlabel '{/Symbol b} [º]'")
    gp.c("set ylabel 'R [1/s]'")

    if type == "log":
        gp.c("set logscale y")

def plotFile(filename: str, xmin=0, xmax=0, type=""):
    customizeGraph(type)
    Spectrum.Spectrum(getTxtFileArray(filename, 0, True)).plotData(xmin, xmax)


directory = "SPEC\\2D\\2D data files"


files = [join(directory, f) for f in listdir(directory)
         if isfile(join(directory, f)) and splitext(join(directory, f))[1] == '.txt']


# for i in range(len(files)):
#     print(files[i])
#     plotFile(files[i])
#     input("press enter to continue")


fitParameters = { "02-NaCl1-01-5s.txt": [{"A": [1000, 2000],"mu": [6.5, 7.5], "range": [5.5, 8.5], "m": -200, "b": 2000},
                                         {"A": [200, 600],"mu": [13, 14.5], "range": [12, 16], "m": -20, "b": 200}],
                  "03-NaCl1-3ordem-01-10s.txt": [{"A": [30],"mu": [19.5], "range": [19, 20.1], "m": -2, "b": 20},
                                                 {"A": [30],"mu": [22.1], "range": [21.5, 23], "m": -2, "b": 20}],
                  "04-NaCl1-4ordemb-01-25s.txt": [{"A": [10],"mu": [26.6], "range": [26, 27], "m": -2, "b": 20}],
                  "05-NaCl1-4ordema-01-25s.txt": [{"A": [5],"mu": [30.2], "range": [30, 31], "m": -2, "b": 20}]}


def fitFile(fname, index=0):
    filename = splitext(fname)[0]

    fitpars = fitParameters[fname][index]
    spec = Spectrum.Spectrum(getTxtFileArray("SPEC\\2D\\2D data files\\" + fname, 0, True))

    for i in range(len(fitpars["A"])):
        spec.addGaussianParameters(fitpars["A"][i], fitpars["mu"][i], 0.2)
    spec.setBaseLinePars(fitpars["m"],fitpars["b"])

    customizeGraph()
    afterfitpars = spec.fitData(fitpars["range"][0], fitpars["range"][1], filename + " " + str(fitpars["range"][0]) + " - "+str(fitpars["range"][1]) + ".pdf")

    print(filename + " " + str(fitpars["range"][0]) + " - "+str(fitpars["range"][1]) + ".pdf")
    print("chi2\t", afterfitpars[0])
    for i in range(len(afterfitpars[1])):
        print(afterfitpars[1][i], "\t", afterfitpars[2][i], "\t", afterfitpars[3][i])


fitFile("02-NaCl1-01-5s.txt")

