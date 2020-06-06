from datetime import datetime, timedelta
from repository.contents import sync


def create_clock_sync_contents(from_date_minutes, to_date_minutes):
    def clock_sync_contents():
        now_date = datetime.utcnow()
        sync(
            now_date - timedelta(minutes=from_date_minutes),
            now_date - timedelta(minutes=to_date_minutes)
        )
    return clock_sync_contents


# everything in minutes
CLOCK_SYNC_CONTENT_CONFIGS = [
    # contents inserted since 1.7h - 0, do it every 10 minutes
    {
        'from_date': 100,
        'to_date': 0,
        'frequency': {'minute': '*/10'}
    },
    # contents inserted since 17h - 1.7h, do it every hours
    {
        'from_date': 1000,
        'to_date': 100,
        'frequency': {'hour': '*/1', 'minute': '1'}
    },
    # contents inserted since 7days - 17h, do it every days
    {
        'from_date': 10000,
        'to_date': 1000,
        'frequency': {'day': '*/1', 'hour': '0', 'minute': '1'}
    },
    # contents inserted since 70days - 7days, do it every 2 monthes
    {
        'from_date': 100000,
        'to_date': 10000,
        'frequency': {'month': '*/2', 'day': '1', 'hour': '0', 'minute': '1'}
    },
    # contents inserted since start - 70days, do it every 2 years
    {
        'from_date': None,
        'to_date': 100000,
        'frequency': {'year': '*/2', 'month': '1', 'day': '1', 'hour': '0', 'minute': '1'}
    },
]

JOBS = []

for clock_sync_content_config in CLOCK_SYNC_CONTENT_CONFIGS:
    from_date = clock_sync_content_config['from_date']
    to_date = clock_sync_content_config['to_date']
    JOBS.append({
        'function': create_clock_sync_contents(from_date, to_date),
        'kwargs': {
            'id': 'contents {} {}'.format(from_date, to_date),
            **clock_sync_content_config['frequency']
        }
    })
