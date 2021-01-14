city = 'Bratislava'
date = '2021-01-15'

from prettytable import PrettyTable
from requests import Session

root = 'https://mojeezdravie.nczisk.sk/api/v1/web'

s = Session()
s.headers.update({
    'Content-Type': 'application/json'
})

driveins = s.get('{}/get_driveins'.format(root)).json()['payload']
my_driveins = [ drivein
                  for drivein in driveins
                    if drivein['city'] == city
              ]

table = PrettyTable()
table.field_names = ['title', 'opens_at', 'break_from', 'break_thru', 'closes_at', 'capacity', 'free', 'capacity_pm', 'free_pm']

for drivein in my_driveins:
    row = [drivein['title']]
    am = s.post('{}/validate_drivein_times'.format(root),
      json={
        'drivein_id': drivein['id'],
        'selected_day': '{} 00:00:00'.format(date)
      }
    ).json()['payload']
    row += [am['opens_at'], am['break_from'] or '', am['break_thru'] or '', am['closes_at'], am['status']['capacity'], am['status']['free']]
    if am['show_radios'] == 1:
        pm = s.post('{}/validate_drivein_times'.format(root),
          json={
            'drivein_id': drivein['id'],
            'selected_day': '{} 12:00:00'.format(date)
          }
        ).json()['payload']
        row += [pm['status']['capacity'], pm['status']['free']]
    else:
        row += ['', '']
    table.add_row(row)

print(table)
