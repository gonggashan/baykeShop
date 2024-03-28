#!/bin/bash

# 执行数据库迁移和静态文件收集
python manage.py migrate --noinput
python manage.py collectstatic --noinput --clear
python manage.py initdata
python manage.py create_superuser

# 在后台启动 sqlite_web
sqlite_web ./db.sqlite3 -p 8001 -H 0.0.0.0 > sqlite_web.log 2>&1 &

# 执行原始 CMD 命令，比如启动 Gunicorn 服务
exec "$@"
