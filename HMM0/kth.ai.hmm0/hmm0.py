"""
Do:
Matrix multiplications

Given information:

"""

a = [[0.2, 0.5, 0.3, 0.0],
     [0.1, 0.4, 0.4, 0.1],
     [0.2, 0.0, 0.4, 0.4],
     [0.2, 0.3, 0.0, 0.5]]

b = [[1.0, 0.0, 0.0],
     [0.0, 1.0, 0.0],
     [0.0, 0.0, 1.0],
     [0.2, 0.6, 0.2]]

pi = [0.0, 0.0, 0.0, 1.0]


def matrixMultiply(m1, m2):
    #TODO check if matrices mult-able
    if m1.shape[1] != m2.shape[0]:
        return False

    result = [[0 for x in range(len(m1))] for y in range(len(m2[0]))]
    for r in range(len(m1)):
        for c in range(len(m2[0])):
            for k in range(len(m2)):
                result[r][c] += m1[r][k] * m2[k][c]

    return result


def main():
    print("HMM_0")






if __name__ == "__main__":
    main()