import json
import os
import sqlite3

setu_config = {
    'SUPERUSERS': [""],
    'PROXIES_HTTP': '',
    'PROXIES_SOCKS': '',
    'PROXIES_SWITCH': 1,
    'ONLINE_SWITCH': 0,
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
        self.online_switch = self.config['ONLINE_SWITCH']

    @staticmethod
    def create_file():
        if not os.path.exists('data/lolicon.db'):
            conn = sqlite3.connect('data/lolicon.db')
            conn.close()
        if not os.path.exists('loliconImages/r18'):
            os.mkdir('loliconImages/r18')
        if not os.path.exists('data'):
            os.mkdir('data')
