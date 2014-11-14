from django.contrib import admin
import models

# Register your models here.
admin.site.register(models.UserProfile)
admin.site.register(models.Question)
admin.site.register(models.Submission)