# schoolDB

## ToDo
- [ ] Незарегистрированные(Главная страница и логин)
    - [ ] Могут отправить резюме(В планах)
- [x] Студент(свой профиль)
    - [x] В профиле список класса(препод названия одноклассники с мылом номером), список оценок, свои данные
- [x] Учителя(свой профиль и students)
    - [x] Профиль: информация(Cвой класс, Предметы, Выставленные оценки) и выставить оценку
    - [x] Во вкладке students возможность смотреть классы(по названию с автодополнением). Список студентов класса + по нажатию на студента его оценки и инфа(ЛЧ: номер почта)
    - [x] Можно выставить оценку при нажатие на студента(убрать кнопку для Staff) 
- [ ] Staff(students, teachers и своим профилем)
    - [x] students: полные ЛЧ
    - [x] teachers: инпут фио с автодополнением. Вывод класс преподователя, его предметы, выставленные оценки.
    - [x] Профиль:
        - [x]  Добавление студента(автогенерация профиля(отправка пароля на почту и его хэширование))
        - [x] Добавление преподавателя(автогенерация профиля(отправка пароля на почту и его хэширование))
        - [ ] Добавление класса(назначение ему учителя(с автозаполнением)(отправка пароля на почту учителю уведомления о том что он теперь ведёт класс))
        - [ ] Рассмотрение резюме/заявок неавторизованных и его перенос в форму добавление 
        студента или препода(В планах)