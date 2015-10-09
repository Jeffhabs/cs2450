"""project1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.decorators import login_required
from accounts.views import logout_page, RegisterView
from polls.views import AuthorQuestionList, ChoiceCreateView, ChoiceVoteView, MyQuestionList, \
    QuestionCloseView, QuestionCreateView, QuestionDetailView, QuestionList

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', QuestionList.as_view(), name="home"),
    url(r'^accounts/logout/', logout_page, name="logout"),
    url(r'^accounts/register/', RegisterView.as_view(), name="registration_register"),
    url(r'^accounts/', include('registration.backends.simple.urls', namespace="accounts")),
    url(r'^questions/add/$', QuestionCreateView.as_view(), name="question-create"),
    url(r'^questions/my/$', login_required(MyQuestionList.as_view()), name="my-questions"),
    url(r'^questions/author/(?P<username>\w+)/$', AuthorQuestionList.as_view(), name="author-questions"),
    url(r'^questions/(?P<pk>\d+)/$', QuestionDetailView.as_view(), name="question-detail"),
    url(r'^questions/(?P<uuid>[-\w]+)/$', QuestionDetailView.as_view(), name="question-private"),
    url(r'^questions/(?P<pk>\d+)/close/$', QuestionCloseView.as_view(), name="question-close"),
    url(r'^questions/(?P<pk>\d+)/choice/add/$', ChoiceCreateView.as_view(), name="choice-create"),
    url(r'^choice/(?P<pk>\d+)/vote/(?P<vote>[-\w]+)/$', ChoiceVoteView.as_view(), name="choice-vote"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
