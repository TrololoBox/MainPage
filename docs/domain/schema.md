# Базовая схема данных

Документ описывает опорные таблицы для аутентификации и авторизации в базе SQLite. Миграции лежат в каталоге `backend/migrations/` и могут применяться скриптом `apply.sh` (переменная `DB_FILE` позволяет указать файл БД). Откат выполняется через `rollback.sh`.

## Таблицы

### roles
| Поле        | Тип       | Ограничения              | Назначение                                        |
|-------------|-----------|--------------------------|---------------------------------------------------|
| id          | INTEGER   | PK, AUTOINCREMENT        | Уникальный идентификатор роли                     |
| name        | TEXT      | NOT NULL, UNIQUE         | Системное имя роли (`admin`, `teacher`, `parent`) |
| description | TEXT      | NULL                     | Человекочитаемое описание                         |
| created_at  | DATETIME  | DEFAULT CURRENT_TIMESTAMP| Дата и время создания записи                      |

### users
| Поле          | Тип       | Ограничения                       | Назначение                                  |
|---------------|-----------|-----------------------------------|---------------------------------------------|
| id            | INTEGER   | PK, AUTOINCREMENT                 | Уникальный идентификатор пользователя       |
| email         | TEXT      | NOT NULL, UNIQUE                  | Логин (e-mail)                              |
| password_hash | TEXT      | NOT NULL                          | Хэш пароля                                  |
| role_id       | INTEGER   | NOT NULL, FK → roles(id)          | Роль пользователя                           |
| is_active     | BOOLEAN   | NOT NULL, DEFAULT 1               | Флаг активности учетной записи              |
| created_at    | DATETIME  | DEFAULT CURRENT_TIMESTAMP         | Время создания                              |
| updated_at    | DATETIME  | DEFAULT CURRENT_TIMESTAMP         | Время последнего обновления                |

### sessions
| Поле          | Тип       | Ограничения                                     | Назначение                                 |
|---------------|-----------|-------------------------------------------------|--------------------------------------------|
| id            | INTEGER   | PK, AUTOINCREMENT                               | Уникальный идентификатор сессии            |
| user_id       | INTEGER   | NOT NULL, FK → users(id), ON DELETE CASCADE    | Владелец сессии                            |
| session_token | TEXT      | NOT NULL, UNIQUE                                | Токен доступа                              |
| user_agent    | TEXT      | NULL                                            | Браузер/клиент                             |
| ip_address    | TEXT      | NULL                                            | IP-адрес, с которого создана сессия        |
| expires_at    | DATETIME  | NOT NULL                                        | Время истечения токена                     |
| revoked_at    | DATETIME  | NULL                                            | Время принудительного завершения сессии    |
| created_at    | DATETIME  | DEFAULT CURRENT_TIMESTAMP                       | Время создания                             |

## Связи
- `users.role_id` → `roles.id` (ограничение `ON DELETE RESTRICT`, чтобы нельзя было удалить роль, пока есть пользователи).
- `sessions.user_id` → `users.id` (ограничение `ON DELETE CASCADE`, чтобы при удалении пользователя его сессии также удалялись).

## Индексы
- `idx_users_role_id` ускоряет выборку пользователей по роли.
- `idx_sessions_user_id` и `idx_sessions_expires_at` ускоряют выборки по пользователю и по сроку жизни токена.
