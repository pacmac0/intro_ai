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

def elemVectorMult(vec1, vec2):
    return [[vec1[e] * vec2[e] for e in range(len(vec1))]]

def getObsColumnByIndex(idx):
    if idx >= len(b[0]):
        sys.stderr.write("index out of range")
    return [row[idx] for row in b]

"""
in case of vector multiplication add vector first!
"""
def getViterbiDelta(prev_delta, ob):
    res_vec = [[0 for col in range(len(prev_delta[0]))]]
    obsCol = getObsColumnByIndex(ob)

    for col in range(len(a[0])):
        max = 0
        for row in range(len(a)):
            val = a[row][col] * prev_delta[0][row] * obsCol[col]
            #print("{} * {} * {} = {}".format(prev_delta[0][row], a[row][col], obsCol[col], val))
            if val > max:
                max = val
        res_vec[0][col] = float("{:.8f}".format(max)) # rounding to two digits
    return res_vec

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
    b = [[0.6, 0.2, 0.1, 0.1],
        [0.1, 0.4, 0.1, 0.4],
        [0.0, 0.0, 0.7, 0.3],
        [0.0, 0.0, 0.1, 0.9]]

    global pi
    pi = [[0.5, 0.0, 0.0, 0.5]]

    global obs
    obs = [2, 0, 3, 1]
    
    delta_timeline = []
    prev_delta = elemVectorMult(pi[0], getObsColumnByIndex(obs[0]))
    delta_timeline.append(prev_delta)
    
    for ob in obs[1:]:
        prev_delta = getViterbiDelta(prev_delta, ob)
        delta_timeline.append(prev_delta)
    
    print(delta_timeline)
    states = [max(enumerate(delta), key=lambda x: x[1])[0] for delta in delta_timeline]

    sys.stdout.write(str(states).strip(' []').replace(',', '') + '\n')


    

if __name__ == "__main__":
    main()

