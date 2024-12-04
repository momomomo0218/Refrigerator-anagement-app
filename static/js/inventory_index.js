const records = document.querySelectorAll('.product_name');
const contextMenu = document.querySelector('#context_menu');
const deleteItemHref = document.querySelector('#delete_item_href');
const deleteItem = document.querySelector('#delete_item');
const discardItemHref = document.querySelector('#discard_item_href');
const discardItem = document.querySelector('#discard_item');
const editItemHref = document.querySelector('#edit_item_href');
deleteItem.addEventListener(
    'click',
    (event) => {
        if (!confirm('消費でいいですか?')) {
            event.preventDefault();
        }
    }
)

discardItem.addEventListener(
    'click',
    (event) => {
        if (!confirm('廃棄でいいですか?')) {
            event.preventDefault();
        }
    }
)


let oldTarget = null
records.forEach(record => {
    record.addEventListener(
        'click',
        e => {
            e.preventDefault();
            if (oldTarget === e.target) {
                contextMenu.setAttribute('hidden', '');
                oldTarget.style.backgroundColor = 'white'
                oldTarget = null
            } else {
                contextMenu.style.left = `${e.target.offsetLeft + 67}px`;
                contextMenu.style.top = `${e.target.offsetTop}px`;
                contextMenu.removeAttribute('hidden');
                if (oldTarget !== null)
                    oldTarget.style.backgroundColor = 'white'
                e.target.style.backgroundColor = 'lightblue'
                oldTarget = e.target
                deleteItemHref.href = '/inventory/delete/' + e.target.getAttribute('data-id')
                discardItemHref.href = '/wasted/discard/' + e.target.getAttribute('data-id')
                editItemHref.href = '/inventory/edit/' + e.target.getAttribute('data-id')
            }
        }
    )
})
