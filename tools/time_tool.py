from datetime import datetime


def time_tool(query=""):

    now = datetime.now()
    q = query.lower()

    # custom formats
    if "dd-mm-yy" in q:
        return now.strftime("%d-%m-%y")

    if "dd-mm-yyyy" in q:
        return now.strftime("%d-%m-%Y")

    if "time" in q:
        return now.strftime("%H:%M:%S")

    # default
    return now.strftime("%A, %d %B %Y — %H:%M:%S")
