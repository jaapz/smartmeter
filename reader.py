#!/usr/bin/env python
""" Read out the telegram my smart meter sends me over it's P1-port every 10
seconds.  """
import serial
import sys
import re
from time import time
from collections import namedtuple

# Contains parsed lines.
Line = namedtuple('Line', 'id value unit line')

# This should match every line in the telegram (except the first and last), and
# parse it into 4 groups.
pattern = re.compile(r'(.*)\(([^\*]*)(?:\*(.*))?\)')


def parse_line(line):
    """ Parses one line into a Line. Tries to parse the value as a float, if
    that doesn't work it falls back to str. """
    m = re.match(pattern, line)
    if m is None:
        return

    try:
        val = float(m.group(2))
    except ValueError:
        val = str(m.group(2))

    return Line(
        line=m.group(0),
        id=m.group(1),
        value=val,
        unit=m.group(3)
    )


def parse_telegram(lines):
    """ Parses a telegram into a list of Lines. """
    # First line is always the meter identifier, we don't need it right now so
    # we just remove it.
    lines.pop()
    return [parse_line(line) for line in lines]


def append_to_csv(filename, identifier, lines):
    """ Append the data for a specific line to the given file. """
    wanted = [l for l in lines if l is not None and l.id == identifier][0]
    with open(filename, 'a') as f:
        f.write('{},{},{}\n'.format(
            int(time()),
            wanted.value,
            wanted.unit
        ))


def main():
    """ Opens the connection and starts listening for new lines on the serial
    connection. Empty lines are discarded. """
    # These settings change per meter, these are the settings that work for
    # mine.
    conn = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate=9600,
        bytesize=serial.SEVENBITS,
        parity=serial.PARITY_EVEN,
        stopbits=serial.STOPBITS_ONE,
        timeout=1
    )

    lines = []
    while True:
        try:
            line = conn.readline()
        except:
            print('Could not read line, exiting.')
            break

        stripped = line.strip()

        if stripped == '':
            continue

        # When we encounter the closing exclamation mark, parse
        # the telegram. Otherwise add this line to the telegram.
        if stripped == '!':
            telegram = parse_telegram(lines)
            # For now only append the current usage to a csv file.
            append_to_csv('./usage.csv', '1-0:1.7.0', telegram)
            lines = []
        else:
            lines.append(stripped)

    try:
        conn.close()
    except:
        print('Could not cleanly close connection')

if __name__ == '__main__':
    main()
