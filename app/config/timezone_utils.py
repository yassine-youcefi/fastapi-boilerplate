from datetime import datetime
import pytz
from app.config.config import settings

def get_dubai_now():
    """Return the current datetime in Dubai timezone (UTC+4)."""
    tz = pytz.timezone('Asia/Dubai')
    return datetime.now(tz)
