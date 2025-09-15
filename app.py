from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)

# CONFIGURAÇÃO DO BANCO DE DADOS
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ecommerce.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # evita warning

db = SQLAlchemy(app)
CORS(app)

# MODELAGEM DO BANCO
# Tabela: Product
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    # "Text" não tem limite de caracteres (diferente de String)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Product {self.name}>"
    
# ROTA - ADICIONAR
@app.route('/api/products/add', methods = ['POST'])
def add_product():
    data = request.json

    if 'name' in data and 'price':
        product = Product (name = data['name'], price = data['price'], description = data.get('description', ''))
        db.session.add(product)
        db.session.commit()
        return jsonify({'message': 'Product added successfully!'})
    
    return jsonify({'message': 'Invalid product data'}), 400

# ROTA - DELETAR
@app.route('/api/products/delete/<int:product_id>', methods = ['DELETE'])
def delete_product(product_id):
    # Recuperar produto da base de dados,
    # Verificar se ele existe, se sim, apagar da base de dados - se não existir, retornar 404
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify ({'message': 'Product deleted sucessfully'})
    
    return jsonify ({'message': 'Product not found'}), 404

# ROTA - RECUPERAÇÃO
@app.route('/api/products/<int:product_id>', methods = ['GET'])
def get_product_details(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify({'id': product.id, 'name': product.name, 'price': product.price, 'description': product.description})
    return jsonify({'message': 'Product not found'}), 404

# ROTA - ATUALIZAÇÃO
@app.route('/api/products/update/<int:product_id>', methods = ['PUT'])
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    
    data = request.json
    if 'name' in data:
        product.name = data['name']

    if 'price' in data:
        product.price = data['price']

    if 'description' in data:
        product.description = data['description']

    db.session.commit()
    return jsonify ({'message': 'Product updated successfully'})

# ROTA - RECUPERAÇÃO DE LISTA DE PRODUTOS
@app.route('/api/products', methods = ['GET'])
def get_products():
    products = Product.query.all()

    product_list = []
    for product in products:
        product_data = ({'id': product.id, 'name': product.name, 'price': product.price})
        product_list.append(product_data)
    return jsonify(product_list)

# ROTA/RAIZ PRINCIPAL - FUNÇÃO A SER EXECUTADA
@app.route("/")
def hello_world():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True)

# PAREI EM 37 MIN