from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, Http404
from django.views.generic import TemplateView, ListView, DetailView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from core.models import Question, Tag, Answer
import math

def paginate(objects_list, request, per_page=10):
    """Функция пагинации"""
    paginator = Paginator(objects_list, per_page)
    page = request.GET.get('page', 1)
    
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    return page_obj

class IndexView(ListView):
    http_method_names = ['get']
    template_name = 'core/index.html'
    context_object_name = 'new_questions'
    paginate_by = 4
    
    def get_queryset(self):
        return Question.objects.new_questions()

class HotQuestionsView(ListView):
    http_method_names = ['get']
    template_name = 'core/hot.html'
    context_object_name = 'hot_questions'
    paginate_by = 4
    
    def get_queryset(self):
        return Question.objects.hot_questions()

class TagQuestionsView(ListView):
    http_method_names = ['get']
    template_name = 'core/tag.html'
    context_object_name = 'tag_questions'
    paginate_by = 4
    
    def get_queryset(self):
        tag_name = self.kwargs.get('tag')
        return Question.objects.by_tag(tag_name)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag_name'] = self.kwargs.get('tag')
        return context

class QuestionDetailView(DetailView):
    http_method_names = ['get']
    template_name = 'core/question.html'
    context_object_name = 'question'
    pk_url_kwarg = 'question_id'
    
    def get_object(self):
        question_id = self.kwargs.get('question_id')
        return get_object_or_404(Question, id=question_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = self.get_object()
        context['answers'] = question.answers.all().order_by('-rating', '-created_at')
        return context

class LoginView(TemplateView):
    http_method_names = ['get']
    template_name = 'core/login.html'

class SignupView(TemplateView):
    http_method_names = ['get']
    template_name = 'core/signup.html'

class AskView(TemplateView):
    http_method_names = ['get']
    template_name = 'core/ask.html'

class SettingsView(TemplateView):
    http_method_names = ['get']
    template_name = 'core/settings.html'