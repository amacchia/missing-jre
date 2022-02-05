import csv
import json


month_dict = {
    'Jan': '01',
    'Feb': '02',
    'Mar': '03',
    'Apr': '04',
    'May': '05',
    'Jun': '06',
    'Jul': '07',
    'Aug': '08',
    'Sep': '09',
    'Oct': '10',
    'Nov': '11',
    'Dec': '12',
}


def convert_date(date: str):
    day, month, year = date.split('-')
    return f'20{year}-{month_dict[month]}-{day}'


with open('jre-episode-list.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames=[
                            'episodeNumber', 'guest', 'date'])
    episode_map = {}
    for row in reader:
        if not row['episodeNumber'].startswith('#'):
            continue
        row['date'] = convert_date(row['date'])
        episode_map[row['episodeNumber']] = row

for i in range(1, 1771):
    if episode_map.get(f'#{i}') == None:
        print(f'Missing ep: {i}')

with open('lambda/master-list.json', 'w') as fp:
    json.dump(episode_map, fp)
