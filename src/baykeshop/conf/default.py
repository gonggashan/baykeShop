'''
@file            :settings.py
@Description     :默认配置
@Date            :2023/09/02 23:32:44
@Author          :幸福关中 && 轻编程
@version         :v1.0
@EMAIL           :1158920674@qq.com
@WX              :baywanyun
'''


import datetime


DEFAULTS_CONF = {
    # 站点title
    "SITE_TITLE": "baykeShop开源商城系统",
    # 站点头Logo
    "SITE_HEADER": "baykeShop Header",
    # 首页title
    "INDEX_TITLE": "baykeShop开源商城系统",
    # 数据表前缀
    "DB_PREFIX": "bayke",
    # 默认管理后台开启自定义菜单
    "CUSTOM_MENU": False,
    # 手机号验证正则
    "REGEX_PHONE": "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$",
    # 邮箱验证正则
    "REGEX_EMAIL": "^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$",
    # 邮箱验证码过期时间
    "EMAIL_CODE_EXP": datetime.timedelta(seconds=300),
    # 验证码随机范围
    "CODE_CHAR": "1234567890",
    # 验证码长度
    "CODE_LENGTH": 4,
    # 支付宝支付配置
    "ALIPAY": {
        "APPID": '2021000122666025',
        "PUBLIC_KEY": 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAnGm4s+aI1LsCwL9i67GSqEICxqfkyzydk6TIA57M9++EHBUAsXHa5mpgUIQwlYKetzsdPnYK8rS7Pkn6RFogF639zoaRBIpCu8K/lazUB2PqykLdV+XH8DqtH3k6lz1hFRAOHDIn3wVqIUOC0H/G4TFsp8Cd/cgLYAFr12Fgm20/OW8GZNnhfZmmcbHc4el9CqWuEt1xRQLAgLiaDjTZ5RrgSwHem2p1kYKjcs0jw1M+IyKIZK0k6s/KwwqsSlG28ysP94nBI1v3vSIL0e25rvv5irYXi78hfmmO8+sBdYxBzkaF7tndTctTxTYMcnk/+1jKijahDW/72zTI0AwSxwIDAQAB',
        "PRIVATE_KEY": 'MIIEpQIBAAKCAQEAwCuqnkSxuJthPdkQIW2k/l4fpDjWT3TPBQy5hOfKUBUUl42xN72fqtWB8fUAmLlLXuDgFzPMY17Hk8huCDFT75Sidy1nLCayKgo4xnoyk+e/VkUQjEprpRkUq0YzZWPUwQK9aSaO+XI+ivkbnDIBw9fmKV+PxLqfnOPH5630SdT5mEF5hhrwmw8RDrUz404u+BilZw0Q2qJshgXES9vafqpTpe/jiUz8A66v9eIAOskcMDTz4iUuCThH2YCQqWtyE6aNzO3NQ+SVpdBfZNQzmqoRlKDUiX8Fb29sdzBPjSHstYr5rXCVI5XFeCFCqaCpzkpnPoX0DfKIGfmW27UWTQIDAQABAoIBAH97eFBOGefxi+zPlpfWeOIV5r+2xNUpFDyxWFEGw3ukwGhZovrrXISj5vRwJ9ko8wsZ+w7pWemB8rvi9ruQnbIN1EljYVI0yXSCG2/vmKXt00yTvIqUxBxeKwwEIgxc0cLI4oZjAe4RD9R5tQtFUU5uZ02DC4jilQgrQ246RBjFfctF4uZCP9LtToKDGlw1rW6He40CUxhyGVtgNGKx+eK+pspDgdTkcwggVwNWckuWBVBLdVty/J9D9vSNNXFltBHnb27NuRiWLjKHrWDJSxi2DiRDt5Djh/ghmLPlQm3rrqOcUcZHFlfuV3w8SMkjFoY4cSNdbuY9+S8aaPTcGbECgYEA5/I6ToS2/7koi65YN3RB6p8d+8GwF0gttisJu/fRNowQODYATiQWLbRMtUC7zeHq8ee8hPgmz/7rT44GgjPj9Z5GLkTnxaJYXOONCslBRQ+ntIct3oRNCcN/2e2mvfYx5aHnyXek69H6itRFY4czblXcWpZAkoIbNMi9uQtKt0cCgYEA1Bl22DcJsj9aXvBJmLyt2yJUjZdWhUwMXGWfEcGM1teJQfD+d/mcCcFKMhVI7ZVTvNFPZNDuU8H9IovYxps+NBTtzWrhpALHm0cdn1DY7sRIrTbMLn9S89qb7hRxV6FD2auV32I8RAWqrvRLY99A7kFYUEed8436tK4VQyr+t8sCgYEAsk9nP6GLRYBEiU1YiBkZ65KzbC10gBF/AsKHUzeqYHLArVXmWiwn2K75IYZIWnhJM/rg1KAoxlHE+H3IxyO5JcOtVDiorSinIZHVhes+ACeO15vsSVoQF2dxzEmEnBi+NziGhj0yThA4ua2CQodXpIThR8qmjXr0C1ofcDgcElUCgYEAtO1X7M7eTZgvXec50Lm60MBzQilD3AdoT/U8ASiLHMXVx1NtryhVTBj/UsPHZyvHt70RLd3wP7CuX6bN73WEVWc5B87R1lessC+0/C86Lktv95pUCKICQBROiYQUv3zIZUkyWtDwudHfrMil+vb564QActL00Ute/nu1lYt6p4sCgYEArfrdz9R4sgsFxoMsaKd9ya7m/Rz+pPWhWOB27PMr7iSKpo6SL7iwM+hUl8M68h7LzbET7C2CYkUtwiSxZDWUH6u5bmyKGXiY8OEyatyvJtWjFZm/bdUtQi5rtd9/+DcBBKMyMi8x/yWSAxlWjvEbzIVvn38aX6xcLLlVceep5zw='
    },
    # 邮箱配置
    "EMAIL_BACKEND_CONF": {
        "EMAIL_HOST": 'smtp.qq.com',
        "EMAIL_PORT": 465,
        "EMAIL_HOST_USER": '2539909370@qq.com',
        "EMAIL_HOST_PASSWORD": 'fhrygoqlndmxebjf',
        "EMAIL_USE_SSL": True,
        "DEFAULT_FORM_EMAIL": '2539909370@qq.com'
    }
}