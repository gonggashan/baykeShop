# 使用官方 Python 运行时的精简版作为基础镜像，以减少镜像的体积。
FROM python:3.9.6-slim-buster

# 在容器内部创建并设置工作目录。
WORKDIR /app

# 将容器的时区设置为上海。
ENV TZ=Asia/Shanghai

# 安全且简洁地设置时区。
RUN echo $TZ > /etc/timezone && \
    ln -sf /usr/share/zoneinfo/$TZ /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

# 为了充分利用 Docker 缓存，首先复制依赖文件，避免每次构建都重复安装相同的依赖。
COPY requirements.txt .

# 安装项目依赖，使用 `--no-cache-dir` 参数以避免缓存无用的文件。
RUN pip install --no-cache-dir -r requirements.txt

# 安装 sqlite_web，确保它在 requirements.txt 文件或这里安装
RUN pip install sqlite-web

# 复制项目的所有文件到容器中的工作目录。
COPY . .

# 复制并设置入口脚本为容器启动命令的入口点
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
