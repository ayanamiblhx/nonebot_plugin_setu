import json
import os
import sqlite3
import pathlib

setu_config = {
    'SUPERUSERS': [""],
    'PROXIES_HTTP': '',
    'PROXIES_SOCKS': '',
    'PROXIES_SWITCH': 1,
    'ONLINE_SWITCH': 0,
}


class Config:
    def __init__(self):
        self.create_file()
        with open('data/setu_config.json', 'r') as file:
            self.config = json.load(file)
        self.super_users = self.config['SUPERUSERS']
        self.proxies_http = self.config['PROXIES_HTTP']
        self.proxies_socks = self.config['PROXIES_SOCKS']
        self.proxies_switch = self.config['PROXIES_SWITCH']
        self.online_switch = self.config['ONLINE_SWITCH']

    @staticmethod
    def create_file():
        pathlib.Path('data').mkdir(parents=True, exist_ok=True)
        pathlib.Path('loliconImages/r18').mkdir(parents=True, exist_ok=True)
        if not os.path.exists('data/setu_config.json'):
            with open('data/setu_config.json', 'w', encoding='utf-8') as f:
                json.dump(setu_config, f, ensure_ascii=False, indent=4)
        if not os.path.exists('data/lolicon.db'):
            conn = sqlite3.connect('data/lolicon.db')
            conn.close()

    def get_file_args(self, args_name: str):
        with open('data/setu_config.json', 'r', encoding='utf-8') as file:
            content = json.load(file)
            if not args_name in content:
                content.update({args_name: ' '})
                with open('data/setu_config.json', 'w', encoding='utf-8') as file_new:
                    json.dump(content, file_new, indent=4)
            return content[args_name]
