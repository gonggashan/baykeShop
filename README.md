docker-compose build  构建项目
docker-compose up     启动项目

<div align="center">

![baykeshop](https://www.bayke.shop/img/logo.png)

<h1>baykeShop开源商城系统</h1>

</div>

## 项目简介

baykeShop（拜客商城系统）是一款全开源Python栈商城系统，后端依托django强大的框架体系，本项目融合了django的传统模版体系，同时轻微结合了前后端分离的开发方式，在不同场景选择了不同的技术栈，使其更具学习和研究价值，并且很好的打包为一个Python包文件，使其二次开发以及集成到自身项目更加简便易用，更是python django初学者开发上手学习的不二选择！

## 项目演示

商城PC端前台：http://s.bayke.shop

## 视频教程

![img](https://www.bayke.shop/site/image/index/1698996448643.png "商城系统开发实战")

**视频教程：[django4商城系统开发实战进阶【免费连载中】_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1Ae411X7dM/)**

- 安装配置：[https://www.bilibili.com/video/BV1ea4y1X72f/](https://www.bilibili.com/video/BV1ea4y1X72f/)
- 功能使用：[https://www.bilibili.com/video/BV1mj411e73h/](https://www.bilibili.com/video/BV1mj411e73h/)

## 安装

```python
pip install baykeshop
```

## 配置

在项目settings.py中的最后引入

```python
# 开发时配置
from baykeshop.conf.develop import *

# 或者

# 部署时配置
from baykeshop.conf.production import *
```

特别说明：本项目覆盖了默认的admin进行了定制，需要将INSTALLED_APPS配置中默认的admin配置注释掉!

```
INSTALLED_APPS = [
    # 'django.contrib.admin',
]
```

## 项目urls.py中引入url

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # baykeshop的全部url
    path('', include("baykeshop.urls")),
    # 开发时静态文件配置
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
]
```

## 迁移数据

```python
python manage.py makemigrations
python manage.py migrate
```

## 初始化必要数据

```python
python manage.py initdata
```

## 部署

部署方式多种多样，本项目作为一个包文件，将不会决定参与到你的部署过程当中，你可以根据你自身项目的需求以及django的官方文档来部署你的项目！

在部署过程中如果采用异步asgi的方式部署，可能会有异步安全类错误 `SynchronousOnlyOperation`，根据django官方文档给的提示和解决方案是在项目的settings.py中配置如下代码即可解决：

```python
import os
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
```

**特别说明**：项目配置中对缓存并没有特别配置，默认使用了django的内存缓存，部署时建议设置为reids缓存或者数据库缓存，否则邮件验证会有小问题！

## 配置说明

邮件配置以及支付宝配置均在后台的**系统分类**下的**广告内容**中配置，特别需要注意的是支付宝的应用私钥格式需要转换为PKCS1格式，可使用支付宝开放平台秘钥工具进行转换！DEBUG模式下支付宝默认为沙箱环境，部署时一定要关闭django的DEBUG模式，否则支付不能正确跳转！

# 社交平台

微信公众号、头条、西瓜视频、B站、抖音账号均为“轻编程”, 可搜索关注，微信公众号会定期发送福利！

# 赞赏支持

如果本项目或教程给您带来了帮助，您可以酌情赞赏创作者！

您的赞赏将有利于该项目的持续维护和开发，以及用作文档服务器的延续！

作为一名敬业的开发者，不能保证能带着你发财致富，但却可以将我的知识传递给您！

如果你也觉得知识就是财富，那么凡赞赏金额大于20元者，将会添加作者微信以及加入微信群与一众志同道合的开发者共同交流，探讨技术，关于该项目作者也会群内答疑，直播答疑，与大家尽情互动！

赞赏留言直接备注您的微信号，我会搜索添加哦！如果没有备注，可以私信我哦！

![输入图片说明](https://www.bayke.shop/site/image/index/1698994683722.png)

# 赞赏记录

| 微信昵称   | 赞赏金额/元 | 渠道        |
| ---------- | ----------- | ----------- |
| WuRay      | 100         | 微信        |
| bin        | 100         | 微信        |
| 挽风       | 50          | 微信        |
| 晨希科技   | 50          | 微信        |
| 知行合一   | 50          | 微信        |
| 亭长       | 100         | 微信        |
| 牛腩炖番茄 | 50          | 微信        |
| 天书       | 50          | 微信        |
| Tan大人    | 20+100      | 支付宝+微信 |
| Zhao       | 20          | 微信        |
| 让风告诉你 | 50          | 微信        |
