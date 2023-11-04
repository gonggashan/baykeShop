from typing import Any, Dict
from django.db.models import Q
from django.views.generic import ListView, DetailView
from django.views.generic.detail import SingleObjectMixin
# Create your views here.
from .models import BaykeArticleContent, BaykeArticleCategory


class BaykeArticleContentListView(ListView):
    """列表页
    """
    model = BaykeArticleContent
    template_name = "article/list.html"
    paginate_by = 20
    paginate_orphans = 2
    context_object_name = "article_list"

    def get_queryset(self):
        queryset = super().get_queryset().exclude(status=0)
        return queryset
    
    def paginate_queryset(self, queryset, page_size):
        page_size = int(self.request.GET.get('per_page', self.paginate_by))
        return super().paginate_queryset(queryset, page_size)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = "全部文章"
        return context


class BaykeArticleCategoryDetailView(SingleObjectMixin, BaykeArticleContentListView):
    """分类列表页

    Args:
        SingleObjectMixin (_type_): _description_
        BaykeArticleContentListView (_type_): _description_
    """
    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=BaykeArticleCategory.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.object
        context['title'] = self.object.name
        return context

    def get_queryset(self):
        queryset = self.object.baykearticlecontent_set.filter(status=1)
        return queryset
    

class BaykeArticleContentDetailView(DetailView):
    """文章详情页

    Args:
        DetailView (_type_): _description_
    """
    model = BaykeArticleContent
    template_name = "article/detail.html"
    context_object_name = "article"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['article_next'] = self.get_object().next_article
        context['article_previous'] = self.get_object().previous_article
        context['title'] = self.get_object().title
        return context
    

class BaykeArticleContentArchivingListView(BaykeArticleContentListView):
    """ 文章归档 """
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = f"{self.kwargs['year']}年{self.kwargs['month']}月的文章归档"
        return context

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            Q(add_date__year=self.kwargs['year']) &
            Q(add_date__month=self.kwargs['month'])
        )
        return queryset
    

class BaykeArticleContentTagsListView(BaykeArticleContentListView):
    """ 文章标签分类 """
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = f"归属标签{self.kwargs['tag']}的文章"
        return context

    def get_queryset(self):
        queryset = super().get_queryset().filter(tags__name=self.kwargs['tag'])
        return queryset


