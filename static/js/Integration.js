const cardContainer = document.getElementById('cardContainer');
const cardItems = cardContainer.getElementsByClassName('card');
let currentIndex = 0;
const cardsToShow = 3; // Number of cards to show at once

function updateCardVisibility() {
    // Hide all cards
    Array.from(cardItems).forEach((item, index) => {
        item.style.display = 'none'; // Hide all items initially
    });
    // Show the current set of cards
    for (let i = 0; i < cardsToShow; i++) {
        const index = currentIndex + i;
        if (index < cardItems.length) {
            cardItems[index].style.display = 'block'; // Show the current item
        }
    }
}

document.getElementById('nextBtn').addEventListener('click', () => {
    if (currentIndex + cardsToShow < cardItems.length) {
        currentIndex += 1; // Move to the next set of cards
    }
    updateCardVisibility();
});

document.getElementById('prevBtn').addEventListener('click', () => {
    if (currentIndex > 0) {
        currentIndex -= 1; // Move to the previous set of cards
    }
    updateCardVisibility();
});

// Initial setup to show the first set of cards
updateCardVisibility();