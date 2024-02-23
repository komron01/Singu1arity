document.addEventListener("DOMContentLoaded", function() {
    // Получаем список диалогов
    const dialogueList = document.getElementById("dialogue-list");

    // Получаем контейнер для отображения сообщений
    const conversationWindow = document.getElementById("conversation-window");

    // Обработчик события клика по элементу списка диалогов
    dialogueList.addEventListener("click", function(event) {
        // Проверяем, был ли клик по элементу списка
        if (event.target.tagName === "LI") {
            // Получаем идентификатор выбранного диалога
            const dialogueId = event.target.dataset.dialogue;

            // Очищаем контейнер для отображения сообщений
            conversationWindow.innerHTML = "";

            // Отображаем историю выбранного диалога
            const dialogueHistory = getDialogueHistory(dialogueId);
            dialogueHistory.forEach(function(message) {
                conversationWindow.innerHTML += `<div class="message">${message}</div>`;
            });
        }
    });

    // Функция для получения истории выбранного диалога (заглушка)
    function getDialogueHistory(dialogueId) {
        // Здесь должен быть ваш код для получения истории диалога из базы данных или другого источника данных
        // В данном случае используется заглушка
        switch (dialogueId) {
            case "dialogue1":
                return ["Сообщение 1 из диалога 1", "Сообщение 2 из диалога 1", "Сообщение 3 из диалога 1"];
            case "dialogue2":
                return ["Сообщение 1 из диалога 2", "Сообщение 2 из диалога 2", "Сообщение 3 из диалога 2"];
            default:
                return [];
        }
    }
});
