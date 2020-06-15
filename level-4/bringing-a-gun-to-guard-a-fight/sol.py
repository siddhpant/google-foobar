from math import ceil, hypot, log


def in_same_quadrant(point1, point2):
    """Return if two points are in same quadrant"""

    # Same sign (0 doesn't have any sign)
    return ((point1[0] == 0 or point1[0] ^ point2[0] >= 0)
            and (point1[1] == 0 or point1[1] ^ point2[1] >= 0))
# End of in_same_quadrant()


def point_encountered_earlier(point1, point2):
    """
    If x2 > x1 or y2 > y1, then the other point isn't in the way.
    Since we are seeing from origin (0, 0) as the pos. of shooter, points
    must be in same quadrant to be in the way.

    This function should be called when slope associated with the points are
    the same, as such it is then sufficient to just check the values of points.
    """

    return abs(point1[0]) < abs(point2[0]) or abs(point1[1]) < abs(point2[1])
# End of point_encountered_earlier()


def get_slope(point):
    """Return slope of a point/position."""

    if point[0] != 0:
        return float(point[1]) / point[0]
    elif point[1] > 0:
        return "+infinity"
    else:
        return "-infinity"
# End of get_slope()


def distance_formula(position_1, position_2):
    """
    Distance (d) between two points (x1, y1), (x2,y2) is given by:
    d = sqrt( (x2 - x1)^2 + (y2-y1)^2 )
    """
    x = position_2[0] - position_1[0]
    y = position_2[1] - position_1[1]
    return hypot(x, y)
# End of distance_formula


def mirror_horizontally(positions, c):
    """
    Mirror points w.r.t. x = c line.
    Reflection of (x, y) due to x = c would be (2c-x, y).
    """

    for index in range(len(positions)):
        i, j = positions[index]
        p = 2*c - i
        q = j
        positions.append((p, q))
# End of mirror_horizontally()


def mirror_vertically(positions, c):
    """
    Mirror points w.r.t. y = c line.
    Reflection of (x, y) due to y = c would be (x, 2c-y).
    """

    for index in range(len(positions)):
        i, j = positions[index]
        p = i
        q = 2*c - j
        positions.append((p, q))
# End of mirror_vertically()


def mirror_coordinates(
    dimensions, my_positions, guard_positions, corners,
    max_x_mirrors, max_y_mirrors
):
    """
    Mirror the coordinates.
    We can mirror it rightwards first, then mirror it upwards.
    Then we can mirror the whole thing to left and downwards.
    It's kind of like unfolding a folded paper.
    Will probably have more mirrors than required.
    """

    corner_x, corner_y = corners[-1]  # First top-right corner

    # The next corner (or the line actually) will be at an increased value.
    # So we will just multiply the respective dimension of the room.
    x_dim, y_dim = dimensions

    # The last corner will be at 2^(iteration - 1) times the offset.
    mirror_count_x = mirror_count_y = 0  # No. of times mirroring/iter happens

    # Log base 2 since each iteration mirrors all the previous ones.
    max_iter_x = ceil(log(max_x_mirrors, 2))
    max_iter_y = ceil(log(max_y_mirrors, 2))

    # Number of iterations must be sufficient to generate the mirrors
    max_iter_x += 0 if 2**max_iter_x > max_x_mirrors else 1
    max_iter_y += 0 if 2**max_iter_y > max_y_mirrors else 1

    # Mirroring to right first. Thus, x = corner_x
    while mirror_count_x < max_iter_x:
        mirror_horizontally(my_positions, corner_x)
        mirror_horizontally(guard_positions, corner_x)
        corner_x += (2**mirror_count_x) * x_dim
        mirror_count_x += 1
    mirror_horizontally(my_positions, x_dim+5)

    # Now mirroring upwards. Thus, y = corner_y
    while mirror_count_y < max_iter_y:
        mirror_vertically(my_positions, corner_y)
        mirror_vertically(guard_positions, corner_y)
        corner_y += (2**mirror_count_y) * y_dim
        mirror_count_y += 1

    # We have made, sort of, the first quadrant (not exactly but ok)
    # Now we just need to mirror it to left and down to get the full mirror
    # Will have extra mirrors

    corner_x, corner_y = corners[0]  # Bottom-left corner

    # Mirror towards left
    mirror_horizontally(my_positions, corner_x)
    mirror_horizontally(guard_positions, corner_x)

    # Mirror downwards
    mirror_vertically(my_positions, corner_y)
    mirror_vertically(guard_positions, corner_y)
# End of mirror_coordinates()


def change_frame_of_ref(dimensions, my_positions, guard_positions, corners):
    """
    Change the frame of reference and make (0, 0) as my_position.
    Also change the dimensions to reflect the current change by showing both
        - left and right distances
        - down and up distances
    from my_position to the wall.

    For eg., we have been given:
        - dimensions = [5, 4]
        - my_positions = [2, 3]
        - guard_positions = [1, 2]
        - corners = []

    The following is the room (m = me, g = guard, * = corners of room)

    4 * . . . . *
    3 . . m . . .
    2 . g . . . .
    1 . . . . . .
    0 * . . . . *
      0 1 2 3 4 5

    After changing frame of reference, we will have:
        - dimensions = [5, 4]  (No change)
        - my_positions = [(0, 0)]  (List of tuples)
        - guard_positions = [(2, 0)]
        - corners = [(-2, -3), (-2, 1), (3, -3), (3, 1)]
    """

    # Set corners
    for x in (0, dimensions[0]):
        for y in (0, dimensions[1]):
            corners.append((x - my_positions[0], y - my_positions[1]))

    # Change position vector of guard_position with my_position as reference
    # List of lists, to store other positions later
    guard_positions[0] -= my_positions[0]
    guard_positions[1] -= my_positions[1]
    guard_positions.append(tuple(guard_positions))
    del guard_positions[0]  # Remove the first two elements, i.e., the flow is
    del guard_positions[0]  # from [1, 2] to [1, 2, (2, 0)] to [(2, 0)]

    # Set as [(0, 0)]
    my_positions.append((0, 0))
    del my_positions[0]
    del my_positions[0]
# End of change_frame_of_ref()


def convert_to_slopes_dict(positions, distance):
    """
    Make dict with slope (from (0, 0)) as key & set of points as value.

    If a position is encountered earlier, use that position, since the latter
    positions are immaterial for our purposes.

    If the distance to a point is greater than the maximum distance a beam can
    travel, then it is of no use too.
    """

    slopes_dict = {}

    for pos in positions:

        # Distance formula but with origin is just sqrt(x^2 + y^2)
        if hypot(pos[0], pos[1]) > distance:
            continue  # Skip this positions

        slope = get_slope(pos)

        if slope in slopes_dict:
            for existing_pos in slopes_dict[slope]:
                if in_same_quadrant(existing_pos, pos):
                    if point_encountered_earlier(existing_pos, pos):
                        break
            else:  # If no break
                slopes_dict[slope].add(pos)
        else:
            slopes_dict[slope] = {pos}

    return slopes_dict
# End of convert_to_slopes_dict()


def num_killable_positions(my_positions, guard_positions, distance):
    """
    Returns number of killable positions. Position we cannot hit occurs when:
        - A killable guard position already exists before that position,
        - The beam cannot reach that position lethally,
        - We hit ourselves first before the guard,
        - We hit a corner, due to which the beam bounces back towards us.

    The first and second case is taken care of by convert_to_slopes_dict().
    The third case is a subset of the second case.

    So we just need to check for the second case now.
    """

    killable_positions = 0  # Number of valid postions

    # If a slope (& hence line y = mx) isn't there in my_positions,
    # all the points associated with that slope are valid.
    for slope in guard_positions.keys():
        if slope not in my_positions:
            killable_positions += len(guard_positions[slope])
            del guard_positions[slope]

    while guard_positions:
        # Get a slope, and points corresponding to it
        guard_slope, positions = guard_positions.popitem()

        for guard in positions:

            found_closer_position = False

            # Slopes which weren't there in my_positions are already removed.
            for pos in my_positions[guard_slope]:
                if in_same_quadrant(pos, guard):
                    if point_encountered_earlier(pos, guard):
                        found_closer_position = True
                        break

            if not found_closer_position:  # If we don't hit ourselves first
                killable_positions += 1

    return killable_positions
# End of num_killable_positions()


def solution(dimensions, my_position, guard_position, distance):
    """
    Params:
        dimensions: List(int) = width and height of the room.
        my_position: List(int) = my position vector in R2.
        guard_position: List(int) = Elite guard's position vector in R2.
        distance: int = Maximum distance the beam can travel.

    Returns the number of distinct directions to fire so as to hit elite guard.
    """

    if not (1 < dimensions[0] <= 1250 and 1 < dimensions[1] <= 1250):
        # Mathematical notation indicating the range
        raise ValueError("The dimensions of the room are not in (1, 1250].")

    x_dim, y_dim = dimensions[0], dimensions[1]

    if (
        not (0 < my_position[0] < x_dim and 0 < guard_position[0] < x_dim)
        or not (0 < my_position[1] < y_dim and 0 < guard_position[1] < y_dim)
    ):
        raise ValueError("Position vector entries must be between 0 and the "
                         "respective dimension of the room.")

    if not 1 < distance <= 10000:
        raise ValueError("Supplied maximum distance the beam can travel to"
                         "is not in range (1, 10000].")

    if my_position == guard_position:
        raise ValueError("Both persons cannot be at the same position.")

    if distance_formula(my_position, guard_position) > distance:
        # We cannot hit the guard as the beam cannot reach him directly.
        return 0

    if distance_formula(my_position, guard_position) == distance:
        # The shortest path is the max distance the beam can travel.
        return 1

    # Number of max mirrors of the room in both (positive) directions
    # ceil(a/b) = (a+b-1)/b
    max_x_mirrors = (distance + dimensions[0] - 1) / dimensions[0]
    max_y_mirrors = (distance + dimensions[1] - 1) / dimensions[1]

    # Plural references to indicate there will be multiple positions later
    # (Due to mirroring)
    my_positions, guard_positions, corners = my_position, guard_position, []

    change_frame_of_ref(dimensions, my_positions, guard_positions, corners)

    # We don't need to mirror every point on room.
    # We are only concerned with our position, the guard's position, & corners.
    mirror_coordinates(dimensions, my_positions, guard_positions, corners,
                       max_x_mirrors, max_y_mirrors)

    # Our reference/start point is (0, 0), so remove it.
    # It's the first entry due to change_frame_of_ref()
    del my_positions[0]

    # Convert to a dict with slopes as key for faster evaluation later
    my_positions = convert_to_slopes_dict(my_positions, distance)
    guard_positions = convert_to_slopes_dict(guard_positions, distance)

    # Return in how many directions we can shoot to kill
    return num_killable_positions(my_positions, guard_positions, distance)
# End of solution()
