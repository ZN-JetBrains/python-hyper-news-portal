from django.urls import path
from django.views.generic.base import RedirectView

from .views import ArticleView
from .views import CreateArticleView
from .views import IndexView
from .views import NewsView

app_name = "news"
urlpatterns = [
    path("", RedirectView.as_view(url="/news/")),
    # path("", IndexView.as_view(), name="index"),
    path("news/", NewsView.as_view(), name="news"),
    path("news/<int:article_id>/", ArticleView.as_view(), name="view_article"),
    path("news/create/", CreateArticleView.as_view(), name="create_article"),
]
