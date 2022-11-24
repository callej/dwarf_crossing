"""
Greedy Algorithm for the Dwarf Bridge Crossing Problem.

This program uses a greedy algorithm to find the minimum time for all the dwarfs to cross the bridge.
A greedy algorithm i dangerous, just because it is greedy. It takes the best option that is right in front
of the eyes of the algorithm at any moment. It doesn't look at the whole picture. This means that it is risky to use,
and that it is not generic. It only works for a specific problem under specific conditions. However, it is usually
easy to implement a greedy algorithm to a problem. Just remember it can go horribly wrong and that it may be
difficult to prove if a greedy algorithm is ok to use for a specific problem.

Nevertheless, I believe (without proving it) that a greedy algorithm can be used to find the solution of
the dwarf problem, as it is originally stated.

The problem:
There are 300 dwarfs that need to cross a bridge in the middle of the crispy cold polar night.
It is a rickety bridge in poor condition which only holds for at most two dwarfs to cross at a time.
It is pitch dark and they only have one lantern, which they need in order to cross the bridge.
If two dwarfs crosses the bridge together someone has to bring the lantern back for the others to be able to cross.
However, no dwarf wants to cross the bridge more than 3 times (i.e. over, back and over again).
Each dwarf requires different amount of time to cross the bridge: 1 min, 2 min, 3 min, …, up to 300 min
for the slowest dwarf. When two dwarfs walk together, they walk in the slowest pace.
What is the fastest time they can cross the bridge for all 300 to be on the other side, and how will they achieve this?


Solution Strategy:
1. Minimize the average of the difference in speed when two dwarfs walk together over the bridge.
2. Minimize the average of the time it take for the dwarfs that need to walk back with the lantern.

The reason for number 1 is that we want to waste as little as possible of a faster dwarf's speed. The speed is given
by the time it takes for a dwarf to cross the bridge. Since all the dwarfs required different amount of time to
cross the bridge the difference in time between two dwarfs will always be at least 1 minute, meaning that the
faster dwarf will have to walk 1 minute slower that what he could. He is loosing one minute. We want to minimize
that loss over all the dwarfs that are crossing. Since it will always be at least 1 minute difference between any
two dwarfs, the average cannot be less that 1 minute. We will aim for an average of 1 minute. If we reach this we
know that we have minimized the time it took for the dwarfs to cross the bridge, which is half the problem, and
which is the reason for number 1 above.

The other half of the problem is that we want to minimize the time it takes for the dwarfs to walk back with the
lantern. This can be done by always making sure that the fastest dwarf that still has crossings left will be on
the other side of the bridge ready to walk back with the lantern.


Implementation:
Note: Even though this problem is well structured and clearly defined I will create a generic implementation where
      the number of the dwarfs can vary, their time to cross can be changed, the maximum crossings can be changed,
      and the maximum number of dwarfs that can cross the bridge together can be changed.
      The two reasons for this are:
      a) The structure and the logic in the code becomes more clear when things are defined in one place instead
         of hardcoded all over the program. The logic also becomes more obvious when the code explicitly shows
         the decisions made.
      b) It is possible to test the algorithm with other conditions very easily and do other experiments.
         However, pay attention to that this is a greedy algorithm, which a risky way to solve a problem and
         also very likely to fail outside of its domain. A domain that is difficult to know exactly.

1. All dwarfs will be sorted after their speed, i.e. after how much time they need to cross the bridge.
2. To start, the two fastest dwarfs will cross the bridge in order to have the fastest dwarf available to
   walk back with the lantern.
3. The fastest of the dwarfs that crossed will walk back with the lantern.
4. Check where the fastest dwarf with at least enough crossings left is located.
   If dwarf is before the bridge (at start), at least 3 crossings left are required. Otherwise the dwarf can't
   go back with the lantern, so the speed is of no benefit.
   If the dwarf is after the bridge (at finish), at least 2 crossings left are required for the same reason.
   4a) If that is before the bridge and we don't waste a faster dwarf to come back with the lantern,
       send that dwarf over together with the second fastest dwarf available
   4b) If that is after the bridge, find the two dwarfs with the least difference in speed. If there are several,
       send the two fastest.
5. Send the fastest dwarf with enough (which is 2) crossings left back with the lantern.
6. Repeat step 4 and 5 until there are no more dwarfs available to cross.
7. Keep track of the crossing times:
   7a) When dwarfs cross together we are aiming for an average of the difference in speed of 1 minute
   7b) For the returning dwarfs we are aiming for an average of (1 + number of returns) / 2.
   7c) Note that these numbers are only valid when the problem is structured as described above, with
       the fastest dwarf crossing the bridge in 1 minute, and when it is always a difference of 1 minute in speed
       between dwarfs next to each other when ordered after their speed, and that the maximum number of
       crossings are 3 for all the dwarfs.
8. Print the result:
   8a) Print the time it took for all the dwarfs to cross.
   8b) Print the scheme showing how the dwarfs crossed the bridge back and forth.
   8c) Print if this is an optimal result as aimed for in point 7 above.
"""

from dwarf import Dwarf, Lantern
import dwarf
import time

NUMBER_OF_DWARFS = 300
MAX_CROSSINGS = 3
MAX_TOGETHER = 2

cross_losses = []
return_times = []


def generate_dwarfs(num_of_dwarfs, max_crossings, start_pos, crossing_times=None):
    """Returns a list of Dwarf objects created with the parameters provided."""
    if crossing_times is None:
        crossing_times = [t for t in range(1, num_of_dwarfs + 1)]
    return [Dwarf(num + 1, crossing_times[num], 0, max_crossings, start_pos) for num in range(num_of_dwarfs)]


def min_time(dwarfs, crossings_required):
    """Returns the crossing time for the dwarf in the provided list that has the lowest crossing time,
       among the dwarfs in the list that have at least the required crossings left."""
    result = None
    for d in dwarfs:
        if d.max_crossings - d.times_crossed() >= crossings_required:
            if result is None:
                result = d.time_needed_for_crossing()
            else:
                result = min(result, d.time_needed_for_crossing())
    return result


def find_fastest_similar_dwarfs(dwarfs, max_together):
    """Returns a list of the dwarfs that have the most similar crossing times from the provided list of dwarfs.
       If there are more than one group of dwarfs that have the same similar times, then the fastest group is returned.
       The length of the returned list is provided by max_together. However not longer than the provided list.
       Note that the provided list of dwarfs needs to be sorted."""
    if len(dwarfs) <= max_together:
        return dwarfs
    else:
        min_index = 0
        min_time_lost = time_lost(dwarfs[0:max_together])
        for index in range(1, len(dwarfs) - max_together + 1):
            if (lt := time_lost(dwarfs[index:index + max_together])) < min_time_lost:
                min_time_lost = lt
                min_index = index
        return dwarfs[min_index:min_index + max_together]


def min_waste(at_start, at_finish, max_together):
    """Returns True if the fastest och the fastest similar dwarfs is faster than the fastest dwarf at finish.
       Otherwise False is returned. This can be used for reducing the time wasted when a fast dwarf are walking
       with a slow, if there may be a faster dwarf returning later with the lantern."""
    return at_finish[0] > find_fastest_similar_dwarfs(at_start, max_together)[0]


def faster_dwarf_at_start(at_start, at_finish, max_together):
    """Returns True is there is a faster dwarf at start that should cross the bridge in order to carry the
       lantern back."""
    if min_time(at_start, 3) is None:
        return False
    elif not at_finish or min_time(at_finish, 2) is None:
        return True
    else:
        return min_time(at_start, 3) < min_time(at_finish, 2) and min_waste(at_start, at_finish, max_together)


def setup(num_of_dwarfs, max_crossings, start_pos):
    """Returns the setup of the problem with all dwarfs at the start and no one at finish or being done, and
       with a blank scheme."""
    return generate_dwarfs(num_of_dwarfs, max_crossings, start_pos), [], [], []


def get_fast_dwarf_to_finish(at_start, at_finish, done, lantern, max_together, scheme):
    """Moves the fastest dwarfs across the bridge and returns the time that this takes."""
    global cross_losses
    slowest_index = min(max_together, len(at_start)) - 1
    crossing_time = at_start[slowest_index].crossing_time
    cross_losses.append(time_lost(at_start[0:slowest_index + 1]))
    crossing_dwarfs = cross(at_start, at_finish, done, 0, min(max_together, len(at_start)), lantern)
    scheme.append(crossing_dwarfs)
    return crossing_time


def time_lost(dwarfs):
    """Returns the time lost when several dwarfs are walking together and they have to walk in the slowest pace."""
    result = 0
    for index in range(len(dwarfs) - 1):
        result += dwarfs[-1].crossing_time - dwarfs[index].crossing_time
    return result


def cross(at_start, at_finish, done, index, count, lantern):
    """Facilitates the crossing over the bridge of the specified dwarfs, and returns the ids of these dwarfs."""
    dwarfs_crossed = []
    if lantern.at_pos(dwarf.START):
        dwarfs_crossed = [d.number() for d in at_start[index:index + count]]
        dwarfs_crossed.append("cross")
        for _ in range(count):
            crossing_dwarf = at_start.pop(index)
            crossing_dwarf.cross(lantern)
            if crossing_dwarf.done():
                done.append(crossing_dwarf)
            else:
                at_finish.append(crossing_dwarf)
    return dwarfs_crossed


def get_similar_dwarfs_to_finish(at_start, at_finish, done, lantern, max_together, scheme):
    """Takes the fastest group of the most similar dwarfs across the bridge, and returns the time this takes."""
    global cross_losses
    if len(at_start) <= max_together:
        crossing_time = at_start[-1].crossing_time
        lost_time = time_lost(at_start)
        crossing_dwarfs = cross(at_start, at_finish, done, 0, min(max_together, len(at_start)), lantern)
    else:
        min_index = 0
        min_time_lost = time_lost(at_start[0:max_together])
        for index in range(1, len(at_start) - max_together + 1):
            if (lt := time_lost(at_start[index:index + max_together])) < min_time_lost:
                min_time_lost = lt
                min_index = index
        crossing_time = at_start[min_index + max_together - 1].crossing_time
        crossing_dwarfs = cross(at_start, at_finish, done, min_index, max_together, lantern)
        lost_time = min_time_lost
    scheme.append(crossing_dwarfs)
    cross_losses.append(lost_time)
    return crossing_time


def cross_the_bridge(at_start, at_finish, done, lantern, max_together, scheme):
    """Selects the most suitable group of dwarfs to cross the bridge, and return the time the crossing takes."""
    at_start.sort()
    at_finish.sort()
    if faster_dwarf_at_start(at_start, at_finish, max_together):
        return get_fast_dwarf_to_finish(at_start, at_finish, done, lantern, max_together, scheme)
    else:
        return get_similar_dwarfs_to_finish(at_start, at_finish, done, lantern, max_together, scheme)


def fastest_available_to_return(at_finish):
    """Returns the fastest dwarf at finish who has enough crossings left to go back with the lantern and then
       be able to return across the bridge again to finish."""
    for d in at_finish:
        if d.max_crossings - d.times_crossed() >= 2:
            return d
    return False


def return_with_lantern(at_start, at_finish, lantern, scheme):
    """Facilitates the dwarf walking back over the bridge to return the lantern for others to cross the bridge.
       Returns the time it takes for the dwarf to walk back with the lantern."""
    at_finish.sort()
    if at_finish and at_start and lantern.at_pos(dwarf.FINISH) and \
            (returning_dwarf := fastest_available_to_return(at_finish)):
        global return_times
        at_finish.remove(returning_dwarf)
        returning_dwarf.go_back(lantern)
        at_start.append(returning_dwarf)
        scheme.append([returning_dwarf.number(), "go back"])
        return_times.append(returning_dwarf.time_needed_for_crossing())
        return returning_dwarf.time_needed_for_crossing()
    else:
        return 0


def print_dwarf_positions(dwarfs_at_start, dwarfs_at_finish, dwarfs_done):
    """Prints the number of dwarfs that are at different locations."""
    print(f"\nDwarf Positions:")
    print(f"Dwarfs At Start: {len(dwarfs_at_start)}")
    print(f"Dwarfs At Finish: {len(dwarfs_at_finish)}")
    print(f"Dwarfs Done: {len(dwarfs_done)}\n")


def greedy_min_crossing(num_of_dwarfs, max_crossings, start_pos, max_together):
    """Sets up the problem and executes the algorithm to solve the problem."""
    t_start = time.time()
    dwarfs_at_start, dwarfs_at_finish, dwarfs_done, scheme = setup(num_of_dwarfs, max_crossings, start_pos)
    lantern = Lantern(dwarf.START)
    total_time = 0
    while dwarfs_at_start:  # Keep going until there are no more dwarfs at start to cross the bridge
        total_time += cross_the_bridge(dwarfs_at_start, dwarfs_at_finish, dwarfs_done, lantern, max_together, scheme)
        total_time += return_with_lantern(dwarfs_at_start, dwarfs_at_finish, lantern, scheme)
    execution_time = time.time() - t_start
    print(f"\nExecution Time: {execution_time * 1000} ms")
    print_dwarf_positions(dwarfs_at_start, dwarfs_at_finish, dwarfs_done)
    return total_time, scheme


def main():
    """Starts the execution and presents the result when done."""
    global cross_losses, return_times
    time_for_crossing, scheme = greedy_min_crossing(NUMBER_OF_DWARFS, MAX_CROSSINGS, dwarf.START, MAX_TOGETHER)
    print(f"Total time for all dwarfs crossing the bridge: {time_for_crossing}")
    print(scheme)
    print("=============================================\n")
    print(f"Crossing Losses:\n{cross_losses}")
    print(f"Average Loss: {sum(cross_losses) / len(cross_losses)}\n")
    print(f"Return Times:\n{return_times}")
    print(f"Total Return Time: {sum(return_times)}")
    print(f"Average Return Time: {sum(return_times) / len(return_times)}\n")
    print("----------------------------------------------------------------------------------------------\n")


if __name__ == '__main__':
    main()
