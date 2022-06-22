import requests
import json
import pandas as pd
from ratelimit import limits, sleep_and_retry

CALLS = 50
RATE_LIMIT = 60

@sleep_and_retry
@limits(calls=CALLS, period=RATE_LIMIT)
def call_api(url):
    response = requests.get(url)
    if response.status_code < 200 or response.status_code >= 300:
        raise Exception('API response: {}'.format(response.status_code))
    return response  # codes in the 2xx range indicate success,


def ExtractCompletedChallenges(user, destination_filename):
    page = 0  # zero-based count
    all_challenges = []

    while(True):
        current_url = ('http://www.codewars.com/api/v1/users/' + user +
                       '/code-challenges/completed?page=' +
                       str(page))
        r = call_api(current_url)

        input_json = r.text
        input_dict = json.loads(input_json)
        all_challenges += input_dict["data"]

        page += 1

        # no more data to extract
        if page > int(input_dict["totalPages"] - 1):
            break

    df = pd.DataFrame(all_challenges, columns=[
                      'id', 'name', 'slug',
                      'completedAt', 'completedLanguages'])
    df.to_csv(destination_filename, sep='\t',
              encoding='utf-8-sig', index=False)
