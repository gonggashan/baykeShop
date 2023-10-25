from django.conf import settings

settings.DEBUG = False

settings.INSTALLED_APPS += [
    'baykeshop.common.AdminConfig',
    'baykeshop.apps.user',
    'baykeshop.apps.article',
    'baykeshop.apps.system',
    'baykeshop.apps.shop',
    'baykeshop.apps.stats',
    'rest_framework',
    'captcha',
    'tinymce',
]

STATIC_ROOT = settings.BASE_DIR / "static"

MEDIA_URL = 'media/'
MEDIA_ROOT = settings.BASE_DIR / 'media'

TINYMCE_CONFIG = {
    'menubar': True,
    'relative_urls': False,
    'toolbar_sticky': False,
    'plugins_exclude': 'upgrade'  # 禁用升级插件
}

SECURE_CROSS_ORIGIN_OPENER_POLICY = None