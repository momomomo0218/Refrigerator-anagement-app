# wasted/views.py
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import WastedMaterial
from ..inventory.models import FixedCategory, Inventory
from ..menus.models import FixedMenuMaterial, MenuMaterialMenu, Menu
from ..shopping.models import ShoppingList
from ..users.models import User, db
from datetime import datetime, timedelta

wasted = Blueprint('wasted', __name__)

@wasted.route('/')
@login_required
def index():
 
    wasted_inventory = WastedMaterial.query.filter_by(user_id=current_user.id).order_by(WastedMaterial.id.desc()).all()#廃棄した順
    materials = {}
    for item in wasted_inventory:
        material = FixedMenuMaterial.query.get(item.material_id)
        if material:
            materials[item.id] = material.name
    return render_template('wasted/wasted_material.j2', wasted_inventory=wasted_inventory, materials=materials)




# inventoryの方に移動
# @wasted.route('/discard/<int:_id>/', methods=['GET'])
# @login_required
# def discard(_id):
#     item = Inventory.query.filter_by(id=_id, user_id=current_user.id).one()

#     wasted_item = WastedMaterial(
#         user_id=item.user_id,
#         category_id=item.category_id,
#         material_id=item.material_id,
#         memo=item.memo,
#         quantity=item.quantity,
#         purchase_date=item.purchase_date, 
#         expiration_date=item.expiration_date, 
#     )
#     db.session.add(wasted_item)
#     db.session.delete(item)
#     db.session.commit()
#     return redirect(url_for('wasted.index'))
