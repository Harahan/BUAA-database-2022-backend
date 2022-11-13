from django.contrib import admin

# Register your models here.
from .models import User, Follow


admin.site.site_header = 'TKSP管理后台'  # 设置header
admin.site.site_title = 'TKSP管理后台'   # 设置title
admin.site.index_title = 'TKSP管理后台'


@admin.register(User)
@admin.register(Follow)
class UserAdmin(admin.ModelAdmin):
	pass
