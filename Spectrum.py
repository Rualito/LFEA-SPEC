import math
import PyGnuplot as gp

class Spectrum:

    mpar = 0
    bpar = 0

    Apars = []
    mupars = []
    sigpars = []

    dataArray = []

    def __init__(self, dataArray:list):
        self.dataArray = dataArray

        if len(dataArray) == 2:
            errorArray = []
            for Ncounts in dataArray[1]:
                errorArray.append(math.sqrt(Ncounts))

            self.dataArray.append(errorArray)

    def addGaussianParameters(self, A0:float, mu0:float, sig0:float):
        self.Apars.append(A0)
        self.mupars.append(mu0)
        self.sigpars.append(sig0)

    def setBaseLinePars(self, m0:float, b0:float):
        mpar = m0
        bpar = b0

    def fitData(self, xmin:float, xmax:float):
        # fun right here

        arrX = []
        arrY = []
        arrErrY = []

        for i in range(len(self.dataArray)):
            if xmin <= self.dataArray[0][i] <= xmax:
                arrX.append(self.dataArray[0][i])
                arrY.append(self.dataArray[1][i])
                arrErrY.append(self.dataArray[2][i])
        gp.c("reset")
        gp.c("set grid")
        gp.s([arrX, arrY, arrErrY])

        gp.c("m=%f" % self.mpar)
        gp.c("b=%f" % self.bpar)

        gp.c("f_reta(x)=m*x+b")

        gaussStr = ""
        viaStr = ""
        for i in range(len(self.Apars)):
            gp.c("A%d=%f" % (i, self.Apars[i]))
            gp.c("mu%d=%f" % (i, self.mupars[i]))
            gp.c("sig%d=%f" % (i, self.sigpars[i]))

            gp.c("gauss%d(x)= A%d/(sqrt(2 pi) sig%d) * exp( -0.5*((x-mu%d)/sig%d)**2/))" % (i, i, i, i, i))
            if i != 0:
                gaussStr += "+"
                viaStr += ", "
            gaussStr += "gauss%d(x)"
            viaStr += "A%d, mu%d, sig%d" % (i, i, i)

        gp.c("ftot(x)="+gaussStr+"f_reta(x)")
        gp.c("fit ftot(x) 'tmp.dat' u 1:2:3 yerrors via "+viaStr)
        gp.c("plot 'tmp.dat' u 1:2:3 w yerrorbars t 'Data', ftot(x) t 'fit'")

        # then view file fit.log to get parameters

    def plotData(self, xmin=0, xmax=0):
        gp.c("reset")
        if not xmin==xmax==0:
            gp.c("set xrange [%f:%f]" % (xmin, xmax))

        gp.s(self.dataArray, "plot.dat")
        gp.c("plot 'plot.dat' u 1:2:3 w yerrorbars")