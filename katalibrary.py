import requests
import json
import pandas as pd
from ratelimit import limits, sleep_and_retry
import sys
CALLS = 25
RATE_LIMIT = 60


@sleep_and_retry
@limits(calls=CALLS, period=RATE_LIMIT)
def call_api(url):
    response = requests.get(url)
    return response


def print_progress_bar(index, total, label=""):
    n_bar = 50  # Progress bar width
    progress = index / total
    sys.stdout.write('\r')
    sys.stdout.write(
        f"[{'=' * int(n_bar * progress):{n_bar}s}] {int(100 * progress)}%  {label}")
    sys.stdout.flush()


def UpdateKataLibrary(library_path, compkatapath):

    df = pd.read_csv(compkatapath, sep='\t')
    library = pd.read_csv(library_path, sep='\t')

    user_ids = df['id'].tolist()  # list of ids of completed katas
    library_ids = library['id'].tolist()  # initial list of ids in library
    kata_info = []  # new collected katas
    missing_katas_ids = []  # list of ids of missing katas from codewars

    for i in range(0, len(user_ids)):
        kata_id = user_ids[i]
        print_progress_bar(i, len(user_ids)-1)
        if kata_id not in library_ids:
            #  make request
            url = 'https://www.codewars.com/api/v1/code-challenges/' + kata_id
            r = call_api(url)
            if r.status_code != 404:  # 404 = kata was deleted
                # check if request was unsuccessful
                if r.status_code < 200 or r.status_code >= 300:
                    print('API response: {}'.format(r.status_code))
                    break
                input_json = r.text
                input_dict = json.loads(input_json)
                kata_info.append(input_dict)
            else:
                missing_katas_ids.append(kata_id)

    print(len(kata_info), "new katas added")
    print(len(missing_katas_ids), "katas missing from codewars")
    print(missing_katas_ids)

    # remove missing katas from df and update compkatas
    new_df = df[~df.id.isin(missing_katas_ids)]
    new_df.to_csv(compkatapath, sep='\t',
                  encoding='utf-8-sig', index=False)

    # merge newly collected kata to library
    new_kata_info = pd.DataFrame(kata_info)
    library = pd.concat([library, new_kata_info], ignore_index=False)
    library.to_csv(library_path, sep='\t',
                   encoding='utf-8-sig', index=False)


# =============================================================================
# before_library = pd.read_csv(library_path, sep='\t')
# start_time = time.time()
# UpdateKataLibrary("data/Unnamed_compkatas")
# print("--- %s seconds ---" % (time.time() - start_time))
# after_library = pd.read_csv(library_path, sep='\t')
# after_library.drop_duplicates()
# =============================================================================

# Note some info found in library are outdated.
# totalAttempts, totalCompleted, totalStars, voteScore,  ...
# To have updated info, ...
