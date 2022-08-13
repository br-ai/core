from django.contrib import admin
from .models  import Countries,  Cities
# Register your models here.

admin.site.register([Countries,  Cities])