import os
import json
import sqlite3

setu_config = {
    'SUPERUSERS': [""],
    'PROXIES_HTTP': '',
    'PROXIES_SOCKS': '',
    'PROXIES_SWITCH': 1,
    'DOWNLOAD_SWITCH': 1,
}


class Config:
    def __init__(self):
        if not os.path.exists('data/setu_config.json'):
            with open('data/setu_config.json', 'w') as file:
                json.dump(setu_config, file)
        with open('data/setu_config.json', 'r') as file:
            self.config = json.load(file)
        self.super_users = self.config['SUPERUSERS']
        self.proxies_http = self.config['PROXIES_HTTP']
        self.proxies_socks = self.config['PROXIES_SOCKS']
        self.proxies_switch = self.config['PROXIES_SWITCH']
        self.download_switch = self.config['DOWNLOAD_SWITCH']

    @staticmethod
    def create_file():
        if not os.path.exists('data/lolicon.db'):
            conn = sqlite3.connect('data/lolicon.db')
            conn.close()
        if not os.path.exists('loliconImages'):
            os.mkdir('loliconImages')
        if not os.path.exists('data'):
            os.mkdir('data')

    @staticmethod
    def create_table():
        conn = sqlite3.connect('data/lolicon.db')
        cursor = conn.cursor()
        table_sql = 'create table if not exists lolicon_images(pid text primary key, uid text, title text,' \
                    ' author text, r18 text ,width integer,height integer,ext text,urls text,upload_date text)'
        tags_sql = 'create table if not exists lolicon_tags(id integer primary key AUTOINCREMENT, pid text, tags text,unique (pid,tags))'
        user_cd_sql = 'create table if not exists user_cd(user_id text primary key, last_time integer ,cd integer)'
        group_cd_sql = 'create table if not exists group_cd(group_id text primary key, cd integer)'
        cursor.execute(table_sql)
        cursor.execute(tags_sql)
        cursor.execute(user_cd_sql)
        cursor.execute(group_cd_sql)
        conn.commit()
        conn.close()