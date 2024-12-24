from firebird.driver import connect, driver_config, DESCRIPTION_NAME, DESCRIPTION_DISPLAY_SIZE

# Connecting to IT Okna DB
driver_config.read('config_data/fb_db.cfg')


def create_connection(db):
    connection = None
    try:
        connection = connect(db)
        connection.isolation_level = 'READ COMMITTED'
    except Exception as e:
        print(f'Database connection error {e}')
    return connection


con = create_connection('employee')
