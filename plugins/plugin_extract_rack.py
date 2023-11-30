#!/usr/bin/env python

import re
from datetime import datetime
from manager import Plugin

class ExtractRackActivities(Plugin):
    def __init__(self, **kwargs):
        self.counter = 0
        self.data = []

    def format_date(self, date):
        date_obj = datetime.strptime(date, "%d/%b/%Y:%H:%M:%S +0100")
        return date_obj.strftime("%Y-%m-%d %H:%M:%S %p")

    def process(self, **kwargs):
        result = re.search(r'(/rack\?action=Opened\+Email&id=(\S+))', kwargs['request_line'], re.IGNORECASE)
        if result and 'time_stamp' in kwargs:
            self.counter += 1
            self.data.append('%s|%s' % (self.format_date(kwargs['time_stamp']), result.group(0)))

    def report(self, **kwargs):
        with open('output/activities.txt', 'w') as f:
            f.writelines('\n'.join(self.data))
        print('[+] Found (%d) matches!' % self.counter)
        print('[+] Saved to file: activities.txt')
        print(self.keywords)