from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import MenuMaterialMenu, Menu, FixedMenuMaterial
from ..users.models import db
from ..inventory.models import Inventory
from .forms import EditMenuForm

menus = Blueprint('menus', __name__)


@menus.route('/get_materials/', methods=['GET'])
@login_required
def get_materials():
    menu_materials = FixedMenuMaterial.query.filter_by().all()
    # menu_materials = MenuMaterial.query.filter_by(user_id=current_user.id).all()
    materials = [{'id': menu_material.id, 'name': menu_material.name, 'category_id': menu_material.category_id}
                 for menu_material in menu_materials]
    return jsonify(materials)


@menus.route('/add/', methods=['GET', 'POST'])
@login_required
def add_menu():
    form = EditMenuForm()
    if request.method == 'POST':
        menu_name = request.form.get('menu_name')
        menu = Menu(user_id=current_user.id, name=menu_name)
        db.session.add(menu)
        db.session.commit()
        return redirect(url_for('menus.edit_menu', menu_id=menu.id))
    menus = Menu.query.filter_by(user_id=current_user.id).all()
    return render_template('menus/add_menu.j2', form=form, menus=menus)


def get_menu_materials_join_query(menu_id):
    return db.session.query(FixedMenuMaterial.id, FixedMenuMaterial.name, MenuMaterialMenu.memo,
                            MenuMaterialMenu.quantity). \
        join(MenuMaterialMenu, FixedMenuMaterial.id == MenuMaterialMenu.fixed_menu_material_id). \
        join(Menu, MenuMaterialMenu.menu_id == Menu.id). \
        filter(MenuMaterialMenu.user_id == current_user.id, MenuMaterialMenu.menu_id == menu_id)


@menus.route('/<int:menu_id>', methods=['GET'])
@login_required
def menu_materials_index(menu_id):
    query = get_menu_materials_join_query(menu_id)
    menu_materials = query.all()
    menu = Menu.query.filter_by(id=menu_id, user_id=current_user.id).one()
    return render_template('menus/menu.j2', menu=menu, menu_materials=menu_materials)


@menus.route('/<int:menu_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_menu(menu_id):
    form = EditMenuForm()
    if request.method == 'POST':
        menu_material_id = request.form.get('menu_material_id')
        quantity = request.form.get('quantity')
        menu_material_menu = MenuMaterialMenu(user_id=current_user.id, menu_id=menu_id,
                                              fixed_menu_material_id=menu_material_id, quantity=quantity)
        db.session.add(menu_material_menu)
        db.session.commit()
        return redirect(url_for('menus.edit_menu', menu_id=menu_id))

    query = get_menu_materials_join_query(menu_id)
    menu_materials = query.all()
    menu = Menu.query.filter_by(id=menu_id, user_id=current_user.id).one()
    return render_template('menus/edit_menu.j2', menu=menu,
                           menu_materials=menu_materials, form=form)


@menus.route('/exist_material/<int:menu_id>/<int:material_id>', methods=['GET'])
@login_required
def exist_material(menu_id, material_id):
    inventory_items = Inventory.query.filter_by(material_id=material_id, user_id=current_user.id).all()
    material = db.session.query(
        FixedMenuMaterial.id, FixedMenuMaterial.name, MenuMaterialMenu.memo, MenuMaterialMenu.quantity). \
        join(MenuMaterialMenu, FixedMenuMaterial.id == MenuMaterialMenu.fixed_menu_material_id). \
        join(Menu, MenuMaterialMenu.menu_id == Menu.id). \
        filter(MenuMaterialMenu.user_id == current_user.id, MenuMaterialMenu.menu_id == menu_id,
               MenuMaterialMenu.fixed_menu_material_id == material_id).one()
    result = []
    for inventory in inventory_items:
        result.append({'id': inventory.id, 'material_name': material.name, 'material_memo': material.memo,
                       'material_quantity': material.quantity, 'purchase_date': inventory.purchase_date,
                       'expiration_date': inventory.expiration_date})
    return jsonify(result)
