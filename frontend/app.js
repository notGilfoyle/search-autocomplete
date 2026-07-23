const searchInput = document.getElementById("searchInput");
const suggestionsList = document.getElementById("suggestionsList");

const API_BASE_URL = "http://localhost:8000";
const DEBOUNCE_DELAY = 250;

let debounceTimer = null;
let currentSuggestions = [];
let selectedIndex = -1;

searchInput.addEventListener("input", () => {
    const prefix = searchInput.value.trim();

    selectedIndex = -1;

    if (debounceTimer !== null) {
        clearTimeout(debounceTimer);
    }

    if (prefix.length === 0) {
        clearSuggestions();
        return;
    }

    debounceTimer = setTimeout(async () => {
        showMessage("Searching...");

        try {
            const suggestions = await fetchSuggestions(prefix);
            currentSuggestions = suggestions;
            renderSuggestions(suggestions);
        } catch (error) {
            showMessage("Could not load suggestions");
        }
    }, DEBOUNCE_DELAY);
});

searchInput.addEventListener("keydown", (event) => {
    if (currentSuggestions.length === 0) {
        return;
    }

    if (event.key === "ArrowDown") {
        event.preventDefault();
        selectedIndex = selectedIndex + 1;

        if (selectedIndex >= currentSuggestions.length) {
            selectedIndex = 0;
        }

        renderSuggestions(currentSuggestions);
    }

    if (event.key === "ArrowUp") {
        event.preventDefault();
        selectedIndex = selectedIndex - 1;

        if (selectedIndex < 0) {
            selectedIndex = currentSuggestions.length - 1;
        }

        renderSuggestions(currentSuggestions);
    }

    if (event.key === "Enter" && selectedIndex >= 0) {
        event.preventDefault();

        const selectedSuggestion = currentSuggestions[selectedIndex];
        chooseSuggestion(selectedSuggestion);
    }
});

async function fetchSuggestions(prefix) {
    const encodedPrefix = encodeURIComponent(prefix);
    const response = await fetch(`${API_BASE_URL}/autocomplete?prefix=${encodedPrefix}`);

    if (!response.ok) {
        throw new Error("Request failed");
    }

    const data = await response.json();

    return data.suggestions;
}

function renderSuggestions(suggestions) {
    suggestionsList.innerHTML = "";

    if (suggestions.length === 0) {
        showMessage("No suggestions found");
        return;
    }

    suggestions.forEach((suggestion, index) => {
        const item = document.createElement("li");

        item.className = "suggestion-item";

        if (index === selectedIndex) {
            item.classList.add("selected");
        }

        item.textContent = suggestion;

        item.addEventListener("click", () => {
            chooseSuggestion(suggestion);
        });

        suggestionsList.appendChild(item);
    });

    suggestionsList.classList.add("visible");
}

function chooseSuggestion(suggestion) {
    searchInput.value = suggestion;
    clearSuggestions();
}

function showMessage(message) {
    suggestionsList.innerHTML = "";

    const item = document.createElement("li");
    item.className = "suggestion-item message";
    item.textContent = message;

    suggestionsList.appendChild(item);
    suggestionsList.classList.add("visible");
}

function clearSuggestions() {
    suggestionsList.innerHTML = "";
    suggestionsList.classList.remove("visible");
    currentSuggestions = [];
    selectedIndex = -1;
}