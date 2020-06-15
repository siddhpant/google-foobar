def min_henchmen(total_lambs):
    """Be generous and pay heftily but to minimum number of henchmen"""

    # Rules state that:
    # - No "more" than twice the LAMBs to seniors (i.e. equal is valid).
    # - Senior's LAMBs should not be less than that of his next two juniors.
    # Thus, dole out 2^x to everyone, where x is the level of seniority.

    minimum = 0
    level = 0

    while total_lambs != 0:  # Explicity is better than implicity
        if total_lambs >= 2**level:
            total_lambs -= 2**level
            minimum += 1
            level += 1
        else:
            break

    return minimum


def max_henchmen(total_lambs):
    """Be stingy and pay maximum number of henchmen but as low as possible"""

    # Rules state that:
    # - No "more" than twice the LAMBs to seniors (i.e. less is valid).
    # - Senior's LAMBs should not be less than that of his next two juniors.
    # Fibonacci series satisfies both the constraints.

    maximum = 1  # The juniorost henchmen
    total_lambs -= 1  # Give him 1 LAMB
    second_junior, immediate_junior = 0, 1

    while total_lambs != 0:
        senior = immediate_junior + second_junior
        if total_lambs >= senior:
            total_lambs -= senior
            maximum += 1
            second_junior = immediate_junior
            immediate_junior = senior
        else:
            break

    return maximum


def solution(total_lambs):
    if total_lambs < 1:
        raise ValueError("Total number of LAMBs must be a natural number.")
    elif total_lambs >= 10**9:
        raise ValueError("Total number of LAMBs must be less than a billion.")
    else:
        return max_henchmen(total_lambs) - min_henchmen(total_lambs)
