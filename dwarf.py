from dwarf_errors import DwarfCrossingError, DwarfStartingPositionError


MAX_CROSSINGS = 3
START = "start"
FINISH = "finish"


class Lantern:
    """Provides lanterns that can be carried by the dwarfs when crossing the bridge."""

    def __init__(self, pos=START):
        """Creates a lantern at the position specified."""
        self.pos = pos

    def move_lantern(self, to_pos):
        """Moves the lantern to the specified position."""
        self.pos = to_pos

    def at_pos(self, pos):
        """Returns True if the lantern is at the specifies position. Otherwise False."""
        return pos == self.pos


class Dwarf:
    """Provides dwarfs with the abilities needed for the dwarfs crossing problem."""

    def __init__(self, dwarf_nr, crossing_time, crossings=0, max_crossings=MAX_CROSSINGS, pos=START):
        """Creates a dwarf with an id number and the properties given."""
        self.dwarf_nr = dwarf_nr
        self.crossing_time = crossing_time
        self.crossings = crossings
        self.max_crossings = max_crossings
        self.pos = pos
        if pos not in [START, FINISH]:
            reason = f"the dwarf does not know where {pos} is. \n" \
                     f"The dwarf only knows where {START} and {FINISH} is, but is told to start at {pos}.\n" \
                     f"No dwarf was created."
            raise DwarfStartingPositionError(dwarf_nr, pos, reason)

    def travel_to(self, to_pos, lantern):
        """Facilitates the move of a dwarf from current position to a different position, with the option to
           bring a lantern to this position."""
        if self.done():
            reason = f"the dwarf already crossed the bridge {self.crossings} times.\n" \
                     f"{self.crossings} crossings out of {self.max_crossings} used"
            raise DwarfCrossingError(self.dwarf_nr, to_pos, reason)
        elif self.pos == to_pos:
            reason = f"the dwarf is already at {self.pos}"
            raise DwarfCrossingError(self.dwarf_nr, to_pos, reason)
        elif to_pos not in [START, FINISH]:
            reason = f"the dwarf does not know where {to_pos} is. \n" \
                     f"The dwarf only knows how to go to {START} and {FINISH}, but is told to go to {to_pos}"
            raise DwarfCrossingError(self.dwarf_nr, to_pos, reason)
        else:
            self += 1
            self.pos = to_pos
            if lantern:
                self.bring_lantern(lantern, to_pos)
            return True

    def cross(self, lantern=None):
        """Facilitates the dwarf crossing the bridge to the finish position."""
        return self.travel_to(FINISH, lantern)

    def go_back(self, lantern=None):
        """Facilitates the dwarf going back over the bridge, returning to the start position."""
        return self.travel_to(START, lantern)

    def bring_lantern(self, lantern, to_pos):
        """Allows the dwarf to bring a lantern when crossing or going back over the bridge."""
        lantern.move_lantern(to_pos)

    def done(self):
        """Returns True if the dwarf has used up all the crossing and are done moving."""
        return self.crossings >= self.max_crossings

    def at_start(self):
        """Returns True if the dwarf is at the start."""
        return self.pos == START

    def at_finish(self):
        """Returns True if the dwarf has crossed the bridge and is at the finish."""
        return self.pos == FINISH

    def number(self):
        """Returns the dwarf's id number."""
        return self.dwarf_nr

    def time_needed_for_crossing(self):
        """Returns the time the dwarf needs for walking over the bridge in either direction."""
        return self.crossing_time

    def times_crossed(self):
        """Returns how many times the dwarf has walked over the bridge in any direction."""
        return self.crossings

    def what_am_i(self):
        """Returns what kind of object the dwarf is. Hopefully a dwarf object. Otherwise we are in trouble..."""
        print(type(self))
        if isinstance(self, Dwarf):
            print("HURRA!!! I am a dwarf!")
        else:
            print("Hmmm... Who am I?")

    def __add__(self, other):
        """Adds and returns the crossing time of two dwarfs, or a dwarf and any number."""
        if isinstance(other, Dwarf):
            other = other.crossing_time
        return self.crossing_time + other

    def __sub__(self, other):
        """Subtracts and returns the crossing time between two dwarfs, or between a dwarf and any number."""
        if isinstance(other, Dwarf):
            other = other.crossing_time
        return self.crossing_time - other

    def __mul__(self, other):
        """Multiplies and returns the crossing time between two dwarfs, or between a dwarf and any number."""
        if isinstance(other, Dwarf):
            other = other.crossing_time
        return self.crossing_time * other

    def __truediv__(self, other):
        """Divides and returns the crossing times between two dwarfs, or between a dwarf and any number."""
        if isinstance(other, Dwarf):
            other = other.crossing_time
        return self.crossing_time / other

    def __floordiv__(self, other):
        """Does a floor division and returns the resulting integer from that division between two dwarfs, or
           between a dwarf and any number."""
        if isinstance(other, Dwarf):
            other = other.crossing_time
        return self.crossing_time // other

    def __and__(self, other):
        """Returns the higher crossing time (i.e. slower pace) for two dwarfs walking together."""
        if isinstance(other, Dwarf):
            other = other.crossing_time
        return max(self.crossing_time, other)

    def __lt__(self, other):
        """Returns True if the crossing time of the dwarf to the left of the operator is less than the crossing time
           of the dwarf to the right, or any number."""
        if isinstance(other, Dwarf):
            other = other.crossing_time
        return self.crossing_time < other

    def __gt__(self, other):
        """Returns True if the crossing time of the dwarf to the left of the operator is greater than the crossing time
                   of the dwarf to the right, or any number."""
        if isinstance(other, Dwarf):
            other = other.crossing_time
        return self.crossing_time > other

    def __le__(self, other):
        """Returns True if the crossing time of the dwarf to the left of the operator is less than or equal to
           the crossing time of the dwarf to the right, or any number."""
        if isinstance(other, Dwarf):
            other = other.crossing_time
        return self.crossing_time <= other

    def __ge__(self, other):
        """Returns True if the crossing time of the dwarf to the left of the operator is greater than or equal to
           the crossing time of the dwarf to the right, or any number."""
        if isinstance(other, Dwarf):
            other = other.crossing_time
        return self.crossing_time >= other

    def __eq__(self, other):
        """Returns True if the crossing time of the dwarf to the left of the operator is equal to
           the crossing time of the dwarf to the right, or any number."""
        if isinstance(other, Dwarf):
            other = other.crossing_time
        return self.crossing_time == other

    def __ne__(self, other):
        """Returns True if the crossing time of the dwarf to the left of the operator is not equal to
           the crossing time of the dwarf to the right, or any number."""
        if isinstance(other, Dwarf):
            other = other.crossing_time
        return self.crossing_time != other

    def __isub__(self, other):
        """Decreases the dwarfs number of crossings with the numerical expression to the right of the operator."""
        self.crossings -= other
        return self

    def __iadd__(self, other):
        """Increases the dwarfs number of crossings with the numerical expression to the right of the operator."""
        self.crossings += other
        return self

    def __imul__(self, other):
        """Multiplies the dwarfs number of crossings with the numerical expression to the right of the operator."""
        self.crossings *= other
        return self

    def __itruediv__(self, other):
        """Divides the dwarfs number of crossings with the numerical expression to the right of the operator."""
        self.crossings /= other
        return self

    def __ifloordiv__(self, other):
        """Floor divides the dwarfs number of crossings with the numerical expression to the right of the operator."""
        self.crossings //= other
        return self

    def __neg__(self):
        """Returns the dwarfs crossing time negated."""
        return -self.crossing_time

    def __pos__(self):
        """Returns the dwarfs crossing time"""
        return self.crossing_time
