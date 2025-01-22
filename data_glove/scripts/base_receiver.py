#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2024/01/20 00:04
# @Author : JIAXUAN LI
# @File : base_receiver.py
# @Software: PyCharm

import socket

from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
from typing import Tuple, Any, Optional


def get_local_ip() -> Optional[str]:
    """
    Retrieve the local IP address of the machine.

    Returns:
        Optional[str]: The local IP address if successfully retrieved;
                       None if an error occurs.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.connect(("8.8.8.8", 80))
            local_ip = sock.getsockname()[0]

        if not local_ip:
            raise ValueError("Local IP address could not be retrieved.")

        return local_ip

    except Exception as error:
        print(f"Error retrieving local IP address: {error}")
        raise SystemExit("Exiting program due to error.")


def print_glove_data(glove_data: Tuple[Any, ...]) -> None:
    """
    Prints specific joint data from the glove data tuple.

    Args:
        glove_data (Tuple[Any, ...]): The tuple containing glove data.
    """
    print(glove_data)
    # print(glove_data[5], glove_data[6], glove_data[8])  # Thumb: base, middle, tip
    # print(glove_data[9], glove_data[10])  # Index finger: base, middle
    # print(glove_data[12], glove_data[13])  # Middle finger: base, middle
    # print(glove_data[15], glove_data[16])  # Ring finger: base, middle
    # print(glove_data[18], glove_data[19])  # Pinky: base, middle
    # print(glove_data[21])  # Palm openness degree


def date_receive(address: str, *args: Any) -> None:
    """
    Processes received OSC messages and determines the glove's hand type.

    Args:
        address (str): The OSC message address.
        *args (Any): Additional arguments from the OSC message.
    """
    if args[2] == 1:  # Left hand
        print_glove_data(args)
    elif args[2] == 2:  # Right hand
        print_glove_data(args)
    else:
        print("Reception Error")


if __name__ == "__main__":
    # Set up an OSC dispatcher
    dispatcher: Dispatcher = Dispatcher()
    dispatcher.map("/v1/animation/slider/all", date_receive)

    # Update with your IP address and port number
    ip: str = get_local_ip()
    port: int = 9400
    server: BlockingOSCUDPServer = BlockingOSCUDPServer((ip, port), dispatcher)

    print("Listening for OSC messages...")
    server.serve_forever()
