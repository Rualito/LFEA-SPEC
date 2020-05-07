def potres(mu_p, sig_p):
    return mu_p/sig_p

def fsr(alist, mulist):
    #lista de a e lista de valores de mu, para um dado cristal.   
    alistcp = alist
    fsrmu = []
    
    sort(alistcp)
    for i in range(2):
        fsrmu[i]=mulist[alist.index(alistcp[i])]
    sort(fsrmu[i])
    return [fsrmu[1]-fsrmu[0], fsrmu[1]-fsrmu[0]]
