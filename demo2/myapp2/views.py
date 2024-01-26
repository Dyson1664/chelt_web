from django.shortcuts import render
from requests.auth import HTTPBasicAuth
import requests
import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()



def home(request):
    return render(request, "home.html")

def day1(request):
    return render(request, "day1.html")

def day2(request):
    return render(request, "day2.html")

def day3(request):
    return render(request, "day3.html")

def day4(request):
    return render(request, "day4.html")

def top5(request):
    return render(request, "top5.html")

def base(request):
    return render(request, "base.html")

def practice(request):
    return render(request, "practice.html")

def test(request):
    return render(request, "apitest.html")


def find_races(request):
    return render(request, "find_races.html")
def races(request):
    RACING_API_USERNAME = os.getenv('RACING_API_USERNAME')
    RACING_API_PASSWORD = os.getenv('RACING_API_PASSWORD')
    print(RACING_API_USERNAME, RACING_API_PASSWORD)
    url = "https://api.theracingapi.com/v1/racecards/free"
    params = {"day": "today"}

    try:
        response = requests.get(url, auth=HTTPBasicAuth(RACING_API_USERNAME, RACING_API_PASSWORD),
                                params=params)
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.RequestException as e:
        # Handle any errors that occur during the request
        return render(request, 'error.html', {'message': str(e)})

    racecards = response.json().get('racecards', [])
    date = racecards[0]['date'] if racecards else None


    races_by_course = {}

    for race in racecards:
        race_type = race.get('type')
        if race_type in ["Hurdle", "Chase", "NH Flat"]:
            course = race.get('course')
            race_details = {
                'race_name': race.get('race_name'),
                'start_time': race.get('off_time'),
                'race_distance': race.get('distance_f'),
                'region': race.get('region'),
                'race_class': race.get('race_class'),
                'type': race.get('type'),
                'prize': race.get('prize'),
                'field_size': race.get('field_size'),
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
    return render(request, 'races.html', {'races_by_course': races_by_course, 'race_date': date})


def results(request):
    rows = []  # Initialize rows outside the if block
    error_message = None

    if request.method == 'POST':
        race = request.POST.get('race')
        try:
            # Connect to your database
            conn = psycopg2.connect(
                dbname="results",
                user="postgres",
                password="1234567890",
                host="localhost"
            )

            # Open a cursor to perform database operations
            cur = conn.cursor()

            # Define your query here
            query = f"SELECT * FROM winners WHERE race = '{race}';"

            # Execute the query
            cur.execute(query)
            rows = cur.fetchall()


            # Close communication with the database
            cur.close()
            conn.close()

        except psycopg2.DatabaseError as error:
            print(error)
            error_message = error

    # Render the same template whether it's POST or GET
    return render(request, 'results.html', {'rows': rows, 'error_message': error_message})
#added function to get the racecards from the api

    #
    #
    # for course, races in races_by_course.items():
    #     print('Course: ', course)
    #
    #     for race in races:
    #         print(
    #             f"  Race Name: {race['race name']}, Start Time: {race['start time']}, Race Distance: {race['race distance']}, Region: {race['region']},"
    #             f"Race Class: {race['race class']}, Type: {race['type']}, Prize: {race['prize']}, Field Size: {race['field size']}, Going: {race['going']} ")
    #         for runner in race['runners']:
    #             print(
    #                 f"    Horse: {runner['horse']}, Age: {runner['age']}, Trainer: {runner['trainer']}, Owner: {runner['owner']}, Jockey: {runner['jockey']},"
    #                 f"Weight: {runner['lbs']}, Number: {runner['number']}, Form: {runner['form']}")
    #         print('\n')
