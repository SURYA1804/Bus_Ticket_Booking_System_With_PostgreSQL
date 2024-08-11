from Display import Display
from Connection import Connection

cur,con = Connection.connection()

Display.display_login_page(cur,con)