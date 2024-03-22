# 使用官方 Python 运行时作为基础镜像，并且选择一个更小的镜像版本来减少构建大小。
FROM python:3.9.6-slim-buster

# 设置时区为上海时间
ENV TZ=Asia/Shanghai

# 使用更安全、更简洁的方式设置时区
RUN echo $TZ > /etc/timezone && \
    ln -sf /usr/share/zoneinfo/$TZ /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

# 设置工作目录
WORKDIR /usr/src/app

# 首先只复制依赖文件，以利用 Docker 构建缓存，避免每次构建都重新安装不变的依赖
COPY requirements.txt .

# 安装项目依赖，使用 `--no-cache-dir` 避免保存无用的文件
RUN pip install --no-cache-dir -r requirements.txt

# 现在复制项目文件到容器内，这样当项目文件变化时不会重新安装未变的依赖
COPY . .

# 应用数据库迁移，初始化必要数据，并设置数据库面板
# 使用 && 连接命令减少镜像层的数量，使镜像更轻量
RUN python manage.py migrate --noinput && \
    python manage.py initdata && \
    (sqlite_web ./db.sqlite3 -p 8001 -H 0.0.0.0 > sqlite_web.log 2>&1 &)

# 暴露端口 8000 和 8001 供访问
EXPOSE 8000 8001

# 使用 CMD 而不是 exec，这是 Dockerfile 中推荐的方式启动服务
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
