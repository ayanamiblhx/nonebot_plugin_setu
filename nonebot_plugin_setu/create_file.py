import os
import json

setu_config = {
    'SUPERUSERS': [""],
    'PROXIES_HTTP': '',
    'PROXIES_SOCKS': '',
    'SETU_CD': 0,
    'SETU_NUM': '80'
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
        self.setu_cd = self.config['SETU_CD']
        self.setu_num = self.config['SETU_NUM']

    @staticmethod
    def create():
        if not os.path.exists('loliconImages'):
            os.mkdir('loliconImages')
        if not os.path.exists('data'):
            os.mkdir('data')
        if not os.path.exists('data/userscd.json'):
            with open('data/userscd.json', 'w') as file:
                file.write('{}')
