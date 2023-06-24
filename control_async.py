import asyncio
import sys
from datetime import datetime

sys.path.append("..")
import logging

import rtde.rtde as rtde
import rtde.rtde_config as rtde_config


# logging.basicConfig(level=logging.INFO)
def setp_to_list(sp):
    sp_list = []
    for i in range(0, 6):
        sp_list.append(sp.__dict__["input_double_register_%i" % i])
    return sp_list


async def list_to_setp(sp, list):
    for i in range(0, 6):
        sp.__dict__["input_double_register_%i" % i] = list[i]
    return sp


def calculate_time_difference(start, end):
    duration = end - start
    return duration


def stdin_listener():
    """
    Listener for quitting the sample
    """
    while True:
        selection = input("Press Q to quit\n")
        if selection == "Q" or selection == "q":
            print("Quitting...")
            break


async def main():
    host = "localhost"
    port = 30004
    config = "control_configuration.xml"

    logging.getLogger().setLevel(logging.INFO)

    config_file = rtde_config.ConfigFile(config)
    state_names, state_types = config_file.get_recipe("state")
    setp_names, setp_types = config_file.get_recipe("setp")
    watchdog_names, watchdog_types = config_file.get_recipe("watchdog")

    rtde_connection = rtde.RTDE(host, port)
    rtde_connection.connect()

    # get controller version
    rtde_connection.get_controller_version()

    # setup recipes
    rtde_connection.send_output_setup(state_names, state_types)
    setp = rtde_connection.send_input_setup(setp_names, setp_types)
    watchdog = rtde_connection.send_input_setup(watchdog_names, watchdog_types)

    # Setpoints to move the robot to

    setp.input_double_register_0 = 0
    setp.input_double_register_1 = 0
    setp.input_double_register_2 = 0
    setp.input_double_register_3 = 0
    setp.input_double_register_4 = 0
    setp.input_double_register_5 = 0

    watchdog.input_int_register_0 = 0

    if not rtde_connection.send_start():
        sys.exit()

    set_position_1 = [-0.12, -0.43, 0.14, 0, 3.11, 0.14]
    set_position_2 = [-0.52, -0.71, 0.21, 0, 3.11, 0.24]
    set_position_3 = [-0.82, -0.81, 0.31, 0, 3.21, 0.34]
    set_position_4 = [-0.62, -0.91, 0.41, 0, 3.31, 0.54]
    set_position_array = [set_position_1, set_position_2, set_position_3, set_position_4]

    control_task = asyncio.create_task(control_cobot(rtde_connection, watchdog, set_position_array, setp))

    loop = asyncio.get_running_loop()

    user_finished = loop.run_in_executor(None, stdin_listener)
    await user_finished

    control_task.cancel()

    rtde_connection.send_pause()
    rtde_connection.disconnect()


async def control_cobot(rtde_connection, watchdog, set_position_array, setp):
    keep_running = True
    move_completed = True
    set_position_index = 0
    start_time = None
    end_time = None
    while keep_running:
        if set_position_index >= len(set_position_array):
            set_position_index = 0


        current_set_position = set_position_array[set_position_index]

        state = rtde_connection.receive()

        if state is None:
            break

        if move_completed and state.output_int_register_0 == 1:
            start_time = datetime.now()
            move_completed = False
            await list_to_setp(setp, current_set_position)
            print(str(set_position_index) + "/" + str(len(set_position_array)) + ": " + str(start_time) + " New pose = "
                  + str(current_set_position))
            rtde_connection.send(setp)
            watchdog.input_int_register_0 = 1
        elif not move_completed and state.output_int_register_0 == 0:
            end_time = datetime.now()
            elapsed_time = calculate_time_difference(start_time, end_time)
            print(str(set_position_index) + "/" + str(len(set_position_array)) + ": " + str(start_time) + "Move to "
                                                                                                          "confirmed "
                                                                                                          "pose = " +
                  str(state.target_q))
            print(str(set_position_index) + "/" + str(len(set_position_array)) + ": " + "Time Elapsed = "
                  + str(elapsed_time))
            move_completed = True
            watchdog.input_int_register_0 = 0
            await asyncio.sleep(1)
        rtde_connection.send(watchdog)
        set_position_index += 1


def run():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
