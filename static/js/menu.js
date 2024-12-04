const initial_category_id = document.getElementById('initial_category_id')?.value
const initial_material_id = document.getElementById('initial_material_id')?.value
let materials = undefined
fetch('/menus/get_materials/')
    .then(response => response.json())
    .then(data => {
        materials = data
        if(initial_category_id) {
            categorySelect.value = initial_category_id
            categorySelect.dispatchEvent(new Event('change'))
        }
    })


const categorySelect = document.getElementById('category_select')
const materialSelect = document.getElementById('material_select')
categorySelect.addEventListener(
    'change',
    () => {
        const category_id = categorySelect.value
        materialSelect.innerHTML = '<option selected value="__NONE"></option>'
        materials.forEach(material => {
            if (material.category_id == category_id) {
                const option = document.createElement('option')
                option.value = material.id
                option.innerText = material.name
                materialSelect.appendChild(option)
            }
        })
        if(initial_material_id)
            materialSelect.value = initial_material_id

    })


// 追加

document.addEventListener('DOMContentLoaded', function() {
    const addToShoppingListBtns = document.querySelectorAll('.add-to-shopping-list-btn');
    addToShoppingListBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const materialId = this.getAttribute('data-material_id');
            const quantityInput = prompt('数量を入力してください:');
            if (quantityInput !== null) {
                const formData = new FormData();
                formData.append('quantity', quantityInput);
                // サーバーサイドのURLを指定せずに、各ボタンに材料IDを格納する
                formData.append('material_id', materialId);
                fetch('/shopping/add_from_menu', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert(data.message);
                    } else {
                        alert(data.error);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            }
        });
    });
});
