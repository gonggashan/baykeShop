#!/bin/sh

# 应用数据库迁移
echo "Applying database migrations"
python manage.py migrate --noinput
echo "manage.py migrate --noinput"
echo "django应用数据库迁移成功"

#初始化必要数据
python manage.py initdata
echo "初始化必要数据 成功"

# 数据库面板
echo "启动 数据库面板"
sqlite_web ./db.sqlite3 -p 8001 -H 0.0.0.0 &

# 启动 Django 应用
echo "Starting Django application"
exec python manage.py runserver 0.0.0.0:8000
