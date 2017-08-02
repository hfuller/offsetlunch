from __future__ import print_function

import psycopg2, psycopg2.extras
import icalendar
import time
from six.moves import urllib
from multiprocessing.dummy import Pool #Threads work and processes don't. WHo knows why? Not me.


class EventProcessor:
    def __init__(self, db):
        self.db = db

        print("Setting up periodic tasks")
        self.pool = Pool(processes=1)
        self.pool.apply_async(self.run_async, [], callback=print)

    def run_async(self):
        while True:
            print("Running async thread stuff")
            self.poll_sources()
            time.sleep(300)
    
    def poll_sources(self):
        print("loading ical event sources from db")
        cur = self.db.cursor(cursor_factory = psycopg2.extras.DictCursor)
        cur.execute(""" SELECT id, name, url FROM event_source WHERE type = 'ical' """)
        sources = cur.fetchall()
        for source in sources:
            print("Loading", source['name'], "from", source['url'])
            f = urllib.request.urlopen(source['url'])
            strcal = f.read().decode("utf-8")
            cal = icalendar.Calendar.from_ical(strcal)
            for event in cal.walk('vevent'):
                print(event)
                e_uid = str(event['UID'])
                e_source_id = source['id']
                e_name = str(event['DESCRIPTION'])
                e_starts_at = str(event['DTSTART'].dt)
                cur.execute(''' INSERT INTO event(uid,source_id,name,starts_at) VALUES(%s,%s,%s,%s) ON CONFLICT (uid) DO UPDATE SET (name,starts_at) = (%s,%s); ''', [e_uid, e_source_id, e_name, e_starts_at, e_name, e_starts_at])
                print("INSERT")
        self.db.commit()
        print("COMMIT")

        pass
