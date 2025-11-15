from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from core.models import Profile, Tag, Question, Answer, QuestionLike, AnswerLike

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)

class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'rating']
    list_filter = ['created_at', 'tags']
    search_fields = ['title', 'text']
    filter_horizontal = ['tags']
    readonly_fields = ['created_at']

class AnswerAdmin(admin.ModelAdmin):
    list_display = ['truncated_text', 'question', 'author', 'created_at', 'rating', 'is_correct']
    list_filter = ['created_at', 'is_correct']
    search_fields = ['text']
    readonly_fields = ['created_at']
    
    def truncated_text(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    truncated_text.short_description = 'Text'

class QuestionLikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'question', 'value']
    list_filter = ['value']
    search_fields = ['user__username', 'question__title']

class AnswerLikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'answer', 'value']
    list_filter = ['value']
    search_fields = ['user__username']

# Перерегистрируем UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Зарегистрируем остальные модели
admin.site.register(Tag, TagAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(QuestionLike, QuestionLikeAdmin)
admin.site.register(AnswerLike, AnswerLikeAdmin)