import sqlite3


class GroupCdDao:
    def __init__(self):
        self.db_path = 'data/lolicon.db'

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
