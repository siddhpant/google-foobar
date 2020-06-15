"""
Return the fewest number of generations to generate the given number of bombs.

We start with 1 bomb of each type. The bombs are "self-replicating".

```
    Every Mach bomb retrieves a sync unit from a Facula bomb;
    for every Mach bomb, a Facula bomb is created;
```
If x Mach bombs and y Facula bombs are there, y sync units are available.
A Mach bomb will take a sync unit & generate a Mach bomb and a Facula bomb.
Thus, we have an extra facula bomb for one iteration.

```
    Every Facula bomb spontaneously creates a Mach bomb.
```
A Facula bomb spontaneously creates a Facula bomb and a Mach bomb.

A cycle/generation can have only one type of bomb replicating.
A cycle/generation necessarily uses all of the either type of bombs.

In effect, sum of number of bombs of current generation yeilds the number of
bombs of next generation for either type.
"""


def solution(mach, facula):
    # Convert str to long int, numbers are in the range [1, 1e50]
    mach, facula = [long(mach)], [long(facula)]  # List for using by reference.

    # One can't have equal numbers of both bombs, unless it's the start state.
    if mach == facula:
        return "0" if mach == 1 else "impossible"

    # Start state is when we have one bomb of each type
    start_state = False

    # The number of generations
    generations = 0

    # m >> f or f >> m is not possible without repeated addition.
    # Repeated addition is just multiplication.
    # We can cut short our findings using modulo instead of simple subtraction.

    while not start_state:
        # We start with one bomb each, & that's the only time they are equal.
        if mach[0] < 1 or facula[0] < 1 or mach[0] == facula[0]:
            generations = "impossible"
            break

        # You can keep generating one type of bomb from 1 bomb of other type.
        if mach[0] == 1:
            generations += facula[0] - 1  # -1 for the initial state
            break
        elif facula[0] == 1:
            generations += mach[0] - 1
            break

        if mach > facula:
            generated, generator = mach, facula
        else:
            generated, generator = facula, mach

        generations += generated[0]/generator[0]
        generated[0] %= generator[0]

        start_state = generated[0] == generator[0] == 1

    return str(generations)
# End of solution()
