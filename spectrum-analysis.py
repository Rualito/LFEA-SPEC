import subprocess

# https://stackoverflow.com/questions/2161932/calling-gnuplot-from-python#2161965

def plotFile(filename):
    name, ext = filename.split(",", 2)
    if ext != "txt":
        print("Wrong file format, returning")
        return

    data = getTxtFileArray(filename)

    tempname = "tempfile.dat"

    generateTempGnuplotFile(tempname, data)




def getTxtFileArray(filename):
    # assuming first line is useless
    file = open(filename, "r")

    lines = file.readlines()
    file.close()

    arr = []

    for i in range(1, len(lines)):
        arr.append(lines[i].split())

    return arr

def generateTempGnuplotFile(filename, array):
    file = open(filename, "w")

    for e in array:
        file.write(' '.join(e))

    file.close()

def xryToTxt(filename):
    pass


print(' '.join(str(e) for e in [1, 2, 3]))
