import requests
import json
import pandas as pd
from ratelimit import limits, sleep_and_retry


# =========================================================================
# Purpose of this module  :
# 1. Create a csv file containing the the number of katas solved on
#    each day
# 2. Create a csv file showing the relationship between the rank of
#    the katas solved and the language used to solve the kata
#
# - The files will be saved to a folder called "data".
# - function returns True if data collection was successful.
# - data collection can take up to 5 minutes depending on old your account is
#   and how many katas you have solved.
#
# =========================================================================

# At 50 API calls per minute, estimated time in seconds = total katas solved

CALLS = 50  # < 150 when number of pages > 1
RATE_LIMIT = 60


@sleep_and_retry
@limits(calls=CALLS, period=RATE_LIMIT)
def call_api(url):
    response = requests.get(url)
    if response.status_code < 200 or response.status_code >= 300:
        raise Exception('API response: {}'.format(response.status_code))
    return response  # codes in the 2xx range indicate success,


def CollectData(user):

    date_count = {}  # stores date and number of katas solved on that date
    language_rank_count = {}
    # There are at most 200 items per page
    page = -1  # zero-based count

    while(True):
        page += 1
        print("Current page = ", page)

        current_url = ('http://www.codewars.com/api/v1/users/' + user +
                       '/code-challenges/completed?page=' +
                       str(page))
        r = call_api(current_url)
        input_json = r.text
        input_dict = json.loads(input_json)
        data = (input_dict["data"])  # data is a list

        if len(data) == 0:  # no more data to extract
            break
        for x in range(0, len(data)):  # for each kata solved
            # find rank of current kata
            kata_rank = get_kata_rank(data[x]["id"])
            if kata_rank is None:
                continue  # deleted katas and katas in beta are ignored

            # extract date
            full_date = data[x]["completedAt"]  # YYYY-MM-DD TIME
            date = full_date[0:10]  # YYYY-MM-DD
            date_count[date] = date_count[date] + \
                1 if date in date_count else 1

            # extract list of completed languages for current kata
            completedLanguages = data[x]["completedLanguages"]
            # update frequency for language-rank relationship
            for lang in completedLanguages:
                if lang in language_rank_count.keys():
                    language_rank_count[lang][kata_rank] += 1
                else:
                    rank_frequency = {
                        '1 kyu': 0, '2 kyu': 0, '3 kyu': 0, '4 kyu': 0,
                        '5 kyu': 0, '6 kyu': 0, '7 kyu': 0, '8 kyu': 0
                    }
                    rank_frequency[kata_rank] = 1
                    language_rank_count[lang] = rank_frequency

    # convert date_count dictionary to dataframe
    date_df = pd.DataFrame(date_count.items(), columns=['Date', 'DateValue'])

    # convert language_rank_count dictionary to dataframe
    lang_df = pd.DataFrame.from_dict(language_rank_count)

    # save dataframes as csv files to data folder
    file_name = "data/" + str(user) + "_language_date_count"
    date_df.to_csv(file_name, sep='\t', encoding='utf-8-sig', index=False)

    file_name = "data/" + str(user) + "_language_rank_count"
    lang_df = lang_df.reset_index(level=0)
    lang_df.to_csv(file_name, sep='\t', encoding='utf-8-sig', index=False)
# =============================================================================
# lang_df should look like this :
# index	python	cpp	vb
# 1 kyu	0	0	0
# 2 kyu	0	2	0
# 3 kyu	1	5	0
# 4 kyu	0	27	0
# 5 kyu	3	24	0
# 6 kyu	7	32	0
# 7 kyu	2	23	0
# 8 kyu	5	39	1
# =============================================================================


def get_kata_rank(kata_id):  # returns the rank of a kata as a string
    url = 'https://www.codewars.com/api/v1/code-challenges/' + kata_id
    r = call_api(url)
    input_json = r.text
    input_dict = json.loads(input_json)
    return input_dict["rank"]["name"]
