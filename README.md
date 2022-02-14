### Users Service
Сервис для создания, просмотра и редактирования профилей пользователей. Написан на FastAPI
1. Запуск сервиса - docker-compose up -d --build
2. Документация swagger по эндпоинту 0.0.0.0:8000/docs

#### Изменения в апи
1. Был добавлен роут для регистрации пользователей
2. Также, роут PATCH /users/{pk} был заменен на /users, так как простой пользователь может обновлять только лишь свой профиль 
