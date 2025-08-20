from django.contrib import admin

from base_data.models import Job, JobCategory, City, Province

admin.site.register(Job)
admin.site.register(JobCategory)
admin.site.register(City)
admin.site.register(Province)
