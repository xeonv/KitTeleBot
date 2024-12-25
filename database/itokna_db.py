from fdb import connect

fb_db_cfg = {'dsn': 'localhost:C:\\ITDB.GDB',
             'user': 'sysdba',
             'password': 'masterkey',
             'charset': 'UTF8'}


def create_connection(db_cfg: dict):
    connection = None
    try:
        connection = connect(**db_cfg)
        connection.isolation_level = 'READ COMMITTED'
    except Exception as e:
        print(f'Database connection error {e}')
    return connection


con = create_connection(fb_db_cfg)
