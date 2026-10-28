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

// Ждем загрузки страницы
document.addEventListener("DOMContentLoaded", function () {

    // Находим форму заправки (если мы на странице /fuel/add/)
    const fuelForm = document.getElementById("fuel-form");
    const formMessages = document.getElementById("form-messages");

    // Если форма существует на этой странице, вешаем на нее обработчик
    if (fuelForm) {
        fuelForm.addEventListener("submit", function (event) {
            // 1. Отменяем стандартную перезагрузку страницы
            event.preventDefault();

            // 2. Собираем данные из формы (включая файлы, если есть, и CSRF-токен)
            const formData = new FormData(fuelForm);

            // 3. Отправляем запрос через fetch
            fetch(window.location.href, {
                method: "POST",
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest' // Говорим Django, что это AJAX
                }
            })
                .then(response => response.json())
                .then(data => {
                    if (data.status === "success") {
                        // Показываем зеленое сообщение
                        formMessages.innerText = data.message;
                        formMessages.style.color = "#2ecc71";
                        fuelForm.reset(); // Очищаем поля формы
                    } else {
                        // Показываем красное сообщение об ошибке
                        formMessages.innerText = "Ошибка! Проверьте введенные данные.";
                        formMessages.style.color = "#ff4444";
                    }
                })
                .catch(error => {
                    console.error("Ошибка сети:", error);
                    formMessages.innerText = "Ошибка сети. Попробуйте позже.";
                    formMessages.style.color = "#ff4444";
                });
        });
    }
});