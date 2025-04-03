// Tab functionality
const tabs = document.querySelectorAll('.tab');
tabs.forEach(tab => {
    tab.addEventListener('click', () => {
        tabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        // Add logic to filter stores based on the selected tab if needed
    });
});

// Store card click functionality
document.querySelectorAll('.store-card').forEach(card => {
    card.addEventListener('click', () => {
        const storeName = card.querySelector('.store-name').textContent;
        window.location.href = `#${storeName}`; // Simulate navigation
    });
});

// Category card click functionality
document.querySelectorAll('.category-card').forEach(card => {
    card.addEventListener('click', () => {
        const categoryName = card.querySelector('.category-name').textContent;
        window.location.href = `#${categoryName}`; // Simulate navigation
    });
});

// Search bar functionality
const searchInput = document.querySelector('#search-input');
const searchButton = document.querySelector('.search-icon');
const storeGrid = document.querySelector('#store-grid');
const storeCards = document.querySelectorAll('.store-card');

searchButton.addEventListener('click', () => {
    const query = searchInput.value.trim().toLowerCase();
    filterStores(query);
});

searchInput.addEventListener('input', () => {
    const query = searchInput.value.trim().toLowerCase();
    filterStores(query);
});

function filterStores(query) {
    storeCards.forEach(card => {
        const storeName = card.querySelector('.store-name').textContent.toLowerCase();
        if (storeName.includes(query)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

// Theme toggle
const themeButton = document.querySelector('.theme-btn');
themeButton.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    const isDark = document.body.classList.contains('dark-mode');
    themeButton.innerHTML = isDark ? '<i class="fas fa-moon"></i>' : '<i class="fas fa-sun"></i>';
});

// Smooth scroll for tabs
const tabsContainer = document.querySelector('.tabs');
tabsContainer.addEventListener('wheel', (e) => {
    e.preventDefault();
    tabsContainer.scrollLeft += e.deltaY;
});