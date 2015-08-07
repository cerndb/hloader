from datetime import date, datetime, timedelta


def json_datetime_handler_default(obj):
    """
    Make date and datetime objects JSON serializable.

    See:
    http://stackoverflow.com/questions/12122007/python-json-encoder-to-support-datetime

    :param obj: by default not serializable object
    :return: serialized object
    """

    if isinstance(obj, date) or isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, timedelta):
        return str(obj)
    else:
        raise TypeError(repr(obj) + " is not JSON serializable")