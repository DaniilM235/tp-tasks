from django.urls import path
from django.contrib import admin
from core.views import (IndexView, HotQuestionsView, TagQuestionsView, 
                       QuestionDetailView, LoginView, SignupView, 
                       AskView, SettingsView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('hot/', HotQuestionsView.as_view(), name='hot'),
    path('tag/<str:tag>/', TagQuestionsView.as_view(), name='tag'),
    path('question/<int:question_id>/', QuestionDetailView.as_view(), name='question'),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('ask/', AskView.as_view(), name='ask'),
    path('settings/', SettingsView.as_view(), name='settings'),
]