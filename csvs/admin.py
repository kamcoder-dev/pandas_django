from django.contrib import admin
from csvs.models import Csv
# Register your models here.
from import_export.admin import ImportExportModelAdmin


@admin.register(Csv)
class View(ImportExportModelAdmin):
    pass
