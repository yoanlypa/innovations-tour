
// calendario.js
document.addEventListener('DOMContentLoaded', function() {
    const calendarEl = document.getElementById('calendar');
    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        events: [
            {
                title: 'Prueba',
                start: '2025-03-27',
                color: 'red'
            }
        ]
    });
    calendar.render();
});