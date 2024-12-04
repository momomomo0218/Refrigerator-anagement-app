from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .forms import CategoryForm, InventoryForm
from .models import FixedCategory, Inventory
from ..menus.models import Menu, FixedMenuMaterial
from ..shopping.models import ShoppingList
from ..users.models import User, db
from ..wasted.models import WastedMaterial
from datetime import datetime, timedelta

inventory = Blueprint('inventory', __name__)


@inventory.route('/')
@login_required
def index():
    inventory_items = Inventory.query.filter_by(user_id=current_user.id).order_by(Inventory.expiration_date).all()
    now = datetime.today()
    # '明日' を計算
    _timedelta = timedelta(days=1)
    tomorrow = (now + _timedelta).strftime('%Y-%m-%d')
    today = now.strftime('%Y-%m-%d')
    return render_template('inventory/inventory_index.j2', inventory=inventory_items, today=today, tomorrow=tomorrow)


@inventory.route('/add/', methods=['GET', 'POST'])
@login_required
def add():
    form = InventoryForm()
    if request.method == 'POST':
        category_id = request.form.get('category_id')
        category = FixedCategory.query.filter_by(id=category_id).one()
        material_id = request.form.get('material_id')
        material = FixedMenuMaterial.query.filter_by(id=material_id).one()
        memo = request.form.get('memo')
        quantity = request.form.get('quantity')
        purchase_date = datetime.strptime(request.form.get('purchase_date'), '%Y-%m-%d').date()
        expiration_date = datetime.strptime(request.form.get('expiration_date'), '%Y-%m-%d').date()
        inventory_table = Inventory(user_id=current_user.id, category_id=category.id,
                                    material_id=material.id, memo=memo, quantity=quantity,
                                    purchase_date=purchase_date, expiration_date=expiration_date)
        db.session.add(inventory_table)
        db.session.commit()
        # Add the new item to the database
        return redirect(url_for('inventory.index'))
    return render_template('inventory/add_inventory.j2', form=form)




#食べる場合
@inventory.route('/delete/<int:_id>/', methods=['GET'])
@login_required
def delete(_id):
    item = Inventory.query.filter_by(id=_id, user_id=current_user.id).first()
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('inventory.index'))


@inventory.route('/edit/<int:inventory_id>/', methods=['GET', 'POST'])
@login_required
def edit(inventory_id):
    inventory_item = Inventory.query.filter_by(user_id=current_user.id, id=inventory_id).one()
    form = InventoryForm()
    form.id = inventory_item.id
    if request.method == 'POST':
        inventory_item.category_id = request.form.get('category_id')
        inventory_item.material_id = request.form.get('material_id')
        inventory_item.memo = request.form.get('memo')
        inventory_item.quantity = request.form.get('quantity')
        inventory_item.purchase_date = datetime.strptime(request.form.get('purchase_date'), '%Y-%m-%d').date()
        inventory_item.expiration_date = datetime.strptime(request.form.get('expiration_date'), '%Y-%m-%d').date()
        db.session.commit()
        # Add the new item to the database
        return redirect(url_for('inventory.index'))
    else:
        form.initial_category_id.data = inventory_item.category_id
        form.initial_material_id.data = inventory_item.material_id
        form.memo.data = inventory_item.memo
        form.quantity.data = inventory_item.quantity
        form.purchase_date.data = inventory_item.purchase_date
        form.expiration_date.data = inventory_item.expiration_date
        return render_template('inventory/edit_inventory.j2', form=form)
