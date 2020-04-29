import PyGnuplot as gp
import numpy as np

def plotFile(filename):
    name, ext = filename.split(",", 2)
    if ext != "txt":
        print("Wrong file format, returning")
        return

    data = getTxtFileArray(filename)

    tempname = "tempfile.dat"

    gp.s(data, tempname)


def getTxtFileArray(filename, n):
    # assuming first line is useless
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

            for j in range(len(vals)):
                #loading the values onto the array
                arr[j].append(vals[j])
        except ValueError:
            continue


    return arr

def xryToTxt(filename):
    pass

print(' '.join(str(e) for e in [1, 2, 3]))


arrX = []
arrY = []
for i in range(5):
    arrX.append(i)
    arrY.append(i**2)

gp.s([arrX, arrY], "temp.dat")
#gp.c('plot "temp.dat"')


print(int("3.1"))