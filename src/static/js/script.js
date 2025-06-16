function filterDishes(category) {
    const dishes = Array.from(document.querySelectorAll('.dish_card'));

    // Сортировка блюд по названию
    dishes.sort((a, b) => {
        const nameA = a.getAttribute('data-name');
        const nameB = b.getAttribute('data-name');
        return nameA.localeCompare(nameB);
    });

    // Обновление DOM после сортировки
    const container = document.querySelector('.dish_table_row'); // Предположим, что это ваш контейнер
    container.innerHTML = ''; // Очищаем контейнер

    dishes.forEach(dish => {
        const dishName = dish.getAttribute('data-name');

        if (category === 'all' || dishName.includes(category.toLowerCase())) {
            container.appendChild(dish); // Добавляем обратно в контейнер
        }
    });
}




