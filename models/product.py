from flask_mysqldb import MySQL

def create_product(name, price, description, image, quantity, mysql):
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO products (name, price, description, image, quantity) "
        "VALUES (%s, %s, %s, %s, %s)",
        (name, price, description, image, quantity)
    )
    mysql.connection.commit()
    cur.close()
def get_all_products(mysql):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    cur.close()
    return products

