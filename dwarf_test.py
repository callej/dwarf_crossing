import unittest
import dwarf
from dwarf import Dwarf, Lantern
from dwarf_errors import DwarfCrossingError, DwarfStartingPositionError
import copy
from random import randint, random


NUMBER_OF_TRIES = 10
NUMBER_OF_DWARFS = 30
MAX_CROSSINGS = 3
START = "start"
FINISH = "finish"

dwarfs = []


def setUpModule():
    # print(f'Run before any test in this module')
    global dwarfs
    for dwarf_nr in range(1, NUMBER_OF_DWARFS + 1):
        dwarfs.append(Dwarf(dwarf_nr, dwarf_nr, 0, MAX_CROSSINGS, START))

# def tearDownModule():
#     print(f'Run after last test in this module')


class DwarfTests(unittest.TestCase):

    # @classmethod
    # def setUpClass(cls) -> None:
    #     print(f'Run before the first test in this class (DwarfTests) is run')

    # @classmethod
    # def tearDownClass(cls) -> None:
    #     print(f'Run after the last test in this class (DwarfTests) is run')

    def setUp(self) -> None:
        # print(f'Run before each test in DwarfTests')
        global dwarfs
        self.dwarfs_at_start = copy.deepcopy(dwarfs)

    # def tearDown(self) -> None:
    #     print(f'Run after each test in DwarfTests')

    # def test_something(self):
    #     self.assertEqual(True, True)  # add assertion here

    def test_dwarf_instance(self):
        self.assertIsInstance(self.dwarfs_at_start[0], Dwarf)
        self.assertEqual(self.dwarfs_at_start[0].dwarf_nr, 1)
        self.assertEqual(self.dwarfs_at_start[0].crossing_time, 1)
        self.assertEqual(self.dwarfs_at_start[0].crossings, 0)
        self.assertEqual(self.dwarfs_at_start[0].max_crossings, MAX_CROSSINGS)
        self.assertEqual(self.dwarfs_at_start[0].pos, START)

    def test_dwarf_instances(self):
        num = 0
        for dwarf1 in self.dwarfs_at_start:
            num += 1
            self.assertIsInstance(dwarf1, Dwarf)
            self.assertEqual(dwarf1.dwarf_nr, num)
            self.assertEqual(dwarf1.number(), num)
            self.assertEqual(dwarf1.crossing_time, num)
            self.assertEqual(dwarf1.time_needed_for_crossing(), num)
            self.assertEqual(dwarf1.crossings, 0)
            self.assertEqual(dwarf1.times_crossed(), 0)
            self.assertEqual(dwarf1.max_crossings, MAX_CROSSINGS)
            self.assertEqual(dwarf1.pos, START)

    def test_dwarf_class(self):
        self.assertIs(type(self.dwarfs_at_start[0]), Dwarf)

    def test_dwarfs_class(self):
        for dwarf1 in self.dwarfs_at_start:
            self.assertIs(type(dwarf1), Dwarf)

    def test_default_dwarf_1(self):
        dwarf1 = Dwarf(738, 391)
        self.assertIsInstance(dwarf1, Dwarf)
        self.assertEqual(dwarf1.dwarf_nr, 738)
        self.assertEqual(dwarf1.number(), 738)
        self.assertEqual(dwarf1.crossing_time, 391)
        self.assertEqual(dwarf1.time_needed_for_crossing(), 391)
        self.assertEqual(dwarf1.crossings, 0)
        self.assertEqual(dwarf1.times_crossed(), 0)
        self.assertEqual(dwarf1.max_crossings, dwarf.MAX_CROSSINGS)
        self.assertEqual(dwarf1.pos, START)

    def test_at_start_1(self):
        for dwarf1 in self.dwarfs_at_start:
            self.assertTrue(dwarf1.at_start())
            self.assertFalse(dwarf1.at_finish())

    @unittest.skipUnless(MAX_CROSSINGS >= 2, f"This test only makes sense if MAX_CROSSINGS >= 2.\n"
                                             f"MAX_CROSSINGS is {MAX_CROSSINGS}")
    def test_at_start_2(self):
        for dwarf1 in self.dwarfs_at_start:
            dwarf1.cross()
            dwarf1.go_back()
            self.assertTrue(dwarf1.at_start())
            self.assertFalse(dwarf1.at_finish())
            self.assertEqual(dwarf1.times_crossed(), 2)

    @unittest.skipUnless(MAX_CROSSINGS == 3, f"This test only makes sense if MAX_CROSSINGS == 3.\n"
                                         f"MAX_CROSSINGS is {MAX_CROSSINGS}")
    def test_at_start_3(self):
        for dwarf1 in self.dwarfs_at_start:
            dwarf1.cross()
            dwarf1.go_back()
            dwarf1.cross()
            with self.assertRaises(DwarfCrossingError) as cm:
                dwarf1.go_back()
            self.assertFalse(dwarf1.at_start())
            self.assertTrue(dwarf1.at_finish())
            self.assertEqual(dwarf1.times_crossed(), 3)
            reason = f"the dwarf already crossed the bridge {MAX_CROSSINGS} times.\n" \
                     f"{dwarf1.crossings} crossings out of {dwarf1.max_crossings} used"
            message = f"\nDwarf number {dwarf1.dwarf_nr} can't cross the bridge to go to {START}, since {reason}"
            self.assertEqual(str(cm.exception), message)
            self.assertEqual(cm.exception.args[0], message)
            self.assertEqual(cm.exception.dwarf_nr, dwarf1.dwarf_nr)
            self.assertEqual(cm.exception.to_pos, dwarf.START)
            self.assertEqual(cm.exception.reason, reason)

    @unittest.skipUnless(MAX_CROSSINGS >= 1, f"This test only makes sense if MAX_CROSSINGS >= 1.\n"
                                             f"MAX_CROSSINGS is {MAX_CROSSINGS}")
    def test_at_finish_1(self):
        for dwarf1 in self.dwarfs_at_start:
            dwarf1.cross()
            self.assertFalse(dwarf1.at_start())
            self.assertTrue(dwarf1.at_finish())
            self.assertEqual(dwarf1.times_crossed(), 1)

    @unittest.skipUnless(MAX_CROSSINGS >= 3, f"This test only makes sense if MAX_CROSSINGS >= 3.\n"
                                             f"MAX_CROSSINGS is {MAX_CROSSINGS}")
    def test_at_finish_2(self):
        for dwarf1 in self.dwarfs_at_start:
            dwarf1.cross()
            dwarf1.go_back()
            dwarf1.cross()
            self.assertFalse(dwarf1.at_start())
            self.assertTrue(dwarf1.at_finish())
            self.assertEqual(dwarf1.times_crossed(), 3)

    def test_exception_1(self):
        dwarf1 = Dwarf(1, 1, 0, 3, dwarf.START)
        dwarf1.cross()
        dwarf1.go_back()
        dwarf1.cross()
        with self.assertRaises(DwarfCrossingError) as cm:
            dwarf1.go_back()
        self.assertFalse(dwarf1.at_start())
        self.assertTrue(dwarf1.at_finish())
        self.assertEqual(dwarf1.times_crossed(), 3)
        reason = f"the dwarf already crossed the bridge {dwarf1.crossings} times.\n" \
                 f"{dwarf1.crossings} crossings out of {dwarf1.max_crossings} used"
        message = f"\nDwarf number {dwarf1.dwarf_nr} can't cross the bridge to go to {dwarf.START}, since {reason}"
        self.assertEqual(str(cm.exception), message)
        self.assertEqual(cm.exception.args[0], message)
        self.assertEqual(cm.exception.dwarf_nr, dwarf1.dwarf_nr)
        self.assertEqual(cm.exception.to_pos, dwarf.START)
        self.assertEqual(cm.exception.reason, reason)
        self.assertNotEqual(cm.exception.to_pos, dwarf1.pos)

    def test_exception_2(self):
        dwarf1 = Dwarf(1, 1, 0, 0, dwarf.START)
        with self.assertRaises(DwarfCrossingError) as cm:
            dwarf1.cross()
        self.assertTrue(dwarf1.at_start())
        self.assertFalse(dwarf1.at_finish())
        self.assertEqual(dwarf1.times_crossed(), 0)
        reason = f"the dwarf already crossed the bridge {dwarf1.crossings} times.\n" \
                 f"{dwarf1.crossings} crossings out of {dwarf1.max_crossings} used"
        message = f"\nDwarf number {dwarf1.dwarf_nr} can't cross the bridge to go to {dwarf.FINISH}, since {reason}"
        self.assertEqual(str(cm.exception), message)
        self.assertEqual(cm.exception.args[0], message)
        self.assertEqual(cm.exception.dwarf_nr, dwarf1.dwarf_nr)
        self.assertEqual(cm.exception.to_pos, dwarf.FINISH)
        self.assertEqual(cm.exception.reason, reason)
        self.assertNotEqual(cm.exception.to_pos, dwarf1.pos)

    def test_exception_3(self):
        dwarf1 = Dwarf(1, 1, 0, 1, dwarf.START)
        dwarf1.cross()
        with self.assertRaises(DwarfCrossingError) as cm:
            dwarf1.go_back()
        self.assertFalse(dwarf1.at_start())
        self.assertTrue(dwarf1.at_finish())
        self.assertEqual(dwarf1.times_crossed(), 1)
        reason = f"the dwarf already crossed the bridge {dwarf1.crossings} times.\n" \
                 f"{dwarf1.crossings} crossings out of {dwarf1.max_crossings} used"
        message = f"\nDwarf number {dwarf1.dwarf_nr} can't cross the bridge to go to {dwarf.START}, since {reason}"
        self.assertEqual(str(cm.exception), message)
        self.assertEqual(cm.exception.args[0], message)
        self.assertEqual(cm.exception.dwarf_nr, dwarf1.dwarf_nr)
        self.assertEqual(cm.exception.to_pos, dwarf.START)
        self.assertEqual(cm.exception.reason, reason)
        self.assertNotEqual(cm.exception.to_pos, dwarf1.pos)

    def test_exception_4(self):
        dwarf1 = Dwarf(1, 1, 0, 2, dwarf.START)
        dwarf1.cross()
        dwarf1.go_back()
        with self.assertRaises(DwarfCrossingError) as cm:
            dwarf1.cross()
        self.assertTrue(dwarf1.at_start())
        self.assertFalse(dwarf1.at_finish())
        self.assertEqual(dwarf1.times_crossed(), 2)
        reason = f"the dwarf already crossed the bridge {dwarf1.crossings} times.\n" \
                 f"{dwarf1.crossings} crossings out of {dwarf1.max_crossings} used"
        message = f"\nDwarf number {dwarf1.dwarf_nr} can't cross the bridge to go to {dwarf.FINISH}, since {reason}"
        self.assertEqual(str(cm.exception), message)
        self.assertEqual(cm.exception.args[0], message)
        self.assertEqual(cm.exception.dwarf_nr, dwarf1.dwarf_nr)
        self.assertEqual(cm.exception.to_pos, dwarf.FINISH)
        self.assertEqual(cm.exception.reason, reason)
        self.assertNotEqual(cm.exception.to_pos, dwarf1.pos)

    def test_exception_5(self):
        dwarf1 = Dwarf(1, 1, 0, 4, dwarf.START)
        dwarf1.cross()
        dwarf1.go_back()
        dwarf1.cross()
        dwarf1.go_back()
        with self.assertRaises(DwarfCrossingError) as cm:
            dwarf1.cross()
        self.assertTrue(dwarf1.at_start())
        self.assertFalse(dwarf1.at_finish())
        self.assertEqual(dwarf1.times_crossed(), 4)
        reason = f"the dwarf already crossed the bridge {dwarf1.crossings} times.\n" \
                 f"{dwarf1.crossings} crossings out of {dwarf1.max_crossings} used"
        message = f"\nDwarf number {dwarf1.dwarf_nr} can't cross the bridge to go to {dwarf.FINISH}, since {reason}"
        self.assertEqual(str(cm.exception), message)
        self.assertEqual(cm.exception.args[0], message)
        self.assertEqual(cm.exception.dwarf_nr, dwarf1.dwarf_nr)
        self.assertEqual(cm.exception.to_pos, dwarf.FINISH)
        self.assertEqual(cm.exception.reason, reason)
        self.assertNotEqual(cm.exception.to_pos, dwarf1.pos)

    def test_exception_6(self):
        dwarf1 = Dwarf(1, 1, 0, 5, dwarf.START)
        dwarf1.cross()
        dwarf1.go_back()
        dwarf1.cross()
        dwarf1.go_back()
        dwarf1.cross()
        with self.assertRaises(DwarfCrossingError) as cm:
            dwarf1.go_back()
        self.assertFalse(dwarf1.at_start())
        self.assertTrue(dwarf1.at_finish())
        self.assertEqual(dwarf1.times_crossed(), 5)
        reason = f"the dwarf already crossed the bridge {dwarf1.crossings} times.\n" \
                 f"{dwarf1.crossings} crossings out of {dwarf1.max_crossings} used"
        message = f"\nDwarf number {dwarf1.dwarf_nr} can't cross the bridge to go to {dwarf.START}, since {reason}"
        self.assertEqual(str(cm.exception), message)
        self.assertEqual(cm.exception.args[0], message)
        self.assertEqual(cm.exception.dwarf_nr, dwarf1.dwarf_nr)
        self.assertEqual(cm.exception.to_pos, dwarf.START)
        self.assertEqual(cm.exception.reason, reason)
        self.assertNotEqual(cm.exception.to_pos, dwarf1.pos)

    def test_exception_7(self):
        dwarf1 = Dwarf(3, 8, 0, 3, dwarf.START)
        dwarf1.cross()
        dwarf1.go_back()
        dwarf1.cross()
        with self.assertRaises(DwarfCrossingError) as cm:
            dwarf1.go_back()
        self.assertFalse(dwarf1.at_start())
        self.assertTrue(dwarf1.at_finish())
        self.assertEqual(dwarf1.times_crossed(), 3)
        reason = f"the dwarf already crossed the bridge {dwarf1.crossings} times.\n" \
                 f"{dwarf1.crossings} crossings out of {dwarf1.max_crossings} used"
        message = f"\nDwarf number {dwarf1.dwarf_nr} can't cross the bridge to go to {dwarf.START}, since {reason}"
        self.assertEqual(str(cm.exception), message)
        self.assertEqual(cm.exception.args[0], message)
        self.assertEqual(cm.exception.dwarf_nr, dwarf1.dwarf_nr)
        self.assertEqual(cm.exception.to_pos, dwarf.START)
        self.assertEqual(cm.exception.reason, reason)
        self.assertNotEqual(cm.exception.to_pos, dwarf1.pos)

    def test_exception_8(self):
        dwarf1 = Dwarf(923, 138, 0, 3, dwarf.START)
        dwarf1.cross()
        dwarf1.go_back()
        dwarf1.cross()
        with self.assertRaises(DwarfCrossingError) as cm:
            dwarf1.go_back()
        self.assertFalse(dwarf1.at_start())
        self.assertTrue(dwarf1.at_finish())
        self.assertEqual(dwarf1.times_crossed(), 3)
        reason = f"the dwarf already crossed the bridge {dwarf1.crossings} times.\n" \
                 f"{dwarf1.crossings} crossings out of {dwarf1.max_crossings} used"
        message = f"\nDwarf number {dwarf1.dwarf_nr} can't cross the bridge to go to {dwarf.START}, since {reason}"
        self.assertEqual(str(cm.exception), message)
        self.assertEqual(cm.exception.args[0], message)
        self.assertEqual(cm.exception.dwarf_nr, dwarf1.dwarf_nr)
        self.assertEqual(cm.exception.to_pos, dwarf.START)
        self.assertEqual(cm.exception.reason, reason)
        self.assertNotEqual(cm.exception.to_pos, dwarf1.pos)

    def test_exception_9(self):
        dwarf1 = Dwarf(1, 1, 3, 3, dwarf.START)
        with self.assertRaises(DwarfCrossingError) as cm:
            dwarf1.cross()
        self.assertTrue(dwarf1.at_start())
        self.assertFalse(dwarf1.at_finish())
        self.assertEqual(dwarf1.times_crossed(), 3)
        reason = f"the dwarf already crossed the bridge {dwarf1.crossings} times.\n" \
                 f"{dwarf1.crossings} crossings out of {dwarf1.max_crossings} used"
        message = f"\nDwarf number {dwarf1.dwarf_nr} can't cross the bridge to go to {dwarf.FINISH}, since {reason}"
        self.assertEqual(str(cm.exception), message)
        self.assertEqual(cm.exception.args[0], message)
        self.assertEqual(cm.exception.dwarf_nr, dwarf1.dwarf_nr)
        self.assertEqual(cm.exception.to_pos, dwarf.FINISH)
        self.assertEqual(cm.exception.reason, reason)
        self.assertNotEqual(cm.exception.to_pos, dwarf1.pos)

    def test_exception_10(self):
        dwarf1 = Dwarf(1, 1, 17, 3, dwarf.START)
        with self.assertRaises(DwarfCrossingError) as cm:
            dwarf1.cross()
        self.assertTrue(dwarf1.at_start())
        self.assertFalse(dwarf1.at_finish())
        self.assertEqual(dwarf1.times_crossed(), 17)
        reason = f"the dwarf already crossed the bridge {dwarf1.crossings} times.\n" \
                 f"{dwarf1.crossings} crossings out of {dwarf1.max_crossings} used"
        message = f"\nDwarf number {dwarf1.dwarf_nr} can't cross the bridge to go to {dwarf.FINISH}, since {reason}"
        self.assertEqual(str(cm.exception), message)
        self.assertEqual(cm.exception.args[0], message)
        self.assertEqual(cm.exception.dwarf_nr, dwarf1.dwarf_nr)
        self.assertEqual(cm.exception.to_pos, dwarf.FINISH)
        self.assertEqual(cm.exception.reason, reason)
        self.assertNotEqual(cm.exception.to_pos, dwarf1.pos)

    def test_exception_11(self):
        dwarf1 = Dwarf(1, 1, 3, 3, dwarf.FINISH)
        with self.assertRaises(DwarfCrossingError) as cm:
            dwarf1.go_back()
        self.assertFalse(dwarf1.at_start())
        self.assertTrue(dwarf1.at_finish())
        self.assertEqual(dwarf1.times_crossed(), 3)
        reason = f"the dwarf already crossed the bridge {dwarf1.crossings} times.\n" \
                 f"{dwarf1.crossings} crossings out of {dwarf1.max_crossings} used"
        message = f"\nDwarf number {dwarf1.dwarf_nr} can't cross the bridge to go to {dwarf.START}, since {reason}"
        self.assertEqual(str(cm.exception), message)
        self.assertEqual(cm.exception.args[0], message)
        self.assertEqual(cm.exception.dwarf_nr, dwarf1.dwarf_nr)
        self.assertEqual(cm.exception.to_pos, dwarf.START)
        self.assertEqual(cm.exception.reason, reason)
        self.assertNotEqual(cm.exception.to_pos, dwarf1.pos)

    def test_exception_12(self):
        dwarf1 = Dwarf(1, 1, 19, 3, dwarf.FINISH)
        with self.assertRaises(DwarfCrossingError) as cm:
            dwarf1.go_back()
        self.assertFalse(dwarf1.at_start())
        self.assertTrue(dwarf1.at_finish())
        self.assertEqual(dwarf1.times_crossed(), 19)
        reason = f"the dwarf already crossed the bridge {dwarf1.crossings} times.\n" \
                 f"{dwarf1.crossings} crossings out of {dwarf1.max_crossings} used"
        message = f"\nDwarf number {dwarf1.dwarf_nr} can't cross the bridge to go to {dwarf.START}, since {reason}"
        self.assertEqual(str(cm.exception), message)
        self.assertEqual(cm.exception.args[0], message)
        self.assertEqual(cm.exception.dwarf_nr, dwarf1.dwarf_nr)
        self.assertEqual(cm.exception.to_pos, dwarf.START)
        self.assertEqual(cm.exception.reason, reason)
        self.assertNotEqual(cm.exception.to_pos, dwarf1.pos)

    def test_exception_13(self):
        dwarf1 = Dwarf(1, 1, 0, 3, dwarf.START)
        with self.assertRaises(DwarfCrossingError) as cm:
            dwarf1.go_back()
        self.assertTrue(dwarf1.at_start())
        self.assertFalse(dwarf1.at_finish())
        self.assertEqual(dwarf1.times_crossed(), 0)
        reason = f"the dwarf is already at {dwarf1.pos}"
        message = f"\nDwarf number {dwarf1.dwarf_nr} can't cross the bridge to go to {dwarf.START}, since {reason}"
        self.assertEqual(str(cm.exception), message)
        self.assertEqual(cm.exception.args[0], message)
        self.assertEqual(cm.exception.dwarf_nr, dwarf1.dwarf_nr)
        self.assertEqual(cm.exception.to_pos, dwarf.START)
        self.assertEqual(cm.exception.reason, reason)
        self.assertEqual(cm.exception.to_pos, dwarf1.pos)

    def test_exception_14(self):
        dwarf1 = Dwarf(1, 1, 0, 3, dwarf.FINISH)
        with self.assertRaises(DwarfCrossingError) as cm:
            dwarf1.cross()
        self.assertFalse(dwarf1.at_start())
        self.assertTrue(dwarf1.at_finish())
        self.assertEqual(dwarf1.times_crossed(), 0)
        reason = f"the dwarf is already at {dwarf1.pos}"
        message = f"\nDwarf number {dwarf1.dwarf_nr} can't cross the bridge to go to {dwarf.FINISH}, since {reason}"
        self.assertEqual(str(cm.exception), message)
        self.assertEqual(cm.exception.args[0], message)
        self.assertEqual(cm.exception.dwarf_nr, dwarf1.dwarf_nr)
        self.assertEqual(cm.exception.to_pos, dwarf.FINISH)
        self.assertEqual(cm.exception.reason, reason)
        self.assertEqual(cm.exception.to_pos, dwarf1.pos)

    def test_exception_15(self):
        dwarf1 = Dwarf(1, 1, 0, 3, dwarf.START)
        with self.assertRaises(DwarfCrossingError) as cm:
            dwarf1.travel_to("start", Lantern(dwarf.START))
        self.assertTrue(dwarf1.at_start())
        self.assertFalse(dwarf1.at_finish())
        self.assertEqual(dwarf1.times_crossed(), 0)
        reason = f"the dwarf is already at {dwarf1.pos}"
        message = f"\nDwarf number {dwarf1.dwarf_nr} can't cross the bridge to go to {dwarf.START}, since {reason}"
        self.assertEqual(str(cm.exception), message)
        self.assertEqual(cm.exception.args[0], message)
        self.assertEqual(cm.exception.dwarf_nr, dwarf1.dwarf_nr)
        self.assertEqual(cm.exception.to_pos, dwarf.START)
        self.assertEqual(cm.exception.reason, reason)
        self.assertEqual(cm.exception.to_pos, dwarf1.pos)

    def test_exception_16(self):
        dwarf1 = Dwarf(1, 1, 0, 3, dwarf.FINISH)
        with self.assertRaises(DwarfCrossingError) as cm:
            dwarf1.travel_to("finish", Lantern(dwarf.START))
        self.assertFalse(dwarf1.at_start())
        self.assertTrue(dwarf1.at_finish())
        self.assertEqual(dwarf1.times_crossed(), 0)
        reason = f"the dwarf is already at {dwarf1.pos}"
        message = f"\nDwarf number {dwarf1.dwarf_nr} can't cross the bridge to go to {dwarf.FINISH}, since {reason}"
        self.assertEqual(str(cm.exception), message)
        self.assertEqual(cm.exception.args[0], message)
        self.assertEqual(cm.exception.dwarf_nr, dwarf1.dwarf_nr)
        self.assertEqual(cm.exception.to_pos, dwarf.FINISH)
        self.assertEqual(cm.exception.reason, reason)
        self.assertEqual(cm.exception.to_pos, dwarf1.pos)

    def test_exception_17(self):
        new_pos = "home"
        dwarf1 = Dwarf(1, 1, 0, 3, dwarf.START)
        with self.assertRaises(DwarfCrossingError) as cm:
            dwarf1.travel_to(new_pos, Lantern(dwarf.START))
        self.assertTrue(dwarf1.at_start())
        self.assertFalse(dwarf1.at_finish())
        self.assertEqual(dwarf1.times_crossed(), 0)
        reason = f"the dwarf does not know where {new_pos} is. \n" \
                     f"The dwarf only knows how to go to {dwarf.START} and {dwarf.FINISH}, but is told to go to {new_pos}"
        message = f"\nDwarf number {dwarf1.dwarf_nr} can't cross the bridge to go to {new_pos}, since {reason}"
        self.assertEqual(str(cm.exception), message)
        self.assertEqual(cm.exception.args[0], message)
        self.assertEqual(cm.exception.dwarf_nr, dwarf1.dwarf_nr)
        self.assertEqual(cm.exception.to_pos, new_pos)
        self.assertEqual(cm.exception.reason, reason)
        self.assertNotEqual(cm.exception.to_pos, dwarf1.pos)

    def test_exception_18(self):
        new_pos = "home"
        dwarf_nr = 1
        with self.assertRaises(DwarfStartingPositionError) as cm:
            dwarf1 = Dwarf(dwarf_nr, 1, 0, 3, new_pos)
        reason = f"the dwarf does not know where {new_pos} is. \n" \
                 f"The dwarf only knows where {dwarf.START} and {dwarf.FINISH} is, but is told to start at {new_pos}.\n" \
                 f"No dwarf was created."
        message = f"\nDwarf number {dwarf_nr} cannot start at {new_pos}, since {reason}"
        self.assertEqual(str(cm.exception), message)
        self.assertEqual(cm.exception.args[0], message)
        self.assertEqual(cm.exception.dwarf_nr, dwarf_nr)
        self.assertEqual(cm.exception.pos, new_pos)
        self.assertEqual(cm.exception.reason, reason)

    def test_dwarf_done_1(self):
        dwarf1 = Dwarf(1, 1, 0, 3, dwarf.START)
        dwarf1.cross()
        dwarf1.go_back()
        self.assertFalse(dwarf1.done())
        dwarf1.cross()
        self.assertTrue(dwarf1.done())

    def test_dwarf_done_2(self):
        dwarf1 = Dwarf(1, 1, 0, 3, dwarf.FINISH)
        dwarf1.go_back()
        dwarf1.cross()
        self.assertFalse(dwarf1.done())
        dwarf1.go_back()
        self.assertTrue(dwarf1.done())

    def test_dwarf_numbers1(self):
        number_of_dwarfs = 10000
        d_min_nr = -10000
        d_max_nr = 10000
        c_min_time = -10000
        c_max_time = 10000
        tc_min = -10000
        tc_max = 10000
        dwarf_numbers = [(randint(d_min_nr, d_max_nr),
                          randint(c_min_time, c_max_time),
                          randint(tc_min, tc_max),
                          randint(tc_min, tc_max))
                         for _ in range(number_of_dwarfs)]
        test_dwarfs = []
        for (d_num, d_time, tc, max_tc) in dwarf_numbers:
            test_dwarfs.append(Dwarf(d_num, d_time, tc, max_tc, dwarf.START))
        index = 0
        for dwarf1 in test_dwarfs:
            self.assertEqual(dwarf1.number(), dwarf_numbers[index][0])
            self.assertEqual(dwarf1.time_needed_for_crossing(), dwarf_numbers[index][1])
            self.assertEqual(dwarf1.times_crossed(), dwarf_numbers[index][2])
            self.assertEqual(dwarf1.max_crossings, dwarf_numbers[index][3])
            self.assertEqual(dwarf1.pos, dwarf.START)
            index += 1

    def test_dwarf_numbers2(self):
        number_of_dwarfs = 10000
        d_min_nr = -10000
        d_max_nr = 10000
        c_min_time = -10000
        c_max_time = 10000
        tc_min = -10000
        tc_max = 10000
        dwarf_numbers = [(randint(d_min_nr, d_max_nr),
                          randint(c_min_time, c_max_time),
                          randint(tc_min, tc_max),
                          randint(tc_min, tc_max))
                         for _ in range(number_of_dwarfs)]
        test_dwarfs = []
        for (d_num, d_time, tc, max_tc) in dwarf_numbers:
            test_dwarfs.append(Dwarf(d_num, d_time, tc, max_tc, dwarf.FINISH))
        index = 0
        for dwarf1 in test_dwarfs:
            self.assertEqual(dwarf1.number(), dwarf_numbers[index][0])
            self.assertEqual(dwarf1.time_needed_for_crossing(), dwarf_numbers[index][1])
            self.assertEqual(dwarf1.times_crossed(), dwarf_numbers[index][2])
            self.assertEqual(dwarf1.max_crossings, dwarf_numbers[index][3])
            self.assertEqual(dwarf1.pos, dwarf.FINISH)
            index += 1


class DwarfOperatorTestsOld(unittest.TestCase):

    def setUp(self) -> None:
        # print(f'Run before each test in DwarfOperatorTests')
        number_of_dwarfs = 1000
        d_min_nr = -10000
        d_max_nr = 10000
        c_min_time = -10000
        c_max_time = 10000
        tc_min = -10000
        tc_max = 10000
        self.d1_num = [(randint(d_min_nr, d_max_nr),
                        randint(c_min_time, c_max_time),
                        randint(tc_min, tc_max),
                        randint(tc_min, tc_max))
                       for _ in range(number_of_dwarfs)]
        self.d2_num = [(randint(d_min_nr, d_max_nr),
                        randint(c_min_time, c_max_time),
                        randint(tc_min, tc_max),
                        randint(tc_min, tc_max))
                       for _ in range(number_of_dwarfs)]
        self.dwarf_numbers = [(self.d1_num[i], self.d2_num[i]) for i in range(number_of_dwarfs)]
        # test_dwarfs = []
        # for (d1, d2) in self.dwarf_numbers:
        #     dwarf1 = Dwarf(d1[0], d1[1], d1[2], d1[3], dwarf.START)
        #     dwarf2 = Dwarf(d2[0], d2[1], d2[2], d2[3], dwarf.START)
        #     test_dwarfs.append((dwarf1, dwarf2))

    def test_add_1(self):
        test_dwarfs = []
        for (d1, d2) in self.dwarf_numbers:
            dwarf1 = Dwarf(d1[0], d1[1], d1[2], d1[3], dwarf.START)
            dwarf2 = Dwarf(d2[0], d2[1], d2[2], d2[3], dwarf.START)
            test_dwarfs.append((dwarf1, dwarf2))
        index = 0
        for d1d2 in test_dwarfs:
            self.assertEqual(d1d2[0] + d1d2[1], self.d1_num[index][1] + self.d2_num[index][1])
            self.assertEqual(d1d2[0] + 1, self.d1_num[index][1] + 1)
            self.assertEqual(d1d2[0] + 5, self.d1_num[index][1] + 5)
            self.assertEqual(d1d2[0] + 24, self.d1_num[index][1] + 24)
            self.assertEqual(d1d2[0] + 117, self.d1_num[index][1] + 117)
            self.assertEqual(d1d2[1] + 2, self.d2_num[index][1] + 2)
            self.assertEqual(d1d2[1] + 6, self.d2_num[index][1] + 6)
            self.assertEqual(d1d2[1] + 29, self.d2_num[index][1] + 29)
            self.assertEqual(d1d2[1] + 118, self.d2_num[index][1] + 118)
            self.assertEqual(d1d2[0].dwarf_nr, self.d1_num[index][0])
            self.assertEqual(d1d2[1].dwarf_nr, self.d2_num[index][0])
            self.assertEqual(d1d2[0].crossing_time, self.d1_num[index][1])
            self.assertEqual(d1d2[1].crossing_time, self.d2_num[index][1])
            self.assertEqual(d1d2[0].crossings, self.d1_num[index][2])
            self.assertEqual(d1d2[1].crossings, self.d2_num[index][2])
            self.assertEqual(d1d2[0].max_crossings, self.d1_num[index][3])
            self.assertEqual(d1d2[1].max_crossings, self.d2_num[index][3])
            self.assertEqual(d1d2[0].pos, dwarf.START)
            self.assertEqual(d1d2[1].pos, dwarf.START)
            index += 1

    def test_add_2(self):
        test_dwarfs = []
        for (d1, d2) in self.dwarf_numbers:
            dwarf1 = Dwarf(d1[0], d1[1], d1[2], d1[3], dwarf.FINISH)
            dwarf2 = Dwarf(d2[0], d2[1], d2[2], d2[3], dwarf.FINISH)
            test_dwarfs.append((dwarf1, dwarf2))
        index = 0
        for d1d2 in test_dwarfs:
            self.assertEqual(d1d2[0] + d1d2[1], self.d1_num[index][1] + self.d2_num[index][1])
            self.assertEqual(d1d2[0] + 1, self.d1_num[index][1] + 1)
            self.assertEqual(d1d2[0] + 5, self.d1_num[index][1] + 5)
            self.assertEqual(d1d2[0] + 24, self.d1_num[index][1] + 24)
            self.assertEqual(d1d2[0] + 117, self.d1_num[index][1] + 117)
            self.assertEqual(d1d2[1] + 2, self.d2_num[index][1] + 2)
            self.assertEqual(d1d2[1] + 6, self.d2_num[index][1] + 6)
            self.assertEqual(d1d2[1] + 29, self.d2_num[index][1] + 29)
            self.assertEqual(d1d2[1] + 118, self.d2_num[index][1] + 118)
            self.assertEqual(d1d2[0].dwarf_nr, self.d1_num[index][0])
            self.assertEqual(d1d2[1].dwarf_nr, self.d2_num[index][0])
            self.assertEqual(d1d2[0].crossing_time, self.d1_num[index][1])
            self.assertEqual(d1d2[1].crossing_time, self.d2_num[index][1])
            self.assertEqual(d1d2[0].crossings, self.d1_num[index][2])
            self.assertEqual(d1d2[1].crossings, self.d2_num[index][2])
            self.assertEqual(d1d2[0].max_crossings, self.d1_num[index][3])
            self.assertEqual(d1d2[1].max_crossings, self.d2_num[index][3])
            self.assertEqual(d1d2[0].pos, dwarf.FINISH)
            self.assertEqual(d1d2[1].pos, dwarf.FINISH)
            index += 1

    def test_sub_1(self):
        test_dwarfs = []
        for (d1, d2) in self.dwarf_numbers:
            dwarf1 = Dwarf(d1[0], d1[1], d1[2], d1[3], dwarf.START)
            dwarf2 = Dwarf(d2[0], d2[1], d2[2], d2[3], dwarf.START)
            test_dwarfs.append((dwarf1, dwarf2))
        index = 0
        for d1d2 in test_dwarfs:
            self.assertEqual(d1d2[0] - d1d2[1], self.d1_num[index][1] - self.d2_num[index][1])
            self.assertEqual(d1d2[0] - 1, self.d1_num[index][1] - 1)
            self.assertEqual(d1d2[0] - 5, self.d1_num[index][1] - 5)
            self.assertEqual(d1d2[0] - 24, self.d1_num[index][1] - 24)
            self.assertEqual(d1d2[0] - 117, self.d1_num[index][1] - 117)
            self.assertEqual(d1d2[1] - 2, self.d2_num[index][1] - 2)
            self.assertEqual(d1d2[1] - 6, self.d2_num[index][1] - 6)
            self.assertEqual(d1d2[1] - 29, self.d2_num[index][1] - 29)
            self.assertEqual(d1d2[1] - 118, self.d2_num[index][1] - 118)
            self.assertEqual(d1d2[0].dwarf_nr, self.d1_num[index][0])
            self.assertEqual(d1d2[1].dwarf_nr, self.d2_num[index][0])
            self.assertEqual(d1d2[0].crossing_time, self.d1_num[index][1])
            self.assertEqual(d1d2[1].crossing_time, self.d2_num[index][1])
            self.assertEqual(d1d2[0].crossings, self.d1_num[index][2])
            self.assertEqual(d1d2[1].crossings, self.d2_num[index][2])
            self.assertEqual(d1d2[0].max_crossings, self.d1_num[index][3])
            self.assertEqual(d1d2[1].max_crossings, self.d2_num[index][3])
            self.assertEqual(d1d2[0].pos, dwarf.START)
            self.assertEqual(d1d2[1].pos, dwarf.START)
            index += 1

    def test_sub_2(self):
        test_dwarfs = []
        for (d1, d2) in self.dwarf_numbers:
            dwarf1 = Dwarf(d1[0], d1[1], d1[2], d1[3], dwarf.FINISH)
            dwarf2 = Dwarf(d2[0], d2[1], d2[2], d2[3], dwarf.FINISH)
            test_dwarfs.append((dwarf1, dwarf2))
        index = 0
        for d1d2 in test_dwarfs:
            self.assertEqual(d1d2[0] - d1d2[1], self.d1_num[index][1] - self.d2_num[index][1])
            self.assertEqual(d1d2[0] - 1, self.d1_num[index][1] - 1)
            self.assertEqual(d1d2[0] - 5, self.d1_num[index][1] - 5)
            self.assertEqual(d1d2[0] - 24, self.d1_num[index][1] - 24)
            self.assertEqual(d1d2[0] - 117, self.d1_num[index][1] - 117)
            self.assertEqual(d1d2[1] - 2, self.d2_num[index][1] - 2)
            self.assertEqual(d1d2[1] - 6, self.d2_num[index][1] - 6)
            self.assertEqual(d1d2[1] - 29, self.d2_num[index][1] - 29)
            self.assertEqual(d1d2[1] - 118, self.d2_num[index][1] - 118)
            self.assertEqual(d1d2[0].dwarf_nr, self.d1_num[index][0])
            self.assertEqual(d1d2[1].dwarf_nr, self.d2_num[index][0])
            self.assertEqual(d1d2[0].crossing_time, self.d1_num[index][1])
            self.assertEqual(d1d2[1].crossing_time, self.d2_num[index][1])
            self.assertEqual(d1d2[0].crossings, self.d1_num[index][2])
            self.assertEqual(d1d2[1].crossings, self.d2_num[index][2])
            self.assertEqual(d1d2[0].max_crossings, self.d1_num[index][3])
            self.assertEqual(d1d2[1].max_crossings, self.d2_num[index][3])
            self.assertEqual(d1d2[0].pos, dwarf.FINISH)
            self.assertEqual(d1d2[1].pos, dwarf.FINISH)
            index += 1

    def test_mul_1(self):
        test_dwarfs = []
        for (d1, d2) in self.dwarf_numbers:
            dwarf1 = Dwarf(d1[0], d1[1], d1[2], d1[3], dwarf.START)
            dwarf2 = Dwarf(d2[0], d2[1], d2[2], d2[3], dwarf.START)
            test_dwarfs.append((dwarf1, dwarf2))
        index = 0
        for d1d2 in test_dwarfs:
            self.assertEqual(d1d2[0] * d1d2[1], self.d1_num[index][1] * self.d2_num[index][1])
            self.assertEqual(d1d2[0] * 1, self.d1_num[index][1] * 1)
            self.assertEqual(d1d2[0] * 5, self.d1_num[index][1] * 5)
            self.assertEqual(d1d2[0] * 24, self.d1_num[index][1] * 24)
            self.assertEqual(d1d2[0] * 117, self.d1_num[index][1] * 117)
            self.assertEqual(d1d2[1] * 2, self.d2_num[index][1] * 2)
            self.assertEqual(d1d2[1] * 6, self.d2_num[index][1] * 6)
            self.assertEqual(d1d2[1] * 29, self.d2_num[index][1] * 29)
            self.assertEqual(d1d2[1] * 118, self.d2_num[index][1] * 118)
            self.assertEqual(d1d2[0].dwarf_nr, self.d1_num[index][0])
            self.assertEqual(d1d2[1].dwarf_nr, self.d2_num[index][0])
            self.assertEqual(d1d2[0].crossing_time, self.d1_num[index][1])
            self.assertEqual(d1d2[1].crossing_time, self.d2_num[index][1])
            self.assertEqual(d1d2[0].crossings, self.d1_num[index][2])
            self.assertEqual(d1d2[1].crossings, self.d2_num[index][2])
            self.assertEqual(d1d2[0].max_crossings, self.d1_num[index][3])
            self.assertEqual(d1d2[1].max_crossings, self.d2_num[index][3])
            self.assertEqual(d1d2[0].pos, dwarf.START)
            self.assertEqual(d1d2[1].pos, dwarf.START)
            index += 1

    def test_mul_2(self):
        test_dwarfs = []
        for (d1, d2) in self.dwarf_numbers:
            dwarf1 = Dwarf(d1[0], d1[1], d1[2], d1[3], dwarf.FINISH)
            dwarf2 = Dwarf(d2[0], d2[1], d2[2], d2[3], dwarf.FINISH)
            test_dwarfs.append((dwarf1, dwarf2))
        index = 0
        for d1d2 in test_dwarfs:
            self.assertEqual(d1d2[0] * d1d2[1], self.d1_num[index][1] * self.d2_num[index][1])
            self.assertEqual(d1d2[0] * 1, self.d1_num[index][1] * 1)
            self.assertEqual(d1d2[0] * 5, self.d1_num[index][1] * 5)
            self.assertEqual(d1d2[0] * 24, self.d1_num[index][1] * 24)
            self.assertEqual(d1d2[0] * 117, self.d1_num[index][1] * 117)
            self.assertEqual(d1d2[1] * 2, self.d2_num[index][1] * 2)
            self.assertEqual(d1d2[1] * 6, self.d2_num[index][1] * 6)
            self.assertEqual(d1d2[1] * 29, self.d2_num[index][1] * 29)
            self.assertEqual(d1d2[1] * 118, self.d2_num[index][1] * 118)
            self.assertEqual(d1d2[0].dwarf_nr, self.d1_num[index][0])
            self.assertEqual(d1d2[1].dwarf_nr, self.d2_num[index][0])
            self.assertEqual(d1d2[0].crossing_time, self.d1_num[index][1])
            self.assertEqual(d1d2[1].crossing_time, self.d2_num[index][1])
            self.assertEqual(d1d2[0].crossings, self.d1_num[index][2])
            self.assertEqual(d1d2[1].crossings, self.d2_num[index][2])
            self.assertEqual(d1d2[0].max_crossings, self.d1_num[index][3])
            self.assertEqual(d1d2[1].max_crossings, self.d2_num[index][3])
            self.assertEqual(d1d2[0].pos, dwarf.FINISH)
            self.assertEqual(d1d2[1].pos, dwarf.FINISH)
            index += 1

    def test_truediv_1(self):
        test_dwarfs = []
        for (d1, d2) in self.dwarf_numbers:
            dwarf1 = Dwarf(d1[0], d1[1], d1[2], d1[3], dwarf.START)
            dwarf2 = Dwarf(d2[0], d2[1], d2[2], d2[3], dwarf.START)
            test_dwarfs.append((dwarf1, dwarf2))
        index = 0
        for d1d2 in test_dwarfs:
            if d1d2[1].crossing_time != 0:
                self.assertEqual(d1d2[0] / d1d2[1], self.d1_num[index][1] / self.d2_num[index][1])
            self.assertEqual(d1d2[0] / 1, self.d1_num[index][1] / 1)
            self.assertEqual(d1d2[0] / 5, self.d1_num[index][1] / 5)
            self.assertEqual(d1d2[0] / 24, self.d1_num[index][1] / 24)
            self.assertEqual(d1d2[0] / 117, self.d1_num[index][1] / 117)
            self.assertEqual(d1d2[1] / 2, self.d2_num[index][1] / 2)
            self.assertEqual(d1d2[1] / 6, self.d2_num[index][1] / 6)
            self.assertEqual(d1d2[1] / 29, self.d2_num[index][1] / 29)
            self.assertEqual(d1d2[1] / 118, self.d2_num[index][1] / 118)
            self.assertEqual(d1d2[0].dwarf_nr, self.d1_num[index][0])
            self.assertEqual(d1d2[1].dwarf_nr, self.d2_num[index][0])
            self.assertEqual(d1d2[0].crossing_time, self.d1_num[index][1])
            self.assertEqual(d1d2[1].crossing_time, self.d2_num[index][1])
            self.assertEqual(d1d2[0].crossings, self.d1_num[index][2])
            self.assertEqual(d1d2[1].crossings, self.d2_num[index][2])
            self.assertEqual(d1d2[0].max_crossings, self.d1_num[index][3])
            self.assertEqual(d1d2[1].max_crossings, self.d2_num[index][3])
            self.assertEqual(d1d2[0].pos, dwarf.START)
            self.assertEqual(d1d2[1].pos, dwarf.START)
            index += 1

    def test_truediv_2(self):
        test_dwarfs = []
        for (d1, d2) in self.dwarf_numbers:
            dwarf1 = Dwarf(d1[0], d1[1], d1[2], d1[3], dwarf.FINISH)
            dwarf2 = Dwarf(d2[0], d2[1], d2[2], d2[3], dwarf.FINISH)
            test_dwarfs.append((dwarf1, dwarf2))
        index = 0
        for d1d2 in test_dwarfs:
            if d1d2[1].crossing_time != 0:
                self.assertEqual(d1d2[0] / d1d2[1], self.d1_num[index][1] / self.d2_num[index][1])
            self.assertEqual(d1d2[0] / 1, self.d1_num[index][1] / 1)
            self.assertEqual(d1d2[0] / 5, self.d1_num[index][1] / 5)
            self.assertEqual(d1d2[0] / 24, self.d1_num[index][1] / 24)
            self.assertEqual(d1d2[0] / 117, self.d1_num[index][1] / 117)
            self.assertEqual(d1d2[1] / 2, self.d2_num[index][1] / 2)
            self.assertEqual(d1d2[1] / 6, self.d2_num[index][1] / 6)
            self.assertEqual(d1d2[1] / 29, self.d2_num[index][1] / 29)
            self.assertEqual(d1d2[1] / 118, self.d2_num[index][1] / 118)
            self.assertEqual(d1d2[0].dwarf_nr, self.d1_num[index][0])
            self.assertEqual(d1d2[1].dwarf_nr, self.d2_num[index][0])
            self.assertEqual(d1d2[0].crossing_time, self.d1_num[index][1])
            self.assertEqual(d1d2[1].crossing_time, self.d2_num[index][1])
            self.assertEqual(d1d2[0].crossings, self.d1_num[index][2])
            self.assertEqual(d1d2[1].crossings, self.d2_num[index][2])
            self.assertEqual(d1d2[0].max_crossings, self.d1_num[index][3])
            self.assertEqual(d1d2[1].max_crossings, self.d2_num[index][3])
            self.assertEqual(d1d2[0].pos, dwarf.FINISH)
            self.assertEqual(d1d2[1].pos, dwarf.FINISH)
            index += 1

    def test_floordiv_1(self):
        test_dwarfs = []
        for (d1, d2) in self.dwarf_numbers:
            dwarf1 = Dwarf(d1[0], d1[1], d1[2], d1[3], dwarf.START)
            dwarf2 = Dwarf(d2[0], d2[1], d2[2], d2[3], dwarf.START)
            test_dwarfs.append((dwarf1, dwarf2))
        index = 0
        for d1d2 in test_dwarfs:
            if d1d2[1].crossing_time != 0:
                self.assertEqual(d1d2[0] // d1d2[1], self.d1_num[index][1] // self.d2_num[index][1])
            self.assertEqual(d1d2[0] // 1, self.d1_num[index][1] // 1)
            self.assertEqual(d1d2[0] // 5, self.d1_num[index][1] // 5)
            self.assertEqual(d1d2[0] // 24, self.d1_num[index][1] // 24)
            self.assertEqual(d1d2[0] // 117, self.d1_num[index][1] // 117)
            self.assertEqual(d1d2[1] // 2, self.d2_num[index][1] // 2)
            self.assertEqual(d1d2[1] // 6, self.d2_num[index][1] // 6)
            self.assertEqual(d1d2[1] // 29, self.d2_num[index][1] // 29)
            self.assertEqual(d1d2[1] // 118, self.d2_num[index][1] // 118)
            self.assertEqual(d1d2[0].dwarf_nr, self.d1_num[index][0])
            self.assertEqual(d1d2[1].dwarf_nr, self.d2_num[index][0])
            self.assertEqual(d1d2[0].crossing_time, self.d1_num[index][1])
            self.assertEqual(d1d2[1].crossing_time, self.d2_num[index][1])
            self.assertEqual(d1d2[0].crossings, self.d1_num[index][2])
            self.assertEqual(d1d2[1].crossings, self.d2_num[index][2])
            self.assertEqual(d1d2[0].max_crossings, self.d1_num[index][3])
            self.assertEqual(d1d2[1].max_crossings, self.d2_num[index][3])
            self.assertEqual(d1d2[0].pos, dwarf.START)
            self.assertEqual(d1d2[1].pos, dwarf.START)
            index += 1

    def test_floordiv_2(self):
        test_dwarfs = []
        for (d1, d2) in self.dwarf_numbers:
            dwarf1 = Dwarf(d1[0], d1[1], d1[2], d1[3], dwarf.FINISH)
            dwarf2 = Dwarf(d2[0], d2[1], d2[2], d2[3], dwarf.FINISH)
            test_dwarfs.append((dwarf1, dwarf2))
        index = 0
        for d1d2 in test_dwarfs:
            if d1d2[1].crossing_time != 0:
                self.assertEqual(d1d2[0] // d1d2[1], self.d1_num[index][1] // self.d2_num[index][1])
            self.assertEqual(d1d2[0] // 1, self.d1_num[index][1] // 1)
            self.assertEqual(d1d2[0] // 5, self.d1_num[index][1] // 5)
            self.assertEqual(d1d2[0] // 24, self.d1_num[index][1] // 24)
            self.assertEqual(d1d2[0] // 117, self.d1_num[index][1] // 117)
            self.assertEqual(d1d2[1] // 2, self.d2_num[index][1] // 2)
            self.assertEqual(d1d2[1] // 6, self.d2_num[index][1] // 6)
            self.assertEqual(d1d2[1] // 29, self.d2_num[index][1] // 29)
            self.assertEqual(d1d2[1] // 118, self.d2_num[index][1] // 118)
            self.assertEqual(d1d2[0].dwarf_nr, self.d1_num[index][0])
            self.assertEqual(d1d2[1].dwarf_nr, self.d2_num[index][0])
            self.assertEqual(d1d2[0].crossing_time, self.d1_num[index][1])
            self.assertEqual(d1d2[1].crossing_time, self.d2_num[index][1])
            self.assertEqual(d1d2[0].crossings, self.d1_num[index][2])
            self.assertEqual(d1d2[1].crossings, self.d2_num[index][2])
            self.assertEqual(d1d2[0].max_crossings, self.d1_num[index][3])
            self.assertEqual(d1d2[1].max_crossings, self.d2_num[index][3])
            self.assertEqual(d1d2[0].pos, dwarf.FINISH)
            self.assertEqual(d1d2[1].pos, dwarf.FINISH)
            index += 1

    def test_and_1(self):
        test_dwarfs = []
        for (d1, d2) in self.dwarf_numbers:
            test_dwarf1 = Dwarf(d1[0], d1[1], d1[2], d1[3], dwarf.START)
            test_dwarf2 = Dwarf(d2[0], d2[1], d2[2], d2[3], dwarf.START)
            test_dwarfs.append((test_dwarf1, test_dwarf2))
        index = 0
        for (dwarf1, dwarf2) in test_dwarfs:
            self.assertEqual(dwarf1 & dwarf2, max(self.d1_num[index][1], self.d2_num[index][1]))
            # self.assertEqual(max(d1d2[0].crossing_time, 1), max(self.d1_num[index][1], 1))
            # self.assertEqual(max(d1d2[0].crossing_time, 5), max(self.d1_num[index][1], 5))
            # self.assertEqual(max(d1d2[0].crossing_time, 24), max(self.d1_num[index][1], 24))
            # self.assertEqual(max(d1d2[0].crossing_time, 117), max(self.d1_num[index][1], 117))
            # self.assertEqual(max(d1d2[1].crossing_time, 2), max(self.d2_num[index][1], 2))
            # self.assertEqual(max(d1d2[1].crossing_time, 6), max(self.d2_num[index][1], 6))
            # self.assertEqual(max(d1d2[1].crossing_time, 29), max(self.d2_num[index][1], 29))
            # self.assertEqual(max(d1d2[1].crossing_time, 118), max(self.d2_num[index][1], 118))
            #
            # self.assertEqual(max(d1d2[0].crossing_time, -d1d2[1].crossing_time), max(self.d1_num[index][1], -self.d2_num[index][1]))
            # self.assertEqual(max(d1d2[0].crossing_time, -1), max(self.d1_num[index][1], -1))
            # self.assertEqual(max(d1d2[0].crossing_time, -5), max(self.d1_num[index][1], -5))
            # self.assertEqual(max(d1d2[0].crossing_time, -24), max(self.d1_num[index][1], -24))
            # self.assertEqual(max(d1d2[0].crossing_time, -117), max(self.d1_num[index][1], -117))
            # self.assertEqual(max(d1d2[1].crossing_time, -2), max(self.d2_num[index][1], -2))
            # self.assertEqual(max(d1d2[1].crossing_time, -6), max(self.d2_num[index][1], -6))
            # self.assertEqual(max(d1d2[1].crossing_time, -29), max(self.d2_num[index][1], -29))
            # self.assertEqual(max(d1d2[1].crossing_time, -118), max(self.d2_num[index][1], -118))
            #
            # self.assertEqual(d1d2[0].dwarf_nr, self.d1_num[index][0])
            # self.assertEqual(d1d2[1].dwarf_nr, self.d2_num[index][0])
            # self.assertEqual(d1d2[0].crossing_time, self.d1_num[index][1])
            # self.assertEqual(d1d2[1].crossing_time, self.d2_num[index][1])
            # self.assertEqual(d1d2[0].crossings, self.d1_num[index][2])
            # self.assertEqual(d1d2[1].crossings, self.d2_num[index][2])
            # self.assertEqual(d1d2[0].max_crossings, self.d1_num[index][3])
            # self.assertEqual(d1d2[1].max_crossings, self.d2_num[index][3])
            # self.assertEqual(d1d2[0].pos, dwarf.START)
            # self.assertEqual(d1d2[1].pos, dwarf.START)
            index += 1

    def test_and_2(self):
        test_dwarfs = []
        for (d1, d2) in self.dwarf_numbers:
            dwarf1 = Dwarf(d1[0], d1[1], d1[2], d1[3], dwarf.FINISH)
            dwarf2 = Dwarf(d2[0], d2[1], d2[2], d2[3], dwarf.FINISH)
            test_dwarfs.append((dwarf1, dwarf2))
        index = 0
        for d1d2 in test_dwarfs:
            self.assertEqual(max(d1d2[0].crossing_time, d1d2[1]), max(self.d1_num[index][1], self.d2_num[index][1]))
            self.assertEqual(max(d1d2[0].crossing_time, 1), max(self.d1_num[index][1], 1))
            self.assertEqual(max(d1d2[0].crossing_time, 5), max(self.d1_num[index][1], 5))
            self.assertEqual(max(d1d2[0].crossing_time, 24), max(self.d1_num[index][1], 24))
            self.assertEqual(max(d1d2[0].crossing_time, 117), max(self.d1_num[index][1], 117))
            self.assertEqual(max(d1d2[1].crossing_time, 2), max(self.d2_num[index][1], 2))
            self.assertEqual(max(d1d2[1].crossing_time, 6), max(self.d2_num[index][1], 6))
            self.assertEqual(max(d1d2[1].crossing_time, 29), max(self.d2_num[index][1], 29))
            self.assertEqual(max(d1d2[1].crossing_time, 118), max(self.d2_num[index][1], 118))

            self.assertEqual(max(d1d2[0].crossing_time, -d1d2[1].crossing_time), max(self.d1_num[index][1], -self.d2_num[index][1]))
            self.assertEqual(max(d1d2[0].crossing_time, -1), max(self.d1_num[index][1], -1))
            self.assertEqual(max(d1d2[0].crossing_time, -5), max(self.d1_num[index][1], -5))
            self.assertEqual(max(d1d2[0].crossing_time, -24), max(self.d1_num[index][1], -24))
            self.assertEqual(max(d1d2[0].crossing_time, -117), max(self.d1_num[index][1], -117))
            self.assertEqual(max(d1d2[1].crossing_time, -2), max(self.d2_num[index][1], -2))
            self.assertEqual(max(d1d2[1].crossing_time, -6), max(self.d2_num[index][1], -6))
            self.assertEqual(max(d1d2[1].crossing_time, -29), max(self.d2_num[index][1], -29))
            self.assertEqual(max(d1d2[1].crossing_time, -118), max(self.d2_num[index][1], -118))

            self.assertEqual(d1d2[0].dwarf_nr, self.d1_num[index][0])
            self.assertEqual(d1d2[1].dwarf_nr, self.d2_num[index][0])
            self.assertEqual(d1d2[0].crossing_time, self.d1_num[index][1])
            self.assertEqual(d1d2[1].crossing_time, self.d2_num[index][1])
            self.assertEqual(d1d2[0].crossings, self.d1_num[index][2])
            self.assertEqual(d1d2[1].crossings, self.d2_num[index][2])
            self.assertEqual(d1d2[0].max_crossings, self.d1_num[index][3])
            self.assertEqual(d1d2[1].max_crossings, self.d2_num[index][3])
            self.assertEqual(d1d2[0].pos, dwarf.FINISH)
            self.assertEqual(d1d2[1].pos, dwarf.FINISH)
            index += 1

    def test_lt_1(self):
        test_dwarfs = []
        for (d1, d2) in self.dwarf_numbers:
            dwarf1 = Dwarf(d1[0], d1[1], d1[2], d1[3], dwarf.START)
            dwarf2 = Dwarf(d2[0], d2[1], d2[2], d2[3], dwarf.START)
            test_dwarfs.append((dwarf1, dwarf2))
        index = 0
        for d1d2 in test_dwarfs:
            self.assertEqual(d1d2[0] < d1d2[1], self.d1_num[index][1] < self.d2_num[index][1])
            self.assertEqual(d1d2[0] < 1, self.d1_num[index][1] < 1)
            self.assertEqual(d1d2[0] < 5, self.d1_num[index][1] < 5)
            self.assertEqual(d1d2[0] < 24, self.d1_num[index][1] < 24)
            self.assertEqual(d1d2[0] < 117, self.d1_num[index][1] < 117)
            self.assertEqual(d1d2[1] < 2, self.d2_num[index][1] < 2)
            self.assertEqual(d1d2[1] < 6, self.d2_num[index][1] < 6)
            self.assertEqual(d1d2[1] < 29, self.d2_num[index][1] < 29)
            self.assertEqual(d1d2[1] < 118, self.d2_num[index][1] < 118)

            self.assertEqual(d1d2[0] < -d1d2[1], self.d1_num[index][1] < -self.d2_num[index][1])
            self.assertEqual(d1d2[0] < -1, self.d1_num[index][1] < -1)
            self.assertEqual(d1d2[0] < -5, self.d1_num[index][1] < -5)
            self.assertEqual(d1d2[0] < -24, self.d1_num[index][1] < -24)
            self.assertEqual(d1d2[0] < -117, self.d1_num[index][1] < -117)
            self.assertEqual(d1d2[1] < -2, self.d2_num[index][1] < -2)
            self.assertEqual(d1d2[1] < -6, self.d2_num[index][1] < -6)
            self.assertEqual(d1d2[1] < -29, self.d2_num[index][1] < -29)
            self.assertEqual(d1d2[1] < -118, self.d2_num[index][1] < -118)

            self.assertEqual(d1d2[0].dwarf_nr, self.d1_num[index][0])
            self.assertEqual(d1d2[1].dwarf_nr, self.d2_num[index][0])
            self.assertEqual(d1d2[0].crossing_time, self.d1_num[index][1])
            self.assertEqual(d1d2[1].crossing_time, self.d2_num[index][1])
            self.assertEqual(d1d2[0].crossings, self.d1_num[index][2])
            self.assertEqual(d1d2[1].crossings, self.d2_num[index][2])
            self.assertEqual(d1d2[0].max_crossings, self.d1_num[index][3])
            self.assertEqual(d1d2[1].max_crossings, self.d2_num[index][3])
            self.assertEqual(d1d2[0].pos, dwarf.START)
            self.assertEqual(d1d2[1].pos, dwarf.START)
            index += 1

    def test_lt_2(self):
        test_dwarfs = []
        for (d1, d2) in self.dwarf_numbers:
            dwarf1 = Dwarf(d1[0], d1[1], d1[2], d1[3], dwarf.FINISH)
            dwarf2 = Dwarf(d2[0], d2[1], d2[2], d2[3], dwarf.FINISH)
            test_dwarfs.append((dwarf1, dwarf2))
        index = 0
        for d1d2 in test_dwarfs:
            self.assertEqual(d1d2[0] < d1d2[1], self.d1_num[index][1] < self.d2_num[index][1])
            self.assertEqual(d1d2[0] < 1, self.d1_num[index][1] < 1)
            self.assertEqual(d1d2[0] < 5, self.d1_num[index][1] < 5)
            self.assertEqual(d1d2[0] < 24, self.d1_num[index][1] < 24)
            self.assertEqual(d1d2[0] < 117, self.d1_num[index][1] < 117)
            self.assertEqual(d1d2[1] < 2, self.d2_num[index][1] < 2)
            self.assertEqual(d1d2[1] < 6, self.d2_num[index][1] < 6)
            self.assertEqual(d1d2[1] < 29, self.d2_num[index][1] < 29)
            self.assertEqual(d1d2[1] < 118, self.d2_num[index][1] < 118)

            self.assertEqual(d1d2[0] < -d1d2[1], self.d1_num[index][1] < -self.d2_num[index][1])
            self.assertEqual(d1d2[0] < -1, self.d1_num[index][1] < -1)
            self.assertEqual(d1d2[0] < -5, self.d1_num[index][1] < -5)
            self.assertEqual(d1d2[0] < -24, self.d1_num[index][1] < -24)
            self.assertEqual(d1d2[0] < -117, self.d1_num[index][1] < -117)
            self.assertEqual(d1d2[1] < -2, self.d2_num[index][1] < -2)
            self.assertEqual(d1d2[1] < -6, self.d2_num[index][1] < -6)
            self.assertEqual(d1d2[1] < -29, self.d2_num[index][1] < -29)
            self.assertEqual(d1d2[1] < -118, self.d2_num[index][1] < -118)

            self.assertEqual(d1d2[0].dwarf_nr, self.d1_num[index][0])
            self.assertEqual(d1d2[1].dwarf_nr, self.d2_num[index][0])
            self.assertEqual(d1d2[0].crossing_time, self.d1_num[index][1])
            self.assertEqual(d1d2[1].crossing_time, self.d2_num[index][1])
            self.assertEqual(d1d2[0].crossings, self.d1_num[index][2])
            self.assertEqual(d1d2[1].crossings, self.d2_num[index][2])
            self.assertEqual(d1d2[0].max_crossings, self.d1_num[index][3])
            self.assertEqual(d1d2[1].max_crossings, self.d2_num[index][3])
            self.assertEqual(d1d2[0].pos, dwarf.FINISH)
            self.assertEqual(d1d2[1].pos, dwarf.FINISH)
            index += 1

    def test_gt_1(self):
        test_dwarfs = []
        for (d1, d2) in self.dwarf_numbers:
            dwarf1 = Dwarf(d1[0], d1[1], d1[2], d1[3], dwarf.START)
            dwarf2 = Dwarf(d2[0], d2[1], d2[2], d2[3], dwarf.START)
            test_dwarfs.append((dwarf1, dwarf2))
        index = 0
        for d1d2 in test_dwarfs:
            self.assertEqual(d1d2[0] > d1d2[1], self.d1_num[index][1] > self.d2_num[index][1])
            self.assertEqual(d1d2[0] > 1, self.d1_num[index][1] > 1)
            self.assertEqual(d1d2[0] > 5, self.d1_num[index][1] > 5)
            self.assertEqual(d1d2[0] > 24, self.d1_num[index][1] > 24)
            self.assertEqual(d1d2[0] > 117, self.d1_num[index][1] > 117)
            self.assertEqual(d1d2[1] > 2, self.d2_num[index][1] > 2)
            self.assertEqual(d1d2[1] > 6, self.d2_num[index][1] > 6)
            self.assertEqual(d1d2[1] > 29, self.d2_num[index][1] > 29)
            self.assertEqual(d1d2[1] > 118, self.d2_num[index][1] > 118)

            self.assertEqual(d1d2[0] > -d1d2[1], self.d1_num[index][1] > -self.d2_num[index][1])
            self.assertEqual(d1d2[0] > -1, self.d1_num[index][1] > -1)
            self.assertEqual(d1d2[0] > -5, self.d1_num[index][1] > -5)
            self.assertEqual(d1d2[0] > -24, self.d1_num[index][1] > -24)
            self.assertEqual(d1d2[0] > -117, self.d1_num[index][1] > -117)
            self.assertEqual(d1d2[1] > -2, self.d2_num[index][1] > -2)
            self.assertEqual(d1d2[1] > -6, self.d2_num[index][1] > -6)
            self.assertEqual(d1d2[1] > -29, self.d2_num[index][1] > -29)
            self.assertEqual(d1d2[1] > -118, self.d2_num[index][1] > -118)

            self.assertEqual(d1d2[0].dwarf_nr, self.d1_num[index][0])
            self.assertEqual(d1d2[1].dwarf_nr, self.d2_num[index][0])
            self.assertEqual(d1d2[0].crossing_time, self.d1_num[index][1])
            self.assertEqual(d1d2[1].crossing_time, self.d2_num[index][1])
            self.assertEqual(d1d2[0].crossings, self.d1_num[index][2])
            self.assertEqual(d1d2[1].crossings, self.d2_num[index][2])
            self.assertEqual(d1d2[0].max_crossings, self.d1_num[index][3])
            self.assertEqual(d1d2[1].max_crossings, self.d2_num[index][3])
            self.assertEqual(d1d2[0].pos, dwarf.START)
            self.assertEqual(d1d2[1].pos, dwarf.START)
            index += 1

    def test_gt_2(self):
        test_dwarfs = []
        for (d1, d2) in self.dwarf_numbers:
            dwarf1 = Dwarf(d1[0], d1[1], d1[2], d1[3], dwarf.FINISH)
            dwarf2 = Dwarf(d2[0], d2[1], d2[2], d2[3], dwarf.FINISH)
            test_dwarfs.append((dwarf1, dwarf2))
        index = 0
        for d1d2 in test_dwarfs:
            self.assertEqual(d1d2[0] > d1d2[1], self.d1_num[index][1] > self.d2_num[index][1])
            self.assertEqual(d1d2[0] > 1, self.d1_num[index][1] > 1)
            self.assertEqual(d1d2[0] > 5, self.d1_num[index][1] > 5)
            self.assertEqual(d1d2[0] > 24, self.d1_num[index][1] > 24)
            self.assertEqual(d1d2[0] > 117, self.d1_num[index][1] > 117)
            self.assertEqual(d1d2[1] > 2, self.d2_num[index][1] > 2)
            self.assertEqual(d1d2[1] > 6, self.d2_num[index][1] > 6)
            self.assertEqual(d1d2[1] > 29, self.d2_num[index][1] > 29)
            self.assertEqual(d1d2[1] > 118, self.d2_num[index][1] > 118)

            self.assertEqual(d1d2[0] > -d1d2[1], self.d1_num[index][1] > -self.d2_num[index][1])
            self.assertEqual(d1d2[0] > -1, self.d1_num[index][1] > -1)
            self.assertEqual(d1d2[0] > -5, self.d1_num[index][1] > -5)
            self.assertEqual(d1d2[0] > -24, self.d1_num[index][1] > -24)
            self.assertEqual(d1d2[0] > -117, self.d1_num[index][1] > -117)
            self.assertEqual(d1d2[1] > -2, self.d2_num[index][1] > -2)
            self.assertEqual(d1d2[1] > -6, self.d2_num[index][1] > -6)
            self.assertEqual(d1d2[1] > -29, self.d2_num[index][1] > -29)
            self.assertEqual(d1d2[1] > -118, self.d2_num[index][1] > -118)

            self.assertEqual(d1d2[0].dwarf_nr, self.d1_num[index][0])
            self.assertEqual(d1d2[1].dwarf_nr, self.d2_num[index][0])
            self.assertEqual(d1d2[0].crossing_time, self.d1_num[index][1])
            self.assertEqual(d1d2[1].crossing_time, self.d2_num[index][1])
            self.assertEqual(d1d2[0].crossings, self.d1_num[index][2])
            self.assertEqual(d1d2[1].crossings, self.d2_num[index][2])
            self.assertEqual(d1d2[0].max_crossings, self.d1_num[index][3])
            self.assertEqual(d1d2[1].max_crossings, self.d2_num[index][3])
            self.assertEqual(d1d2[0].pos, dwarf.FINISH)
            self.assertEqual(d1d2[1].pos, dwarf.FINISH)
            index += 1

    def test_le_1(self):
        test_dwarfs = []
        for (d1, d2) in self.dwarf_numbers:
            dwarf1 = Dwarf(d1[0], d1[1], d1[2], d1[3], dwarf.START)
            dwarf2 = Dwarf(d2[0], d2[1], d2[2], d2[3], dwarf.START)
            test_dwarfs.append((dwarf1, dwarf2))
        index = 0
        for d1d2 in test_dwarfs:
            self.assertEqual(d1d2[0] <= d1d2[1], self.d1_num[index][1] <= self.d2_num[index][1])
            self.assertEqual(d1d2[0] <= 1, self.d1_num[index][1] <= 1)
            self.assertEqual(d1d2[0] <= 5, self.d1_num[index][1] <= 5)
            self.assertEqual(d1d2[0] <= 24, self.d1_num[index][1] <= 24)
            self.assertEqual(d1d2[0] <= 117, self.d1_num[index][1] <= 117)
            self.assertEqual(d1d2[1] <= 2, self.d2_num[index][1] <= 2)
            self.assertEqual(d1d2[1] <= 6, self.d2_num[index][1] <= 6)
            self.assertEqual(d1d2[1] <= 29, self.d2_num[index][1] <= 29)
            self.assertEqual(d1d2[1] <= 118, self.d2_num[index][1] <= 118)

            self.assertEqual(d1d2[0] <= -d1d2[1], self.d1_num[index][1] <= -self.d2_num[index][1])
            self.assertEqual(d1d2[0] <= -1, self.d1_num[index][1] <= -1)
            self.assertEqual(d1d2[0] <= -5, self.d1_num[index][1] <= -5)
            self.assertEqual(d1d2[0] <= -24, self.d1_num[index][1] <= -24)
            self.assertEqual(d1d2[0] <= -117, self.d1_num[index][1] <= -117)
            self.assertEqual(d1d2[1] <= -2, self.d2_num[index][1] <= -2)
            self.assertEqual(d1d2[1] <= -6, self.d2_num[index][1] <= -6)
            self.assertEqual(d1d2[1] <= -29, self.d2_num[index][1] <= -29)
            self.assertEqual(d1d2[1] <= -118, self.d2_num[index][1] <= -118)

            self.assertEqual(d1d2[0].dwarf_nr, self.d1_num[index][0])
            self.assertEqual(d1d2[1].dwarf_nr, self.d2_num[index][0])
            self.assertEqual(d1d2[0].crossing_time, self.d1_num[index][1])
            self.assertEqual(d1d2[1].crossing_time, self.d2_num[index][1])
            self.assertEqual(d1d2[0].crossings, self.d1_num[index][2])
            self.assertEqual(d1d2[1].crossings, self.d2_num[index][2])
            self.assertEqual(d1d2[0].max_crossings, self.d1_num[index][3])
            self.assertEqual(d1d2[1].max_crossings, self.d2_num[index][3])
            self.assertEqual(d1d2[0].pos, dwarf.START)
            self.assertEqual(d1d2[1].pos, dwarf.START)
            index += 1

    def test_le_2(self):
        test_dwarfs = []
        for (d1, d2) in self.dwarf_numbers:
            dwarf1 = Dwarf(d1[0], d1[1], d1[2], d1[3], dwarf.FINISH)
            dwarf2 = Dwarf(d2[0], d2[1], d2[2], d2[3], dwarf.FINISH)
            test_dwarfs.append((dwarf1, dwarf2))
        index = 0
        for d1d2 in test_dwarfs:
            self.assertEqual(d1d2[0] <= d1d2[1], self.d1_num[index][1] <= self.d2_num[index][1])
            self.assertEqual(d1d2[0] <= 1, self.d1_num[index][1] <= 1)
            self.assertEqual(d1d2[0] <= 5, self.d1_num[index][1] <= 5)
            self.assertEqual(d1d2[0] <= 24, self.d1_num[index][1] <= 24)
            self.assertEqual(d1d2[0] <= 117, self.d1_num[index][1] <= 117)
            self.assertEqual(d1d2[1] <= 2, self.d2_num[index][1] <= 2)
            self.assertEqual(d1d2[1] <= 6, self.d2_num[index][1] <= 6)
            self.assertEqual(d1d2[1] <= 29, self.d2_num[index][1] <= 29)
            self.assertEqual(d1d2[1] <= 118, self.d2_num[index][1] <= 118)

            self.assertEqual(d1d2[0] <= -d1d2[1], self.d1_num[index][1] <= -self.d2_num[index][1])
            self.assertEqual(d1d2[0] <= -1, self.d1_num[index][1] <= -1)
            self.assertEqual(d1d2[0] <= -5, self.d1_num[index][1] <= -5)
            self.assertEqual(d1d2[0] <= -24, self.d1_num[index][1] <= -24)
            self.assertEqual(d1d2[0] <= -117, self.d1_num[index][1] <= -117)
            self.assertEqual(d1d2[1] <= -2, self.d2_num[index][1] <= -2)
            self.assertEqual(d1d2[1] <= -6, self.d2_num[index][1] <= -6)
            self.assertEqual(d1d2[1] <= -29, self.d2_num[index][1] <= -29)
            self.assertEqual(d1d2[1] <= -118, self.d2_num[index][1] <= -118)

            self.assertEqual(d1d2[0].dwarf_nr, self.d1_num[index][0])
            self.assertEqual(d1d2[1].dwarf_nr, self.d2_num[index][0])
            self.assertEqual(d1d2[0].crossing_time, self.d1_num[index][1])
            self.assertEqual(d1d2[1].crossing_time, self.d2_num[index][1])
            self.assertEqual(d1d2[0].crossings, self.d1_num[index][2])
            self.assertEqual(d1d2[1].crossings, self.d2_num[index][2])
            self.assertEqual(d1d2[0].max_crossings, self.d1_num[index][3])
            self.assertEqual(d1d2[1].max_crossings, self.d2_num[index][3])
            self.assertEqual(d1d2[0].pos, dwarf.FINISH)
            self.assertEqual(d1d2[1].pos, dwarf.FINISH)
            index += 1

    def test_ge_1(self):
        test_dwarfs = []
        for (d1, d2) in self.dwarf_numbers:
            dwarf1 = Dwarf(d1[0], d1[1], d1[2], d1[3], dwarf.START)
            dwarf2 = Dwarf(d2[0], d2[1], d2[2], d2[3], dwarf.START)
            test_dwarfs.append((dwarf1, dwarf2))
        index = 0
        for d1d2 in test_dwarfs:
            self.assertEqual(d1d2[0] >= d1d2[1], self.d1_num[index][1] >= self.d2_num[index][1])
            self.assertEqual(d1d2[0] >= 1, self.d1_num[index][1] >= 1)
            self.assertEqual(d1d2[0] >= 5, self.d1_num[index][1] >= 5)
            self.assertEqual(d1d2[0] >= 24, self.d1_num[index][1] >= 24)
            self.assertEqual(d1d2[0] >= 117, self.d1_num[index][1] >= 117)
            self.assertEqual(d1d2[1] >= 2, self.d2_num[index][1] >= 2)
            self.assertEqual(d1d2[1] >= 6, self.d2_num[index][1] >= 6)
            self.assertEqual(d1d2[1] >= 29, self.d2_num[index][1] >= 29)
            self.assertEqual(d1d2[1] >= 118, self.d2_num[index][1] >= 118)

            self.assertEqual(d1d2[0] >= -d1d2[1], self.d1_num[index][1] >= -self.d2_num[index][1])
            self.assertEqual(d1d2[0] >= -1, self.d1_num[index][1] >= -1)
            self.assertEqual(d1d2[0] >= -5, self.d1_num[index][1] >= -5)
            self.assertEqual(d1d2[0] >= -24, self.d1_num[index][1] >= -24)
            self.assertEqual(d1d2[0] >= -117, self.d1_num[index][1] >= -117)
            self.assertEqual(d1d2[1] >= -2, self.d2_num[index][1] >= -2)
            self.assertEqual(d1d2[1] >= -6, self.d2_num[index][1] >= -6)
            self.assertEqual(d1d2[1] >= -29, self.d2_num[index][1] >= -29)
            self.assertEqual(d1d2[1] >= -118, self.d2_num[index][1] >= -118)

            self.assertEqual(d1d2[0].dwarf_nr, self.d1_num[index][0])
            self.assertEqual(d1d2[1].dwarf_nr, self.d2_num[index][0])
            self.assertEqual(d1d2[0].crossing_time, self.d1_num[index][1])
            self.assertEqual(d1d2[1].crossing_time, self.d2_num[index][1])
            self.assertEqual(d1d2[0].crossings, self.d1_num[index][2])
            self.assertEqual(d1d2[1].crossings, self.d2_num[index][2])
            self.assertEqual(d1d2[0].max_crossings, self.d1_num[index][3])
            self.assertEqual(d1d2[1].max_crossings, self.d2_num[index][3])
            self.assertEqual(d1d2[0].pos, dwarf.START)
            self.assertEqual(d1d2[1].pos, dwarf.START)
            index += 1

    def test_ge_2(self):
        test_dwarfs = []
        for (d1, d2) in self.dwarf_numbers:
            dwarf1 = Dwarf(d1[0], d1[1], d1[2], d1[3], dwarf.FINISH)
            dwarf2 = Dwarf(d2[0], d2[1], d2[2], d2[3], dwarf.FINISH)
            test_dwarfs.append((dwarf1, dwarf2))
        index = 0
        for d1d2 in test_dwarfs:
            self.assertEqual(d1d2[0] >= d1d2[1], self.d1_num[index][1] >= self.d2_num[index][1])
            self.assertEqual(d1d2[0] >= 1, self.d1_num[index][1] >= 1)
            self.assertEqual(d1d2[0] >= 5, self.d1_num[index][1] >= 5)
            self.assertEqual(d1d2[0] >= 24, self.d1_num[index][1] >= 24)
            self.assertEqual(d1d2[0] >= 117, self.d1_num[index][1] >= 117)
            self.assertEqual(d1d2[1] >= 2, self.d2_num[index][1] >= 2)
            self.assertEqual(d1d2[1] >= 6, self.d2_num[index][1] >= 6)
            self.assertEqual(d1d2[1] >= 29, self.d2_num[index][1] >= 29)
            self.assertEqual(d1d2[1] >= 118, self.d2_num[index][1] >= 118)

            self.assertEqual(d1d2[0] >= -d1d2[1], self.d1_num[index][1] >= -self.d2_num[index][1])
            self.assertEqual(d1d2[0] >= -1, self.d1_num[index][1] >= -1)
            self.assertEqual(d1d2[0] >= -5, self.d1_num[index][1] >= -5)
            self.assertEqual(d1d2[0] >= -24, self.d1_num[index][1] >= -24)
            self.assertEqual(d1d2[0] >= -117, self.d1_num[index][1] >= -117)
            self.assertEqual(d1d2[1] >= -2, self.d2_num[index][1] >= -2)
            self.assertEqual(d1d2[1] >= -6, self.d2_num[index][1] >= -6)
            self.assertEqual(d1d2[1] >= -29, self.d2_num[index][1] >= -29)
            self.assertEqual(d1d2[1] >= -118, self.d2_num[index][1] >= -118)

            self.assertEqual(d1d2[0].dwarf_nr, self.d1_num[index][0])
            self.assertEqual(d1d2[1].dwarf_nr, self.d2_num[index][0])
            self.assertEqual(d1d2[0].crossing_time, self.d1_num[index][1])
            self.assertEqual(d1d2[1].crossing_time, self.d2_num[index][1])
            self.assertEqual(d1d2[0].crossings, self.d1_num[index][2])
            self.assertEqual(d1d2[1].crossings, self.d2_num[index][2])
            self.assertEqual(d1d2[0].max_crossings, self.d1_num[index][3])
            self.assertEqual(d1d2[1].max_crossings, self.d2_num[index][3])
            self.assertEqual(d1d2[0].pos, dwarf.FINISH)
            self.assertEqual(d1d2[1].pos, dwarf.FINISH)
            index += 1

    def test_eq_1(self):
        test_dwarfs = []
        for (d1, d2) in self.dwarf_numbers:
            dwarf1 = Dwarf(d1[0], d1[1], d1[2], d1[3], dwarf.START)
            dwarf2 = Dwarf(d2[0], d2[1], d2[2], d2[3], dwarf.START)
            test_dwarfs.append((dwarf1, dwarf2))
        index = 0
        for d1d2 in test_dwarfs:
            self.assertEqual(d1d2[0] == d1d2[1], self.d1_num[index][1] == self.d2_num[index][1])
            self.assertEqual(d1d2[0] == 1, self.d1_num[index][1] == 1)
            self.assertEqual(d1d2[0] == 5, self.d1_num[index][1] == 5)
            self.assertEqual(d1d2[0] == 24, self.d1_num[index][1] == 24)
            self.assertEqual(d1d2[0] == 117, self.d1_num[index][1] == 117)
            self.assertEqual(d1d2[1] == 2, self.d2_num[index][1] == 2)
            self.assertEqual(d1d2[1] == 6, self.d2_num[index][1] == 6)
            self.assertEqual(d1d2[1] == 29, self.d2_num[index][1] == 29)
            self.assertEqual(d1d2[1] == 118, self.d2_num[index][1] == 118)

            self.assertEqual(d1d2[0] == -d1d2[1], self.d1_num[index][1] == -self.d2_num[index][1])
            self.assertEqual(d1d2[0] == -1, self.d1_num[index][1] == -1)
            self.assertEqual(d1d2[0] == -5, self.d1_num[index][1] == -5)
            self.assertEqual(d1d2[0] == -24, self.d1_num[index][1] == -24)
            self.assertEqual(d1d2[0] == -117, self.d1_num[index][1] == -117)
            self.assertEqual(d1d2[1] == -2, self.d2_num[index][1] == -2)
            self.assertEqual(d1d2[1] == -6, self.d2_num[index][1] == -6)
            self.assertEqual(d1d2[1] == -29, self.d2_num[index][1] == -29)
            self.assertEqual(d1d2[1] == -118, self.d2_num[index][1] == -118)

            self.assertTrue(d1d2[0] == self.d1_num[index][1])
            self.assertTrue(d1d2[1] == self.d2_num[index][1])
            self.assertTrue(d1d2[0] == d1d2[0])
            self.assertTrue(d1d2[1] == d1d2[1])

            self.assertEqual(d1d2[0].dwarf_nr, self.d1_num[index][0])
            self.assertEqual(d1d2[1].dwarf_nr, self.d2_num[index][0])
            self.assertEqual(d1d2[0].crossing_time, self.d1_num[index][1])
            self.assertEqual(d1d2[1].crossing_time, self.d2_num[index][1])
            self.assertEqual(d1d2[0].crossings, self.d1_num[index][2])
            self.assertEqual(d1d2[1].crossings, self.d2_num[index][2])
            self.assertEqual(d1d2[0].max_crossings, self.d1_num[index][3])
            self.assertEqual(d1d2[1].max_crossings, self.d2_num[index][3])
            self.assertEqual(d1d2[0].pos, dwarf.START)
            self.assertEqual(d1d2[1].pos, dwarf.START)
            index += 1

    def test_eq_2(self):
        test_dwarfs = []
        for (d1, d2) in self.dwarf_numbers:
            dwarf1 = Dwarf(d1[0], d1[1], d1[2], d1[3], dwarf.FINISH)
            dwarf2 = Dwarf(d2[0], d2[1], d2[2], d2[3], dwarf.FINISH)
            test_dwarfs.append((dwarf1, dwarf2))
        index = 0
        for d1d2 in test_dwarfs:
            self.assertEqual(d1d2[0] == d1d2[1], self.d1_num[index][1] == self.d2_num[index][1])
            self.assertEqual(d1d2[0] == 1, self.d1_num[index][1] == 1)
            self.assertEqual(d1d2[0] == 5, self.d1_num[index][1] == 5)
            self.assertEqual(d1d2[0] == 24, self.d1_num[index][1] == 24)
            self.assertEqual(d1d2[0] == 117, self.d1_num[index][1] == 117)
            self.assertEqual(d1d2[1] == 2, self.d2_num[index][1] == 2)
            self.assertEqual(d1d2[1] == 6, self.d2_num[index][1] == 6)
            self.assertEqual(d1d2[1] == 29, self.d2_num[index][1] == 29)
            self.assertEqual(d1d2[1] == 118, self.d2_num[index][1] == 118)

            self.assertEqual(d1d2[0] == -d1d2[1], self.d1_num[index][1] == -self.d2_num[index][1])
            self.assertEqual(d1d2[0] == -1, self.d1_num[index][1] == -1)
            self.assertEqual(d1d2[0] == -5, self.d1_num[index][1] == -5)
            self.assertEqual(d1d2[0] == -24, self.d1_num[index][1] == -24)
            self.assertEqual(d1d2[0] == -117, self.d1_num[index][1] == -117)
            self.assertEqual(d1d2[1] == -2, self.d2_num[index][1] == -2)
            self.assertEqual(d1d2[1] == -6, self.d2_num[index][1] == -6)
            self.assertEqual(d1d2[1] == -29, self.d2_num[index][1] == -29)
            self.assertEqual(d1d2[1] == -118, self.d2_num[index][1] == -118)

            self.assertTrue(d1d2[0] == self.d1_num[index][1])
            self.assertTrue(d1d2[1] == self.d2_num[index][1])
            self.assertTrue(d1d2[0] == d1d2[0])
            self.assertTrue(d1d2[1] == d1d2[1])

            self.assertEqual(d1d2[0].dwarf_nr, self.d1_num[index][0])
            self.assertEqual(d1d2[1].dwarf_nr, self.d2_num[index][0])
            self.assertEqual(d1d2[0].crossing_time, self.d1_num[index][1])
            self.assertEqual(d1d2[1].crossing_time, self.d2_num[index][1])
            self.assertEqual(d1d2[0].crossings, self.d1_num[index][2])
            self.assertEqual(d1d2[1].crossings, self.d2_num[index][2])
            self.assertEqual(d1d2[0].max_crossings, self.d1_num[index][3])
            self.assertEqual(d1d2[1].max_crossings, self.d2_num[index][3])
            self.assertEqual(d1d2[0].pos, dwarf.FINISH)
            self.assertEqual(d1d2[1].pos, dwarf.FINISH)
            index += 1

    def test_ne_1(self):
        test_dwarfs = []
        for (d1, d2) in self.dwarf_numbers:
            dwarf1 = Dwarf(d1[0], d1[1], d1[2], d1[3], dwarf.START)
            dwarf2 = Dwarf(d2[0], d2[1], d2[2], d2[3], dwarf.START)
            test_dwarfs.append((dwarf1, dwarf2))
        index = 0
        for d1d2 in test_dwarfs:
            self.assertEqual(d1d2[0] != d1d2[1], self.d1_num[index][1] != self.d2_num[index][1])
            self.assertEqual(d1d2[0] != 1, self.d1_num[index][1] != 1)
            self.assertEqual(d1d2[0] != 5, self.d1_num[index][1] != 5)
            self.assertEqual(d1d2[0] != 24, self.d1_num[index][1] != 24)
            self.assertEqual(d1d2[0] != 117, self.d1_num[index][1] != 117)
            self.assertEqual(d1d2[1] != 2, self.d2_num[index][1] != 2)
            self.assertEqual(d1d2[1] != 6, self.d2_num[index][1] != 6)
            self.assertEqual(d1d2[1] != 29, self.d2_num[index][1] != 29)
            self.assertEqual(d1d2[1] != 118, self.d2_num[index][1] != 118)

            self.assertEqual(d1d2[0] != -d1d2[1], self.d1_num[index][1] != -self.d2_num[index][1])
            self.assertEqual(d1d2[0] != -1, self.d1_num[index][1] != -1)
            self.assertEqual(d1d2[0] != -5, self.d1_num[index][1] != -5)
            self.assertEqual(d1d2[0] != -24, self.d1_num[index][1] != -24)
            self.assertEqual(d1d2[0] != -117, self.d1_num[index][1] != -117)
            self.assertEqual(d1d2[1] != -2, self.d2_num[index][1] != -2)
            self.assertEqual(d1d2[1] != -6, self.d2_num[index][1] != -6)
            self.assertEqual(d1d2[1] != -29, self.d2_num[index][1] != -29)
            self.assertEqual(d1d2[1] != -118, self.d2_num[index][1] != -118)

            self.assertFalse(d1d2[0] != self.d1_num[index][1])
            self.assertFalse(d1d2[1] != self.d2_num[index][1])
            self.assertFalse(d1d2[0] != d1d2[0])
            self.assertFalse(d1d2[1] != d1d2[1])

            self.assertEqual(d1d2[0].dwarf_nr, self.d1_num[index][0])
            self.assertEqual(d1d2[1].dwarf_nr, self.d2_num[index][0])
            self.assertEqual(d1d2[0].crossing_time, self.d1_num[index][1])
            self.assertEqual(d1d2[1].crossing_time, self.d2_num[index][1])
            self.assertEqual(d1d2[0].crossings, self.d1_num[index][2])
            self.assertEqual(d1d2[1].crossings, self.d2_num[index][2])
            self.assertEqual(d1d2[0].max_crossings, self.d1_num[index][3])
            self.assertEqual(d1d2[1].max_crossings, self.d2_num[index][3])
            self.assertEqual(d1d2[0].pos, dwarf.START)
            self.assertEqual(d1d2[1].pos, dwarf.START)
            index += 1

    def test_ne_2(self):
        test_dwarfs = []
        for (d1, d2) in self.dwarf_numbers:
            dwarf1 = Dwarf(d1[0], d1[1], d1[2], d1[3], dwarf.FINISH)
            dwarf2 = Dwarf(d2[0], d2[1], d2[2], d2[3], dwarf.FINISH)
            test_dwarfs.append((dwarf1, dwarf2))
        index = 0
        for d1d2 in test_dwarfs:
            self.assertEqual(d1d2[0] != d1d2[1], self.d1_num[index][1] != self.d2_num[index][1])
            self.assertEqual(d1d2[0] != 1, self.d1_num[index][1] != 1)
            self.assertEqual(d1d2[0] != 5, self.d1_num[index][1] != 5)
            self.assertEqual(d1d2[0] != 24, self.d1_num[index][1] != 24)
            self.assertEqual(d1d2[0] != 117, self.d1_num[index][1] != 117)
            self.assertEqual(d1d2[1] != 2, self.d2_num[index][1] != 2)
            self.assertEqual(d1d2[1] != 6, self.d2_num[index][1] != 6)
            self.assertEqual(d1d2[1] != 29, self.d2_num[index][1] != 29)
            self.assertEqual(d1d2[1] != 118, self.d2_num[index][1] != 118)

            self.assertEqual(d1d2[0] != -d1d2[1], self.d1_num[index][1] != -self.d2_num[index][1])
            self.assertEqual(d1d2[0] != -1, self.d1_num[index][1] != -1)
            self.assertEqual(d1d2[0] != -5, self.d1_num[index][1] != -5)
            self.assertEqual(d1d2[0] != -24, self.d1_num[index][1] != -24)
            self.assertEqual(d1d2[0] != -117, self.d1_num[index][1] != -117)
            self.assertEqual(d1d2[1] != -2, self.d2_num[index][1] != -2)
            self.assertEqual(d1d2[1] != -6, self.d2_num[index][1] != -6)
            self.assertEqual(d1d2[1] != -29, self.d2_num[index][1] != -29)
            self.assertEqual(d1d2[1] != -118, self.d2_num[index][1] != -118)

            self.assertFalse(d1d2[0] != self.d1_num[index][1])
            self.assertFalse(d1d2[1] != self.d2_num[index][1])
            self.assertFalse(d1d2[0] != d1d2[0])
            self.assertFalse(d1d2[1] != d1d2[1])

            self.assertEqual(d1d2[0].dwarf_nr, self.d1_num[index][0])
            self.assertEqual(d1d2[1].dwarf_nr, self.d2_num[index][0])
            self.assertEqual(d1d2[0].crossing_time, self.d1_num[index][1])
            self.assertEqual(d1d2[1].crossing_time, self.d2_num[index][1])
            self.assertEqual(d1d2[0].crossings, self.d1_num[index][2])
            self.assertEqual(d1d2[1].crossings, self.d2_num[index][2])
            self.assertEqual(d1d2[0].max_crossings, self.d1_num[index][3])
            self.assertEqual(d1d2[1].max_crossings, self.d2_num[index][3])
            self.assertEqual(d1d2[0].pos, dwarf.FINISH)
            self.assertEqual(d1d2[1].pos, dwarf.FINISH)
            index += 1

    def test_isub_1(self):
        test_dwarfs = []
        for (d1, d2) in self.dwarf_numbers:
            dwarf1 = Dwarf(d1[0], d1[1], d1[2], d1[3], dwarf.START)
            dwarf2 = Dwarf(d2[0], d2[1], d2[2], d2[3], dwarf.START)
            test_dwarfs.append((dwarf1, dwarf2))
        index = 0
        for (d1, d2) in test_dwarfs:
            d1 -= 1
            d2 -= 17
            self.assertEqual(d1.crossings, self.d1_num[index][2] - 1)
            self.assertEqual(d2.crossings, self.d2_num[index][2] - 17)

            self.assertEqual(d1.dwarf_nr, self.d1_num[index][0])
            self.assertEqual(d2.dwarf_nr, self.d2_num[index][0])
            self.assertEqual(d1.crossing_time, self.d1_num[index][1])
            self.assertEqual(d2.crossing_time, self.d2_num[index][1])
            self.assertEqual(d1.max_crossings, self.d1_num[index][3])
            self.assertEqual(d2.max_crossings, self.d2_num[index][3])
            self.assertEqual(d1.pos, dwarf.START)
            self.assertEqual(d2.pos, dwarf.START)
            index += 1

        start_crossings = 10
        d3 = Dwarf(1, 1, start_crossings, 3, dwarf.START)
        d4 = Dwarf(2, 2, 2 * start_crossings, 3, dwarf.FINISH)
        for i in range(1, 21):
            d3 -= 1
            d4 -= 2
            self.assertEqual(d3.times_crossed(), start_crossings - i)
            self.assertEqual(d4.times_crossed(), 2*start_crossings - 2*i)
            self.assertEqual(d3.dwarf_nr, 1)
            self.assertEqual(d4.dwarf_nr, 2)
            self.assertEqual(d3.crossing_time, 1)
            self.assertEqual(d4.crossing_time, 2)
            self.assertEqual(d3.max_crossings, 3)
            self.assertEqual(d4.max_crossings, 3)
            self.assertEqual(d3.pos, dwarf.START)
            self.assertEqual(d4.pos, dwarf.FINISH)

    def test_isub_2(self):
        test_dwarfs = []
        for (d1, d2) in self.dwarf_numbers:
            dwarf1 = Dwarf(d1[0], d1[1], d1[2], d1[3], dwarf.FINISH)
            dwarf2 = Dwarf(d2[0], d2[1], d2[2], d2[3], dwarf.FINISH)
            test_dwarfs.append((dwarf1, dwarf2))
        index = 0
        for (d1, d2) in test_dwarfs:
            d1 -= 1
            d2 -= 17
            self.assertEqual(d1.crossings, self.d1_num[index][2] - 1)
            self.assertEqual(d2.crossings, self.d2_num[index][2] - 17)

            self.assertEqual(d1.dwarf_nr, self.d1_num[index][0])
            self.assertEqual(d2.dwarf_nr, self.d2_num[index][0])
            self.assertEqual(d1.crossing_time, self.d1_num[index][1])
            self.assertEqual(d2.crossing_time, self.d2_num[index][1])
            self.assertEqual(d1.max_crossings, self.d1_num[index][3])
            self.assertEqual(d2.max_crossings, self.d2_num[index][3])
            self.assertEqual(d1.pos, dwarf.FINISH)
            self.assertEqual(d2.pos, dwarf.FINISH)
            index += 1

        start_crossings = 10
        d3 = Dwarf(1, 1, start_crossings, 3, dwarf.START)
        d4 = Dwarf(2, 2, 2 * start_crossings, 3, dwarf.FINISH)
        for i in range(1, 21):
            d3 -= 1
            d4 -= 2
            self.assertEqual(d3.times_crossed(), start_crossings - i)
            self.assertEqual(d4.times_crossed(), 2*start_crossings - 2*i)
            self.assertEqual(d3.dwarf_nr, 1)
            self.assertEqual(d4.dwarf_nr, 2)
            self.assertEqual(d3.crossing_time, 1)
            self.assertEqual(d4.crossing_time, 2)
            self.assertEqual(d3.max_crossings, 3)
            self.assertEqual(d4.max_crossings, 3)
            self.assertEqual(d3.pos, dwarf.START)
            self.assertEqual(d4.pos, dwarf.FINISH)

    def test_iadd_1(self):
        test_dwarfs = []
        for (d1, d2) in self.dwarf_numbers:
            dwarf1 = Dwarf(d1[0], d1[1], d1[2], d1[3], dwarf.START)
            dwarf2 = Dwarf(d2[0], d2[1], d2[2], d2[3], dwarf.START)
            test_dwarfs.append((dwarf1, dwarf2))
        index = 0
        for (d1, d2) in test_dwarfs:
            d1 += 1
            d2 += 17
            self.assertEqual(d1.crossings, self.d1_num[index][2] + 1)
            self.assertEqual(d2.crossings, self.d2_num[index][2] + 17)

            self.assertEqual(d1.dwarf_nr, self.d1_num[index][0])
            self.assertEqual(d2.dwarf_nr, self.d2_num[index][0])
            self.assertEqual(d1.crossing_time, self.d1_num[index][1])
            self.assertEqual(d2.crossing_time, self.d2_num[index][1])
            self.assertEqual(d1.max_crossings, self.d1_num[index][3])
            self.assertEqual(d2.max_crossings, self.d2_num[index][3])
            self.assertEqual(d1.pos, dwarf.START)
            self.assertEqual(d2.pos, dwarf.START)
            index += 1

        start_crossings = -10
        d3 = Dwarf(1, 1, start_crossings, 3, dwarf.START)
        d4 = Dwarf(2, 2, 2 * start_crossings, 3, dwarf.FINISH)
        for i in range(1, 21):
            d3 += 1
            d4 += 2
            self.assertEqual(d3.times_crossed(), start_crossings + i)
            self.assertEqual(d4.times_crossed(), 2*start_crossings + 2*i)
            self.assertEqual(d3.dwarf_nr, 1)
            self.assertEqual(d4.dwarf_nr, 2)
            self.assertEqual(d3.crossing_time, 1)
            self.assertEqual(d4.crossing_time, 2)
            self.assertEqual(d3.max_crossings, 3)
            self.assertEqual(d4.max_crossings, 3)
            self.assertEqual(d3.pos, dwarf.START)
            self.assertEqual(d4.pos, dwarf.FINISH)

    def test_iadd_2(self):
        test_dwarfs = []
        for (d1, d2) in self.dwarf_numbers:
            dwarf1 = Dwarf(d1[0], d1[1], d1[2], d1[3], dwarf.FINISH)
            dwarf2 = Dwarf(d2[0], d2[1], d2[2], d2[3], dwarf.FINISH)
            test_dwarfs.append((dwarf1, dwarf2))
        index = 0
        for (d1, d2) in test_dwarfs:
            d1 += 1
            d2 += 17
            self.assertEqual(d1.crossings, self.d1_num[index][2] + 1)
            self.assertEqual(d2.crossings, self.d2_num[index][2] + 17)

            self.assertEqual(d1.dwarf_nr, self.d1_num[index][0])
            self.assertEqual(d2.dwarf_nr, self.d2_num[index][0])
            self.assertEqual(d1.crossing_time, self.d1_num[index][1])
            self.assertEqual(d2.crossing_time, self.d2_num[index][1])
            self.assertEqual(d1.max_crossings, self.d1_num[index][3])
            self.assertEqual(d2.max_crossings, self.d2_num[index][3])
            self.assertEqual(d1.pos, dwarf.FINISH)
            self.assertEqual(d2.pos, dwarf.FINISH)
            index += 1

        start_crossings = -10
        d3 = Dwarf(1, 1, start_crossings, 3, dwarf.START)
        d4 = Dwarf(2, 2, 2 * start_crossings, 3, dwarf.FINISH)
        for i in range(1, 21):
            d3 += 1
            d4 += 2
            self.assertEqual(d3.times_crossed(), start_crossings + i)
            self.assertEqual(d4.times_crossed(), 2 * start_crossings + 2 * i)
            self.assertEqual(d3.dwarf_nr, 1)
            self.assertEqual(d4.dwarf_nr, 2)
            self.assertEqual(d3.crossing_time, 1)
            self.assertEqual(d4.crossing_time, 2)
            self.assertEqual(d3.max_crossings, 3)
            self.assertEqual(d4.max_crossings, 3)
            self.assertEqual(d3.pos, dwarf.START)
            self.assertEqual(d4.pos, dwarf.FINISH)

    def test_imul_1(self):
        test_dwarfs = []
        for (d1, d2) in self.dwarf_numbers:
            dwarf1 = Dwarf(d1[0], d1[1], d1[2], d1[3], dwarf.START)
            dwarf2 = Dwarf(d2[0], d2[1], d2[2], d2[3], dwarf.START)
            test_dwarfs.append((dwarf1, dwarf2))
        index = 0
        for (d1, d2) in test_dwarfs:
            d1 *= 1
            d2 *= 17
            self.assertEqual(d1.crossings, self.d1_num[index][2] * 1)
            self.assertEqual(d2.crossings, self.d2_num[index][2] * 17)

            self.assertEqual(d1.dwarf_nr, self.d1_num[index][0])
            self.assertEqual(d2.dwarf_nr, self.d2_num[index][0])
            self.assertEqual(d1.crossing_time, self.d1_num[index][1])
            self.assertEqual(d2.crossing_time, self.d2_num[index][1])
            self.assertEqual(d1.max_crossings, self.d1_num[index][3])
            self.assertEqual(d2.max_crossings, self.d2_num[index][3])
            self.assertEqual(d1.pos, dwarf.START)
            self.assertEqual(d2.pos, dwarf.START)
            index += 1

        start_crossings = 2
        d3 = Dwarf(1, 1, start_crossings, 3, dwarf.START)
        d4 = Dwarf(2, 2, 3 + start_crossings, 3, dwarf.FINISH)
        for i in range(1, 11):
            d3 *= 2
            d4 *= 3
            self.assertEqual(d3.times_crossed(), start_crossings * 2**i)
            self.assertEqual(d4.times_crossed(), (3 + start_crossings) * 3**i)
            self.assertEqual(d3.dwarf_nr, 1)
            self.assertEqual(d4.dwarf_nr, 2)
            self.assertEqual(d3.crossing_time, 1)
            self.assertEqual(d4.crossing_time, 2)
            self.assertEqual(d3.max_crossings, 3)
            self.assertEqual(d4.max_crossings, 3)
            self.assertEqual(d3.pos, dwarf.START)
            self.assertEqual(d4.pos, dwarf.FINISH)

    def test_imul_2(self):
        test_dwarfs = []
        for (d1, d2) in self.dwarf_numbers:
            dwarf1 = Dwarf(d1[0], d1[1], d1[2], d1[3], dwarf.FINISH)
            dwarf2 = Dwarf(d2[0], d2[1], d2[2], d2[3], dwarf.FINISH)
            test_dwarfs.append((dwarf1, dwarf2))
        index = 0
        for (d1, d2) in test_dwarfs:
            d1 *= 1
            d2 *= 17
            self.assertEqual(d1.crossings, self.d1_num[index][2] * 1)
            self.assertEqual(d2.crossings, self.d2_num[index][2] * 17)

            self.assertEqual(d1.dwarf_nr, self.d1_num[index][0])
            self.assertEqual(d2.dwarf_nr, self.d2_num[index][0])
            self.assertEqual(d1.crossing_time, self.d1_num[index][1])
            self.assertEqual(d2.crossing_time, self.d2_num[index][1])
            self.assertEqual(d1.max_crossings, self.d1_num[index][3])
            self.assertEqual(d2.max_crossings, self.d2_num[index][3])
            self.assertEqual(d1.pos, dwarf.FINISH)
            self.assertEqual(d2.pos, dwarf.FINISH)
            index += 1

        start_crossings = 2
        d3 = Dwarf(1, 1, start_crossings, 3, dwarf.START)
        d4 = Dwarf(2, 2, 3 + start_crossings, 3, dwarf.FINISH)
        for i in range(1, 11):
            d3 *= 2
            d4 *= 3
            self.assertEqual(d3.times_crossed(), start_crossings * 2**i)
            self.assertEqual(d4.times_crossed(), (3 + start_crossings) * 3**i)
            self.assertEqual(d3.dwarf_nr, 1)
            self.assertEqual(d4.dwarf_nr, 2)
            self.assertEqual(d3.crossing_time, 1)
            self.assertEqual(d4.crossing_time, 2)
            self.assertEqual(d3.max_crossings, 3)
            self.assertEqual(d4.max_crossings, 3)
            self.assertEqual(d3.pos, dwarf.START)
            self.assertEqual(d4.pos, dwarf.FINISH)

    def test_itruediv_1(self):
        test_dwarfs = []
        for (d1, d2) in self.dwarf_numbers:
            dwarf1 = Dwarf(d1[0], d1[1], d1[2], d1[3], dwarf.START)
            dwarf2 = Dwarf(d2[0], d2[1], d2[2], d2[3], dwarf.START)
            test_dwarfs.append((dwarf1, dwarf2))
        index = 0
        for (d1, d2) in test_dwarfs:
            d1 /= 1
            d2 /= 17
            self.assertEqual(d1.crossings, self.d1_num[index][2] / 1)
            self.assertEqual(d2.crossings, self.d2_num[index][2] / 17)

            self.assertEqual(d1.dwarf_nr, self.d1_num[index][0])
            self.assertEqual(d2.dwarf_nr, self.d2_num[index][0])
            self.assertEqual(d1.crossing_time, self.d1_num[index][1])
            self.assertEqual(d2.crossing_time, self.d2_num[index][1])
            self.assertEqual(d1.max_crossings, self.d1_num[index][3])
            self.assertEqual(d2.max_crossings, self.d2_num[index][3])
            self.assertEqual(d1.pos, dwarf.START)
            self.assertEqual(d2.pos, dwarf.START)
            index += 1

        start_crossings3 = 1024
        start_crossings4 = 59049
        d3 = Dwarf(1, 1, start_crossings3, 3, dwarf.START)
        d4 = Dwarf(2, 2, start_crossings4, 3, dwarf.FINISH)
        for i in range(1, 11):
            d3 /= 2
            d4 /= 3
            self.assertEqual(d3.times_crossed(), start_crossings3 / 2**i)
            self.assertEqual(d4.times_crossed(), start_crossings4 / 3**i)
            self.assertEqual(d3.dwarf_nr, 1)
            self.assertEqual(d4.dwarf_nr, 2)
            self.assertEqual(d3.crossing_time, 1)
            self.assertEqual(d4.crossing_time, 2)
            self.assertEqual(d3.max_crossings, 3)
            self.assertEqual(d4.max_crossings, 3)
            self.assertEqual(d3.pos, dwarf.START)
            self.assertEqual(d4.pos, dwarf.FINISH)

    def test_itruediv_2(self):
        test_dwarfs = []
        for (d1, d2) in self.dwarf_numbers:
            dwarf1 = Dwarf(d1[0], d1[1], d1[2], d1[3], dwarf.FINISH)
            dwarf2 = Dwarf(d2[0], d2[1], d2[2], d2[3], dwarf.FINISH)
            test_dwarfs.append((dwarf1, dwarf2))
        index = 0
        for (d1, d2) in test_dwarfs:
            d1 /= 1
            d2 /= 17
            self.assertEqual(d1.crossings, self.d1_num[index][2] / 1)
            self.assertEqual(d2.crossings, self.d2_num[index][2] / 17)

            self.assertEqual(d1.dwarf_nr, self.d1_num[index][0])
            self.assertEqual(d2.dwarf_nr, self.d2_num[index][0])
            self.assertEqual(d1.crossing_time, self.d1_num[index][1])
            self.assertEqual(d2.crossing_time, self.d2_num[index][1])
            self.assertEqual(d1.max_crossings, self.d1_num[index][3])
            self.assertEqual(d2.max_crossings, self.d2_num[index][3])
            self.assertEqual(d1.pos, dwarf.FINISH)
            self.assertEqual(d2.pos, dwarf.FINISH)
            index += 1

        start_crossings3 = 1024
        start_crossings4 = 59049
        d3 = Dwarf(1, 1, start_crossings3, 3, dwarf.START)
        d4 = Dwarf(2, 2, start_crossings4, 3, dwarf.FINISH)
        for i in range(1, 11):
            d3 /= 2
            d4 /= 3
            self.assertEqual(d3.times_crossed(), start_crossings3 / 2**i)
            self.assertEqual(d4.times_crossed(), start_crossings4 / 3**i)
            self.assertEqual(d3.dwarf_nr, 1)
            self.assertEqual(d4.dwarf_nr, 2)
            self.assertEqual(d3.crossing_time, 1)
            self.assertEqual(d4.crossing_time, 2)
            self.assertEqual(d3.max_crossings, 3)
            self.assertEqual(d4.max_crossings, 3)
            self.assertEqual(d3.pos, dwarf.START)
            self.assertEqual(d4.pos, dwarf.FINISH)

    def test_ifloordiv_1(self):
        test_dwarfs = []
        for (d1, d2) in self.dwarf_numbers:
            dwarf1 = Dwarf(d1[0], d1[1], d1[2], d1[3], dwarf.START)
            dwarf2 = Dwarf(d2[0], d2[1], d2[2], d2[3], dwarf.START)
            test_dwarfs.append((dwarf1, dwarf2))
        index = 0
        for (d1, d2) in test_dwarfs:
            d1 //= 1
            d2 //= 17
            self.assertEqual(d1.crossings, self.d1_num[index][2] // 1)
            self.assertEqual(d2.crossings, self.d2_num[index][2] // 17)

            self.assertEqual(d1.dwarf_nr, self.d1_num[index][0])
            self.assertEqual(d2.dwarf_nr, self.d2_num[index][0])
            self.assertEqual(d1.crossing_time, self.d1_num[index][1])
            self.assertEqual(d2.crossing_time, self.d2_num[index][1])
            self.assertEqual(d1.max_crossings, self.d1_num[index][3])
            self.assertEqual(d2.max_crossings, self.d2_num[index][3])
            self.assertEqual(d1.pos, dwarf.START)
            self.assertEqual(d2.pos, dwarf.START)
            index += 1

        start_crossings3 = 1024
        start_crossings4 = 59049
        d3 = Dwarf(1, 1, start_crossings3, 3, dwarf.START)
        d4 = Dwarf(2, 2, start_crossings4, 3, dwarf.FINISH)
        for i in range(1, 11):
            d3 //= 2
            d4 //= 3
            self.assertEqual(d3.times_crossed(), start_crossings3 // 2**i)
            self.assertEqual(d4.times_crossed(), start_crossings4 // 3**i)
            self.assertEqual(d3.dwarf_nr, 1)
            self.assertEqual(d4.dwarf_nr, 2)
            self.assertEqual(d3.crossing_time, 1)
            self.assertEqual(d4.crossing_time, 2)
            self.assertEqual(d3.max_crossings, 3)
            self.assertEqual(d4.max_crossings, 3)
            self.assertEqual(d3.pos, dwarf.START)
            self.assertEqual(d4.pos, dwarf.FINISH)

    def test_ifloordiv_2(self):
        test_dwarfs = []
        for (d1, d2) in self.dwarf_numbers:
            dwarf1 = Dwarf(d1[0], d1[1], d1[2], d1[3], dwarf.FINISH)
            dwarf2 = Dwarf(d2[0], d2[1], d2[2], d2[3], dwarf.FINISH)
            test_dwarfs.append((dwarf1, dwarf2))
        index = 0
        for (d1, d2) in test_dwarfs:
            d1 //= 1
            d2 //= 17
            self.assertEqual(d1.crossings, self.d1_num[index][2] // 1)
            self.assertEqual(d2.crossings, self.d2_num[index][2] // 17)

            self.assertEqual(d1.dwarf_nr, self.d1_num[index][0])
            self.assertEqual(d2.dwarf_nr, self.d2_num[index][0])
            self.assertEqual(d1.crossing_time, self.d1_num[index][1])
            self.assertEqual(d2.crossing_time, self.d2_num[index][1])
            self.assertEqual(d1.max_crossings, self.d1_num[index][3])
            self.assertEqual(d2.max_crossings, self.d2_num[index][3])
            self.assertEqual(d1.pos, dwarf.FINISH)
            self.assertEqual(d2.pos, dwarf.FINISH)
            index += 1

        start_crossings3 = 1024
        start_crossings4 = 59049
        d3 = Dwarf(1, 1, start_crossings3, 3, dwarf.START)
        d4 = Dwarf(2, 2, start_crossings4, 3, dwarf.FINISH)
        for i in range(1, 11):
            d3 //= 2
            d4 //= 3
            self.assertEqual(d3.times_crossed(), start_crossings3 // 2**i)
            self.assertEqual(d4.times_crossed(), start_crossings4 // 3**i)
            self.assertEqual(d3.dwarf_nr, 1)
            self.assertEqual(d4.dwarf_nr, 2)
            self.assertEqual(d3.crossing_time, 1)
            self.assertEqual(d4.crossing_time, 2)
            self.assertEqual(d3.max_crossings, 3)
            self.assertEqual(d4.max_crossings, 3)
            self.assertEqual(d3.pos, dwarf.START)
            self.assertEqual(d4.pos, dwarf.FINISH)

    def test_neg_1(self):
        test_dwarfs = []
        for (d1, d2) in self.dwarf_numbers:
            dwarf1 = Dwarf(d1[0], d1[1], d1[2], d1[3], dwarf.START)
            dwarf2 = Dwarf(d2[0], d2[1], d2[2], d2[3], dwarf.START)
            test_dwarfs.append((dwarf1, dwarf2))
        index = 0
        for (d1, d2) in test_dwarfs:
            self.assertEqual(-d1, -self.d1_num[index][1])
            self.assertEqual(-d2, -self.d2_num[index][1])

            self.assertEqual(d1.dwarf_nr, self.d1_num[index][0])
            self.assertEqual(d2.dwarf_nr, self.d2_num[index][0])
            self.assertEqual(d1.crossing_time, self.d1_num[index][1])
            self.assertEqual(d2.crossing_time, self.d2_num[index][1])
            self.assertEqual(d1.max_crossings, self.d1_num[index][3])
            self.assertEqual(d2.max_crossings, self.d2_num[index][3])
            self.assertEqual(d1.pos, dwarf.START)
            self.assertEqual(d2.pos, dwarf.START)
            index += 1

    def test_neg_2(self):
        test_dwarfs = []
        for (d1, d2) in self.dwarf_numbers:
            dwarf1 = Dwarf(d1[0], d1[1], d1[2], d1[3], dwarf.FINISH)
            dwarf2 = Dwarf(d2[0], d2[1], d2[2], d2[3], dwarf.FINISH)
            test_dwarfs.append((dwarf1, dwarf2))
        index = 0
        for (d1, d2) in test_dwarfs:
            self.assertEqual(-d1, -self.d1_num[index][1])
            self.assertEqual(-d2, -self.d2_num[index][1])

            self.assertEqual(d1.dwarf_nr, self.d1_num[index][0])
            self.assertEqual(d2.dwarf_nr, self.d2_num[index][0])
            self.assertEqual(d1.crossing_time, self.d1_num[index][1])
            self.assertEqual(d2.crossing_time, self.d2_num[index][1])
            self.assertEqual(d1.max_crossings, self.d1_num[index][3])
            self.assertEqual(d2.max_crossings, self.d2_num[index][3])
            self.assertEqual(d1.pos, dwarf.FINISH)
            self.assertEqual(d2.pos, dwarf.FINISH)
            index += 1

    def test_pos_1(self):
        test_dwarfs = []
        for (d1, d2) in self.dwarf_numbers:
            dwarf1 = Dwarf(d1[0], d1[1], d1[2], d1[3], dwarf.START)
            dwarf2 = Dwarf(d2[0], d2[1], d2[2], d2[3], dwarf.START)
            test_dwarfs.append((dwarf1, dwarf2))
        index = 0
        for (d1, d2) in test_dwarfs:
            self.assertEqual(+d1, self.d1_num[index][1])
            self.assertEqual(+d2, self.d2_num[index][1])

            self.assertEqual(d1.dwarf_nr, self.d1_num[index][0])
            self.assertEqual(d2.dwarf_nr, self.d2_num[index][0])
            self.assertEqual(d1.crossing_time, self.d1_num[index][1])
            self.assertEqual(d2.crossing_time, self.d2_num[index][1])
            self.assertEqual(d1.max_crossings, self.d1_num[index][3])
            self.assertEqual(d2.max_crossings, self.d2_num[index][3])
            self.assertEqual(d1.pos, dwarf.START)
            self.assertEqual(d2.pos, dwarf.START)
            index += 1

    def test_pos_2(self):
        test_dwarfs = []
        for (d1, d2) in self.dwarf_numbers:
            dwarf1 = Dwarf(d1[0], d1[1], d1[2], d1[3], dwarf.FINISH)
            dwarf2 = Dwarf(d2[0], d2[1], d2[2], d2[3], dwarf.FINISH)
            test_dwarfs.append((dwarf1, dwarf2))
        index = 0
        for (d1, d2) in test_dwarfs:
            self.assertEqual(+d1, self.d1_num[index][1])
            self.assertEqual(+d2, self.d2_num[index][1])

            self.assertEqual(d1.dwarf_nr, self.d1_num[index][0])
            self.assertEqual(d2.dwarf_nr, self.d2_num[index][0])
            self.assertEqual(d1.crossing_time, self.d1_num[index][1])
            self.assertEqual(d2.crossing_time, self.d2_num[index][1])
            self.assertEqual(d1.max_crossings, self.d1_num[index][3])
            self.assertEqual(d2.max_crossings, self.d2_num[index][3])
            self.assertEqual(d1.pos, dwarf.FINISH)
            self.assertEqual(d2.pos, dwarf.FINISH)
            index += 1


class DwarfExceptionsTests(unittest.TestCase):

    def test_startpos_exception(self):
        start_pos = "home"
        dwarf_nr = 1
        dwarf1 = Dwarf(dwarf_nr, 2, 3, 4, dwarf.START)
        reason = f"this i just a test: " \
                 f"{dwarf1.dwarf_nr}, {dwarf1.crossing_time}, {dwarf1.crossings}, {dwarf1.max_crossings}, {dwarf1.pos}."
        with self.assertRaises(DwarfStartingPositionError) as cm:
            raise DwarfStartingPositionError(dwarf_nr, start_pos, reason)

        message = f"\nDwarf number {dwarf_nr} cannot start at {start_pos}, since {reason}"
        self.assertEqual(str(cm.exception), message)
        self.assertEqual(cm.exception.args[0], message)
        self.assertEqual(cm.exception.dwarf_nr, dwarf_nr)
        self.assertEqual(cm.exception.pos, start_pos)
        self.assertEqual(cm.exception.reason, reason)

    def test_crossing_exception(self):
        to_pos = "home"
        dwarf_nr = 1
        dwarf1 = Dwarf(dwarf_nr, 2, 3, 4, dwarf.START)
        reason = f"this i just a test: " \
                 f"{dwarf1.dwarf_nr}, {dwarf1.crossing_time}, {dwarf1.crossings}, {dwarf1.max_crossings}, {dwarf1.pos}."
        with self.assertRaises(DwarfCrossingError) as cm:
            raise DwarfCrossingError(dwarf_nr, to_pos, reason)

        message = f"\nDwarf number {dwarf_nr} can't cross the bridge to go to {to_pos}, since {reason}"
        self.assertEqual(str(cm.exception), message)
        self.assertEqual(cm.exception.args[0], message)
        self.assertEqual(cm.exception.dwarf_nr, dwarf_nr)
        self.assertEqual(cm.exception.to_pos, to_pos)
        self.assertEqual(cm.exception.reason, reason)


class DwarfOperatorTests(unittest.TestCase):

    def setUp(self) -> None:
        # print(f'Run before each test in DwarfOperatorTests')
        number_of_dwarfs = 1000
        d_min_nr = -10000
        d_max_nr = 10000
        c_min_time = -10000
        c_max_time = 10000
        tc_min = -10000
        tc_max = 10000
        self.d1_num = [{"dwarf_nr": randint(d_min_nr, d_max_nr),
                        "crossing_time": randint(c_min_time, c_max_time),
                        "crossings": randint(tc_min, tc_max),
                        "max_crossings": randint(tc_min, tc_max)}
                       for _ in range(number_of_dwarfs)]
        self.d2_num = [{"dwarf_nr": randint(d_min_nr, d_max_nr),
                        "crossing_time": randint(c_min_time, c_max_time),
                        "crossings": randint(tc_min, tc_max),
                        "max_crossings": randint(tc_min, tc_max)}
                       for _ in range(number_of_dwarfs)]
        self.dwarf_numbers = [(self.d1_num[i], self.d2_num[i]) for i in range(number_of_dwarfs)]

    def test_and_1(self):
        test_dwarfs = []
        for (d1, d2) in self.dwarf_numbers:
            test_dwarf1 = Dwarf(d1["dwarf_nr"], d1["crossing_time"], d1["crossings"], d1["max_crossings"], dwarf.START)
            test_dwarf2 = Dwarf(d2["dwarf_nr"], d2["crossing_time"], d2["crossings"], d2["max_crossings"], dwarf.START)
            test_dwarfs.append((test_dwarf1, test_dwarf2))
        index = 0
        for (dwarf1, dwarf2) in test_dwarfs:
            self.assertEqual(dwarf1 & dwarf2, max(self.d1_num[index]["crossing_time"], self.d2_num[index]["crossing_time"]))
            self.assertEqual(dwarf1 & 1, max(self.d1_num[index]["crossing_time"], 1))
            self.assertEqual(dwarf1 & 5, max(self.d1_num[index]["crossing_time"], 5))
            self.assertEqual(dwarf1 & 24, max(self.d1_num[index]["crossing_time"], 24))
            self.assertEqual(dwarf1 & 117, max(self.d1_num[index]["crossing_time"], 117))
            self.assertEqual(dwarf2 & 2, max(self.d2_num[index]["crossing_time"], 2))
            self.assertEqual(dwarf2 & 6, max(self.d2_num[index]["crossing_time"], 6))
            self.assertEqual(dwarf2 & 29, max(self.d2_num[index]["crossing_time"], 29))
            self.assertEqual(dwarf2 & 118, max(self.d2_num[index]["crossing_time"], 118))

            self.assertEqual(dwarf1 & -dwarf2, max(self.d1_num[index]["crossing_time"], -self.d2_num[index]["crossing_time"]))
            self.assertEqual(dwarf1 & -1, max(self.d1_num[index]["crossing_time"], -1))
            self.assertEqual(dwarf1 & -5, max(self.d1_num[index]["crossing_time"], -5))
            self.assertEqual(dwarf1 & -24, max(self.d1_num[index]["crossing_time"], -24))
            self.assertEqual(dwarf1 & -117, max(self.d1_num[index]["crossing_time"], -117))
            self.assertEqual(dwarf2 & -2, max(self.d2_num[index]["crossing_time"], -2))
            self.assertEqual(dwarf2 & -6, max(self.d2_num[index]["crossing_time"], -6))
            self.assertEqual(dwarf2 & -29, max(self.d2_num[index]["crossing_time"], -29))
            self.assertEqual(dwarf2 & -118, max(self.d2_num[index]["crossing_time"], -118))

            self.assertEqual(dwarf1.dwarf_nr, self.d1_num[index]["dwarf_nr"])
            self.assertEqual(dwarf2.dwarf_nr, self.d2_num[index]["dwarf_nr"])
            self.assertEqual(dwarf1.crossing_time, self.d1_num[index]["crossing_time"])
            self.assertEqual(dwarf2.crossing_time, self.d2_num[index]["crossing_time"])
            self.assertEqual(dwarf1.crossings, self.d1_num[index]["crossings"])
            self.assertEqual(dwarf2.crossings, self.d2_num[index]["crossings"])
            self.assertEqual(dwarf1.max_crossings, self.d1_num[index]["max_crossings"])
            self.assertEqual(dwarf2.max_crossings, self.d2_num[index]["max_crossings"])
            self.assertEqual(dwarf1.pos, dwarf.START)
            self.assertEqual(dwarf2.pos, dwarf.START)
            index += 1

    def test_and_2(self):
        test_dwarfs = []
        for (d1, d2) in self.dwarf_numbers:
            test_dwarf1 = Dwarf(d1["dwarf_nr"], d1["crossing_time"], d1["crossings"], d1["max_crossings"], dwarf.FINISH)
            test_dwarf2 = Dwarf(d2["dwarf_nr"], d2["crossing_time"], d2["crossings"], d2["max_crossings"], dwarf.FINISH)
            test_dwarfs.append((test_dwarf1, test_dwarf2))
        index = 0
        for (dwarf1, dwarf2) in test_dwarfs:
            self.assertEqual(dwarf1 & dwarf2, max(self.d1_num[index]["crossing_time"], self.d2_num[index]["crossing_time"]))
            self.assertEqual(dwarf1 & 1, max(self.d1_num[index]["crossing_time"], 1))
            self.assertEqual(dwarf1 & 5, max(self.d1_num[index]["crossing_time"], 5))
            self.assertEqual(dwarf1 & 24, max(self.d1_num[index]["crossing_time"], 24))
            self.assertEqual(dwarf1 & 117, max(self.d1_num[index]["crossing_time"], 117))
            self.assertEqual(dwarf2 & 2, max(self.d2_num[index]["crossing_time"], 2))
            self.assertEqual(dwarf2 & 6, max(self.d2_num[index]["crossing_time"], 6))
            self.assertEqual(dwarf2 & 29, max(self.d2_num[index]["crossing_time"], 29))
            self.assertEqual(dwarf2 & 118, max(self.d2_num[index]["crossing_time"], 118))

            self.assertEqual(dwarf1 & -dwarf2, max(self.d1_num[index]["crossing_time"], -self.d2_num[index]["crossing_time"]))
            self.assertEqual(dwarf1 & -1, max(self.d1_num[index]["crossing_time"], -1))
            self.assertEqual(dwarf1 & -5, max(self.d1_num[index]["crossing_time"], -5))
            self.assertEqual(dwarf1 & -24, max(self.d1_num[index]["crossing_time"], -24))
            self.assertEqual(dwarf1 & -117, max(self.d1_num[index]["crossing_time"], -117))
            self.assertEqual(dwarf2 & -2, max(self.d2_num[index]["crossing_time"], -2))
            self.assertEqual(dwarf2 & -6, max(self.d2_num[index]["crossing_time"], -6))
            self.assertEqual(dwarf2 & -29, max(self.d2_num[index]["crossing_time"], -29))
            self.assertEqual(dwarf2 & -118, max(self.d2_num[index]["crossing_time"], -118))

            self.assertEqual(dwarf1.dwarf_nr, self.d1_num[index]["dwarf_nr"])
            self.assertEqual(dwarf2.dwarf_nr, self.d2_num[index]["dwarf_nr"])
            self.assertEqual(dwarf1.crossing_time, self.d1_num[index]["crossing_time"])
            self.assertEqual(dwarf2.crossing_time, self.d2_num[index]["crossing_time"])
            self.assertEqual(dwarf1.crossings, self.d1_num[index]["crossings"])
            self.assertEqual(dwarf2.crossings, self.d2_num[index]["crossings"])
            self.assertEqual(dwarf1.max_crossings, self.d1_num[index]["max_crossings"])
            self.assertEqual(dwarf2.max_crossings, self.d2_num[index]["max_crossings"])
            self.assertEqual(dwarf1.pos, dwarf.FINISH)
            self.assertEqual(dwarf2.pos, dwarf.FINISH)
            index += 1

    def test_sort(self):
        test_dwarfs1 = []
        test_dwarfs2 = []
        for (d1, d2) in self.dwarf_numbers:
            test_dwarf1 = Dwarf(d1["dwarf_nr"], d1["crossing_time"], d1["crossings"], d1["max_crossings"], dwarf.FINISH)
            test_dwarf2 = Dwarf(d2["dwarf_nr"], d2["crossing_time"], d2["crossings"], d2["max_crossings"], dwarf.FINISH)
            test_dwarfs1.append(test_dwarf1)
            test_dwarfs2.append(test_dwarf2)
        test_dwarfs1.sort()
        test_dwarfs2.sort()
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
