# 基于官方 Python 运行时的精简版作为基础镜像，以减少镜像的体积。
FROM python:3.9.6-slim-buster

# 在容器内部创建并设置工作目录。
WORKDIR /app

# 将容器的时区设置为上海，并安全地设置时区，同时优化了安装依赖的步骤。
ENV TZ=Asia/Shanghai
RUN echo $TZ > /etc/timezone && \
    ln -sf /usr/share/zoneinfo/$TZ /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
    apt-get update && apt-get install -y --no-install-recommends tzdata && \
    rm -rf /var/lib/apt/lists/*

# 为了充分利用 Docker 缓存，首先复制依赖文件，避免每次构建都重复安装相同的依赖。
COPY requirements.txt .

# 安装项目依赖，使用 `--no-cache-dir` 参数以避免缓存无用的文件。
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目的所有文件到容器中的工作目录。
COPY . .

# 将启动脚本复制到/usr/local/bin/并给予执行权限。
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# 设置容器的默认启动命令。实际启动命令在 docker-entrypoint.sh 中定义。
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["gunicorn", "baykeproject.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
