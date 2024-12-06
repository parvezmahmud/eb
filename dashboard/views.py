from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from dashboard.models import EXAM_BATCH_BUNIT, EXAM_BATCH_CARDS_BUNIT, EXAM_BATCH_CUNIT, EXAM_BATCH_CARDS_CUNIT
from .forms import CARD_FORM, CREATE_TEST, QuestionForm
from django.forms import formset_factory, modelformset_factory



# @user_passes_test(lambda u: u.is_superuser)
def home(request):
    if request.user.is_superuser:
        return redirect('dashboard-home')
    else:
        return redirect('students-home')
def dashboard_home(request):
    unit = ['B-UNIT', 'C-UNIT']
    redirect_links = ['b-unit-home', 'c-unit-home']
    context = {
        'units': list(zip(unit, redirect_links))
    }
    return render(request, 'dashboard/dashboard_home.html', context)

def bunit(request):
    cards = EXAM_BATCH_CARDS_BUNIT.objects.all().order_by('-created')
    exams = EXAM_BATCH_BUNIT.objects.all().order_by('-created')
    create_card = 'card-bunit'
    create_question = 'create-exam-bunit'
    edit_question = 'edit-test-bunit'
    context = {
        'exams': exams,
        'cards': cards,
        'create_card': create_card,
        'create_question': create_question,
        'topic': 'B-UNIT',
        'edit_test': edit_question
    }
    return render(request, 'dashboard/unit.html', context)

def cunit(request):
    cards = EXAM_BATCH_CARDS_CUNIT.objects.all().order_by('-created')
    exams = EXAM_BATCH_CUNIT.objects.all().order_by('-created')
    create_card = 'card-cunit'
    create_question = 'create-exam-cunit'
    edit_question = 'edit-test-cunit'
    context = {
        'exams': exams,
        'cards': cards,
        'create_card': create_card,
        'create_question': create_question,
        'topic': 'C-UNIT',
        'edit_test': edit_question
    }
    return render(request, 'dashboard/unit.html', context)

def create_exam_bunit(request):
    if request.method == 'POST':
        select_form = CREATE_TEST(request.POST)
        try:
            if select_form.is_valid():
                title = select_form.cleaned_data['title']
                number_of_questions = select_form.cleaned_data['number_of_questions']
                marks = select_form.cleaned_data['marks']
                time = select_form.cleaned_data['time']
                request.session['title'] = title
                request.session['number_of_questions'] = number_of_questions
                request.session['marks'] = marks
                request.session['time'] = time
                return redirect('create-question-bunit')
            else:
                select_form = CREATE_TEST()
                context = {
                    "invalid_data": "Data is not valid",
                    'form': select_form
                }
                return render(request, 'dashboard/question/create-exam.html', context)
        except:
            select_form = CREATE_TEST()
    else:
        select_form = CREATE_TEST()
        return render(request, 'dashboard/question/create-exam.html', {'form': select_form})

#Create Question for B UNIT    
def create_questions_bunit(request):
    # Retrieve session data with fallback values
    title = str(request.session.get('title', ''))
    number_of_questions = request.session.get('number_of_questions', 0)
    marks = request.session.get('marks', 0)
    time = request.session.get('time', 0)

    if not all([title, number_of_questions, marks, time]):
        # Redirect if session variables are missing
        return redirect('create-exam-bunit')

    # Convert to appropriate types and validate
    try:
        number_of_questions = int(number_of_questions)
        marks = int(marks)
        time = int(time)
    except (ValueError, TypeError):
        return redirect('b-unit-home')  # Redirect to ensure data is set properly

    # Formset initialization
    QuestionFormSet = formset_factory(QuestionForm, extra=number_of_questions)
    if request.method == 'POST':
        formset = QuestionFormSet(request.POST)
        if formset.is_valid():
            exam = EXAM_BATCH_BUNIT.objects.create(
                title=title,
                number_of_questions=number_of_questions,
                marks=marks,
                time=time,
            )
            for idx, form in enumerate(formset):
                question = form.save(commit=False)
                question.order = idx + 1
                question.save()
                exam.questions.add(question)
            return redirect('b-unit-home')
        else:
            return redirect('b-unit-home')
    else:
        formset = QuestionFormSet()
    
    context = {
        'title': title,
        'num_of_ques': number_of_questions,
        'marks': marks,
        'time': time,
        'formset': formset,
    }
    return render(request, 'dashboard/question/create-question.html', context)


#Create Exam For C UNIT
def create_exam_cunit(request):
    if request.method == 'POST':
        select_form = CREATE_TEST(request.POST)
        try:
            if select_form.is_valid():
                title = select_form.cleaned_data['title']
                number_of_questions = select_form.cleaned_data['number_of_questions']
                marks = select_form.cleaned_data['marks']
                time = select_form.cleaned_data['time']
                request.session['title'] = title
                request.session['number_of_questions'] = number_of_questions
                request.session['marks'] = marks
                request.session['time'] = time
                return redirect('create-question-cunit')
            else:
                select_form = CREATE_TEST()
                context = {
                    "invalid_data": "Data is not valid",
                    'form': select_form
                }
                return render(request, 'dashboard/question/create-exam.html', context)
        except:
            select_form = CREATE_TEST()
    else:
        select_form = CREATE_TEST()
        return render(request, 'dashboard/question/create-exam.html', {'form': select_form})


#Create Exam For C UNIT
def create_questions_cunit(request):
    # Retrieve session data with fallback values
    title = str(request.session.get('title', ''))
    number_of_questions = request.session.get('number_of_questions', 0)
    marks = request.session.get('marks', 0)
    time = request.session.get('time', 0)

    if not all([title, number_of_questions, marks, time]):
        # Redirect if session variables are missing
        return redirect('create-exam-cunit')

    # Convert to appropriate types and validate
    try:
        number_of_questions = int(number_of_questions)
        marks = int(marks)
        time = int(time)
    except (ValueError, TypeError):
        return redirect('c-unit-home')  # Redirect to ensure data is set properly

    # Formset initialization
    QuestionFormSet = formset_factory(QuestionForm, extra=number_of_questions)
    if request.method == 'POST':
        formset = QuestionFormSet(request.POST)
        if formset.is_valid():
            exam = EXAM_BATCH_CUNIT.objects.create(
                title=title,
                number_of_questions=number_of_questions,
                marks=marks,
                time=time,
            )
            for idx, form in enumerate(formset):
                question = form.save(commit=False)
                question.order = idx + 1
                question.save()
                exam.questions.add(question)
            return redirect('c-unit-home')
        else:
            return redirect('c-unit-home')
    else:
        formset = QuestionFormSet()
    
    context = {
        'title': title,
        'num_of_ques': number_of_questions,
        'marks': marks,
        'time': time,
        'formset': formset,
    }
    return render(request, 'dashboard/question/create-question.html', context)