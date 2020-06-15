"""
Code dished out in 5-10 minutes after reading the problem.

Of course, this is incorrect (passes some test cases and not others).

If you understand the problem, you'll be able to point out where this code
is wrong, and why it works for the given test cases. Hint: Check for 26.
"""

from math import ceil, floor, log


def number_of_operations(pellets):
    """Param: pellets is long"""

    # Optimising for lower edge cases.
    if pellets in (1L, 2L, 3L):
        return pellets - 1  # 0 for 1, 1 for 2, and 2 for 3.

    # We can divide by the entire group in half.
    # Thus, the number of steps can be logarithm (base 2) of total pellets.
    # If the number isn't perfect power, get the ceil and floor of power.

    # If divisible by 2, divide by 2
    if pellets & 1 == 0:
        return number_of_operations(pellets >> 1) + 1

    log_pellets = log(pellets, 2)

    if log_pellets != int(log_pellets):  # Not a perfect power of 2

        ceil_log_pellets = int(ceil(log_pellets))
        floor_log_pellets = int(floor(log_pellets))

        ceil_pellets_diff = abs(pellets - 2**ceil_log_pellets)
        floor_pellets_diff = abs(pellets - 2**floor_log_pellets)
        
        print locals()

        if ceil_pellets_diff < floor_pellets_diff:
            return ceil_pellets_diff + ceil_log_pellets
        else:
            return floor_pellets_diff + floor_log_pellets
    else:
        return log_pellets
# End of number_of_operations()
