import os
import time
import datetime
import argparse
import requests
from parsers import *


def get_html(url):
    r = requests.get(url)
    html = r.content.decode("utf-8")
    return html


def crawl_grad():
    # html = open("data/grad_sample.html").read()
    html = get_html("https://www.laundryalert.com/cgi-bin/stan9570/LMPage")
    data = parse_grad(html)
    return data


def crawl_munger1():
    # html = open("data/munger1_sample.html").read()
    html = get_html("https://www.laundryalert.com/cgi-bin/stan9570/LMRoom?CallingPage=LMPage&Halls=16&PreviousHalls=&RoomPersistence=&MachinePersistenceA=&MachinePersistenceB=")
    data = parse_hall(html)
    return data


def to_csv(data, timestamp, dest_path, reset=False):
    if reset:
        f = open(dest_path, "w")
    else:
        f = open(dest_path, "a")
    for d in data:
        f.write(", ".join(d) + ", {}\n".format(timestamp))
    f.close()


def parse_args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--delta", "-d", type=int, default=10, help="Interval in second")
    p.add_argument("--output_path", type=str, help="Where to put outputdata")
    p.add_argument("--reset", "-r", action="store_true", help="Remove all data")
    p.add_argument("--verbose", "-v", action="store_true", help="Be verbose")
    return p.parse_args()


def main():
    args = parse_args()
    t0 = 0
    reset = args.reset
    while True:
        if time.time() - t0 < args.delta:
            pass
        else:
            t0 = time.time()
            timestamp = datetime.datetime.now()
            print(timestamp)
            data = crawl_grad()
            if args.output_path:
                dest = os.path.join(args.output_path, "grad.csv")
                to_csv(data, timestamp, dest, reset=reset)
            data = crawl_munger1()
            if args.output_path:
                dest = os.path.join(args.output_path, "munger1.csv")
                to_csv(data, timestamp, dest, reset=reset)
            reset = False


if __name__ == "__main__":
    main()
