from django.contrib import admin
from .models import EXAM_BATCH_BUNIT, EXAM_BATCH_CUNIT, EXAM_BATCH_CARDS_CUNIT, EXAM_BATCH_CARDS_BUNIT, Question, BUNITSCORESHEET, CUNITSCORESHEET

mymodels = [EXAM_BATCH_BUNIT, EXAM_BATCH_CARDS_BUNIT, EXAM_BATCH_CUNIT, EXAM_BATCH_CARDS_CUNIT, Question, BUNITSCORESHEET, CUNITSCORESHEET]
admin.site.register(mymodels)
