from flask_mysqldb import MySQL

def create_user(mysql, username, email, hashed_password):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                (username, email, hashed_password))
    mysql.connection.commit()
    cur.close()

def get_user_by_email(mysql, email):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, username, password FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()
    return user
