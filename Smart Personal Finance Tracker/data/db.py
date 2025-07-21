import sqlite3
from datetime import datetime


class FinanceDB:
    def __init__(self, db_file="finance.db"):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                type TEXT,
                category TEXT,
                amount REAL,
                description TEXT)''')
        self.conn.commit()

    def add_transaction(self, t_type, category, amount, description):
        if t_type == "Expense":
            amount = -abs(amount)
        else:
            amount = abs(amount)
        self.cursor.execute('''
            INSERT INTO transactions (date, type, category, amount, description)
            VALUES (?, ?, ?, ?, ?)
        ''', (datetime.now().strftime("%Y-%m-%d %H:%M"), t_type, category, amount, description))
        self.conn.commit()

    def get_balance(self):
        self.cursor.execute('SELECT SUM(amount) FROM transactions')
        result = self.cursor.fetchone()[0]
        return result if result else 0.0

    def get_all_transactions(self):
        self.cursor.execute('SELECT date, type, category, amount, description FROM transactions')
        return self.cursor.fetchall()