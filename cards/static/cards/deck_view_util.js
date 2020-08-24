document.addEventListener('DOMContentLoaded', (event)=> {    

    getCards(event, document.querySelector('.decks').dataset.id)

    document.querySelector('#show-deck-form').onclick = showDeckForm;

    document.querySelectorAll('.decks').forEach(element => {
        element.onclick = getCards;
    });



});


function showDeckForm(){
    const form = document.querySelector('form');
    if (form.style.display === 'block') {
        form.style.display = 'none';
    } else {
        form.style.display = 'block';
    }
}

function getCards(event, id) {

    // give the function an optional id parameter, so it can be called once the site is loaded
    if (!id) {
        id = this.dataset.id
    }
    
    fetch(`decks/get_cards/${id}`)
    .then(response => response.json())
    .then(result => {
        console.log(result)
        document.querySelector('.card-container').innerHTML = ""

        const cardContainer = document.createElement('ul');
        cardContainer.classList.add('list-group');

        const deckName = document.createElement('h2');
        deckName.innerHTML = result.name;

        const deckDescription = document.createElement('p');
        deckDescription.innerHTML = result.description;

        result.cards.forEach(card => {
            const listObject =  document.createElement('li');
            listObject.classList.add('list-group-item');
            listObject.innerHTML = `${card.english} - ${card.character} (${card.pinyin})`;
            cardContainer.append(listObject);
        })
        document.querySelector('.card-container').append(deckName, deckDescription, cardContainer);
    })
}
