from django.test import TestCase
from django.shortcuts import get_list_or_404

# Create your tests here.
from .models import BaykeArticleCategory, BaykeArticleContent


class BaykeArticleCategoryTestCase(TestCase):

    def setUp(self):
        # 在每个测试方法之前运行
        self.category1 = BaykeArticleCategory.objects.create(
            name="Category 1",
            desc="This is the first category",
            keywords="Key words for category 1",
            parent=None,
            status=True,
            sort=1,
        )
        self.category2 = BaykeArticleCategory.objects.create(
            name="Category 2",
            desc="This is the second category",
            keywords="Key words for category 2",
            parent=self.category1,
            status=True,
            sort=2,
        )

    def test_category_creation(self):
        """测试分类的创建"""
        category = BaykeArticleCategory.objects.get(name="Category 1")
        self.assertEqual(category.name, "Category 1")
        self.assertEqual(category.desc, "This is the first category")
        self.assertEqual(category.keywords, "Key words for category 1")
        self.assertEqual(category.parent, None)
        self.assertEqual(category.status, True)
        self.assertEqual(category.sort, 1)

    def test_category_parent(self):
        """测试分类的父类"""
        category = BaykeArticleCategory.objects.get(name="Category 2")
        self.assertEqual(category.parent.name, "Category 1")

    def test_category_str(self):
        """测试分类的字符串表示"""
        category = BaykeArticleCategory.objects.get(name="Category 1")
        self.assertEqual(str(category), category.name)


class BaykeArticleContentTest(TestCase):

    def setUp(self):
        # 在每个测试方法之前运行
        self.article_category = BaykeArticleCategory.objects.create(
            name = '测试分类'
        )
        self.draft_content = BaykeArticleContent.objects.create(
            title='草稿标题',
            desc='草稿描述',
            keywords='草稿关键词',
            category=self.article_category, 
            content='草稿内容',
            status=0  # 设置为草稿状态
        )

        self.publish_content = BaykeArticleContent.objects.create(
            title='发布标题',
            desc='发布描述',
            keywords='发布关键词',
            category=self.article_category,
            content='发布内容',
            status=1  # 设置为发布状态
        )

    def test_model_instance(self):
        """测试是否正确创建了 BaykeArticleContent 实例"""
        self.assertTrue(self.draft_content.title == '草稿标题')
        self.assertTrue(self.publish_content.title == '发布标题')

    def test_model_str(self):
        """测试 str() 方法是否返回正确的字符串表示形式"""
        self.assertTrue(str(self.draft_content) == '草稿标题')
        self.assertTrue(str(self.publish_content) == '发布标题')

    def test_model_get_status_display(self):
        """测试 get_status_display() 方法返回的状态显示文本是否正确"""
        self.assertTrue(self.draft_content.get_status_display() == '草稿')
        self.assertTrue(self.publish_content.get_status_display() == '发布')

    def test_model_save_and_reload(self):
        """测试 save() 方法是否正确保存数据，并使用 get() 方法重新加载数据"""
        self.draft_content.title = '更新后的草稿标题'
        self.draft_content.save()
        updated_content = BaykeArticleContent.objects.get(id=self.draft_content.id)
        self.assertTrue(updated_content.title == '更新后的草稿标题')