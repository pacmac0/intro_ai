a = [[0.0, 0.8, 0.1, 0.1], 
     [0.1, 0.0, 0.8, 0.1], 
     [0.1, 0.1, 0.0, 0.8],
     [0.8, 0.1, 0.1, 0.0]]

b= [[0.9, 0.1, 0.0, 0.0],
    [0.0, 0.9, 0.1, 0.0],
    [0.0, 0.0, 0.9, 0.1],
    [0.1, 0.0, 0.0, 0.9]]

pi = [1.0, 0.0, 0.0, 0.0] 
obs = [1, 2, 3, 0, 1, 2, 3]

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
    return res_mat

def elemVectorMult(vec1, vec2):
    return [[vec1[e] * vec2[e] for e in range(len(vec1))]]

def observationCol(pos):
    return [b[row][obs[pos]] for row in range(len(b))]



def main():

    v1 = [0.5, 0.0, 0.0, 0.5]
    v2 = [0.1, 0.4, 0.3, 0.9]

    #print(elemVectorMult(v1, v2))
    print(observationCol(0))
    print(matrixMultiply(elemVectorMult(v1, v2), a))
     





if __name__ == "__main__":
    main()
