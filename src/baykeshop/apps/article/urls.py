from django.urls import path
from . import views

app_name = "baykearticle"

urlpatterns = [
    path('', views.BaykeArticleContentListView.as_view(), name='article-list'),
    path('category/<int:pk>/', views.BaykeArticleCategoryDetailView.as_view(), name='category-detail'),
    path('content/<int:pk>/', views.BaykeArticleContentDetailView.as_view(), name='content-detail'),
    path('archive/<int:year>/<int:month>/', views.BaykeArticleContentMonthArchiveView.as_view(), name='archive-list'),
    path('tags/<int:pk>/', views.BaykeArticleTagsToArticleListView.as_view(), name='tags-list'),
]