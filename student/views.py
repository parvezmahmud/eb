from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from .forms import SignUpForm, StudentInfoForm
from functools import wraps
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from dashboard.models import BUNITSCORESHEET, CUNITSCORESHEET,EXAM_BATCH_CARDS_BUNIT, EXAM_BATCH_CARDS_CUNIT
from .models import STUDENTINFO


def user_field_required(field_name, redirect_url='/not-authorized/'):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Assuming Student is linked to the User model via OneToOneField
            user_info = getattr(request.user, 'studentinfo', None)
            if not request.user.is_authenticated or not user_info or not getattr(user_info, field_name, False):
                return redirect(redirect_url)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

# Create your views here.
def students_home(request):
    if request.user.is_superuser:
        return redirect('dashboard-home')
    return render(request, 'student/home.html')

def unauthorized(request):
    return render(request, 'student/unauthorized.html')


def signup_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        posted_form = SignUpForm(request.POST)
        if request.POST['password'] == request.POST['confirm_password']:
            if posted_form.is_valid():
                try:
                    user = User.objects.create_user(request.POST['email'], password=request.POST['password'])
                    login(request, user)
                    return redirect('user-info')
                except:
                    context = {
                    "err": "Something went wrong, try again",
                    "form": form,
                    }
                    return render(request, 'student/signup.html', context)
            else:
                context = {
                    "err": "Invalid Form",
                    "form": form,
                }
                return render(request, 'student/signup.html', context)
        else:
            context = {
                "error": "Passwords do not match",
                "form": form,
            }
            return render(request, 'student/signup.html', context)
    else:
        context = {
            "form": form
        }
        return render(request, 'student/signup.html', context)
    
def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            if STUDENTINFO.objects.filter(user=user):
                return redirect('profile')
            else:
                return redirect('user-info')
        else:
            context = {
                "wpa": "Wrong E-mail and/or Password", #wrong email/pass
            }
            return render(request, 'student/login.html', context)
    else:
        return render(request, 'student/login.html')


def logout_user(request):
    logout(request)
    return redirect('students-home')

@login_required(login_url='/login')
def student_info(request):
    form = StudentInfoForm()
    if request.method == 'POST':
        info_form = StudentInfoForm(request.POST)
        if info_form.is_valid():
            STUDENTINFO.objects.create(
                name=info_form.cleaned_data['name'],
                college = info_form.cleaned_data['college'],
                phone=info_form.cleaned_data['phone'],
                bkash_number=info_form.cleaned_data['bkash_number'],
                user = request.user,
                is_approved = False,
                cancelled = False,
            )
            return redirect('students-home')
        else:
            context = {
                "err": "Invalid Form",
                'form': form
            }
            return render(request, 'student/student-info.html', context)
    return render(request, 'student/student-info.html', {'form': form})


@login_required(login_url='/login')
@user_field_required('is_approved')
def student_profile(request):
    user = get_object_or_404(STUDENTINFO, user=request.user)
    try:
        bunit_exams = get_list_or_404(BUNITSCORESHEET, user=request.user)
    except:
        bunit_exams = []
    try:
        cunit_exams = get_list_or_404(CUNITSCORESHEET, user=request.user)
    except:
        cunit_exams = []
    context = {
        'user': user,
        'exams': bunit_exams + cunit_exams
    }
    return render(request, 'student/profile.html', context)

def student_bunit(request):
    data = EXAM_BATCH_CARDS_BUNIT.objects.all()
    context = {
        'cards': data
    }
    return render(request, 'student/unit.html', context)

def student_cunit(request):
    data = EXAM_BATCH_CARDS_CUNIT.objects.all()
    context = {
        'cards': data
    }
    return render(request, 'student/unit.html', context)


def leaderboard_bunit(request):
    if request.method == "GET":
        # Get all users who have UserScore entries
        users_with_scores = User.objects.filter(bunitscoresheet__isnull=False).distinct()

        leaderboard_data = []

        for user in users_with_scores:
            user_scores = BUNITSCORESHEET.objects.filter(user=user)
            total_score = sum(score.score for score in user_scores)
            user_info = STUDENTINFO.objects.get(user=user)
            leaderboard_data.append({
                'user': user,
                'score': total_score,
                'info': user_info,
            })

        # Sort the leaderboard data by total_score in descending order
        leaderboard_data.sort(key=lambda x: x['score'], reverse=True)

        context = {
            "leaderboard_data": leaderboard_data
        }
        return render(request, 'dashboard/question/leader-board.html', context)
    
def leaderboard_cunit(request):
    if request.method == "GET":
        # Get all users who have UserScore entries
        users_with_scores = User.objects.filter(cunitscoresheet__isnull=False).distinct()

        leaderboard_data = []

        for user in users_with_scores:
            user_scores = CUNITSCORESHEET.objects.filter(user=user)
            total_score = sum(score.score for score in user_scores)
            user_info = STUDENTINFO.objects.get(user=user)
            leaderboard_data.append({
                'user': user,
                'score': total_score,
                'info': user_info,
            })

        # Sort the leaderboard data by total_score in descending order
        leaderboard_data.sort(key=lambda x: x['score'], reverse=True)

        context = {
            "leaderboard_data": leaderboard_data
        }
        return render(request, 'dashboard/question/leader-board.html', context)