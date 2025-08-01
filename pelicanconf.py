import subprocess


def commit_hash():
    try:
        return (
            subprocess.check_output(["git", "rev-parse", "--short", "HEAD"])
            .decode()
            .strip()
        )
    except Exception:
        return None


AUTHOR = "Chris Tapper"
SITENAME = "Chris Tapper"
SITEURL = ""

PATH = "content"

TIMEZONE = "Australia/Sydney"

DEFAULT_LANG = "en"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
    ("Pelican", "https://getpelican.com/"),
    ("Python.org", "https://www.python.org/"),
    ("Jinja2", "https://palletsprojects.com/p/jinja/"),
    ("You can modify those links in your config file", "#"),
)

# Social widget
SOCIAL = (
    ("You can add links in your config file", "#"),
    ("Another social link", "#"),
)

DEFAULT_PAGINATION = 10

THEME = "theme"

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

# Prevent generation of unwanted pages
ARCHIVES_SAVE_AS = ""
ARTICLES_SAVE_AS = ""
AUTHORS_SAVE_AS = ""
CATEGORIES_SAVE_AS = ""
TAGS_SAVE_AS = ""

JINJA_GLOBALS = {
    "DEV": True,
    "VERSION": commit_hash(),
}
