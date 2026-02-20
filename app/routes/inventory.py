from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Product, Transaction, Category
import pandas as pd
import io

inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('/add', methods=['POST'])
@login_required
def add():
    name = request.form['pname']
    stock = int(request.form['pstock'])
    price = float(request.form['pprice'])
    category_id = int(request.form['pcategory'])
    
    new_product = Product(name=name, stock=stock, price=price, category_id=category_id)
    db.session.add(new_product)
    
    # Log transaction
    db.session.flush() # get id
    trans = Transaction(product_id=new_product.id, user_id=current_user.id, type='IN', quantity=stock)
    db.session.add(trans)
    
    db.session.commit()
    flash("Product added successfully!", "success")
    return redirect(url_for('main.index'))

@inventory_bp.route('/category/add', methods=['POST'])
@login_required
def add_category():
    name = request.form['cname']
    if Category.query.filter_by(name=name).first():
        flash("Category already exists!", "danger")
    else:
        new_category = Category(name=name)
        db.session.add(new_category)
        db.session.commit()
        flash("Category added successfully!", "success")
    return redirect(url_for('main.index'))

@inventory_bp.route('/category/add_page', methods=['POST'])
@login_required
def add_category_page():
    name = request.form['cname']
    if Category.query.filter_by(name=name).first():
        flash("Category already exists!", "danger")
    else:
        new_category = Category(name=name)
        db.session.add(new_category)
        db.session.commit()
        flash("Category added successfully!", "success")
    return redirect(url_for('main.categories'))

@inventory_bp.route('/delete/<int:pid>')
@login_required
def delete(pid):
    product = Product.query.get_or_404(pid)
    db.session.delete(product)
    db.session.commit()
    flash("Product deleted successfully!", "success")
    return redirect(url_for('main.index'))

@inventory_bp.route('/edit/<int:pid>', methods=['GET', 'POST'])
@login_required
def edit(pid):
    product = Product.query.get_or_404(pid)
    categories = Category.query.all()
    
    if request.method == 'POST':
        product.name = request.form['pname']
        product.category_id = int(request.form['pcategory'])
        old_stock = product.stock
        new_stock = int(request.form['pstock'])
        product.price = float(request.form['pprice'])
        
        # Log stock change
        diff = new_stock - old_stock
        if diff != 0:
            trans_type = 'IN' if diff > 0 else 'OUT'
            trans = Transaction(product_id=product.id, user_id=current_user.id, type=trans_type, quantity=abs(diff))
            db.session.add(trans)
            
        product.stock = new_stock
        db.session.commit()
        flash("Product updated successfully!", "success")
        return redirect(url_for('main.index'))
        
    return render_template('edit_product.html', product=product, categories=categories)

@inventory_bp.route('/export_csv')
@login_required
def export_csv():
    products = Product.query.all()
    data = [{
        'id': p.id,
        'name': p.name,
        'stock': p.stock,
        'price': p.price
    } for p in products]
    
    df = pd.DataFrame(data)
    output = io.BytesIO()
    df.to_csv(output, index=False)
    output.seek(0)
    
    return send_file(output, mimetype='text/csv', as_attachment=True, download_name='inventory.csv')
