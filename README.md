# Задача 5 SMTP клиент
Программа для отправки электронной почты с помощью протокола SMTP.
## Использование:
  Запуская smtp.py.
  Пример запуска:
  `py smtp.py`
  Текст сообщения нужно написать в файле send_text.txt в папке info.
  Все настройки необходимо сделать в файле send_info.ini в папке info.
  Пример:
  `[SMTP]
  receivers=example@chtoto.ru //Получатели через запятую слитно.
  topic=I Send //Тема сообщения
  attachments=cat.jpg,cat2.jpg,cool.docx //Список приложений через запятую. (приложения должны лежать в папке info)

  [LOGIN]
  login= //Логин yandex почты
  password= //Пароль yandex почты`
