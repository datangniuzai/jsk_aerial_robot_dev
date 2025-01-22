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


class GloveDataHandler:
    def __init__(self):
        self.latest_data = None

        self.enable_record = True
        self.recording_times = 0
        self.glove_data_save = []
        self.csv_file_path = None

    def csv_init(self, gesture_num):
        self.csv_file_path = f"gesture{gesture_num}_data.csv"
        with open(self.csv_file_path, "w", newline="") as csv_file:
            csvwriter = csv.writer(csv_file)
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

    def one_gesture_data_save(self, address, *args):
        if self.enable_record:
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
            if len(self.glove_data_save) == 3000:
                with open(self.csv_file_path, "a", newline="") as csvfile:
                    csvwriter = csv.writer(csvfile)
                    numpy_matrix = np.array(self.glove_data_save)
                    csvwriter.writerows(numpy_matrix)
                self.glove_data_save = []
                self.recording_times = +1
                print("Recording one time")
                if self.recording_times == 5:
                    self.enable_record = False
                    print("Recording Over")

        self.latest_data = args

    def get_data(self):
        if self.latest_data is not None:
            print(f"Data: {self.latest_data}")
        else:
            print("No data.")


def main():

    glove_data_handler = GloveDataHandler()
    ip = "127.0.0.1"
    port = 9400
    gesture_num = int(input("Gesture Number: "))
    glove_data_handler.csv_init(gesture_num)
    dispatcher_instance = dispatcher.Dispatcher()
    dispatcher_instance.map("/v1/animation/slider/all", glove_data_handler.one_gesture_data_save)
    server = osc_server.BlockingOSCUDPServer((ip, port), dispatcher_instance)
    server.serve_forever()


if __name__ == "__main__":

    main()
