from datetime import datetime
import json


from django.conf import settings
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpRequest
from django.shortcuts import render
from django.views import View


def load_news() -> list[dict]:
    with open(settings.NEWS_JSON_PATH, "r") as file_in:
        articles = json.load(file_in)
    return articles


def save_article(article: dict[str, str]) -> None:
    articles = load_news()
    articles.append(article)

    with open(settings.NEWS_JSON_PATH, "w") as file_out:
        json.dump(articles, file_out)


class IndexView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return HttpResponse("Coming soon")


class NewsView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        all_unique_dates = set()
        processed_news = []
        for article in load_news():
            processed_article = article
            date = processed_article["created"].split(" ")[0]
            all_unique_dates.add(date)
            processed_article["created"] = date
            processed_news.append(processed_article)

        all_unique_dates = list(all_unique_dates)
        all_unique_dates.sort(reverse=True)

        sorted_news: dict[str, list[dict]] = {date: [] for date in all_unique_dates}
        for article in processed_news:
            date = article["created"]
            sorted_news[date].append(article)

        # if searching
        query = request.GET.get("q")
        if query:
            searched_news: dict[str, list[dict]] = {date: [] for date in all_unique_dates}
            for date, articles in sorted_news.items():
                for article in articles:
                    if query in article["title"]:
                        searched_news[date].append(article)
            return render(request, "news/news.html", {"news": searched_news})

        return render(request, "news/news.html", {"news": sorted_news})


class ArticleView(View):
    template_name = "news/article.html"

    def get(self, request: HttpRequest, article_id: int, *args, **kwargs) -> HttpResponse:
        for article in load_news():
            if article.get("link") == article_id:
                return render(request, "news/article.html", {"article": article})
        raise Http404


class CreateArticleView(View):
    link = 1000

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return render(request, "news/create.html")

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        title = request.POST.get("title")
        text = request.POST.get("text")

        if title and text:
            now = datetime.now()
            created = now.strftime("%Y-%m-%d %H:%M:%S")
            article = {
                "link": CreateArticleView.link,
                "created": created,
                "title": title,
                "text": text
            }
            save_article(article)
            CreateArticleView.link += 1

        return HttpResponseRedirect("/news/")
