import os
from motor.motor_asyncio import AsyncIOMotorClient

class Color:
    primary = 0x3EE2B7
    transparent = 0x2F3136
    blurple_old = 0x7289DA
    blurple = 0x5865F2
    danger = 0xE92323
    warning = 0xE9B623
    success = 0x44E923

class Auth:
    discord_auth = {
        "debug":"OTMyMjgxMTAyNDg2MzcyNDQz.Gtp0M1.Ttfzsx268d0DI_w70hgc9i-I8aS10-iTg85Al8",
        "release": "OTMyMjgxMTAyNDg2MzcyNDQz.Gtp0M1.Ttfzsx268d0DI_w70hgc9i-I8aS10-iTg85Al8"
    }
    qiwi_auth = ""
    
class Other:
    shard_count = 1
    slash = None
    premium_cost = 99
    invoice_lifetime = 360 # в минутах
    p2p = None
    uptime = 0
class Config:
    MONGO_CLIENT = AsyncIOMotorClient('mongodb+srv://Sparkle:gTgZoK7MVq0PnF9P@cluster0.c3g21uf.mongodb.net/?retryWrites=true&w=majority') 
    DB = MONGO_CLIENT.Sparkle
    DEFAULT_GUILD_DATA = {'color': 0xa8a6f0}
    OLD_MONGO_CLIENT = AsyncIOMotorClient('mongodb+srv://Sparkle:gTgZoK7MVq0PnF9P@cluster0.c3g21uf.mongodb.net/?retryWrites=true&w=majority')
    OLD_DB = OLD_MONGO_CLIENT.Sparkle