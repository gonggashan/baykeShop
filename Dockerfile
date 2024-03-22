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

# 将入口脚本复制到容器内
COPY entrypoint.sh /usr/src/app/entrypoint.sh

# 使入口脚本可执行
RUN chmod +x /usr/src/app/entrypoint.sh

# 使用入口脚本作为容器启动命令
CMD ["/usr/src/app/entrypoint.sh"]