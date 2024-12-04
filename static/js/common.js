const body = document.querySelector('body');
const header = document.querySelector('header');
document.getElementById('hamburger').addEventListener(
    'click',
    function() {
        if (this.classList.toggle('open')) {
            header.classList.add('pointer_event_auto')
            body.classList.add('pointer_event_none')
        } else {
            header.classList.remove('pointer_event_auto')
            body.classList.remove('pointer_event_none')
        }
    }
)