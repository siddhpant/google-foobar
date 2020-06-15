from fractions import Fraction, gcd
from itertools import starmap
from operator import mul, sub


def transpose(matrix):
    """Return transpose of a matrix."""
    return map(list, zip(*matrix))
# End of transpose()


def multiply_matrices(A, B):
    """Multiply two matrices A and B (A * B)."""

    # Empty lists
    if not A or not B:
        raise ValueError("Cannot multiply empty lists/matrices.")

    B_transpose = transpose(B)

    assert len(A) == len(B), ("Number of columns of A must be equal to "
                              "number of rows of B for multiplying matrices.")

    return [[sum(starmap(mul, zip(A_row, B_col)))
            for B_col in B_transpose] for A_row in A]
# End of multiply_matrices()


def subtract_matrices(A, B):
    """Subtract two matrices A and B (A - B)"""

    # Empty lists
    if not A or not B:
        raise ValueError("Cannot multiply empty lists/matrices.")

    # Assuming uniform matrices (same number of elements in every row).
    assert len(A) == len(B) and len(A[0]) == len(B[0]),\
        "Order must be same for subtracting matrices"

    return [map(sub, A[i], B[i]) for i in range(len(A))]
# End of subtract_matrices()


def get_identity_matrix(order):
    """Return an identity matrix of the given order."""

    # Initialise the matrix with all zeroes.
    identity_matrix = [[Fraction(0)]*order for _ in range(order)]

    # Now set diagonal elements as 1.
    for i in range(order):
        identity_matrix[i][i] = Fraction(1)

    return identity_matrix
# End of get_identity_matrix()


def invert_matrix(A):
    """Find inverse of a matrix using Gauss-Jordan."""

    # Empty lists
    if not A:
        raise ValueError("Cannot invert empty list/matrix.")

    # Assuming uniform matrices (same number of elements in every row).
    assert len(A) == len(A[0]), "Only square matrices can be inverted."

    order = len(A)

    # [A | I] but using different lists/matrices.
    I = get_identity_matrix(order)

    # Gauss elimination
    for i in range(order):
        # Make the leading one.
        if A[i][i] != 1:
            row_divisor = A[i][i]
            A[i] = [element/row_divisor for element in A[i]]
            I[i] = [element/row_divisor for element in I[i]]

        # Make all entries below the leading one zero.
        for row in range(i+1, order):
            multiple = A[row][i]
            for col in range(order):
                A[row][col] -= A[i][col]*multiple
                I[row][col] -= I[i][col]*multiple

    # Continue with Gauss-Jordan (the zeroth row/col is the topmost corner)
    for i in range(order-1, 0, -1):
        # Make all entries above the leading one zero.
        for j in range(i-1, -1, -1):
            multiple = A[j][i]
            A[j][i] = Fraction(0)  # Before leading 1, everything is 0
            for k in range(order-1, -1, -1):
                I[j][k] -= I[i][k]*multiple

    if A == get_identity_matrix(order):
        return I
    else:
        raise RuntimeError("The matrix couldn't be inverted.")
# End of invert_matrix()


def move_terminal_rows_to_end(transition_matrix, absorbing_states):
    """
    Move all zero rows to the bottom/end of the matrix while preserving order.
    """

    t_mat = transition_matrix  # New reference, this doesn't copy
    last_index = len(t_mat) - 1
    num_absorbing_states = len(absorbing_states)

    for i in range(num_absorbing_states):
        # Get the index of the bottom-most zero row vector.
        state = absorbing_states.pop(-1)

        if state != last_index:
            # Interchange rows
            t_mat[state], t_mat[last_index] = t_mat[last_index], t_mat[state]

            # Interchange columns
            for row in t_mat:
                row[state], row[last_index] = row[last_index], row[state]

        # Decrement for next iteration.
        last_index -= 1

    return t_mat
# End of move_terminal_rows_to_end()


def get_probabilities_list(transition_matrix, number_of_states, t):
    """
    For t transient states and s absorbing states,
    P = [Q,  R ] whose orders respectively are [txt, txs]
        [0, I_s]                               [sxt, sxs]
    The fundamental matrix is given by the inverse of matrix (I_t - Q).
    (Note: I_x is identity matrix of order x.)

    Probability of being absorbed by state j from state i is given by
    entry (i,j) of matrix N*R
    """

    Q, R = [], []

    for i, row in enumerate(transition_matrix):
        denominator = sum(row)
        if i < t:
            Q.append([numerator / denominator for numerator in row[:t]])
            R.append([numerator / denominator for numerator in row[t:]])
            # row[t:] is equivalent to row[-s:] as total states = t + s
        else:
            break

    # N = (I_t - Q)^-1
    N = invert_matrix(subtract_matrices(get_identity_matrix(t), Q))

    # We just need the solution starting from state 0.
    return multiply_matrices(N, R)[0]
# End of get_probabilities_list()


def lcm(a, b):
    """Return least common multiple of two numbers"""
    return (a*b) / gcd(a, b)
# End of lcm()


def solution(transition_matrix):

    # If just state 0 is there, it will stay there.
    if len(transition_matrix) == len(transition_matrix[0]) == 1:
        return [1, 1]

    # Convert ints to fractions for convenience in dealing with probability.
    transition_matrix = [map(Fraction, states) for states in transition_matrix]

    # Get indices of terminal states (with 0 probability to transition).
    absorbing_states = [index for index, row in enumerate(transition_matrix)
                        if set(row) == {0}]

    number_of_states = len(transition_matrix)
    number_of_transient_states = number_of_states - len(absorbing_states)

    # Move the terminal states' row to the end
    transition_matrix = move_terminal_rows_to_end(transition_matrix,
                                                  absorbing_states)

    # Get the list having the required probabilities
    probabilities = get_probabilities_list(transition_matrix, number_of_states,
                                           number_of_transient_states)

    numerators = [probability.numerator for probability in probabilities]
    denominators = [probability.denominator for probability in probabilities]

    denominator_lcm = reduce(lcm, denominators)

    for index, numerator in enumerate(numerators):
        numerators[index] *= denominator_lcm / denominators[index]

    numerators.append(denominator_lcm)

    return numerators
# End of solution()
