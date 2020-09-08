import sys

"""
we always assume the input is given correct and does not has to be checked specifically
"""


def getMatricesFromStdIn():
    for num, line in enumerate(sys.stdin):
        line = line.replace('\n', '')
        if line[-1] == " ":
            line = line[:-1]
        args = [float(val) for val in line.split(" ")]

        # create global variables for the matrices
        if num == 0:
            row_count = int(args[0])  # could be used to check if it fits
            col_count = int(args[1])
            args = args[2:]
            args = [args[i:i + col_count] for i in range(0, len(args), col_count)]
            global a
            a = args
            pass
        elif num == 1:
            row_count = int(args[0])  # could be used to check if it fits
            col_count = int(args[1])
            args = args[2:]
            args = [args[i:i + col_count] for i in range(0, len(args), col_count)]
            global b
            b = args
            pass
        elif num == 2:
            row_count = int(args[0])  # could be used to check if it fits
            col_count = int(args[1])
            args = args[2:]
            args = [args[i:i + col_count] for i in range(0, len(args), col_count)]
            global pi
            pi = args
            pass
        elif num == 3:
            row_count = 1
            col_count = int(args[0])  # could be used to check if it fits
            args = args[1:]
            args = [args[i:i + col_count] for i in range(0, len(args), col_count)]
            global obs
            obs = args
            pass
        else:
            pass


def elementMultiply(m1, m2):
    return [[m1[row][col] * m2[row][col] for col in range(len(m1[row]))] for row in range(len(m1))]


def observationColumn(pos):
    return [[b[row][obs[pos]] for row in range(len(b))]]


def findMaxNonZeroProb(m):
    max_value = []
    max_index = []
    for row in m:
        max_value.append(max(row))
        max_index.append([i for i, j in enumerate(row) if j == max_value[-1] and j > 0])
    return max_value, max_index


def listTranspose(l):
    return list(map(list, zip(*l)))


def backtracking(Xs):
    if type(Xs[0]) == list:
        return [backtracking(x) for x in Xs]
    else:
        global argmax_states
        prev_states = argmax_states[-len(Xs)][Xs[-1]]
        if len(prev_states) > 1:
            return [(Xs + [s]) for s in prev_states]
        else:
            return Xs + prev_states


def reverseNestedList(lists):
    if type(lists[0]) == list:
        return [reverseNestedList(l) for l in lists]
    else:
        return lists[::-1]


def main():
    print('test')
    getMatricesFromStdIn()
    global obs
    obs = [int(ob) for ob in obs[0]]
    delta = elementMultiply(observationColumn(0), pi)
    global argmax_states
    argmax_states = []
    for step in range(1, len(obs)):
        new_delta = elementMultiply(elementMultiply([delta[-1] for i in range(len(a))], listTranspose(a)), listTranspose([observationColumn(step)[0] for i in range(len(a))]))
        max_prob, argmax = findMaxNonZeroProb(new_delta)
        delta.append(max_prob)
        argmax_states.append(argmax)

    Xt = [i for i, j in enumerate(delta[-1]) if j == max(delta[-1])]
    if len(Xt) > 1:
        Xt = [[x] for x in Xt]

    for i in range(len(delta) - 1):
        Xt = backtracking(Xt)

    # reverse the result lists Xt
    sequence = reverseNestedList(Xt)
    print(sequence)

if __name__ == "__main__":
    main()