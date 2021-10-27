from datetime import datetime
import json
import nonebot

setu_cd = nonebot.get_driver().config.setu_cd


def readJson():
    with open(r'data/userscd.json', 'r') as f_in:
        data = json.load(f_in)
        f_in.close()
        return data


def writeJson(qid: str, time: int, data: dict):
    data[qid] = time
    with open(r'data/userscd.json', 'w') as f_out:
        json.dump(data, f_out)
        f_out.close()


def deleteJson(qid: str, data: dict):
    del data[qid]
    with open(r'data/userscd.json', 'w') as f_out:
        json.dump(data, f_out)
        f_out.close()


def check(user_id) -> 'bool,int':
    data = readJson()
    if user_id in data:
        last_time = datetime.strptime(data[user_id], "%Y-%m-%d %H:%M:%S")
        this_time = datetime.now()
        timespan = (this_time - last_time).total_seconds()
        if timespan > setu_cd:
            writeJson(user_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), data)
            return True, 0
        else:
            return False, setu_cd - timespan
    else:
        writeJson(user_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), data)
        return True, 0
