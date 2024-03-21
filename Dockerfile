# 使用官方 Python 运行时作为父镜像
FROM python:3.10

# 设置时区为上海时间
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 设置工作目录
WORKDIR /usr/src/app

# 将项目依赖文件复制到容器内
COPY requirements.txt ./

# 安装项目依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件和启动脚本到容器内
COPY . ./
COPY entrypoint.sh entrypoint.sh

# 为启动脚本添加执行权限
RUN chmod +x entrypoint.sh

# 暴露端口 8000 供访问
EXPOSE 8000

# 设置启动脚本为入口点
ENTRYPOINT ["./entrypoint.sh"]
