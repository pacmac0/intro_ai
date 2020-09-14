import sys

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
            pass
        elif num == 1:
            row_count = int(args[0]) # could be used to check if it fits
            col_count = int(args[1])
            args = args[2:]
            args = [args[i:i + col_count] for i in range(0, len(args), col_count)]
            global b
            b = args
            pass
        elif num == 2:
            row_count = int(args[0]) # could be used to check if it fits
            col_count = int(args[1])
            args = args[2:]
            args = [args[i:i + col_count] for i in range(0, len(args), col_count)]
            global pi
            pi = args
            pass
        elif num == 3:
            row_count = 1
            col_count = int(args[0]) # could be used to check if it fits
            args = args[1:]
            args = [args[i:i + col_count] for i in range(0, len(args), col_count)]
            global obs
            obs = args
            pass
        else:
            pass

def elemVectorMult(vec1, vec2): # returns [[]]
    return [[vec1[e] * vec2[e] for e in range(len(vec1))]]

def elemMatrixMult(m1, m2):
    return [[m1[row][col] * m2[row][col] for col in range(len(m1[row]))] for row in range(len(m1))]

def elemMatrixAddition(*args): 
    mat = args[0]
    for m in args[1:]:
        mat = [[mat[row][col] + m[row][col] for col in range(len(mat[row]))] for row in range(len(mat))]
    return mat

def getObsColumnByIndex(idx): # returns []
    if idx >= len(b[0]):
        sys.stderr.write("index out of range")
    return [row[idx] for row in b]

"""
in case of vector multiplication add vector first!
"""
def matrixMultiply(mat1, mat2): # returns [[]]
    res_mat = [[0 for row in range(len(mat2[0]))] for col in range(len(mat1))]
    for row1_idx, row in enumerate(mat1):
        for col2_idx in range(len(mat2[0])):
            for val_idx in range(len(row)):
                res_mat[row1_idx][col2_idx] += row[val_idx] * mat2[val_idx][col2_idx]
                res_mat[row1_idx][col2_idx] = float("{:.8f}".format(res_mat[row1_idx][col2_idx])) # rounding to two digits
    return res_mat

def matrixTranspose(m):
    return list(map(list, zip(*m)))

def getNextAlpha(alpha, ob_idx): # returns [[]]
    return elemVectorMult(matrixMultiply(alpha, a)[0], getObsColumnByIndex(ob_idx))

def getNextBeta(beta, ob_idx): # returns [[]]
    return matrixTranspose(matrixMultiply(a, matrixTranspose(elemVectorMult(getObsColumnByIndex(ob_idx), beta[0]))))

def getDiGammas(alpha_seq, beta_seq):
    di_gammas = [0] * (len(obs) - 1)
    for t in range(len(di_gammas)):
        di_gammas[t] = elemMatrixMult(elemMatrixMult(matrixTranspose(alpha_seq[t] * len(a)), a), (elemMatrixMult([getObsColumnByIndex(obs[t + 1])], beta_seq[t + 1])) * len(a))
        di_gammas[t] = [[di_gammas[t][row][col]/sum(alpha_seq[-1][0]) for col in range(len(di_gammas[t][0]))] for row in range(len(di_gammas[t]))]
    return di_gammas

def getProbOfSequence(alpha):
    return sum(alpha[0])

def getGamma(alpha_seq, beta_seq):
    gammas = []
    for t in range(len(alpha_seq)):
        gamma_t = [(alpha_seq[t][0][i] * beta_seq[t][0][i])/ getProbOfSequence(alpha_seq[-1]) for i in range(len(alpha_seq[t][0]))]
        gammas.append(gamma_t)
    return gammas

def getNewA(gammas, di_gammas):
    newA = [[0 for c in a[0]] for r in a]
    for row in range(len(newA)):
        for col in range(len(newA[row])):
            di_gamma = elemMatrixAddition(*di_gammas)
            sum_gamma = []
            for gs in zip(*gammas):
                sum_gamma.append(sum(gs))
            
            newA[row][col] = di_gamma[row][col] / sum_gamma[row]
    return newA



def main():
    """
    getMatricesFromStdIn()
    global obs
    obs = [int(ob) for ob in obs[0]]

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
    pi = [[0.5, 0.0, 0.0, 0.5]]
    global obs
    obs = [3, 0, 0, 2]

    alpha = elemVectorMult(pi[0], getObsColumnByIndex(obs[0])) # inits alpha by element vise multiplication of pi and first observations emission prob.
    alpha_seq = [alpha]
    for ob in obs[1:]:
        alpha = getNextAlpha(alpha, ob)
        alpha_seq.append(alpha)
    
    beta = [[1 for x in pi[0]]]
    beta_seq = [beta]
    for ob in obs[::-1]:
        beta = getNextBeta(beta, ob)
        beta_seq.append(beta)
    beta_seq = beta_seq[::-1]

    print(beta_seq)

    di_gammas = getDiGammas(alpha_seq, beta_seq)
    gammas = getGamma(alpha_seq, beta_seq)
    
    """
    for t,g in enumerate(di_gammas):
        #g = matrixTranspose(g)
        di_g = [sum(row) for row in g]
        print(di_g)
        print(gamma[t])
        print()
    """
    #print(getNewA(gammas, di_gammas))

if __name__ == "__main__":
    main()

