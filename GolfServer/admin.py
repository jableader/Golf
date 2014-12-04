from django.contrib import admin
import models

# Register your models here.
admin.site.register(models.Profile)
admin.site.register(models.Question, models.QuestionAdmin)
admin.site.register(models.Submission)
admin.site.register(models.Sponsor)