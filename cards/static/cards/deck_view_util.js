document.addEventListener('DOMContentLoaded', (event)=> {    

    fetch(`decks/get_cards`)
    .then(response => response.json())
    .then(result => {
        renderCards(result)
    });

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

function getCards(event) {

    // give the function an optional id parameter, so it can be called once the site is loaded
    let url = `decks/get_cards`
    if (this.dataset.id) {
        url = `decks/get_cards/${this.dataset.id}`
    } 
    
    fetch(url)
    .then(response => response.json())
    .then(result => {
        renderCards(result)
    })
}

function renderCards(deck) {
    document.querySelector('.card-container').innerHTML = ""

    const cardContainer = document.createElement('ul');
    cardContainer.classList.add('list-group');

    const deckName = document.createElement('h2');
    deckName.innerHTML = deck.name;

    const deckDescription = document.createElement('p');
    deckDescription.innerHTML = deck.description;

    deck.cards.forEach(card => {
        const listObject =  document.createElement('li');
        listObject.classList.add('list-group-item');
        listObject.innerHTML = `${card.english} - ${card.character} (${card.pinyin})`;
        cardContainer.append(listObject);
    })

    if (deckName.innerHTML !== 'All Cards'){
        const addToDeck = document.createElement('a');
        addToDeck.setAttribute("href", `decks/add/${deck.id}`);
        addToDeck.innerHTML = 'Add Cards';
        document.querySelector('.card-container').append(deckName, deckDescription, addToDeck, cardContainer);
    } else {
        document.querySelector('.card-container').append(deckName, deckDescription, cardContainer);
    }
    
}
