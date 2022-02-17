from datetime import datetime

def date_format_utc(str_dt):
    # Received html date format %Y-%m-%dT%H:%M (2022-02-11T09:14)
    # SQL format YYYY-MM-DD hh:mm:ssTZD (2022-02-11 09:14:00+00:00)

    if str_dt is None:
        return ""

    fmt_datetime = datetime.strptime(str_dt, '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d %H:%M:%S')
    fmt_timezone = "+00:00"

    return fmt_datetime + fmt_timezone
