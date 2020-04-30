import PyGnuplot as gp
import numpy as np

from os import  listdir
from os.path import isfile, join, splitext
from decimal import Decimal

def plotFile(filename, n):
    name, ext = splitext(filename)
    if ext != ".txt":
        print("Wrong file format, returning")
        return

    data = getTxtFileArray(filename, n)

    tempname = "tempfile.dat"

    gp.s(data, tempname)
    gp.c("plot 'tempfile.dat' u 1:2 w lp")

def getTxtFileArray(filename, n):
    file = open(filename, "r")

    lines = file.readlines()
    file.close()

    arr = []
    for i in range(n):
        arr.append([])

    for i in range(len(lines)):
        vals = []
        try:
            strVal = lines[i].split()

            for str in strVal:
                # converting all the strings into values, with the try checking for any incompatible value
                vals.append(float(str))

            for j in range(n):
                # loading the values onto the array
                arr[j].append(vals[j])
        except ValueError:
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

mainDataDir = "SPEC"

def convertXRYDirToTxt(dir):
    xryNames = [f for f in listdir(dir) if isfile(join(dir, f)) and splitext(join(dir, f))[1]=='.xry']

    fullPathNames = [join(dir, name) for name in xryNames]
    [xryToTxt(fullName) for fullName in fullPathNames]

def convertAll():
    convertXRYDirToTxt("SPEC\\2D\\2D data files")
    convertXRYDirToTxt("SPEC\\3D\\3D data files\\1seccao")
    convertXRYDirToTxt("SPEC\\3D\\3D data files\\2seccao")
    convertXRYDirToTxt("SPEC\\4D\\4D data files")
    convertXRYDirToTxt("SPEC\\5D\\5D data files")

def __main__():
    convertAll()


__main__()
