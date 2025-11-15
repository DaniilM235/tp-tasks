from django.shortcuts import render
from django.http import JsonResponse, Http404
from django.views.generic import TemplateView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
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

class IndexView(TemplateView):
    http_method_names = ['get']
    template_name = 'core/index.html'
    COUNT_FAKE_QUESTIONS = 30
    QUESTIONS_PER_PAGE = 4

    def get_fake_questions(self):
        return [{
            'id': i,
            'question_text': f"Fake question #{i}",
            'question_detail_text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'
        } for i in range(self.COUNT_FAKE_QUESTIONS)]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questions = self.get_fake_questions()
        page_obj = paginate(questions, self.request, self.QUESTIONS_PER_PAGE)
        
        context['page_obj'] = page_obj
        context['new_questions'] = page_obj.object_list
        return context

class HotQuestionsView(TemplateView):
    http_method_names = ['get']
    template_name = 'core/hot.html'
    COUNT_FAKE_QUESTIONS = 25
    QUESTIONS_PER_PAGE = 4

    def get_fake_hot_questions(self):
        return [{
            'id': i,
            'question_text': f"Hot question #{i}",
            'question_detail_text': 'This is a popular question with many answers and votes.',
            'rating': 100 - i
        } for i in range(self.COUNT_FAKE_QUESTIONS)]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questions = self.get_fake_hot_questions()
        page_obj = paginate(questions, self.request, self.QUESTIONS_PER_PAGE)
        
        context['page_obj'] = page_obj
        context['hot_questions'] = page_obj.object_list
        return context

class TagQuestionsView(TemplateView):
    http_method_names = ['get']
    template_name = 'core/tag.html'
    QUESTIONS_PER_PAGE = 4

    def get_fake_tag_questions(self, tag):
        return [{
            'id': i,
            'question_text': f"Question about {tag} #{i}",
            'question_detail_text': f'This question is related to {tag} tag.',
        } for i in range(15)]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = self.kwargs.get('tag', '')
        questions = self.get_fake_tag_questions(tag)
        page_obj = paginate(questions, self.request, self.QUESTIONS_PER_PAGE)
        
        context['page_obj'] = page_obj
        context['tag_questions'] = page_obj.object_list
        context['tag_name'] = tag
        return context

class QuestionDetailView(TemplateView):
    http_method_names = ['get']
    template_name = 'core/question.html'

    def get_fake_question(self, question_id):
        return {
            'id': question_id,
            'question_text': f"How to build a moon park? (Question #{question_id})",
            'question_detail_text': 'Lorem ipsum — dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat.',
            'tags': ['black-jack', 'bender'],
            'rating': 5
        }

    def get_fake_answers(self, question_id):
        return [
            {
                'id': 1,
                'text': 'First of all I would like to thank you for the invitation to participate in such a ... Russia is the huge territory which in many respects needs to be render habitable.',
                'rating': 15,
                'is_correct': True
            },
            {
                'id': 2,
                'text': 'Another answer explaining how to build a moon park with detailed steps and considerations.',
                'rating': 8,
                'is_correct': False
            }
        ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question_id = self.kwargs.get('question_id')
        
        context['question'] = self.get_fake_question(question_id)
        context['answers'] = self.get_fake_answers(question_id)
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