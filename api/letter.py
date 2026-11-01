# Vercel Python serverless function
# GET /api/letter?to=Nama&msg=Pesan&theme=red
# Pisahkan halaman dengan baris kosong atau tanda "|" di dalam msg.
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json

THEMES = {"red": 0, "orange": 25, "pink": 330, "purple": 270, "blue": 210, "green": 140}

DEFAULT_TITLE = "The Sworn Blade"

DEFAULT_MSG = """Hear me, Your Majesty, for I fear I shall not have the courage to speak twice.

Long before I knew thy name, I swore an oath upon this blade. “I shall stand between the realm and the dark, and I shall not falter.” A simple vow, made by a simple man. None told me that one day the very thing I swore to protect would wear a crown, and look upon me with eyes that make a soldier forget his sword.

Thou didst ask why I never lift my gaze in thy presence. Hear the truth, then. ’Tis not reverence alone. Were I to look upon thee overlong, I should forget that I am but a servant of the crown, and thou art the crown itself. And a kingdom hath no room for a queen who loves a soldier.

The war-horns sound in the north. The border burns. The council hath spoken, and their command is iron: go, and sever what binds thee here. And God forgive me, I shall obey. Not from fear, for I have stared down death a hundred times and never trembled so as I do now. I obey because a knight who breaks his oath for love is a knight unworthy of the love he sought.

So I ask nothing of thee. Do not wait for me. Let no candle burn at thy window. Rule, and rule wisely. Laugh, and let the halls ring with it. Live, my Queen, as though I had never come.

But know this. Beneath my armour, where no blade may reach, I shall carry thy name like a banked ember. Through cold marches and bitter nights, through every wound and every wearied league, I shall whisper it to the dark, and the dark shall not have me.

And if the gods are merciful, if I survive the steel and the winter and the long, long years, I shall come back through this gate. No helm. No banner. No orders. Only a man, and the oath he could not keep, and the one he could never break.

If the door be open still, I am home.

If it be shut, I shall kneel upon this very stone, and thank heaven that I was ever loved by thee at all."""


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        q = parse_qs(urlparse(self.path).query)
        title = q.get("to", [DEFAULT_TITLE])[0].strip()[:40] or DEFAULT_TITLE
        message = q.get("msg", [DEFAULT_MSG])[0].strip()[:4000] or DEFAULT_MSG
        theme = q.get("theme", ["red"])[0]
        if theme not in THEMES:
            theme = "red"

        body = json.dumps(
            {"title": title, "message": message, "hue": THEMES[theme]},
            ensure_ascii=False,
        ).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "s-maxage=60")
        self.end_headers()
        self.wfile.write(body)
