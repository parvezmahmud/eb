from django.shortcuts import render

# Create your views here.
def students_home(request):
    return render(request, 'student/home.html')