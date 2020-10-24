"""
Author: Ethan Johnson
Last Modified: October 24th, 2020
File Name: reader.py
"""


def parse_line(line):
    output = list(line)
    for i in range(1, len(output)):
        if output[i] == ' ':
            output[i] = '+'

    return "".join(output)


def read_from_file(filename):
    output = []
    file = open(filename, "r")

    for line in file:
        output.append('https://google.com/maps/search/' + parse_line(line))

    return output
