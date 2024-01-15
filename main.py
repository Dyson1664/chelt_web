import requests
from requests.auth import HTTPBasicAuth

url = "https://api.theracingapi.com/v1/racecards/free"
params = {
    "day": "today"
}

response = requests.request("GET", url, auth=HTTPBasicAuth('tVZc01kImFmrQ87tu6tJNyQs', 'WVxhNvh8K0rWJTWP5cWSHRiT'), params=params)
racecards = response.json().get('racecards', [])

races_by_course = {}

for race in racecards:
    race_type = race.get('type')
    if race_type in ["Hurdle", "Chase", "NH Flat"]:
        course = race.get('course')
        race_details = {
            'race name': race.get('race_name'),
            'start time': race.get('off_time'),
            'race distance': race.get('distance_f'),
            'region': race.get('region'),
            'race class': race.get('race_class'),
            'type': race.get('type'),
            'prize': race.get('prize'),
            'field size': race.get('field_size'),
            'going': race.get('going'),
            'runners': []
            }

        for runner in race.get('runners', []):
            runner_details = {
                'horse': runner.get('horse'),
                'age': runner.get('age'),
                'trainer': runner.get('trainer'),
                'owner': runner.get('owner'),
                'jockey': runner.get('jockey'),
                'lbs': runner.get('lbs'),
                'number': runner.get('number'),
                'form': runner.get('form'),
            }

            race_details['runners'].append(runner_details)

        if course not in races_by_course:
            races_by_course[course] = [race_details]
        else:
            races_by_course[course].append(race_details)


for course, races in races_by_course.items():
    print('Course: ', course)
    for race in races:
        print(f"  Race Name: {race['race name']}, Start Time: {race['start time']}, Race Distance: {race['race distance']}, Region: {race['region']},"
              f"Race Class: {race['race class']}, Type: {race['type']}, Prize: {race['prize']}, Field Size: {race['field size']}, Going: {race['going']}")
        for runner in race['runners']:
            print(f"    Horse: {runner['horse']}, Age: {runner['age']}, Trainer: {runner['trainer']}, Owner: {runner['owner']}, Jockey: {runner['jockey']},"
                  f"Weight: {runner['lbs']}, Number: {runner['number']}, Form: {runner['form']}")
























# for race in racecards:
#     race_type = race.get('type')
#     if race_type in ["Hurdle", "Chase", "NH Flat"]:
#         course = race.get('course')
#         race_details = {
#         'Race name': race.get('race_name'),
#         'Distance': race.get("distance_f"),
#         'Prize': race.get("prize"),
#         'Field size': race.get("field_size"),
#         'Going': race.get("going"),
#         "Runners": []
#         }
#         runners = race.get('runners', [])
#         for runner in runners:
#             horse = runner.get('horse')
#             runner_details = {
#             'Trainer': runner.get("trainer"),
#             'Owner': runner.get("owner"),
#             'Jockey': runner.get("jockey"),
#             "Racing weight lbs": runner.get("lbs")
#             }
#             race_details['Runners'].append(runner_details)
#
#
#
#             if course not in dict:
#                 dict[course] = [race_details]
#             else:
#                 dict[course].append(race_details)
#
#
#             # if horse not in dict:
#             #     dict2[horse] = [runner_details]
#             # else:
#             #     dict2[horse].append(runner_details)
#
# for place, info in dict.items():
#     print(f'Course: {place}')
#     for i in info:
#         for k, v in i.items():
#             print(f'{k}: {v}')
#             # horse_info = i.get('Runners')
#             # for horse in horse_info:
#             #     print(horse)
#
#


#
#     print('\n')
#
# print('***********************************')
#
# for horse, info in dict2.items():
#     print(f'Horse: {horse}')
#     for i in info:
#         for k, v in i.items():
#             print(f'{k}: {v}')
#     print('\n')

