import numpy as np
import time

class NoResult(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        
def solve_eqn(numOfNotes, score, bad, pa):

    def scoreA(numOfNotes: int):
        return np.array([1e6/numOfNotes*np.array([1,0.65]),[1,1]])
    def scoreB(score:int, pa:int, bad:int):
        return np.array([score,pa-bad]) 
    
    now = time.time()
    while(True):
        A = scoreA(numOfNotes)
        B = scoreB(score,pa,bad)
        X = np.linalg.inv(A).dot(B)
        Xa = np.around(X)
        if(np.sum((Xa-X)**2) <= 1e-3 and min(Xa)>=0 and sum(abs(Xa))<=pa):
            res = np.append(Xa,bad)
            #print(res)
            break
        else:
            bad = bad + 1
            if(bad>pa):
                raise NoResult
    #print(time.time()-now)

    return res

def solve_pre(numOfNotes, score, bad, pa):
    now = time.time()
    while(True):
        tmp = score*numOfNotes/1e6
        perfect = (tmp - 0.65 * (pa - bad)) / 0.35
        good = (pa - tmp -bad) / 0.35

        X = np.array([perfect,good,bad])
        Xa = np.around(X)
        if(np.sum((Xa-X)**2) <= 1e-3 and min(Xa)>=0 and sum(abs(Xa))<=pa):
            #print(Xa)
            break
        else:
            bad = bad + 1
            if(bad>pa or good<0):
                raise NoResult
    #print(time.time()-now)

    return Xa