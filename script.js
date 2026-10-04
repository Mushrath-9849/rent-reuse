function requestItem(itemName) {
    alert(
        "Rental request sent for: " +
        itemName +
        "\n\nThe owner will review your request."
    );
}
function searchItems() {

    const input = document.getElementById("searchInput");

    const searchText = input.value.toLowerCase();

    const cards = document.querySelectorAll(".item-card");

    cards.forEach(function(card) {

        const itemName = card
            .querySelector("h3")
            .textContent
            .toLowerCase();

        const description = card
            .querySelector("p")
            .textContent
            .toLowerCase();

        if (
            itemName.includes(searchText) ||
            description.includes(searchText)
        ) {
            card.style.display = "block";
        } else {
            card.style.display = "none";
        }

    });
}