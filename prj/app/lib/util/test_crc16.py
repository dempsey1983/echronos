#
# eChronos Real-Time Operating System
# Copyright (C) 2015  National ICT Australia Limited (NICTA), ABN 62 102 206 173.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, version 3, provided that these additional
# terms apply under section 7:
#
#   No right, title or interest in or to any trade mark, service mark, logo or
#   trade name of of National ICT Australia Limited, ABN 62 102 206 173
#   ("NICTA") or its licensors is granted. Modified versions of the Program
#   must be plainly marked as such, and must not be distributed using
#   "eChronos" as a trade mark or product name, or misrepresented as being the
#   original Program.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# @TAG(NICTA_AGPL)
#

import unittest
from util.crc16 import Crc16Ccitt, crc16ccitt


class TestCase(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(crc16ccitt(), 0xffff)

    def test_expected(self):
        # Test values determined from:
        #   http://www.lammertbies.nl/comm/info/crc-calculation.html
        for inp, expected in [
                (b'0', 0xD7A3),
                (b'0a', 0x641D),
                (b'123456789', 0x29B1),
                (b'foo_bar', 0x37DF)]:
            self.assertEqual(crc16ccitt(inp), expected)

    def test_multi(self):
        for inp, expected in [
                ((b'0', b'a'), 0x641D),
                ((b'1234', b'56789'), 0x29B1),
                ((b'foo_', b'bar'), 0x37DF)]:
            self.assertEqual(crc16ccitt(*inp), expected)

    def test_reuse(self):
        crc = Crc16Ccitt()

        for byte in b'foo':
            crc.add(byte)
        self.assertEqual(crc.result(reset=False), 0x630A)

        for byte in b'bar':
            crc.add(byte)
        self.assertEqual(crc.result(reset=False), 0xBE35)

        crc.reset()

        for byte in b'foo':
            crc.add(byte)
        self.assertEqual(crc.result(), 0x630A)

        for byte in b'bar':
            crc.add(byte)
        self.assertEqual(crc.result(), 0x5F59)
