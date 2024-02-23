document.addEventListener("DOMContentLoaded", function() {
    setTimeout(function() {
        var animation1 = document.getElementById("animation1");
        var animation2 = document.getElementById("animation2");

        // Добавляем классы для анимации
        animation1.classList.add("move-left");
        animation2.classList.add("move-right");

        // Устанавливаем таймер для удаления элементов после завершения анимации
        setTimeout(function() {
            // Удаляем блокирующие элементы
            animation1.remove();
            animation2.remove();

            // Восстанавливаем доступ к элементам страницы
            document.querySelectorAll('.profile-info *').forEach(function(el) {
                el.style.pointerEvents = 'auto';
            });
            document.querySelectorAll('.friends-list *').forEach(function(el) {
                el.style.pointerEvents = 'auto';
            });
            document.querySelectorAll('.news-feed *').forEach(function(el) {
                el.style.pointerEvents = 'auto';
            });
        }, 2000); // Длительность анимации в миллисекундах (2000 мс или 2 секунды)
    }, 2000); // Время в миллисекундах (2 секунды)

    // Во время анимации блокируем доступ к интерактивным элементам
    document.querySelectorAll('.profile-info *').forEach(function(el) {
        el.style.pointerEvents = 'none';
    });
    document.querySelectorAll('.friends-list *').forEach(function(el) {
        el.style.pointerEvents = 'none';
    });
    document.querySelectorAll('.news-feed *').forEach(function(el) {
        el.style.pointerEvents = 'none';
    });
});
