#!/usr/bin/env python

# xvg2gp: xmgrace to gnuplot translator
# Usage: python xvg2gp.py xmgrace_file.xmg > filename.gp
#
# written by Synge Todo <wistaria@phys.s.u-tokyo.ac.jp>
# based on avr2gpt by Julen Larrucea http://www.larrucea.eu

import sys

if len(sys.argv) < 2:
    print("Usage: " + sys.argv[0] + " xmgrace_file.xmg > filename.gp")
    sys.exit(127)

input = sys.argv[1]
print("# input file: " + input)

parse_xy = "off"
title = ""
xlabel = ""
ylabel = ""
all_data = []
line_titles = []

# Parse data from xmgrace file
for line in open(input, "r"):
    data = line.strip().split()
    if len(data) > 1 and data[0] == "@":
        # Plotting options
        if len(data) > 2 and data[1] == "title":
            title = " ".join(data[2:])
        if len(data) > 3 and data[1] == "xaxis" and data[2] == "label":
            xlabel = " ".join(data[3:])
        if len(data) > 3 and data[1] == "yaxis" and data[2] == "label":
            ylabel = " ".join(data[3:])
        if len(data) > 3 and data[2] == "legend":
            line_titles.append(" ".join(data[3:]))
    elif len(data) > 1 and data[0] == "@TYPE":
        parse_xy="on"
        line_data=[]
    else:
        # Get the points for each line
        if parse_xy == "on":
            if "&" in line:
                parse_xy = "off"
                all_data.append(line_data)
            else:
                line_data.append([line.split()[0], line.split()[1]])

# add last dataset
if parse_xy == "on":
    all_data.append(line_data)

# output gnuplot script
print("set title " + title)
print("set ylabel " + ylabel)
print("set xlabel " + xlabel)
plot_command = "plot"
for i in range(len(all_data)):
    plot_command = plot_command + " '-' index " + str(i) + " u 1:2 title " + line_titles[i] + " w l,"
print(plot_command.rstrip(","))

# output data
for i in range(len(all_data)):
    print("")
    print("# " + line_titles[i])
    for j in range(len(all_data[i])):
        print(" ".join(all_data[i][j]))
