from datetime import datetime
from .create_file import Config
import json

setu_cd = Config().setu_cd


def read_json(location: str):
    with open(location, 'r') as f_in:
        data = json.load(f_in)
        return data


def write_json(qid: str, time: int, data: dict):
    data[qid] = time
    with open(r'data/userscd.json', 'w') as f_out:
        json.dump(data, f_out)


def delete_json(qid: str, data: dict):
    del data[qid]
    with open(r'data/userscd.json', 'w') as f_out:
        json.dump(data, f_out)


def check(user_id) -> 'bool,int':
    data = read_json(r'data/userscd.json')
    if user_id in data:
        last_time = datetime.strptime(data[user_id], "%Y-%m-%d %H:%M:%S")
        this_time = datetime.now()
        timespan = (this_time - last_time).total_seconds()
        if timespan > setu_cd:
            write_json(user_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), data)
            return True, 0
        else:
            return False, setu_cd - timespan
    else:
        write_json(user_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), data)
        return True, 0
