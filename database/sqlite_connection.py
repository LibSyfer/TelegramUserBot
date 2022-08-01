import sqlite3

try:
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    print("База данных успешно создана и подключена")
    cursor.execute("CREATE TABLE IF NOT EXISTS listened_channels(name TEXT NOT NULL, channel_id INTEGER PRIMARY KEY)")
    cursor.execute("CREATE TABLE IF NOT EXISTS storage_channel_ids(name TEXT NOT NULL, channel_id INTEGER PRIMARY KEY)")
    cursor.execute("CREATE TABLE IF NOT EXISTS admins(name TEXT NOT NULL, user_id INTEGER PRIMARY KEY)")
except:
    print("Error")

def get_listened_channels():
    cursor.execute("SELECT * FROM listened_channels;")
    result = cursor.fetchall()
    return result

def add_listened_channel(name, channel_id):
    cursor.execute("INSERT INTO listened_channels VALUES(?, ?);", (name, channel_id))
    sqlite_connection.commit()
    return True

def remove_listened_channel(name, channel_id):
    cursor.execute("DELETE FROM listened_channels WHERE name='{}';".format(name))

# add_listened_channel("канал1", 1)
# add_listened_channel("канал2", 2)
# add_listened_channel("канал3", 3)
#
# print(get_listened_channels())
