import database
import interface
from datetime import datetime

connection, cursor = database.open_connection()
# database.init_database(connection, cursor)
# database.insert_data(connection, cursor)
interface.start()
database.close_connection(connection, cursor)
