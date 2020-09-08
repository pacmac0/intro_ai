"""
Do:
Matrix multiplications

Given information:
From pi we know, at t=0 we arew in state "D"
"""
import sys
from decimal import Decimal

def getMatricesFromStdIn():
    for num, line in enumerate(sys.stdin):
        line = line.replace('\n','')
        args = [float(val) for val in line.split(" ")]
        row_count = int(args[1])
        col_count = int(args[0])
        args = args[2:]
        print(args)

        print([[args[cn] for cn in range(col_count)] for rn in range(row_count)])


        if num == 0:
            #print("a")
            pass
        elif num == 1:
            #print("b")
            pass
        elif num == 2:
            #print("pi")
            pass
        else:
            pass


        #print(args)

a = [[0.2, 0.5, 0.3, 0.0],
     [0.1, 0.4, 0.4, 0.1],
     [0.2, 0.0, 0.4, 0.4],
     [0.2, 0.3, 0.0, 0.5]]

b = [[1.0, 0.0, 0.0],
     [0.0, 1.0, 0.0],
     [0.0, 0.0, 1.0],
     [0.2, 0.6, 0.2]]

pi = [[0.0, 0.0, 0.0, 1.0]]

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

def main():
    getMatricesFromStdIn()
    next_emission = matrixMultiply(matrixMultiply(pi, a), b)
    
    str_out = "{} {}".format(str(len(next_emission)), str(len(next_emission[0])))
    for val in next_emission[0]:
        str_out =  str_out + " " + str(val)
    print(str_out)

if __name__ == "__main__":
    main()
