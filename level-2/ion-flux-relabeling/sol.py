def find_head(level, num, left, right, val):

    if val == left or val == right:
        return num
    else:
        level -= 1
        num = left if val < left else right
        left = num - 2**level
        right = num - 1
        return find_head(level, num, left, right, val)


def solution(h, q):

    root = 2**h-1
    answer = []

    for node in q:
        if node == root:
            answer.append(-1)
        else:
            left = root // 2
            right = root - 1
            answer.append(find_head(h-1, root, left, right, node))

    return answer
