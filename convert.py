from os import listdir
from os.path import isfile, join, splitext
from decimal import Decimal

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


def convertAll():
    convertXRYDirToTxt("SPEC\\2D\\2D data files")
    convertXRYDirToTxt("SPEC\\3D\\3D data files\\1seccao")
    convertXRYDirToTxt("SPEC\\3D\\3D data files\\2seccao")
    convertXRYDirToTxt("SPEC\\4D\\4D data files")
    convertXRYDirToTxt("SPEC\\5D\\5D data files")

convertAll()