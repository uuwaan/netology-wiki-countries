import json
import requests

import wikipedia
import ratelim
import indicator

COUNTRIES_FILE = "countries.json"
LINKS_FILE = "country_links.txt"

FMT_OUTPUT = "{0} - {1}"
FMT_PROGRESS = "found {0}/{1}"
MSG_DONE = "Done!"

API_RATELIMIT = 10
PMN_WIDTH = 20


def terms_list(terms_path):
    with open(terms_path, "r", encoding="utf-8-sig") as terms_file:
        file_data = json.load(terms_file)
    return [item["name"]["common"] for item in file_data]


def main():
    pacman = indicator.Pacman(PMN_WIDTH)
    rlim = ratelim.TokenBucket(API_RATELIMIT)
    terms = terms_list(COUNTRIES_FILE)
    nterms = len(terms)
    with open(LINKS_FILE, "w", encoding="utf-8") as out_file, \
            requests.Session() as sess:
        for idx, (term, url) in enumerate(wikipedia.PageFinder(terms, sess)):
            out_file.writelines((FMT_OUTPUT.format(term, url), "\n"))
            pacman.update(FMT_PROGRESS.format(idx + 1, nterms))
            rlim.wait(1)
    pacman.clear()
    print(MSG_DONE)


main()
