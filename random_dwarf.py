from dwarf import Dwarf
import dwarf
import random
import copy
import matplotlib.pyplot as plt
import numpy as np
import time


NUMBER_OF_TRIES = 1000
NUMBER_OF_DWARFS = 300
MAX_CROSSINGS = 3
MAX_TOGETHER = 2


def random_crossing(tries, num_of_dwarfs, max_crossings, start_pos, max_together):
    dwarfs = []
    for dwarf_nr in range(1, num_of_dwarfs+1):
        dwarfs.append(Dwarf(dwarf_nr, dwarf_nr, 0, max_crossings, start_pos))

    best_times = []
    best_scheme = []
    for try_nr in range(1, tries + 1):
        scheme = []
        total_time = 0
        dwarfs_at_start = copy.deepcopy(dwarfs)  # List of dwarfs at start position
        dwarfs_at_finish = []                    # List of dwarfs at finish with crossings left
        dwarfs_done = []                         # List of dwarfs at finish with no crossings left
        while len(dwarfs_at_start) > 0:        # Keep going until there are no more dwarfs at start to cross the bridge
            crossing_time = 0
            crossing_dwarfs = []
            for _ in range(min(max_together, len(dwarfs_at_start))):
                crossing_dwarf = dwarfs_at_start.pop(random.randint(0, len(dwarfs_at_start) - 1))
                crossing_time = crossing_dwarf & crossing_time
                crossing_dwarf.cross()
                crossing_dwarfs.append(crossing_dwarf.dwarf_nr)
                if crossing_dwarf.done():
                    dwarfs_done.append(crossing_dwarf)
                else:
                    dwarfs_at_finish.append(crossing_dwarf)
            total_time += crossing_time
            if crossing_dwarfs:
                crossing_dwarfs.append("cross")
                scheme.append(crossing_dwarfs)
            if dwarfs_at_finish and dwarfs_at_start:
                returning_dwarf = dwarfs_at_finish.pop(random.randint(0, len(dwarfs_at_finish) - 1))
                returning_dwarf.go_back()
                dwarfs_at_start.append(returning_dwarf)
                total_time += returning_dwarf.time_needed_for_crossing()
                scheme.append([returning_dwarf.dwarf_nr, "go back"])
        if best_times == [] or total_time < best_times[-1][1]:
            best_times.append([try_nr, total_time])
            best_scheme = copy.deepcopy(scheme)
    return best_times, best_scheme


def main():
    t1 = time.time()
    for _ in range(25):
        times, scheme = random_crossing(NUMBER_OF_TRIES, NUMBER_OF_DWARFS, MAX_CROSSINGS, dwarf.START, MAX_TOGETHER)
        print(times)
        print("=============================================\n")
        print(scheme)
        print()
        t = np.array(times)
        plt.plot(t[:, 0], t[:, 1])
    print(f"Time used for the program: {time.time() - t1:.3f} seconds\n")
    plt.show()


if __name__ == '__main__':
    main()
