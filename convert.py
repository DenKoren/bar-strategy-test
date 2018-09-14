import sys
import csv
import os.path

from trader import Trader
from bars import Bar


src = sys.argv[1]
dst = sys.argv[2]
aggregation = sys.argv[3]

in_file = open(src, "r")

out_opens = open(os.path.join(dst, 'openings.csv'), 'w')
out_closes = open(os.path.join(dst, 'closes.csv'), 'w')
out_maxs = open(os.path.join(dst, 'maxes.csv'), 'w')
out_mins = open(os.path.join(dst, 'mines.csv'), 'w')
out_avg_openclose = open(os.path.join(dst, 'average_open-close.csv'), 'w')
out_avg_maxmin = open(os.path.join(dst, 'average_max-min.csv'), 'w')

history = csv.reader(in_file)

openings = csv.writer(out_opens)
closes = csv.writer(out_closes)
maxes = csv.writer(out_maxs)
mines = csv.writer(out_mins)
mids_oc = csv.writer(out_avg_openclose)
mids_mm = csv.writer(out_avg_maxmin)


def fmt(bar):
    """
    :type bar: Bar
    :rtype: str
    """
    return """
    
    """.format(
        ts=bar.datetime.timestamp(),
        open=bar.open
    )


for row in history:
    bar = Trader.parse_chart_row(row)

    openings.writerow([bar.datetime.timestamp(), bar.open])
    closes.writerow([bar.datetime.timestamp(), bar.close])
    maxes.writerow([bar.datetime.timestamp(), bar.max])
    mines.writerow([bar.datetime.timestamp(), bar.min])
    mids_oc.writerow([bar.datetime.timestamp(), (bar.open + bar.close) / 2])
    mids_mm.writerow([bar.datetime.timestamp(), (bar.min + bar.max) / 2])
