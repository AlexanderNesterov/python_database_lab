import database
import interface
from datetime import datetime

connection, cursor = database.open_connection()
interface.start()
database.close_connection(connection, cursor)
