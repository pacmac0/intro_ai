import sys
import math
import random

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

def getObservationsFromFile():
    for line in sys.stdin:
        line = line.replace('\n','')
        args = [int(val) for val in line.strip().split(" ")]
        global t_total
        t_total = args[0]
        global obs
        obs = args[1:]
    
# re-estimate pi
def reestimatePi():
    pi = gamma_t_list[0]

# re-estimate A
def reestimateA():
    for i in range(n):
        denominator = 0
        for t in range(t_total-1):
            denominator += gamma_t_list[t][i]
        for j in range(n):
            numerator = 0
            for t in range(t_total-1):
                numerator += di_gamma_t_list[t][i][j]
            a[i][j] = numerator/ (denominator + 0.001)

# re-estimate B
def reestimateB():
    for i in range(n):
        denominator = 0
        for t in range(t_total):
            denominator += gamma_t_list[t][i]
        for j in range(m):
            numerator = 0
            for t in range(t_total):
                if j == obs[t]:
                    numerator += gamma_t_list[t][i]
            
            b[i][j] = numerator / (denominator + 0.001)

def printResults():
    str_out_a = str(len(a)) + ' ' +  str(len(a[0])) + ' '
    for row in a:
        for val in row:
            str_out_a = str_out_a + str(round(val, 6)) + ' '
    str_out_a = str_out_a.strip()
    print(str_out_a)

    str_out_b = str(len(b)) + ' ' +  str(len(b[0])) + ' '
    for row in b:
        for val in row:
            str_out_b = str_out_b + str(round(val, 6)) + ' '
    str_out_b = str_out_b.strip()
    print(str_out_b)
    print(pi)

def initModel():
    epsilon = 0.05
    global a
    a = [[random.uniform((1 / n) - epsilon, (1 / n) + epsilon) for s in range(n)] for s in range(n)]
    for row in a:
        if sum(row) != 1.0:
            row[-1] = 1 - sum(row[:-1])

    global b
    b = [[random.uniform((1 / m) - epsilon, (1 / m) + epsilon) for s in range(m)] for s in range(n)]
    for row in b:
        if sum(row) != 1.0:
            row[-1] = 1 - sum(row[:-1])

    global pi
    pi = [random.uniform((1 / n) - epsilon, (1 / n) + epsilon) for s in range(n)]
    if sum(pi) != 1.0:
        pi[-1] = 1 - sum(pi[:-1])

def initModelUniform():
    global a
    a = [[1/n for s in range(n)] for s in range(n)]
    global b
    #b = [[1/m for s in range(m)] for s in range(n)]
    epsilon = 0.05
    b = [[random.uniform((1 / m) - epsilon, (1 / m) + epsilon) for s in range(m)] for s in range(n)]
    for row in b:
        if sum(row) != 1.0:
            row[-1] = 1 - sum(row[:-1])
    global pi
    pi = [1/n for s in range(n)]

def initModelDiagonal():
    global a
    a = [[1,0,0],
         [0,1,0],
         [0,0,1]]
    global b
    epsilon = 0.05
    b = [[random.uniform((1 / m) - epsilon, (1 / m) + epsilon) for s in range(m)] for s in range(n)]
    for row in b:
        if sum(row) != 1.0:
            row[-1] = 1 - sum(row[:-1])
    global pi
    pi = [0,0,1]

def main():
    """
    global a
    a = [[0.54, 0.26, 0.20], 
         [0.19, 0.53, 0.28], 
         [0.22, 0.18, 0.6]]
    global b
    b= [[0.50, 0.20, 0.11, 0.19],
        [0.22, 0.28, 0.23, 0.27],
        [0.19, 0.21, 0.15, 0.45]]
    global pi
    pi = [0.3, 0.2, 0.5]
    """
    # similar init
    eps = 1e-4
    global a
    # a = [[0.7 * random.uniform(1-eps, 1+eps), 0.05 * random.uniform(max(0, 1-eps), 1+eps), 0.25 * random.uniform(1-eps, 1+eps)],
    #      [0.1 * random.uniform(1-eps, 1+eps), 0.8 * random.uniform(1-eps, 1+eps), 0.1 * random.uniform(1-eps, 1+eps)],
    #      [0.2 * random.uniform(1-eps, 1+eps), 0.3 * random.uniform(1-eps, 1+eps), 0.5 * random.uniform(1-eps, 1+eps)]]
    a = [[0.69, 0.04, 0.24], [0.11, 0.82, 0.09], [0.22, 0.29, 0.51]]
    # for i in range(len(a)):
    #     a[i] = [a[i][j] / sum(a[i]) for j in range(len(a[i]))]
    global b
    b = [[0.71, 0.21, 0.11, 0.01], [0.09, 0.42, 0.29, 0.21], [0.01, 0.12, 0.19, 0.71]]
    # b= [[0.7 * random.uniform(1-eps, 1+eps), 0.2 * random.uniform(1-eps, 1+eps), 0.1 * random.uniform(1-eps, 1+eps), random.uniform(0, eps)],
    #     [0.1 * random.uniform(1-eps, 1+eps), 0.4 * random.uniform(1-eps, 1+eps), 0.3 * random.uniform(1-eps, 1+eps), 0.2 * random.uniform(1-eps, 1+eps)],
    #     [random.uniform(0, eps), 0.1 * random.uniform(1-eps, 1+eps), 0.2 * random.uniform(1-eps, 1+eps), 0.7 * random.uniform(1-eps, 1+eps)]]
    # for i in range(len(b)):
    #     b[i] = [b[i][j] / sum(b[i]) for j in range(len(b[i]))]
    global pi
    # pi = [random.uniform(1-eps, 1), random.uniform(0, eps), random.uniform(0, eps)]
    # pi = [pi[j] / sum(pi) for j in range(len(pi))]
    pi = [0.98, 0.01, 0.01]
    global n
    n = 3
    global m
    m = 4
    print("a")
    print(a)
    print("b")
    print(b)
    print('pi')
    print(pi)
    
    #initModel()
    #initModelUniform()
    #initModelDiagonal()
    getObservationsFromFile()
    
    #getMatricesFromStdIn()
    
    # iterating
    max_interations =1000
    iterations_done = 0
    oldLogProb = -float('inf')
    
    while True:
        
        global cts
        cts = [0.0 for t in range(t_total)]
        c0 = 0.0
        # init alpha0
        alpha_t_list = []
        alpha_0 = [0.0 for s in range(n)]
        for i in range(n):
            alpha_0[i] = pi[i] * [row[obs[0]] for row in b][i]
            c0 += alpha_0[i]
        # scale
        cts[0] = 1/c0
        alpha_0 = [p * cts[0] for p in alpha_0]
        alpha_t_list.append(alpha_0)

        # get alpha_t's
        for t in range(1, t_total):
            new_alpha_t = [0.0 for s in range(n)]
            for i in range(n):
                for j in range(n):
                    new_alpha_t[i] += alpha_t_list[-1][j] * a[j][i]
                new_alpha_t[i] *= [row[obs[t]] for row in b][i]
            cts[t] = 1/sum(new_alpha_t)
            # scaleing
            new_alpha_t = [p * cts[t] for p in new_alpha_t]
            alpha_t_list.append(new_alpha_t)
        
        # beta
        global beta_t_list
        beta_t_list = [[0.0 for v in range(n)] for t in range(t_total)]
        beta_t_list[t_total-1] = [cts[-1] for v in range(n)]
        
        for t in range(t_total-2, -1, -1):
            for i in range(n):
                for j in range(n):
                    beta_t_list[t][i] += a[i][j] *  [row[obs[t+1]] for row in b][j] * beta_t_list[t+1][j]
                # scale
                beta_t_list[t][i] *= cts[t]
        
        # di_gamma and gamma for scalled alpha, beta
        global di_gamma_t_list
        di_gamma_t_list = []
        global gamma_t_list # [[[]]]
        gamma_t_list = [] # [[]]
        for t in range(t_total-1):
            gamma_t = [0.0 for v in range(n)]
            di_gamma_t = [[0.0 for c in range(n)] for r in range(n)]
            for i in range(n):
                for j in range(n):
                    di_gamma_t[i][j] = alpha_t_list[t][i] * a[i][j] * [row[obs[t+1]] for row in b][j] * beta_t_list[t+1][j]
                    gamma_t[i] += di_gamma_t[i][j]
            gamma_t_list.append(gamma_t)
            di_gamma_t_list.append(di_gamma_t)
        # special case gamma_T-1(i)
        gamma_t_list.append(alpha_t_list[-1])

        # re etimate the HMMs lambda 
        reestimatePi()
        reestimateA()
        reestimateB()

        # logarithmic probability
        logProb = 0.0
        for i in range(t_total):
            logProb += math.log(cts[i])
        logProb = -logProb


        iterations_done += 1
        if iterations_done >= max_interations or logProb < oldLogProb:
            break
        oldLogProb = logProb

        
        
    # end while
    
    #print('The training converged after {} iterations.'.format(iterations_done))
    print(iterations_done)
    printResults()
    print()

if __name__ == "__main__":
    main()
