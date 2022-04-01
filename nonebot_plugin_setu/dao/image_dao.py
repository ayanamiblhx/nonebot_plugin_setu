import json
import sqlite3
from typing import List


class ImageDao:
    def __init__(self):
        self.db_path = 'data/lolicon.db'
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            'create table if not exists lolicon_images(pid text primary key, uid text, title text,'
            ' author text, r18 text ,width integer,height integer,ext text,urls text,upload_date text)')
        self.cursor.execute(
            'create table if not exists lolicon_tags('
            'id integer primary key AUTOINCREMENT, pid text, tags text,unique (pid,tags))')
        self.cursor.execute(
            'create table if not exists lolicon_api(id integer primary key AUTOINCREMENT, address text)')
        self.conn.commit()
        self.conn.close()

    def add_images(self, datas):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        for data in datas:
            pid = data['pid']
            uid = data['uid']
            title = data['title']
            author = data['author']
            r18 = data['r18']
            width = data['width']
            height = data['height']
            ext = data['ext']
            urls = json.dumps(data['urls'])
            upload_date = data['uploadDate']
            sql = "INSERT OR IGNORE INTO lolicon_images(pid, uid, title, author, r18, width, height, ext, urls, upload_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            cursor.execute(sql, (pid, uid, title, author, r18, width, height, ext, urls, upload_date))
            tags = data['tags']
            for tag in tags:
                sql = "INSERT OR IGNORE INTO lolicon_tags(pid, tags) VALUES (?, ?)"
                cursor.execute(sql, (pid, tag))
        conn.commit()
        conn.close()

    def get_images_by_pid(self, pid):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        sql = f"select * from lolicon_images where pid='{pid}'"
        data = self.processing_data(conn, cursor, sql)
        return data

    def get_images_by_tags(self, tags: List[str], r18: bool = False, num: int = 1, **kwargs):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        sql = "select * from lolicon_images where pid in (select pid from lolicon_tags"
        sql += f" where tags like '%{tags[0]}%'"
        for tag in tags[1:]:
            sql += f" or tags like '%{tag}%'"
        sql += f") group by pid having r18={r18} order by random() limit {num}"
        img_data = self.processing_data(conn, cursor, sql)
        return img_data

    @staticmethod
    def processing_data(conn, cursor, sql):
        cursor.execute(sql)
        img_infos = cursor.fetchall()
        img_description = cursor.description
        img_datas = {"data": []}
        for img_info in img_infos:
            data = {}
            for idx, col in enumerate(img_description):
                if col[0] == 'urls':
                    data[col[0]] = json.loads(img_info[idx])
                elif col[0] == 'r18':
                    data[col[0]] = img_info[idx] == '1'
                else:
                    data[col[0]] = img_info[idx]
            tags = []
            sql = f"select tags from lolicon_tags where pid='{data['pid']}'"
            tag_infos = cursor.execute(sql).fetchall()
            for tag_info in tag_infos:
                tags.append(tag_info[0])
            data['tags'] = tags
            img_datas['data'].append(data)
        conn.close()
        return img_datas

    def get_top_tags(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        sql = "select tags,count(*) as count from lolicon_tags group by tags order by count desc limit 10"
        cursor.execute(sql)
        top_tags = cursor.fetchall()
        data = []
        for tag in top_tags:
            data.append({'tags': tag[0], 'count': tag[1]})
        conn.close()
        return data

    def get_random_images(self, num: int, r18: bool = False):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        sql = f"select * from lolicon_images where r18={r18} order by random() limit {num}"
        data = self.processing_data(conn, cursor, sql)
        return data

    def get_images_by_uid(self, uid, num: int = 1, r18: bool = False, **kwargs):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        sql = f"select * from lolicon_images where uid='{uid}' and r18={r18} order by random() limit {num}"
        data = self.processing_data(conn, cursor, sql)
        return data

    def get_api(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        sql = "select address from lolicon_api where id=1"
        cursor.execute(sql)
        data = cursor.fetchone()
        conn.close()
        return data[0] if data else None

    def set_or_update_api(self, api_address: str):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        sql_insert = "INSERT OR IGNORE INTO lolicon_api VALUES (?, ?)"
        cursor.execute(sql_insert, (1, api_address))
        sql_update = "UPDATE lolicon_api SET address=? WHERE id=1"
        cursor.execute(sql_update, (api_address,))
        conn.commit()
        conn.close()
