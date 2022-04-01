import sqlite3


class GroupDao:
    def __init__(self):
        self.db_path = 'data/lolicon.db'
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            'create table if not exists group_cd(group_id text primary key, cd integer)')
        self.cursor.execute(
            'create table if not exists group_interval(group_id text primary key, group_interval integer default 0)')
        self.cursor.execute(
            'create table if not exists group_r18(group_id text primary key, r18 integer default 0)')
        self.conn.commit()
        self.conn.close()

    def get_group_cd(self, group_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            'SELECT cd FROM group_cd WHERE group_id = ?',
            (group_id,)
        )
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None

    def set_group_cd(self, group_id, cd):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT OR IGNORE INTO group_cd (group_id, cd) VALUES (?, ?)',
            (group_id, cd)
        )
        conn.commit()
        conn.close()

    def update_group_cd(self, group_id, cd):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE group_cd SET cd = ? WHERE group_id = ?',
            (cd, group_id)
        )
        conn.commit()
        conn.close()

    def get_group_interval(self, group_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            'SELECT group_interval FROM group_interval WHERE group_id = ?',
            (group_id,)
        )
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None

    def set_or_update_group_interval(self, group_id, interval):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT OR IGNORE INTO group_interval (group_id, group_interval) VALUES (?, ?)',
            (group_id, interval)
        )
        cursor.execute(
            'UPDATE group_interval SET group_interval = ? WHERE group_id = ?',
            (interval, group_id)
        )
        conn.commit()
        conn.close()

    def get_group_r18(self, group_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            'SELECT r18 FROM group_r18 WHERE group_id = ?',
            (group_id,)
        )
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else 0

    def set_or_update_group_r18(self, group_id, r18: int = 0):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT OR IGNORE INTO group_r18 (group_id, r18) VALUES (?, ?)',
            (group_id, r18)
        )
        cursor.execute(
            'UPDATE group_r18 SET r18 = ? WHERE group_id = ?',
            (r18, group_id)
        )
        conn.commit()
        conn.close()
