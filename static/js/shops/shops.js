document.addEventListener('DOMContentLoaded', () => {
    const storeGrid = document.getElementById('storeGrid');
    const storeCards = document.querySelectorAll('.store-card');
    const categoryLinks = document.querySelectorAll('.categories ul li a');
    const prevPageBtn = document.getElementById('prevPage');
    const nextPageBtn = document.getElementById('nextPage');
    const pageNumbersContainer = document.getElementById('pageNumbers');

    let currentPage = 1;
    const itemsPerPage = 12; // 12 та дўкон (4 тадан 3 қатор)
    let filteredCards = Array.from(storeCards);

    // Функция пагинацияни янгиловчи
    function updatePagination() {
        const totalItems = filteredCards.length;
        const totalPages = Math.ceil(totalItems / itemsPerPage);

        // Барча карточкаларни яшириш
        storeCards.forEach(card => card.classList.add('hidden'));

        // Фақат жорий саҳифадаги карточкаларни кўрсатиш
        const start = (currentPage - 1) * itemsPerPage;
        const end = start + itemsPerPage;
        filteredCards.slice(start, end).forEach(card => card.classList.remove('hidden'));

        // Пагинация тугмаларини яратиш
        pageNumbersContainer.innerHTML = '';
        for (let i = 1; i <= totalPages; i++) {
            const pageBtn = document.createElement('button');
            pageBtn.textContent = i;
            pageBtn.classList.toggle('active', i === currentPage);
            pageBtn.addEventListener('click', () => {
                currentPage = i;
                updatePagination();
            });
            pageNumbersContainer.appendChild(pageBtn);
        }

        // Олдинги ва Кейинги тугмаларини фаол/нофаол қилиш
        prevPageBtn.disabled = currentPage === 1;
        nextPageBtn.disabled = currentPage === totalPages;
    }

    // Категория фильтрлаш
    categoryLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            categoryLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');

            const category = link.getAttribute('data-category');
            filteredCards = Array.from(storeCards).filter(card => 
                category === 'all' || card.getAttribute('data-category') === category
            );

            currentPage = 1; // Жорий саҳифани 1 га қайтариш
            updatePagination();
        });
    });

    // Олдинги саҳифа
    prevPageBtn.addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            updatePagination();
        }
    });

    // Кейинги саҳифа
    nextPageBtn.addEventListener('click', () => {
        const totalPages = Math.ceil(filteredCards.length / itemsPerPage);
        if (currentPage < totalPages) {
            currentPage++;
            updatePagination();
        }
    });

    // Илк юкланишда пагинацияни янгиловчи
    updatePagination();
});