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
        row_count = int(args[0]) # could be used to check if it fits
        col_count = int(args[1])
        args = args[2:]
        args = [args[i:i + col_count] for i in range(0, len(args), col_count)]
        
        # create global variables for the matrices
        if num == 0:
            global a
            a = args
            pass
        elif num == 1:
            global b
            b = args
            pass
        elif num == 2:
            global pi
            pi = args
            pass
        else:
            pass


"""
Transforms a row- to a column vector
"""
def transformRowVector(vec):
    return [[val] for val in vec[0]]
    

"""
in case of vector multiplication add vector first!
"""
def matrixMultiply(mat1, mat2):
    #TODO check if matrices mult-able
    res_mat = [[0 for row in range(len(mat2[0]))] for col in range(len(mat1))]
    for row1_idx, row in enumerate(mat1):
        for col2_idx in range(len(mat2[0])):
            for val_idx in range(len(row)):
                res_mat[row1_idx][col2_idx] += row[val_idx] * mat2[val_idx][col2_idx]
                res_mat[row1_idx][col2_idx] = float("{:.8f}".format(res_mat[row1_idx][col2_idx])) # rounding to two digits

    return res_mat

"""
returns the column index of starting Observation in b-matrix

Unused!!!
"""
def getStartObs(pi, b):
    prob_list = [0 for x in range(len(b[0]))]

    for state_idx, state in enumerate(b):
        for obs_idx, obs in enumerate(state):
            prob_list[obs_idx] += pi[0][state_idx] * obs

    return prob_list.index(max(prob_list))

def main():
    getMatricesFromStdIn()
    next_emission = matrixMultiply(matrixMultiply(pi, a), b)
    
    str_out = "{} {}".format(str(len(next_emission)), str(len(next_emission[0])))
    for val in next_emission[0]:
        str_out =  str_out + " " + str(val)
    print(str_out)
    
if __name__ == "__main__":
    main()