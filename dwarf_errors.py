

class DwarfErrors(Exception):
    pass


class DwarfCrossingError(DwarfErrors):

    def __init__(self, dwarf_nr, to_pos, reason):
        self.dwarf_nr = dwarf_nr
        self.to_pos = to_pos
        self.reason = reason
        message = f"\nDwarf number {dwarf_nr} can't cross the bridge to go to {to_pos}, since {reason}"
        super().__init__(message)


class DwarfStartingPositionError(DwarfErrors):

    def __init__(self, dwarf_nr, pos, reason):
        self.dwarf_nr = dwarf_nr
        self.pos = pos
        self.reason = reason
        message = f"\nDwarf number {dwarf_nr} cannot start at {pos}, since {reason}"
        super().__init__(message)
