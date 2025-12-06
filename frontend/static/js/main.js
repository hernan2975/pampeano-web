// Interactividad adicional para pampeano-web
document.addEventListener('DOMContentLoaded', function() {
    // Cerrar mensajes de éxito/error después de 5 segundos
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s';
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });

    // Confirmación para acciones destructivas
    document.querySelectorAll('[data-confirm]').forEach(button => {
        button.addEventListener('click', function(e) {
            const message = this.getAttribute('data-confirm') || '¿Está seguro?';
            if (!confirm(message)) e.preventDefault();
        });
    });

    // Modo offline detection
    function updateOnlineStatus() {
        const status = document.getElementById('online-status');
        if (status) {
            status.textContent = navigator.onLine ? '🟢 Online' : '🔴 Offline';
            status.style.color = navigator.onLine ? '#2a9d8f' : '#e76f51';
        }
    }

    window.addEventListener('online', updateOnlineStatus);
    window.addEventListener('offline', updateOnlineStatus);
    updateOnlineStatus();
});
