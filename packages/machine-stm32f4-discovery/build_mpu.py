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

import os
from prj import execute, commonpath


def run(system, _=None):
    return system_build(system)


def system_build(system):
    inc_path_args = ['-I%s' % i for i in system.include_paths]
    common_flags = ['-mthumb', '-g3', '-mlittle-endian', '-mcpu=cortex-m4', '-mfloat-abi=hard', '-mfpu=fpv4-sp-d16']
    a_flags = common_flags
    c_flags = common_flags + ['-O0', '-fdata-sections', '-fno-common', '-fno-zero-initialized-in-bss']

    # '--print-memory-usage' is a very useful flag here if you are
    # memory-constrained, but only works with recent versions of ld
    ld_flags = []

    all_input_files = system.c_files + system.asm_files
    all_input_files = [os.path.normpath(os.path.abspath(path)) for path in all_input_files]
    common_parent_path = commonpath(all_input_files)

    # Compile all C files.
    c_obj_files = [os.path.join(system.output, os.path.relpath(os.path.abspath(c_file_path.replace('.c', '.o')),
                                                               common_parent_path)) for c_file_path in system.c_files]

    for c_path, obj_path in zip(system.c_files, c_obj_files):
        os.makedirs(os.path.dirname(obj_path), exist_ok=True)
        execute(['arm-none-eabi-gcc', '-ffreestanding', '-c', c_path, '-o', obj_path, '-Wall', '-Werror'] +
                c_flags + inc_path_args)

    # Assemble all asm files.
    asm_obj_files = [os.path.join(system.output, os.path.relpath(os.path.abspath(asm_file_path.replace('.s', '.o')),
                                                                 common_parent_path))
                     for asm_file_path in system.asm_files]
    for asm_file_path, obj_file_path in zip(system.asm_files, asm_obj_files):
        os.makedirs(os.path.dirname(obj_file_path), exist_ok=True)
        execute(['arm-none-eabi-as', '-o', obj_file_path, asm_file_path] + a_flags + inc_path_args)

    # Perform final link
    obj_files = asm_obj_files + c_obj_files
    execute(['arm-none-eabi-ld', '-T', system.linker_script, '-o', system.output_file] + ld_flags + obj_files)
