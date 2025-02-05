# Используем официальный образ PostgreSQL
FROM postgres:16-alpine

# Устанавливаем пароль и пользователя (или задаем их через переменные среды)
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=1Qwerty

# Копируем SQL-скрипты инициализации (если есть)
COPY migrations/ /docker-entrypoint-initdb.d/

# Открываем порт PostgreSQL
EXPOSE 5432

# Запускаем PostgreSQL
CMD ["postgres"]