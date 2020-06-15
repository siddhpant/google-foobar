"""
We are asked to find the sum floor(i*sqrt(2)) where i ranges from 1 to n.

floor(r), floor(2*r), floor(3*r).... where r is an irrational number forms a
Beatty sequence B(r).

https://en.wikipedia.org/wiki/Beatty_sequence


Let sum(r, n) denote the sum of Beatty sequence B(r) till nth term.


For r >= 2:

Let s = r - 1

Then,
sum(r, n) = floor(r) + floor(2*r) + floor(3*r) + ... + floor(n*r)
          = floor(r-1+1) + floor(2*(r-1+1)) + floor(3*(r-1+1)) + ...
                                                            + floor(n*(r-1+1))
          = floor(s + 1) + floor(2*(s + 1)) + floor(3*(s + 1)) + ...
                                                            + floor(n*(s + 1))
          = floor(s)+1 + floor(2*s)+2 + floor(3*s)+3 + ... + floor(n*s)+n
                            [As 1, 2, 3, etc. don't have any fractional part]
          = floor(s) + floor(2*s) + floor(3*s) + ... + floor(n*s)
            + 1      + 2          + 3          + ... + n
                                                        [Separated the terms]
          = sun(s, n) + n*(n+1)/2


Now, for r < 2 (sqrt(2) < 2):

Beatty's theorem states that if r > 1, there exists an irrational s, such that

                            1/r + 1/s = 1

and the sequences of B(r) and B(s) are complementary, that is, they partition
the set of natural numbers.

Now,
Let x = floor(n*r)

As they partition the set of natural numbers,
                sum(r, n) + sum(s, floor(n*r/s))
              = sum(r, n) + sum(s, floor(x/s)) = x*(x + 1)/2

Now,

floor(x/s) = floor(x*(1/s))
           = floor(x*(1 - 1/r)) -----> [Due to Beatty's theorem]
           = floor(x - x/r)
           = floor(x - floor(n*r)/r)
           = floor(x - n)
           = x - n -----> [ints]
           = floor(n*r) - n
           = floor(n*r - n) -----> [As n is a positive int with 0 frac part]
           = floor(n(r - 1))

Let n' = floor(n(r - 1)). Then, n + n' = x ; and floor(x/s) = n'

Thus,
sum(r, n) + sum(s, n') = (n + n')*(n + n' + 1)/2
or sum(r, n) = (n + n')*(n + n' + 1)/2 - sum(s, n')


Now, for r = sqrt(2):

s = sqrt(2) + 2  -----> [From Beatty's theorem]
n' = floor(n*(sqrt(2) - 1))

Thus,

sum(sqrt(2), n) = (n + n')*(n + n' + 1)/2 - sum((sqrt(2) + 2), n')

Now, s > 2, thus,
sum((sqrt(2) + 2), n') = sum((sqrt(2) + 1), n') + n'*(n' + 1)/2
                       = sum(sqrt(2), n') + n'*(n' + 1)/2 + n'*(n' + 1)/2
                       = sum(sqrt(2), n') + n'*(n' + 1)

Hence,

sum(sqrt(2), n) = (n + n')*(n + n' + 1)/2 - sum(sqrt(2), n') - n'*(n' + 1)
                = (n*n + n*n' + n + n*n' + n')/2 - sum(sqrt(2), n') - n'*(n'+1)
                = n*n' + n*(n+1)/2 + n'/2 - n'*(n'+1) - sum(sqrt(2), n')
                = n*n' + n*(n + 1)/2 + n'*(n' + 1)/2 - sum(sqrt(2), n')

Thus, we get a recursive formula.


Useless side note: The given sequence (with r = sqrt(2)) is A001951 on OEIS.
"""


# Set some variables which will be needed during recursion

GOOGOL = 10**100  # Google foobar hmmmm...

# import decimal
# decimal.getcontext().prec = 101
# sqrt_2 = Decimal(2).sqrt()
# Now get all the digits after the decimal point, it's (sqrt(2) - 1)*10^100
# This is done to get precision right, which is the bug we are exploiting

SQRT_2_MINUS_1 = long("41421356237309504880168872420969807856967187537694"
                      "80731766797379907324784621070388503875343276415727")


# These were set so as to not repeatedly make new objects.

# Functions implementing the solution are as follows


def sigma_n(n):
    """Return the sum of first n natural numbers."""
    return n * (n + 1) / 2
# End of sigma_n()


def sum_beatty(n):
    """Sum the sequence using the equation derived"""

    if n == 0:
        return 0

    n_prime = (n * SQRT_2_MINUS_1) // GOOGOL  # int division will act as floor

    return n*n_prime + sigma_n(n) - sigma_n(n_prime) - sum_beatty(n_prime)
# End of sum_beatty()


def solution(str_n):

    # Convert from string to long
    n = long(str_n)

    # The foobar tests will have valid inputs, so we don't need to check here
    """
    if not (1 <= n <= GOOGOL):
        raise ValueError("n must be in range [1, 10^100].")
    """

    return str(sum_beatty(n))
# End of solution


# End of file
