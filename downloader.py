#!/usr/bin/python3
import shlex
import re
from subprocess import Popen, PIPE
from threading import Timer


def run(cmd, timeout_sec):
    proc = Popen(shlex.split(cmd), stdout=PIPE, stderr=PIPE)
    timer = Timer(timeout_sec, proc.kill)
    try:
        timer.start()
        stdout, stderr = proc.communicate()
    finally:
        timer.cancel()
        return stdout.decode('utf-8')


def parseSearchResults(data):
    results = []
    data = data.splitlines()

    while len(data) > 0:
        line = data.pop(0)
        if re.match('\[.+\]', line):
            try:
                link = re.split('^\[.+\]\s', line)[1]

                line = data.pop(0)
                size = re.match('Size:\s(.+KB)', line).group(1)
                bitrate = re.search('Bitrate:\s(.+)\sLen', line).group(1)
                length = re.search('Length:\s(.+)\sQueue', line).group(1)
                queue = re.search('Queue:\s(.+)\sSpeed', line).group(1)
                speed = re.search('Speed:\s(.+)\sFree', line).group(1)
                free = re.search('Free:\s(.+)\sfiletype', line).group(1)

                filetype = re.search('\.([a-zA-Z0-9]+)$', link).group(1)

                result = {
                    'link': link,
                    'size:': size,
                    'bitrate:': bitrate,
                    'length:': length,
                    'queue:': queue,
                    'speed:': speed,
                    'free:': free,
                    'filetype:': filetype,
                }
                results.append(result)

            except Exception as e:
                pass

    return results


out = run('museekcontrol --gs "holla back girl"', 5)
print(out)
