import sqlite3

def create_table():
    conn = sqlite3.connect('datacurve.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE submitted_code (
            id INTEGER PRIMARY KEY,
            code TEXT,
            output TEXT
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()


def query_table():
    conn = sqlite3.connect('datacurve.db')
    cursor = conn.cursor()
    result = cursor.execute('''
        SELECT * from submitted_code
    ''')
    for row in result.fetchall():
        print(row)
    cursor.close()
    conn.close()


def add_code_submission(code, output):
    conn = sqlite3.connect('datacurve.db')
    cursor = conn.cursor()
    cursor.execute(f'''
        INSERT INTO submitted_code (code, output) VALUES ('{code.code}', '{output}')
    ''')
    conn.commit()
    cursor.close()
    conn.close()


if __name__ == "__main__":
    #create_table()
    query_table()