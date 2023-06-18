#!/usr/bin/env python
# Copyright (c) 2020-2022, Universal Robots A/S,
# All rights reserved.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the Universal Robots A/S nor the names of its
#      contributors may be used to endorse or promote products derived
#      from this software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL UNIVERSAL ROBOTS A/S BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import argparse
import logging
import sys
import twin_writer
import rtde.rtde as rtde
import rtde.rtde_config as rtde_config

from model.base_model import BaseModel

sys.path.append("..")

# parameters
host = "localhost"
port = 30004
config = "record_configuration.xml"
frequency = 1

config_file = rtde_config.ConfigFile(config)
output_names, output_types = config_file.get_recipe("out")

rtde_connection = rtde.RTDE(host, port)
rtde_connection.connect()

# get controller version
rtde_connection.get_controller_version()

# setup recipes
if not rtde_connection.send_output_setup(output_names, output_types, frequency):
    logging.error("Unable to configure output")
    sys.exit()

# start data synchronization
if not rtde_connection.send_start():
    logging.error("Unable to start synchronization")
    sys.exit()


twin_writer = twin_writer.TwinWriter(output_names, output_types)

header_row = twin_writer.get_header_row()
print("\n ".join(str(x) for x in header_row))

keep_running = True
while keep_running:
    try:
        state = rtde_connection.receive()
        if state is not None:
            data_row = twin_writer.get_data_row(state)
            base_model = BaseModel.get_from_rows(header_row, data_row)
            print("\n".join(str(x) for x in data_row))

    except KeyboardInterrupt:
        keep_running = False
    except rtde.RTDEException:
        rtde_connection.disconnect()
        sys.exit()

sys.stdout.write("\rComplete!\n")

rtde_connection.send_pause()
rtde_connection.disconnect()
