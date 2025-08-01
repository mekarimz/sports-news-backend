from flask import Flask, jsonify
import feedparser
from flask_cors import CORS
from dateutil import parser as date_parser
import pytz
from datetime import datetime

app = Flask(__name__)
CORS(app)

# IST timezone
IST = pytz.timezone('Asia/Kolkata')

rss_feeds = [
    # 🏏 Cricket (India)
    {"url": "https://www.espncricinfo.com/rss/content/story/feeds/0.xml", "sport": "Cricket", "name": "ESPN Cricinfo", "country": "India"},
    {"url": "https://www.cricbuzz.com/rss/news", "sport": "Cricket", "name": "Cricbuzz", "country": "India"},
    {"url": "https://feeds.bbci.co.uk/sport/cricket/rss.xml", "sport": "Cricket", "name": "BBC Cricket", "country": "World"},

    # 🏈 General Sports
    {"url": "https://www.espn.com/espn/rss/news", "sport": "General", "name": "ESPN", "country": "World"},
    {"url": "https://sports.yahoo.com/rss/", "sport": "General", "name": "Yahoo Sports", "country": "World"},
    {"url": "https://www.cbssports.com/rss/headlines/", "sport": "General", "name": "CBS Sports", "country": "World"},
    {"url": "https://scores.nbcsports.com/rss/headlines.asp", "sport": "General", "name": "NBC Sports", "country": "World"},
    {"url": "https://feeds.bbci.co.uk/sport/rss.xml", "sport": "General", "name": "BBC Sport", "country": "World"},
    {"url": "https://www.skysports.com/rss/12040", "sport": "General", "name": "Sky Sports", "country": "World"},
    {"url": "https://www.sportingnews.com/us/rss", "sport": "General", "name": "Sporting News", "country": "World"},
    {"url": "https://www.si.com/rss/si_topstories.rss", "sport": "General", "name": "Sports Illustrated", "country": "World"},
    {"url": "https://bleacherreport.com/articles/feed", "sport": "General", "name": "Bleacher Report", "country": "World"},

    # ⚽ Football / Soccer
    {"url": "https://www.goal.com/feeds/en/news", "sport": "Football", "name": "Goal.com", "country": "World"},
    {"url": "https://www.fifa.com/rss/index.xml", "sport": "Football", "name": "FIFA", "country": "World"},
    {"url": "https://www.uefa.com/rssfeed/championsleague/rss.xml", "sport": "Football", "name": "UEFA Champions League", "country": "World"},
    {"url": "https://www.premierleague.com/news/rss", "sport": "Football", "name": "Premier League", "country": "World"},

    # 🏀 Basketball
    {"url": "https://www.espn.com/espn/rss/nba/news", "sport": "Basketball", "name": "NBA (ESPN)", "country": "World"},
    {"url": "https://www.cbssports.com/rss/headlines/nba", "sport": "Basketball", "name": "CBS NBA", "country": "World"},

    # 🏎️ F1 / Motorsports
    {"url": "https://www.formula1.com/rss.xml", "sport": "Motorsports", "name": "Formula 1", "country": "World"},
    {"url": "https://feeds.bbci.co.uk/sport/formula1/rss.xml", "sport": "Motorsports", "name": "BBC F1", "country": "World"},

    # 🎾 Tennis
    {"url": "https://www.atptour.com/en/media/rss-feed", "sport": "Tennis", "name": "ATP Tour", "country": "World"},
    {"url": "https://www.wtatennis.com/rss", "sport": "Tennis", "name": "WTA Tennis", "country": "World"},

    # 🏌️ Golf
    {"url": "https://www.pgatour.com/bin/data/feeds/rss.xml", "sport": "Golf", "name": "PGA Tour", "country": "World"},
    {"url": "https://www.golfchannel.com/rss", "sport": "Golf", "name": "Golf Channel", "country": "World"},

    # 🥊 MMA / Boxing
    {"url": "https://www.ufc.com/rss/news", "sport": "MMA", "name": "UFC", "country": "World"},
    {"url": "https://www.mmafighting.com/rss/current", "sport": "MMA", "name": "MMA Fighting", "country": "World"},

    # 🧠 Bridge (Mind Sport)
    {"url": "https://bridgewinners.com/rss/bw_rss/", "sport": "Bridge", "name": "Bridge Winners", "country": "World"},

    # 🇮🇳 India-specific general
    {"url": "https://sports.ndtv.com/rss/all", "sport": "General", "name": "NDTV Sports", "country": "India"},
    {"url": "https://timesofindia.indiatimes.com/rssfeeds/4719148.cms", "sport": "General", "name": "TOI Sports", "country": "India"},
]

@app.route('/news')
def get_news():
    all_news = []

    for feed in rss_feeds:
        d = feedparser.parse(feed["url"])
        for entry in d.entries[:10]:  # Limit per feed
            published = entry.get("published", None)
            if published:
                try:
                    published_dt = date_parser.parse(published)
                    ist_time = published_dt.astimezone(IST)
                except Exception:
                    ist_time = datetime.now(IST)
            else:
                ist_time = datetime.now(IST)

            all_news.append({
                "title": entry.title,
                "link": entry.link,
                "published": ist_time.strftime('%Y-%m-%d %H:%M:%S'),
                "source": feed["name"],
                "sport": feed["sport"],
                "country": feed.get("country", "World")
            })

    # Optional: Sort by latest
    all_news.sort(key=lambda x: x['published'], reverse=True)
    return jsonify(all_news)

if __name__ == '__main__':
    app.run(debug=True)
