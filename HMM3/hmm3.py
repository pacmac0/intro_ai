import sys
import math

"""
we always assume the input is given correct and does not has to be checked specifically
"""
def getMatricesFromStdIn():
    for num, line in enumerate(sys.stdin):
        line = line.replace('\n','')
        if line[-1] == " ":
            line = line[:-1]
        args = [float(val) for val in line.split(" ")]
        
        # create global variables for the matrices
        if num == 0:
            row_count = int(args[0]) # could be used to check if it fits
            col_count = int(args[1])
            args = args[2:]
            args = [args[i:i + col_count] for i in range(0, len(args), col_count)]
            global a
            a = args
            global n
            n = len(a)
            pass
        elif num == 1:
            row_count = int(args[0]) # could be used to check if it fits
            col_count = int(args[1])
            args = args[2:]
            args = [args[i:i + col_count] for i in range(0, len(args), col_count)]
            global b
            b = args
            global m
            m = len(b[0])
            pass
        elif num == 2:
            row_count = int(args[0]) # could be used to check if it fits
            col_count = int(args[1])
            args = args[2:]
            global pi
            pi = [val for val in args]
            pass
        elif num == 3:
            row_count = 1
            col_count = int(args[0]) # could be used to check if it fits
            args = args[1:]
            global obs
            obs = [int(val) for val in args]
            global t_total
            t_total = len(obs)
            pass
        else:
            pass

def elemVectorMult(v1, v2): # returns []
    return [v1[e] * v2[e] for e in range(len(v1))]

def matrixMultiply(mat1, mat2): # returns [[]]
    res_mat = [[0 for row in range(len(mat2[0]))] for col in range(len(mat1))]
    for row1_idx, row in enumerate(mat1):
        for col2_idx in range(len(mat2[0])):
            for val_idx in range(len(row)):
                res_mat[row1_idx][col2_idx] += row[val_idx] * mat2[val_idx][col2_idx]
                res_mat[row1_idx][col2_idx] = float("{:.20f}".format(res_mat[row1_idx][col2_idx])) # rounding to two digits
    return res_mat

def getObsColumnByIndex(idx): # returns []
    if idx >= len(b[0]):
        sys.stderr.write("index out of range")
    return [row[idx] for row in b]

""" Compromised !!!!!!!!!!!!!!!
def getNextAlpha(alpha_t, new_t):
    new_alpha_t = elemVectorMult(matrixMultiply([alpha_t], a)[0], getObsColumnByIndex(obs[new_t]))
    cts[new_t] = 1/sum(alpha_t)
    new_alpha_t = [alpha_ti * cts[new_t] for alpha_ti in new_alpha_t]
    return new_alpha_t


def getNextBeta(beta_t1, new_t):

    new_beta_t = [0.0 for x in range(n)]
    observation = getObsColumnByIndex(obs[new_t+1])
    for i in range(n-1):
        for j in range(n-1):
            new_beta_t[i] =+ a[i][j] * observation[j] * beta_t1[j]
        # scale
        new_beta_t[i] = cts[new_t] * new_beta_t[i]
    return new_beta_t
"""
def getGammas(t):
    observation = getObsColumnByIndex(obs[t])
    gamma_t = [0.0 for v in range(n)]
    di_gamma_t = [[0.0 for c in range(n)] for r in range(n)]
    for i in range(n):
        for j in range(n):
            di_gamma_t[i][j] = alpha_t_list[t][i] * a[i][j] * observation[j] * beta_t_list[t][j]
            gamma_t[i] =+ di_gamma_t[i][j]
    return gamma_t, di_gamma_t

# re-estimate pi
def reestimatePi():
    pi = gamma_t_list[0]

# re-estimate A
def reestimateA():
    for i in range(n-1):
        denominator = 0
        for t in range(t_total-2):
            denominator =+ gamma_t_list[t][i]
        for j in range(n-1):
            numerator = 0
            for t in range(t_total-2):
                numerator =+ di_gamma_t_list[t][i][j]
            a[i][j] = numerator/denominator

# re-estimate B
def reestimateB():
    for i in range(n-1):
        denominator = 0
        for t in range(t_total-1):
            denominator =+ gamma_t_list[t][i]
        for j in range(m-1):
            numerator = 0
            for t in range(t_total-1):
                if j == obs[t]:
                    numerator =+ gamma_t_list[t][i]
            b[i][j] = numerator / denominator

def main():
    """
    global a
    a = [[0.6, 0.1, 0.1, 0.2], 
         [0.0, 0.3, 0.2, 0.5], 
         [0.8, 0.1, 0.0, 0.1],
         [0.2, 0.0, 0.1, 0.7]]
    global b
    b= [[0.6, 0.2, 0.1, 0.1],
        [0.1, 0.4, 0.1, 0.4],
        [0.0, 0.0, 0.7, 0.3],
        [0.0, 0.0, 0.1, 0.9]]
    global pi
    pi = [0.5, 0.0, 0.0, 0.5]
    global obs
    obs = [3, 0, 0, 2]
    global n
    n = 4
    global m
    m = 4
    global t_total
    t_total = 4
    """
    getMatricesFromStdIn()
    
    # iterating
    max_interations = 30
    iterations_done = 0
    logProb = 0.0
    oldLogProb = -float('inf')
    
    # init alpha and beta (scaled)
    alpha_t = elemVectorMult(pi, getObsColumnByIndex(obs[0]))
    # scaling
    global cts
    cts = [0.0 for t in range(t_total)]
    cts[0] = 1/sum(alpha_t)
    alpha_t = [alpha_t_item * cts[0] for alpha_t_item in alpha_t]
    
    global alpha_t_list
    alpha_t_list = [alpha_t]
    for t in range(1, t_total):
        alpha_t = elemVectorMult(matrixMultiply([alpha_t], a)[0], getObsColumnByIndex(obs[t]))
        cts[t] = 1/sum(alpha_t)
        alpha_t = [alpha_ti * cts[t] for alpha_ti in alpha_t]
        alpha_t_list.append(alpha_t)

    # beta
    global beta_t_list
    beta_t_list = [[cts[-1] for t in range(n)]]

    for t in range(t_total-2, -1, -1):
        new_beta_t = [0.0 for x in range(n)]
        observation = getObsColumnByIndex(obs[t+1])
        for i in range(n):
            for j in range(n):
                new_beta_t[i] += a[i][j] * observation[j] * beta_t_list[-1][j]
            # scale
            new_beta_t[i] *= cts[t]
        beta_t_list.append(new_beta_t)
    
    # di_gamma and gamma for scalled alpha, beta
    global di_gamma_t_list
    di_gamma_t_list = []
    global gamma_t_list # [[[]]]
    gamma_t_list = [] # [[]]
    for t in range(t_total-2):
        gamma_t, di_gamma_t = getGammas(t)
        gamma_t_list.append(gamma_t)
        di_gamma_t_list.append(di_gamma_t)
    # special case gamma_T-1(i)
    gamma_t_list.append(alpha_t_list[t_total-2])

    # re etimate the HMM lambda 
    reestimatePi()
    reestimateB()
    reestimateA()
    
    # logarithmic probability of O
    logProb = 0.0
    for i in range(t_total-1):
        # TODO log of 0 not possible, maybe exchange all zeros in cts with other value
        logProb =+ math.log(cts[i])
    logProb = -logProb
     

if __name__ == "__main__":
    main()

