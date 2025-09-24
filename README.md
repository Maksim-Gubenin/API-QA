
# API-сервис для вопросов и ответов


Проект для тестирования и обеспечения качества API с использованием Django и Docker.

## Технологии

- **Backend**: Django + Django REST Framework
- **Database**: PostgreSQL
- **Web Server**: Nginx
- **Containerization**: Docker + Docker Compose
- **Python**: 3.12

## Предварительные требования

- Docker (20.10+)
- Docker Compose (2.0+)
- Git

## Установка и запуск

### 1. Клонирование репозитория

```bash
    git clone https://github.com/Maksim-Gubenin/API-QA.git
    
    cd API-QA
```

### 2. Настройка переменных окружения
Создайте файл `.env` в корневой директории:

```bash
  cp .env.example .env
```

Отредактируйте `.env` файл, указав необходимые настройки (уже настроены по умолчанию):

```bash
    DJANGO_SECRET_KEY=your-super-secret-key-here
    DJANGO_DEBUG=0
    ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
    POSTGRES_DB=qa_db
    POSTGRES_USER=qa_user
    POSTGRES_PASSWORD=qa_password
    POSTGRES_HOST=db
    POSTGRES_PORT=5432
```

**Важно**: Замените `your-super-secret-key-here` на настоящий секретный ключ для production использования.

### 3. Запуск приложения

```bash
    docker-compose up --build
```

Приложение будет доступно по адресу: **http://localhost**

### 4. Остановка приложения

```bash
    docker-compose down
```

### 5. Запуск в фоновом режиме

```bash
    docker-compose up -d --build
```

## Управление приложением

### Особенности реализации

#### Идентификаторы пользователей (UUID)

Для ответов используется поле user_id типа UUID. Клиент должен самостоятельно генерировать UUID и передавать его при создании ответа:

```bash
curl -X POST http://localhost:8000/questions/1/answers/ \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "123e4567-e89b-12d3-a456-426614174000",
    "text": "Ответ на вопрос"
  }'
```

#### Админка Django
Вопросы: доступны для управления через админку

Ответы: управление через админку ограничено из-за использования UUID полей

### Возможные улучшения

- Автогенерация UUID: Реализовать автоматическую генерацию user_id на сервере

- Аутентификация: Добавить систему аутентификации пользователей

### Загрузка тестовых данных

Для загрузки тестовых данных используется кастомная команда:

```bash
    docker-compose exec web python manage.py load_test_data
```

### Создание суперпользователя

```bash
    docker-compose exec web python manage.py createsuperuser
```

После создания суперпользователя доступна админ-панель: **http://localhost/admin**


### Запуск тестов

```bash
    docker-compose exec web python manage.py test
```

### Запуск линтеров

```bash
    docker-compose exec web poetry run lint
```

### Просмотр логов

Логи веб-приложения:

```bash
    docker-compose logs web
```


Логи базы данных:

```bash
    docker-compose logs db
```

Логи nginx:

```bash
    docker-compose logs nginx
```

Логи в реальном времени:

```bash
    docker-compose logs -f web
```

## Методы API:

Вопросы (Questions):

- GET **/questions/** — список всех вопросов
- POST **/questions/** — создать новый вопрос
- GET **/questions/{id}/** — получить вопрос и все ответы на него
- DELETE **/questions/{id}/** — удалить вопрос (вместе с ответами)


Ответы (Answers):
- POST **/questions/{id}/answers/** — добавить ответ к вопросу
- GET **/answers/{id}** — получить конкретный ответ
- DELETE **/answers/{id}** — удалить ответ

**Разработано**: Губенин МАксим Андреевич  
**Контакты**

- telegram: @SKDM25
- mail: maksimgubenin@mail.ru

**Версия**: 1.0.0