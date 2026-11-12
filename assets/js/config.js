/* Настройки отправки заявок.
   endpoint — адрес своего сервера (например, https://api.voriq.ru/lead), принимает POST JSON
              {name, contact, type, msg, page}. Если указан — форма шлёт туда, токен бота на клиенте не нужен.
   Пока endpoint пустой — работает прежняя схема: заявка уходит прямо в @voriq_applicationsBot
   (токен в form.js зашифрован, как на текущем сайте). */
window.VORIQ_FORM = {
  endpoint: '',
  telegramFallback: true,
};
