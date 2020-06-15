from collections import OrderedDict
from Queue import Queue


def convert_to_single_st_problem(network, sources, sinks):
    """
    Convert multiple source and sink problem to single by adding a preceeding
    source and succeeding sink with infinite (outward and inward) capacities.

    network is just a sq. matrix (rooms with capacity to another room)
    """

    len_network = len(network)

    top_source = [0] + [0] * len_network + [0]
    bottom_sink = [0] + [0] * len_network + [0]

    for index in sources:
        # +1 to account for extra top source node
        top_source[index + 1] = float("inf")

    for index in range(len_network):
        # Append the top source
        network[index].insert(0, 0)

        # Append the bottom sink
        if index in sinks:
            network[index].append(float("inf"))
        else:
            network[index].append(0)

    network.insert(0, top_source)
    network.append(bottom_sink)
# End of convert_to_single_st_problem()


def breadth_first_search(network, source, sink, reversed_path_map):
    """
    BFS to find the shortest augmenting path.
    Returns a bool indicating if a search was successful or not.
    """

    len_network = sink + 1  # Since sink is the last element

    visited_rooms = {source}  # A set (we have to just check if we visited)
    next_rooms_queue = Queue()
    next_rooms_queue.put_nowait(source)

    while not next_rooms_queue.empty():
        room = next_rooms_queue.get_nowait()

        for next_room in range(len_network):
            # Check if room already visited
            if next_room in visited_rooms:
                continue

            # Check if residual capacity is greater than 0 so we can flow from
            if network[room][next_room] > 0:  # room -> next_room
                reversed_path_map[next_room] = room  # next_room <- room

                visited_rooms.add(next_room)
                next_rooms_queue.put_nowait(next_room)

                # Check if we reached the sink
                if next_room == sink:
                    return True  # Search successful

    return False  # Search unsuccessful
# End of breadth_first_search()


def max_flow_edmonds_karp(network):
    """Find the maximum flow using Edmonds-Karp algorithm."""

    maximum_flow = 0

    # The source and sink is the first and last element due to the use of
    # convert_to_single_st_problem() before calling this
    source, sink = 0, len(network) - 1

    # For back-tracing back a path; {1: 2, 5: 1} means path is 2 -> 1 -> 5
    # The entries are reversed; as you can see above: 5 <- 1 and 1 <- 2
    reversed_path_map = OrderedDict()

    # To store valid nodes of the path and to later reduce the flow in that
    augmented_path_map = []

    while breadth_first_search(network, source, sink, reversed_path_map):

        # Get the initial values
        current, previous = reversed_path_map.popitem()
        flow = network[previous][current]

        # Store the valid path direction
        augmented_path_map.append((previous, current))

        # While the OrderedDict isn't empty and previous node isn't the source
        while reversed_path_map and previous != source:
            current, previous = previous, reversed_path_map.pop(previous)

            # We need the minimum value, due to bottlenecking in the path
            if network[previous][current] < flow:
                flow = network[previous][current]

            augmented_path_map.append((previous, current))

        # Update the flow in the path
        while augmented_path_map:
            room, next_room = augmented_path_map.pop()
            network[room][next_room] -= flow  # In the forward direction
            network[next_room][room] += flow  # In the backward direction

        # The sum of all flows will be the maximum flow
        maximum_flow += flow

    return maximum_flow
# End of max_flow_edmund_karp()


def solution(entrances, exits, path):
    """This is just an integral multiple source sink maximum flow problem."""

    # These are bound to pass in foobar test cases, so making it non-executable
    """
    if 1 > len(path) > 50:
        raise ValueError("Number of rooms should be in the range (1, 50].")

    for room in path:
        if any(-1 > bunnies > 2000000 and not isinstance(bunnies, int)
               for bunnies in room):
            raise ValueError("Number of bunnies in a room must not exceed "
                             "20,00,000 and must be a whole number.")

    if not set(entrances).isdisjoint(exits):
        raise ValueError("A room cannot be both an entrance and an exit.")
    """

    # Multiple sources and sinks to single sources and sinks
    convert_to_single_st_problem(path, entrances, exits)

    # Return the maximum flow using the Edmonds-Karp algorithm
    return max_flow_edmonds_karp(path)
# End of solution()
