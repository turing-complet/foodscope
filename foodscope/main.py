import json
import os

import requests

# food_url = "https://foodb.ca/api/v1/foodreport/food"
compound_url = "https://foodb.ca/api/v1/compoundreport/compound"
report_url = "https://foodb.ca/api/v1/contentreport/content"


def prep_data(data):
    data["api_key"] = os.getenv("FOODB_KEY")
    return json.dumps(data)


def get_compound(name):
    search = {"compound_name": name, "page": 1}
    resp = requests.get(compound_url, data=prep_data(search))
    return resp.json()


def get_matching_foods(compound_id):
    search = {"compound_id": compound_id, "page": 1}
    resp = requests.get(report_url, data=prep_data(search))
    return resp.json()


if __name__ == "__main__":
    sulfur = get_compound("sulfur")
    print(sulfur)
    sulfur_id = sulfur["value"]["id"]
    foods = get_matching_foods(sulfur_id)
    print(foods)
