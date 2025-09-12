from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# CONFIGURAÇÃO DO BANCO DE DADOS
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ecommerce.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # evita warning
db = SQLAlchemy(app)

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

# ROTA/RAIZ PRINCIPAL - FUNÇÃO A SER EXECUTADA
@app.route("/")
def hello_world():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True)
