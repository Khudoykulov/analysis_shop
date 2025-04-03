// script.js
document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => {
        // Remove active class from all tabs
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        // Add active class to clicked tab
        tab.classList.add('active');

        // Placeholder for updating the price chart based on the selected tab
        const tabName = tab.getAttribute('data-tab');
        console.log(`Switching to ${tabName} price history`);

        // You can update the price chart here (e.g., using Chart.js)
        // For now, we'll just log the tab change
    });
});

// Optional: Add interactivity for the "Add Amazon Price Watch" button
document.querySelector('.add-price-watch-btn').addEventListener('click', () => {
    alert('Price watch added! You will be notified when the price drops.');
});