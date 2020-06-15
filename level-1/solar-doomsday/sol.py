from math import sqrt

solution_list = []


def solution(area):

    low_root = int(sqrt(area))
    low_sq = low_root**2
    solution_list.append(low_sq)

    diff = area - low_sq

    if diff == 1:
        solution_list.append(1)
        return solution_list
    elif diff == 0:
        return solution_list
    else:
        return solution(diff)


if __name__ == "__main__":
    area = int(input("Enter area: "))
    print(solution(area))
