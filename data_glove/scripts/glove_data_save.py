#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2024/01/20 00:04
# @Author : JIAXUAN LI
# @File : glove_data_save.py
# @Software: PyCharm

import csv
import time
import numpy as np
from pythonosc import dispatcher, osc_server

from base_receiver import get_local_ip


class GloveDataHandler:
    def __init__(self) -> None:
        """
        Constructor: Initializes the glove data handler.
        Initializes parameters related to data recording, the data storage list, and the CSV file path.
        """
        self.latest_data: list = []
        self.enable_record: bool = True
        self.recording_times: int = 0
        self.glove_data_save: list = []
        self.csv_file_path: str = None

    def csv_init(self, gesture_num: int) -> None:
        """
        Initializes the CSV file for saving glove data.
        Creates a file named "gesture<gesture_num>_data.csv" and writes the header.

        :param gesture_num: The gesture number used to name the CSV file.
        """
        self.csv_file_path = f"gesture{gesture_num}_data.csv"
        with open(self.csv_file_path, "w", newline="") as csv_file:
            csvwriter = csv.writer(csv_file)
            # Write the header of the CSV file
            csvwriter.writerow(
                [
                    "Thumb.base",
                    "Thumb.middle",
                    "Thumb.tip",
                    "IndexFinger.base",
                    "IndexFinger.middle",
                    "MiddleFinger.base",
                    "MiddleFinger.middle",
                    "RingFinger.base",
                    "RingFinger.middle",
                    "Pinky.base",
                    "Pinky.middle",
                    "PalmOpennessDegree",
                ]
            )

    def one_gesture_data_save(self, address: str, *args: tuple) -> None:
        """
        Receives glove data for one gesture and saves it to the CSV file.
        Every 3000 data points, the data will be written to the CSV file and reset.

        When the recording reaches 5 times, it stops recording.

        :param address: The OSC address for the message
        :param *args: The parameters passed with the OSC message, containing glove joint data.
        """
        if self.enable_record:
            # Append the current glove data to the list
            self.glove_data_save.append(
                [
                    args[5],
                    args[6],
                    args[8],
                    args[9],
                    args[10],
                    args[12],
                    args[13],
                    args[15],
                    args[16],
                    args[18],
                    args[19],
                    args[21],
                ]
            )
            # Once 3000 data points are received, save them to the CSV file
            if len(self.glove_data_save) == 3000:
                with open(self.csv_file_path, "a", newline="") as csvfile:
                    csvwriter = csv.writer(csvfile)
                    numpy_matrix = np.array(self.glove_data_save)
                    csvwriter.writerows(numpy_matrix)
                self.glove_data_save = []  # Reset the data list
                self.recording_times += 1  # Increment the recording count
                print("Recording one time")
                # Stop recording after 5 times
                if self.recording_times == 5:
                    self.enable_record = False
                    print("Recording Over")

        self.latest_data = args  # Update the latest data

    def get_data(self) -> None:
        """
        Retrieves the latest glove data and prints it.
        If no data is available, prints a message indicating that.

        :return: None
        """
        if self.latest_data is not None:
            print(f"Data: {self.latest_data}")
        else:
            print("No data.")


def main() -> None:
    """
    Main function: Initializes the glove data handler and starts the OSC server to receive data.
    1. Prompts the user to enter the gesture number and initializes the CSV file.
    2. Configures the dispatcher to handle incoming OSC messages.
    3. Starts the OSC server and begins receiving data.
    """
    glove_data_handler = GloveDataHandler()

    local_ip = get_local_ip()
    port: int = 9400

    gesture_num: int = int(input("Gesture Number: "))
    glove_data_handler.csv_init(gesture_num)
    dispatcher_instance = dispatcher.Dispatcher()
    dispatcher_instance.map("/v1/animation/slider/all", glove_data_handler.one_gesture_data_save)
    server = osc_server.BlockingOSCUDPServer((local_ip, port), dispatcher_instance)
    server.serve_forever()


if __name__ == "__main__":
    main()  # Execute the main function
