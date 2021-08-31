from flask import Flask
from flask import json
from flask.globals import request
from flask.json import jsonify
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Akash135#",
    database="Crud"
)

mycursor = db.cursor()

# creating an instance of flask app
app = Flask(__name__)

@app.route('/products', methods=['GET', 'POST'])
def get_and_add_products():

    if request.method == 'POST':

        product_details = request.get_json()
        print(product_details)
        
        product_name = product_details.get('product_name')
        product_desc = product_details.get('product_desc')
        product_quantity = product_details.get('product_quantity')
        product_price = product_details.get('product_price')

        mycursor.execute(
            "INSERT INTO product (product_name, product_desc, product_quantity, product_price) VALUES (%s, %s, %s, %s)", (product_name, product_desc, product_quantity, product_price))
        db.commit()

        return jsonify({
            "message": "product added"
        }), 200
    
    else:
        mycursor.execute("SELECT * FROM product")
        products = []
        # Fetching all the products from the database
        for product in mycursor:
            # Assigning the data
            product_detail = {
                "product_id": product[0],
                "product_name": product[1],
                "product_desc": product[2],
                "product_quantity": product[3],
                "product_price": product[4]
            }
            # Appending product details
            products.append(product_detail)
            
        # Cast the list into json format
        return jsonify(products), 200
        
# GET PRODUCT BY ID
@app.route('/products/<int:id>')
def get_product_by_id(id):
    mycursor.execute(f"SELECT * FROM product WHERE id = {id}")
    for product in mycursor:
        if product:
            product_detail = {
                    "product_id": product[0],
                    "product_name": product[1],
                    "product_desc": product[2],
                    "product_quantity": product[3],
                    "product_price": product[4]
                }
        
            return jsonify(product_detail), 200
        
    return jsonify({
        "message": f"product doesn't exists with the id: {id}"
    }), 204

# DELETE PRODUCT
@app.route('/products/delete/<int:id>', methods=['DELETE'])
def delete_product_by_id(id):
    
    mycursor.execute(f"SELECT * FROM product WHERE id = {id}")
    
    for product in mycursor:
        # if the product with the specific id exists, if true then delete the product
        if product:
            mycursor.execute(f"DELETE FROM product WHERE id = {id}")
            db.commit()
            return jsonify(
                {
                    "message": "product deleted"
                }
            ), 200

    return jsonify(
        {
            "message": f"product doesn't exists with the id: {id}"
        }
    ), 204
 
 
# update the product
@app.route('/products/update/<int:id>', methods=['PUT'])
def updateProduct(id):
    mycursor.execute(f"SELECT * FROM product WHERE id = {id}")
    
    for product in mycursor:
        if product:
            product_details = request.get_json()
            product_name = product_details.get('product_name')
            product_desc = product_details.get('product_desc')
            product_quantity = product_details.get('product_quantity')
            product_price = product_details.get('product_price')
            
            # if all the fields are given then update the entry
            if product_name and product_desc and product_quantity and product_price:
                sql = "UPDATE product SET product_name = %s, product_desc = %s, product_quantity=%s, product_price = %s WHERE id = %s"
                val = (product_name, product_desc, product_quantity, product_price, id)
                mycursor.execute(sql, val)
                db.commit()
            else:
                return jsonify({
                    "message": "Field missing."
                }), 204
            
        return jsonify({
            "message": "product_updated"
        }), 200
        
    return jsonify({
        "message": f"product doesn't exists with the id: {id}"
    }), 204
 
   
if __name__ == '__main__':
    app.run(debug=True)
