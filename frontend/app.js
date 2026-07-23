const searchInput = document.getElementById("searchInput");
const suggestionsList = document.getElementById("suggestionsList");

const API_BASE_URL = "http://localhost:8000";

searchInput.addEventListener("input", async () => {
    const prefix = searchInput.value.trim();

    if (prefix.length === 0) {
        clearSuggestions();
        return;
    }

    const suggestions = await fetchSuggestions(prefix);
    renderSuggestions(suggestions);
});

async function fetchSuggestions(prefix) {
    const encodedPrefix = encodeURIComponent(prefix);
    const response = await fetch(`${API_BASE_URL}/autocomplete?prefix=${encodedPrefix}`);
    const data = await response.json();

    return data.suggestions;
}

function renderSuggestions(suggestions) {
    suggestionsList.innerHTML = "";

    if (suggestions.length === 0) {
        clearSuggestions();
        return;
    }

    suggestions.forEach((suggestion) => {
        const item = document.createElement("li");

        item.className = "suggestion-item";
        item.textContent = suggestion;

        item.addEventListener("click", () => {
            searchInput.value = suggestion;
            clearSuggestions();
        });

        suggestionsList.appendChild(item);
    });

    suggestionsList.classList.add("visible");
}

function clearSuggestions() {
    suggestionsList.innerHTML = "";
    suggestionsList.classList.remove("visible");
}