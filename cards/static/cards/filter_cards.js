document.addEventListener('DOMContentLoaded', (event)=> {    

    document.querySelector('.filter-cards').onkeyup = function () {
        const ul = document.querySelector('.list-group');
        const li = ul.querySelectorAll('div');
        const filter = this.value.toLowerCase();

        li.forEach(ele => {
            const text = ele.querySelector('inline').innerHTML.toLowerCase();
            const btn = ele.querySelector('button').disabled; 
            if (filter === '') {
                ele.style.display = 'block';
            } else if (text.indexOf(filter) > -1 && !btn ) {
                ele.style.display = 'block';
            } else {
                ele.style.display = 'none';
            }
        });
    }

    const btns = document.querySelectorAll('.btn-add-to-deck');

    btns.forEach(ele => {
        ele.onclick = function () {
            fetch(`${this.dataset.deck}`, {
                method: 'PUT',
                body: JSON.stringify({
                    card: this.dataset.card
                })
            })
            .then(response => response.json())
            .then(result => {
                this.disabled = true;
                this.innerHTML = result.message;
                this.classList.remove('btn-outline-primary');
                this.classList.add('btn-secondary');
                this.dataset.added = true
            })
        }
    })

});