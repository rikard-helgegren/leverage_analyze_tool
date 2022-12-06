#!/usr/bin/env python3
#
# Copyright (C) 2022 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

import os
import sys
import subprocess

import model.constants as constants

# Compile c++ algorithms
program_folder = os.path.dirname(os.path.realpath(sys.argv[0]))
command = ['g++','-O2','-pthread','-fPIC','-shared','-o',
          constants.program_folder + '/compiled_code/calculateHistogramOutput.so',
          constants.program_folder + '/model/histogram/calculateHistogramOutput.cpp']
subprocess.run(command)
