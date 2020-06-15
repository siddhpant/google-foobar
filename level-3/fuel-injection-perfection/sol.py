def solution(pellets):
    # Convert from string
    pellets = long(pellets)

    # Max 309 digits
    if pellets >= 1e310:
        raise ValueError("Too many number of pellets. Must be <10^310")

    number_of_operations = 0

    while pellets != 1:
        # If divisible by 2, divide in half.
        if pellets & 1 == 0:
            pellets >>= 1
        # Increasing to 4 would be erroneous, so decrement pellets in case of 3
        elif pellets == 3:
            pellets -= 1
        # Now for odd numbers.
        else:
            # Similar to the use of `n & (n-1)` for determining of power of 2.
            # More trailing zeroes in binary means better shot at dividing by 2
            # as a number is not divisible by 2 if it has the LSB set as 1,
            # and it's a power of 2 if it has just MSB set as 1.
            # The more trailing zeroes you have, more repeated divisions by 2
            # is possible (you keep on right shifting it, so more zeroes mean
            # more right shifts possible).
            plus_one = (pellets+1) & pellets
            minus_one = (pellets-1) & (pellets-2)  # x-2 preceeds x-1

            # Lower number should be preferred to avoid unnecessary increase.
            if minus_one < plus_one:
                pellets -= 1
            else:
                pellets += 1

        # One operation is done
        number_of_operations += 1

    return number_of_operations
# End of solution()
