#!/usr/bin/env python3
import csv
from icalendar import Calendar, Event, Alarm
from datetime import datetime
import argparse
from datetime import timedelta
parser = argparse.ArgumentParser()
parser.add_argument('input', type=str, help='Input csv file containing calendar events')
parser.add_argument('output', type=str, help='Output ics file')
args = parser.parse_args()



def csv2ical(input_file, output_file):
  """csv2ical

  Convert a cvs file with event information to ical, which can be imported into
  Google Calendar, Microsoft Outlook and etc.

  Parameters
  ----------
  input_file : str
  output_file : str

  Returns
  -------
  Empty
  """
 
  ### set reminder before shift start ####
  tigger_before_shift = timedelta(minutes=-int(60)) 
  duration = timedelta(minutes=-int(45)) 
  
  with open(input_file) as csv_file:
    reader = csv.reader(csv_file)


    # required to be compliant:
    cal = Calendar()
    cal.add('prodid', '-//'+input_file+'//mxm.dk//')
    cal.add('version', '2.0')
    cal.add('X-WR-TIMEZONE', 'Asia/Hong_Kong')
    cal.add('X-WR-CALNAME', '更表')
    cal.add('X-WR-CALDESC', '更表')
    cal.add('CALSCALE', 'GREGORIAN')


    for n, row in enumerate(reader):
      #Skip header row
      if n == 0:
        continue
      summary = row[0]
      if row[2] == '':
           dtstart = datetime.strptime(row[1]+' 00:00', '%Y/%m/%d %H:%M')
           set_alarm = False 
      else: 
           dtstart = datetime.strptime(row[1]+' '+row[2], '%Y/%m/%d %H:%M')
           set_alarm = True 
      dtend = dtstart + timedelta(minutes=495) 
      description = row[5].strip()
      location = row[4].strip()
     
      event = Event()
      event.add('summary', summary)
      event.add('dtstart', dtstart)
      event.add('dtend', dtend)
      event.add('description', description)
      event.add('location', location)
      if set_alarm == True :
         alarm=Alarm()
         alarm.add('TRIGGER',tigger_before_shift)
         alarm.add('DESCRIPTION','返工啦')
         alarm.add('REPEAT','3')
         alarm.add('DURATION',duration)
         alarm.add('ACTION','DISPLAY')
         event.add_component(alarm)
      cal.add_component(event)
    with open(output_file, 'wb') as out_f:
      out_f.write(cal.to_ical())
      out_f.close()


def main(args):
  csv2ical(args.input, args.output)
  

if __name__ == "__main__":
  main(parser.parse_args())
