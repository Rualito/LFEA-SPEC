import PyGnuplot as gp
import numpy as np

from os import listdir
from os.path import isfile, join, splitext
from decimal import Decimal

def isNaN(num):
    return num != num

def plotFile(filename, n):
    name, ext = splitext(filename)
    if ext != ".txt":
        print("Wrong file format, returning")
        return

    data = getTxtFileArray(filename, n)

    tempname = "tempfile.dat"

    gp.s(data, tempname)
    gp.c("plot 'tempfile.dat' u 1:2 w lp")

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
                arr[0].append(vals[0])
                arr[1].append(vals[1])
                for j in range(1, n):
                    arr[1][-1] += vals[j]
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

def __main__():
    # convertAll()

    # data = getDataArray("SPEC\\2D\\2D data files", "NaCl")
    # gp.s(data)

    # gp.c("plot 'tmp.dat' u 1:2")

    pass


crystal = crystalNames[5]
directory = "SPEC\\4D\\4D data files"
crystalFiles = [join(directory, fname) for fname in listdir(directory)
                if crystal.casefold() in fname.casefold() and splitext(fname)[1] == ".txt"]

crystalFilesname = [fname for fname in listdir(directory)
                if crystal.casefold() in fname.casefold() and splitext(fname)[1] == ".txt"]
for i in range(len(crystalFiles)):
    print(crystalFilesname[i], printFileParameters(crystalFiles[i]))
# __main__()
