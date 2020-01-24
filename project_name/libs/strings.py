"""
libs.strings

By default, uses `en-gb.json` file inside the `strings` top-level folder.

If language changes, set `libs.strings.default_locale` and
run `libs.strings.refresh()`.
"""
import json
import os.path

default_locale = "en-gb"
cached_strings = {}


def refresh():
    print("Refreshing...")
    global cached_strings
    if os.path.exists(f"project_name/strings/{default_locale}.json"):
        with open(f"project_name/strings/{default_locale}.json") as f:
            cached_strings = json.load(f)
    else:
        with open(f"strings/{default_locale}.json") as f:
            cached_strings = json.load(f)


def gettext(name):
    return cached_strings[name]


refresh()
