from datetime import datetime, timedelta


def get_date_range(today=None):
    if today:
        yesterday = (datetime.strptime(today, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
        return [(yesterday, today)]
    else:
        today = datetime.now().strftime("%Y-%m-%d")
        week_ago = (datetime.strptime(today, "%Y-%m-%d") - timedelta(days=7)).strftime("%Y-%m-%d")
        return [(week_ago, today)]
