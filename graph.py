#!/usr/bin/env python
""" This script looks for usage.csv in the current working directory and
renders a graph in svg format. """
import pygal
import arrow

with open('./usage.csv', 'r') as f:
    values = []
    times = []
    for i, line in enumerate(f.xreadlines()):
        line_contents = line.split(',')
        values.append(float(line_contents[1]))

        if i % 300 == 0:
            times.append(arrow.get(line_contents[0]).format('DD-MM-YYYY HH:mm:ss'))
        else:
            times.append('')

    c = pygal.Line()
    c.title = 'Power usage in kW'
    c.x_labels = times
    c.x_label_rotation = 30
    c.add('power', values, fill=True, show_dots=False)
    c.render_to_file('./usage.svg')
