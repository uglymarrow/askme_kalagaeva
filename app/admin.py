from django.contrib import admin

from app.models import Profile, Tag, AnsLike, QuestLike, Question, Answer

# Register your models here.

admin.site.register(Profile)
admin.site.register(Tag)
admin.site.register(AnsLike)
admin.site.register(QuestLike)
admin.site.register(Question)
admin.site.register(Answer)