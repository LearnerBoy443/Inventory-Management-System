from flask import Blueprint, render_template, request
from flask_login import login_required
from app.models import Product, Transaction, Category
from app.extensions import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def index():
    products = Product.query.all()
    categories = Category.query.all()
    total_products = len(products)
    
    # Calculate stats
    low_stock = sum(1 for p in products if p.stock < 10)
    inventory_value = sum(p.stock * p.price for p in products)
    
    return render_template('index.html', 
                           products=products,
                           categories=categories,
                           total_products=total_products,
                           low_stock=low_stock,
                           inventory_value=inventory_value)

@main_bp.route('/products')
@login_required
def products():
    products = Product.query.all()
    return render_template('products.html', products=products)

@main_bp.route('/categories')
@login_required
def categories():
    categories = Category.query.all()
    return render_template('categories.html', categories=categories)
