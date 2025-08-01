from flask import Flask, jsonify
import feedparser
from flask_cors import CORS
from dateutil import parser as date_parser
import pytz

app = Flask(__name__)
CORS(app)

# ✅ Full list of global + Indian sports news RSS feeds
feed_urls = [
    # 🌍 Global General Sports
    "https://www.espn.com/espn/rss/news",
    "https://sports.yahoo.com/rss/",
    "https://feeds.bbci.co.uk/sport/rss.xml",
    "https://www.cbssports.com/rss/headlines/",
    "https://scores.nbcsports.com/rss/headlines.asp",
    "https://www.skysports.com/rss/12040",
    "https://www.si.com/rss/si_topstories.rss",
    "https://bleacherreport.com/articles/feed",
    "https://www.sportingnews.com/us/rss",

    # ⚽ Football / Soccer
    "https://www.goal.com/feeds/en/news",
    "https://www.fifa.com/rss/index.xml",
    "https://www.uefa.com/rssfeed/championsleague/rss.xml",
    "https://www.premierleague.com/news/rss",

    # 🏀 Basketball
    "https://www.espn.com/espn/rss/nba/news",
    "https://www.cbssports.com/rss/headlines/nba",

    # 🏏 Cricket
    "https://www.espncricinfo.com/rss/content/story/feeds/0.xml",
    "https://feeds.bbci.co.uk/sport/cricket/rss.xml",
    "https://www.cricbuzz.com/rss/news",

    # 🏎️ F1 / Motorsports
    "https://www.formula1.com/rss.xml",
    "https://feeds.bbci.co.uk/sport/formula1/rss.xml",

    # 🎾 Tennis
    "https://www.atptour.com/en/media/rss-feed",
    "https://www.wtatennis.com/rss",

    # 🏌️ Golf
    "https://www.pgatour.com/bin/data/feeds/rss.xml",
    "https://www.golfchannel.com/rss",

    # 🥊 MMA / UFC / Boxing
    "https://www.ufc.com/rss/news",
    "https://www.mmafighting.com/rss/current",

    # 🇮🇳 Indian Sports Sources
    "https://timesofindia.indiatimes.com/rssfeeds/4719148.cms",
    "https://indianexpress.com/section/sports/feed/",
    "https://www.hindustantimes.com/sports/rss",
    "https://www.thehindu.com/sport/feeder/default.rss",
    "https://www.news18.com/rss/sports.xml",
    "https://www.sportskeeda.com/feed",
    "https://thebridge.in/rss/sports/"
]

def is_indian_source(link):
    indian_domains = ["indiatimes", "indianexpress", "hindustantimes", "thehindu", "news18", "sportskeeda", "thebridge"]
    return any(domain in link for domain in indian_domains)

def convert_to_ist(published_time):
    try:
        dt = date_parser.parse(published_time)
        dt_utc = dt.astimezone(pytz.utc)
        dt_ist = dt_utc.astimezone(pytz.timezone("Asia/Kolkata"))
        return dt_ist.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return ""

@app.route('/')
def index():
    return jsonify({"message": "Sports API is running", "endpoint": "/news"})

@app.route('/news')
def get_news():
    all_entries = []

    for url in feed_urls:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            item = {
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "published": convert_to_ist(entry.get("published", "")),
                "source": url,
                "isIndian": is_indian_source(entry.get("link", ""))
            }
            all_entries.append(item)

    # ✅ Remove duplicates by title
    seen_titles = set()
    unique_entries = []
    for item in all_entries:
        if item["title"] not in seen_titles:
            unique_entries.append(item)
            seen_titles.add(item["title"])

    return jsonify(unique_entries)

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
