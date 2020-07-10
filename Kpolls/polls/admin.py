from django.contrib import admin
from .models import Prompt, Choice
# Register your models here.

class PromptAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('prompt_text',)}

admin.site.register(Prompt, PromptAdmin)
admin.site.register(Choice)
