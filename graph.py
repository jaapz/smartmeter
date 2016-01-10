#!/usr/bin/env python
""" This script looks for usage.csv in the current working directory and
renders a graph in svg format. """
import pygal
import arrow


def render_graph(date, values):
    """ Renders a graph containing the given data and saving it as
    {date}-usage.svg. """
    c = pygal.Line()
    c.title = 'Power usage on {}'.format(date)
    #c.x_labels = [str(i) for i in range(0, 25)]
    #c.x_label_rotation = 30
    c.add('usage in kW', values, fill=True, show_dots=False)
    c.render_to_file('./{}-usage.svg'.format(date))


def main():
    """ Read the data in usage.csv and group it into days. """
    with open('./usage.csv', 'r') as f:
        dates = {}

        for i, line in enumerate(f.xreadlines()):
            line_contents = line.split(',')
            date = arrow.get(line_contents[0])
            key = date.format('DD-MM-YYYY')

            # if new date, create new item in values list
            try:
                values = dates[key]
            except KeyError:
                dates[key] = []
                values = dates[key]

            values.append(float(line_contents[1]))

    for date, values in dates.iteritems():
        print('Rendering graph for {}'.format(date))
        render_graph(date, values)

if __name__ == '__main__':
    main()
