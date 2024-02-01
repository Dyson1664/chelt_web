from django.shortcuts import render
from requests.auth import HTTPBasicAuth
import requests
import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()

import pytz
from django.utils import timezone

from datetime import datetime, timedelta
from django.core.cache import cache
from django.http import HttpResponse
from django.utils.text import slugify

from django.http import JsonResponse
import json

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

def format_distance(distance_furlongs):
    if distance_furlongs is None:
        return "Unknown distance"

    try:
        # Convert to float and calculate miles and furlongs
        total_furlongs = float(distance_furlongs)
        miles = int(total_furlongs // 8)
        furlongs = int(total_furlongs % 8)

        # Format the result
        return f"{miles}m {furlongs}f" if miles > 0 else f"{furlongs}f"
    except ValueError:
        return "Invalid distance"

def races(request):
    RACING_API_USERNAME = os.getenv('RACING_API_USERNAME')
    RACING_API_PASSWORD = os.getenv('RACING_API_PASSWORD')

    # Create a unique key for caching based on the current date
    today = datetime.now().astimezone(pytz.timezone("Europe/London")).date()
    cache_key = f'races_data_{today}'

    # Check if the data is already in the cache
    races_by_course = cache.get(cache_key)

    if races_by_course is None:
        # Data not in cache, fetch from API
        try:
            url = "https://api.theracingapi.com/v1/racecards/free"
            params = {"day": "today"}
            response = requests.get(url, auth=HTTPBasicAuth(RACING_API_USERNAME, RACING_API_PASSWORD), params=params)
            response.raise_for_status()
            racecards = response.json().get('racecards', [])

            races_by_course = {}
            for race in racecards:
                race_type = race.get('type')
                if race_type in ["Hurdle", "Chase", "NH Flat"]:
                    course = race.get('course')
                    race_name_slug = slugify(race.get('race_name'))
                    distance_str = race.get('distance_f')
                    formatted_distance = format_distance(distance_str)
                    race_details = {
                        'race_name': race.get('race_name'),
                        'start_time': race.get('off_time'),
                        'race_distance': formatted_distance,
                        'region': race.get('region'),
                        'race_class': race.get('race_class'),
                        'type': race.get('type'),
                        'prize': race.get('prize'),
                        'field_size': race.get('field_size'),
                        'going': race.get('going'),
                        'age_band': race.get('age_band'),
                        'race_type': race_type,
                        'race_name_slug': race_name_slug,
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


            now = timezone.now()

            # 'midnight' should be the start of the next day, timezone-aware
            midnight = datetime.combine(now.date() + timedelta(days=1), datetime.min.time())
            midnight = timezone.make_aware(midnight, pytz.timezone("Europe/London"))
            seconds_until_midnight = (midnight - now).seconds


            # Cache the data until midnight
            cache.set(cache_key, races_by_course, timeout=seconds_until_midnight)
        except requests.RequestException as e:
            return render(request, 'error.html', {'message': str(e)})

    return render(request, 'races.html', {'races_by_course': races_by_course, 'race_date': today})


def results(request):
    data = {'rows': [], 'error': None}

    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            race = json.loads(request.body).get('race')
            # Database connection and query execution
            with psycopg2.connect(
                dbname="results",
                user="postgres",
                password="1234567890",
                host="localhost"
            ) as conn:
                with conn.cursor() as cur:
                    query = "SELECT * FROM winners WHERE race = %s;"
                    cur.execute(query, [race])
                    data['rows'] = cur.fetchall()
        except psycopg2.DatabaseError as error:
            data['error'] = str(error)

        return JsonResponse(data)

    # For non-AJAX requests or other methods, redirect or show an error
    return render(request, 'results.html', data)




