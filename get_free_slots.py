from prettytable import PrettyTable
from requests import Session
import argparse

parser = argparse.ArgumentParser(description='Get free slots for AG testing')
parser.add_argument('--date', type=str, help='Format 2021-01-15', required=True)
parser.add_argument('--city', type=str, required=True)
args = parser.parse_args()

root = 'https://mojeezdravie.nczisk.sk/api/v1/web'

s = Session()
s.headers.update({
    'Content-Type': 'application/json'
})

driveins = s.get('{}/get_driveins'.format(root)).json()['payload']
my_driveins = [ drivein
                  for drivein in driveins
                    if drivein['city'] == args.city
              ]

table = PrettyTable()
table.field_names = ['title', 'opens_at', 'break_from', 'break_thru', 'closes_at', 'capacity', 'free', 'capacity_pm', 'free_pm']

for drivein in my_driveins:
    row = [drivein['title']]
    am = s.post('{}/validate_drivein_times'.format(root),
      json={
        'drivein_id': drivein['id'],
        'selected_day': '{} 00:00:00'.format(args.date)
      }
    ).json()['payload']
    row += [am['opens_at'], am['break_from'] or '', am['break_thru'] or '', am['closes_at'], am['status']['capacity'], am['status']['free']]
    if am['show_radios'] == 1:
        pm = s.post('{}/validate_drivein_times'.format(root),
          json={
            'drivein_id': drivein['id'],
            'selected_day': '{} 12:00:00'.format(args.date)
          }
        ).json()['payload']
        row += [pm['status']['capacity'], pm['status']['free']]
    else:
        row += ['', '']
    table.add_row(row)

print(table)
