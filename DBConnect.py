import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="PyReddit",
    user="postgres",
    password="Slirb007")

cur = conn.cursor()

cur.execute('SELECT version()')

# display the PostgreSQL database server version
db_version = cur.fetchone()

print(db_version)

#Close the db conenction
cur.close()