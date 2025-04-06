from flask import Blueprint, jsonify, request, current_app
from flask_mysqldb import MySQL
from models.product import get_all_products
from products.utils import allowed_file
from werkzeug.utils import secure_filename
import os
product_bp = Blueprint('products', __name__)
mysql = MySQL()


@product_bp.route('/api/products', methods=['GET'])
def get_products():
    products = get_all_products(mysql)
    if not products:
        return jsonify({'message': 'No products found'}), 404
    product_list = [
        {
            'id': product[0],
            'name': product[1],
            'price': product[2],
            'description': product[3],
            'image': product[4],
            'quantity': product[5]
        } for product in products
    ]

    return jsonify(product_list), 200

@product_bp.route('/api/products', methods=['POST'])
def add_product():
    name = request.form.get('name')
    price = request.form.get('price')
    description = request.form.get('description')
    quantity = request.form.get('quantity')
    image = request.files.get('image')

    if not all([name, price, description, quantity, image]):
        return jsonify({'error': 'جميع الحقول ضرورية'}), 400

    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)
        relative_path = f"/uploads/{filename}"

        try:
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO products (name, price, description, image, quantity) VALUES (%s, %s, %s, %s, %s)",
                (name, price, description, image, quantity)
            )
            mysql.connection.commit()
            cur.close()
            return jsonify({'message': 'تم رفع المنتوج بالصورة 🖼️'}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'صيغة الصورة غير مدعومة'}), 400
