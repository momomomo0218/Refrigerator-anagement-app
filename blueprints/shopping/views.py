# shopping/views.py
from flask import Blueprint, render_template, request, redirect, url_for, get_flashed_messages,jsonify,flash
from flask_login import login_required, current_user
from .models import ShoppingList
from ..inventory.models import FixedCategory, Inventory
from ..menus.models import FixedMenuMaterial, MenuMaterialMenu, Menu
from .models import ShoppingList
from ..users.models import User, db
from datetime import datetime, timedelta
# from .forms import ShoppingListForm


shopping = Blueprint('shopping', __name__)




#表示
@shopping.route('/')
@login_required
def index():
#追加  
     # FixedMenuMaterialとの結合
    shopping_items = (
        db.session.query(ShoppingList, FixedMenuMaterial.name)
        .join(FixedMenuMaterial, ShoppingList.material_id == FixedMenuMaterial.id)
        .filter(ShoppingList.user_id == current_user.id)
        .all()
    )
#ここまで

    return render_template('shopping/index.j2', title='買い物リスト', shopping_items=shopping_items)




# メニューからの追加
@shopping.route('/add_from_menu', methods=['POST'])
@login_required
def add_from_menu_to_shopping_list():
    material_id = request.form.get('material_id')
    category_id = request.form.get('category_id')
    quantity = request.form.get('quantity')

    material = FixedMenuMaterial.query.filter_by(id=material_id).first()
    material_name = material.name if material else None
    if material:
        shopping_item = ShoppingList(
            user_id=current_user.id,
            category_id=material.category_id,
            material_id=material.id,
            quantity=quantity,
        )
        db.session.add(shopping_item)
        db.session.commit()
        flash('メニューから商品を買い物リストに追加しました！', 'success')
    else:
        flash('指定されたメニュー材料が見つかりませんでした。', 'error')

    return jsonify({'success': True, 'message': '買い物リストに商品を追加しました！', 'material_name': material_name}) 



@shopping.route('/delete/<int:item_id>', methods=['GET', 'POST'])
@login_required
def delete_shopping_item(item_id):
    shopping_item = ShoppingList.query.filter_by(id=item_id, user_id=current_user.id).first()

    db.session.delete(shopping_item)
    db.session.commit()

    flash('買い物リストから商品を削除しました！', 'success')
    return redirect(url_for('shopping.index'))



