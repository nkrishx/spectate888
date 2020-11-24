from django.contrib import admin
from .models import Market,Match,Selection,Sport
# Register your models here.

admin.site.register(Market)
admin.site.register(Match)
admin.site.register(Selection)
admin.site.register(Sport)
