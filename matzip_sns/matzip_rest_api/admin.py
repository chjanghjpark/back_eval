from django.contrib import admin
from matzip_rest_api.models.models import Evaluate, Store, Userinfo, Comment

admin.site.register(Userinfo)
admin.site.register(Evaluate)
admin.site.register(Store)
admin.site.register(Comment)
