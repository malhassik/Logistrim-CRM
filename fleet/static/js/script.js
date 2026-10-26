// Ждем, пока загрузится весь HTML
document.addEventListener("DOMContentLoaded", function () {

    // 1. Находим наши элементы на странице
    const searchInput = document.getElementById("search-input");
    const tableRows = document.querySelectorAll("tbody tr"); // Находим все строки таблицы

    // 2. Вешаем слушатель на ввод текста в поле поиска
    searchInput.addEventListener("keyup", function () {
        // Получаем текст, который ввел пользователь, и переводим в нижний регистр
        const searchText = searchInput.value.toLowerCase();

        // 3. Проходимся по каждой строке таблицы
        tableRows.forEach(function (row) {
            // Берем весь текст из строки (госномер, марка, пробег и т.д.)
            const rowText = row.innerText.toLowerCase();

            // 4. Если текст строки содержит то, что мы ищем...
            if (rowText.includes(searchText)) {
                row.style.display = ""; // ...показываем строку
            } else {
                row.style.display = "none"; // ...иначе скрываем её
            }
        });
    });
});