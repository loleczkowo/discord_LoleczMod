import random
import string
import json
import os


def convert_time(hours: float) -> str:
    '''Converts hours to days, hours, and minutes into a string format'''
    total_minutes = int(hours * 60)
    days = total_minutes // 1440
    remaining_minutes = total_minutes % 1440
    hrs = remaining_minutes // 60
    minutes = remaining_minutes % 60

    result = []
    if days > 0:
        result.append(f"{days} day{'s' if days > 1 else ''}")
    if hrs > 0:
        result.append(f"{hrs} hour{'s' if hrs > 1 else ''}")
    if minutes > 0 or not result:  # Include minutes if no other values exist
        result.append(f"{minutes} minute{'s' if minutes > 1 else ''}")

    if len(result) == 1:
        return result[0]
    elif len(result) == 2:
        return f"{result[0]} and {result[1]}"
    else:
        return f"{', '.join(result[:-1])} and {result[-1]}"


def gen_code(len=5):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choices(characters, k=len))


def load_json(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {}


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
