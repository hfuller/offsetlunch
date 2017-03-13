from __future__ import print_function
import psycopg2
import psycopg2.extras
import json
from six.moves import urllib
import icalendar

print("Loading config file.")
with open("config.json") as jconfig:
	config = json.load(jconfig)
print("ok")

db = psycopg2.connect(dbname=config['db']['name'], user=config['db']['user'], password=config['db']['password'])

print("loading ical event sources from db")
cur = db.cursor(cursor_factory = psycopg2.extras.DictCursor)
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
		cur.execute(''' INSERT INTO event(uid,source_id,name,starts_at) VALUES(%s,%s,%s,%s) on conflict (uid) do update set (name,starts_at) = (%s,%s); ''',
				[e_uid, e_source_id, e_name, e_starts_at, e_name, e_starts_at])
		print("INSERT")
db.commit()
print("COMMIT")
