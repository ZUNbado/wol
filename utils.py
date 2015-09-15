from wakeonlan import wol
import ping, os
from tinydb import TinyDB

def get_status(ip, timeout = 1):
    return 1 if ping.do_one(ip, timeout, 64) else 0

def wakehost(mac):
    wol.send_magic_packet(mac)

def getdb():
    db = os.environ.get('DB_FILE', '/tmp/db.json')
    return TinyDB(db)
