from django.contrib import admin
from .models import Userdetail,Usergroupdetail

# Register your models here.


admin.site.register(Userdetail)
admin.site.register(Usergroupdetail)
admin.site.register(Course)
admin.site.register(CourseAccess)