#!/bin/sh

# 应用数据库迁移
echo "Applying database migrations"
python manage.py migrate --noinput
echo "manage.py migrate --noinput"
echo "django应用数据库迁移成功"

# 启动 Django 应用
echo "Starting Django application"
exec python manage.py runserver 0.0.0.0:8000
