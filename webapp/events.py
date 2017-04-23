#!/usr/bin/python3
# -*- coding: utf-8 -*-
# events.py

class Events(object):
    """
    Manages calendar events
    """
    def __init__(self):
        pass
        
    def get_events(self, date_start='20160101', date_end='20171231'):
        """
        retrieve the events for date range from database
        (currently just returns test data)
        """
        events = [
            ['20170417', '0900', 'Initial Version'],
            ['20170417', '1100', 'Update with database'],
            ['20170422', '0930', 'bug fixes'],
            ['20170422', '1130', 'more fixes'],
            ['20170422', '1400', 'calendar page'],
            ]
        print(events)
        return events

    def parse_events_for_web(self, events):
        """
        takes a flat dataset of events and parses into dictionary
        ready for web display
        {'date':'20170417', 'event':[
            {'time':'0900', 'details':'Initial Version'},
            {'time':'1100', 'details':'Update with database'},
            ]
        },
        {'date':'20170422', 'event':[
            {'time':'0930', 'details':'bug fixes'},
            {'time':'1130', 'details':'more fixes'},
            {'time':'1400', 'details':'calendar page'},
            ]
        },        
        """
        all_days = []
        for e in events:
            print('e = ', e)
            all_days.append(e[0])
        unique_days = list(set(all_days))
        print('unique days = ', unique_days)
        res = []
        cur_event = {}
        current_day = ''
        for day in unique_days:  # what the hell - use something better
            cur_event = {}
            cur_event['date'] = day
            for e in events:
                days_events = []
                if e[0] == day:
                    cur_event['event'] = {'time': e[1], 'details': e[2]}
                    days_events.append(cur_event)
                    
            res.append(days_events)
        return res