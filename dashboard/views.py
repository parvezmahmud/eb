from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from dashboard.models import EXAM_BATCH_BUNIT, EXAM_BATCH_CARDS_BUNIT,Question, EXAM_BATCH_CUNIT, EXAM_BATCH_CARDS_CUNIT, UserAnswer, BUNITSCORESHEET, CUNITSCORESHEET
from .forms import CARD_FORM, CREATE_TEST, QuestionForm, AnswerForm, EDIT_CARD_BUNIT, EDIT_CARD_CUNIT
from django.forms import formset_factory, modelformset_factory
import uuid
from django import forms
from django.db import transaction
from student.models import STUDENTINFO
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.core.cache import cache

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




def home(request):
    if request.user.is_superuser:
        return redirect('dashboard-home')
    else:
        return redirect('students-home')
def dashboard_home(request):
    unit = ['B-UNIT', 'C-UNIT', 'STUDENTS']
    redirect_links = ['b-unit-home', 'c-unit-home', 'dashboard-students-home']
    context = {
        'units': list(zip(unit, redirect_links))
    }
    return render(request, 'dashboard/dashboard_home.html', context)

@user_passes_test(lambda u: u.is_superuser, login_url='/not-authorized/')
def bunit(request):
    cards = EXAM_BATCH_CARDS_BUNIT.objects.all().order_by('-created')
    exams = EXAM_BATCH_BUNIT.objects.all().order_by('-created')
    create_card = 'create-card-bunit'
    create_question = 'create-exam-bunit'
    edit_question = 'edit-test-bunit'
    edit_card = 'edit-card-bunit'
    delete_card = 'delete-card-bunit'
    context = {
        'exams': exams,
        'cards': cards,
        'create_card': create_card,
        'create_question': create_question,
        'topic': 'B-UNIT',
        'edit_test': edit_question,
        'edit_card': edit_card,
        'dlt_card': delete_card,
    }
    return render(request, 'dashboard/unit.html', context)

@user_passes_test(lambda u: u.is_superuser, login_url='/not-authorized/')
def cunit(request):
    cards = EXAM_BATCH_CARDS_CUNIT.objects.all().order_by('-created')
    exams = EXAM_BATCH_CUNIT.objects.all().order_by('-created')
    create_card = 'create-card-cunit'
    create_question = 'create-exam-cunit'
    edit_question = 'edit-test-cunit'
    edit_card = 'edit-card-cunit'
    delete_card = 'delete-card-cunit'
    context = {
        'exams': exams,
        'cards': cards,
        'create_card': create_card,
        'create_question': create_question,
        'topic': 'C-UNIT',
        'edit_test': edit_question,
        'edit_card': edit_card,
        'dlt_card': delete_card,
    }
    return render(request, 'dashboard/unit.html', context)

@user_passes_test(lambda u: u.is_superuser, login_url='/not-authorized/')
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
@user_passes_test(lambda u: u.is_superuser, login_url='/not-authorized/')
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
@user_passes_test(lambda u: u.is_superuser, login_url='/not-authorized/')
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
@user_passes_test(lambda u: u.is_superuser, login_url='/not-authorized/')
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

@login_required(login_url='/login')
def ind_exam(request, id):
    try:
        data = get_object_or_404(EXAM_BATCH_BUNIT, id=id)
        context = {
            'exam': data
        }
        return render(request, 'dashboard/question/ind.html', context)
    except:
        data = get_object_or_404(EXAM_BATCH_CUNIT, id=id)
        context = {
            'exam': data
        }
        return render(request, 'dashboard/question/ind.html', context)
    

@login_required(login_url='/login')
@user_field_required('is_approved')
def take_exam(request, id):
    try:
        exam = get_object_or_404(EXAM_BATCH_BUNIT, id=id)
    except:
        exam = get_object_or_404(EXAM_BATCH_CUNIT, id=id)
    questions = exam.questions.all()
    AnswerFormSet = modelformset_factory(UserAnswer, form=AnswerForm, extra=len(questions))

    if request.method == 'POST':
        formset = AnswerFormSet(request.POST, queryset=UserAnswer.objects.none())
        if formset.is_valid():
            attempt_id = uuid.uuid4().hex
            request.session['attempt_id'] = attempt_id
            answers = []
            total_selected = 0
            for form, question in zip(formset.forms, questions):
                try:
                    form.cleaned_data['selected_option']
                    selected = form.cleaned_data['selected_option']
                    total_selected += 1
                except KeyError:
                    selected = "No choice was selected"
                user_answer = UserAnswer(
                        question=question,
                        selected_option=selected,
                    )
                answers.append(user_answer)
                request.session[f'{attempt_id}_{question.id}'] = selected
            request.session['total_selected'] = total_selected
        return redirect('exam-result', id=id)
    else:
        formset = AnswerFormSet(queryset=UserAnswer.objects.none())
        for form, question in zip(formset.forms, questions):
            form.fields['selected_option'].widget = forms.RadioSelect(
                choices=[
                    (question.option1, question.option1),
                    (question.option2, question.option2),
                    (question.option3, question.option3),
                    (question.option4, question.option4),
                ]
            )
            form.fields['selected_option'].label = question.question_text

    return render(request, 'dashboard/question/take-exam.html', {'exam': exam, 'formset': formset, 'exam_duration': exam.time })


@login_required(login_url='/login')
@user_field_required('is_approved')
def result(request, id):
        
        try:
            exam = get_object_or_404(EXAM_BATCH_BUNIT, id=id)
            user = request.user
            attempt_id = request.session.get('attempt_id')
            if not attempt_id:
                return redirect('take_exam', exam=id)
            user_answers = []
            questions = exam.questions.all()
            total_selected: int = request.session.get('total_selected')
            for question in questions:
                selected_option = request.session.get(f'{attempt_id}_{question.id}')
                if selected_option:
                    user_answer = UserAnswer(
                        question=question,
                        selected_option=selected_option
                    )
                    user_answers.append(user_answer)
                else:
                    pass
            score = sum(1 for answer in user_answers if answer.is_correct())
            wrong_ans = total_selected - score
            neg_score = wrong_ans * .25
            if score - neg_score > 0:
                final_score = score - neg_score
            else:
                final_score = 0
            if BUNITSCORESHEET.objects.filter(user=user, exam=exam).count() > 0:
                return render(request, 'dashboard/question/result.html', {'exam': exam, 'user_answers': user_answers, 'score': score, 'final_score': final_score, 'selected': total_selected, 'wrong': wrong_ans})
            else:
                BUNITSCORESHEET.objects.create(
                    user=user,
                    exam=exam,
                    score=final_score
                )
                return render(request, 'dashboard/question/result.html', {'exam': exam, 'user_answers': user_answers, 'score': score, 'final_score': final_score, 'selected': total_selected, 'wrong': wrong_ans})
        except:
            exam = get_object_or_404(EXAM_BATCH_CUNIT, id=id)
            user = request.user
            attempt_id = request.session.get('attempt_id')
            if not attempt_id:
                return redirect('take_exam', exam=id)
            user_answers = []
            questions = exam.questions.all()
            total_selected: int = request.session.get('total_selected')
            for question in questions:
                selected_option = request.session.get(f'{attempt_id}_{question.id}')
                if selected_option:
                    user_answer = UserAnswer(
                        question=question,
                        selected_option=selected_option
                    )
                    user_answers.append(user_answer)
                else:
                    pass
            score = sum(1 for answer in user_answers if answer.is_correct())
            wrong_ans = total_selected - score
            neg_score = wrong_ans * .25
            if score - neg_score > 0:
                final_score = score - neg_score
            else:
                final_score = 0
            if CUNITSCORESHEET.objects.filter(user=user, exam=exam).count() > 0:
                return render(request, 'dashboard/question/result.html', {'exam': exam, 'user_answers': user_answers, 'score': score, 'final_score': final_score, 'selected': total_selected, 'wrong': wrong_ans})
            else:
                CUNITSCORESHEET.objects.create(
                    user=user,
                    exam=exam,
                    score=final_score
                )
                return render(request, 'dashboard/question/result.html', {'exam': exam, 'user_answers': user_answers, 'score': score, 'final_score': final_score, 'selected': total_selected, 'wrong': wrong_ans})
        


@user_passes_test(lambda u: u.is_superuser, login_url='/not-authorized/')
def edit_test_and_questions(request, id):
    try:
        test = get_object_or_404(EXAM_BATCH_BUNIT, id=id)
    except:
        test = get_object_or_404(EXAM_BATCH_CUNIT, id=id)

    if request.method == 'POST':
        test_form = CREATE_TEST(request.POST)
    else:
        initial_data = {
            'title': test.title,
            'number_of_questions': test.number_of_questions,
            'marks': test.marks,
            'time': test.time,
        }
        test_form = CREATE_TEST(initial=initial_data)

    # Add the `order` field to manage the order of questions.
    QuestionFormSet = modelformset_factory(
        Question, 
        form=QuestionForm, 
        extra=0, 
        can_delete=True,
        fields=['question_text', 'option1', 'option1_is_correct', 
                'option2', 'option2_is_correct', 'option3', 
                'option3_is_correct', 'option4', 'option4_is_correct']
    )

    formset = QuestionFormSet(request.POST or None, queryset=test.questions.all())

    if request.method == 'POST':
        if test_form.is_valid() and formset.is_valid():
            with transaction.atomic():
                # Save test details
                test.title = test_form.cleaned_data['title']
                test.number_of_questions = test_form.cleaned_data['number_of_questions']
                test.marks = test_form.cleaned_data['marks']
                test.time = test_form.cleaned_data['time']
                test.save()

                # Collect valid instances and retain their original order
                instances = formset.save(commit=False)
                form_order_mapping = {form.instance.id: idx for idx, form in enumerate(formset.forms) if form.instance.id}

                # Save questions and assign the correct order
                for instance in instances:
                    instance.test = test  # Ensure the question is associated with the correct test
                    instance.order = form_order_mapping.get(instance.id, instance.order)  # Retain the submitted order
                    instance.save()

                # Handle deleted objects
                for obj in formset.deleted_objects:
                    obj.delete()

                # Redirect based on the unit
                if test.unit == 'B-UNIT':
                    return redirect('b-unit-home')
                else:
                    return redirect('c-unit-home')



    context = {
        'test_form': test_form,
        'formset': formset,
        'test': test,
        'num_of_ques': test.number_of_questions
    }

    return render(request, 'dashboard/question/edit-test.html', context)

@user_passes_test(lambda u: u.is_superuser, login_url='/not-authorized/')
def delete_question(request, id):
    if request.method == 'POST':
        try:
            obj = get_object_or_404(EXAM_BATCH_BUNIT, id=id)
            obj.delete()
            return redirect('b-unit-home')
        except:
            obj = get_object_or_404(EXAM_BATCH_CUNIT, id=id)
            obj.delete()
            return redirect('c-unit-home')
    else:
        return redirect('dashboard-home')
    
@user_passes_test(lambda u: u.is_superuser, login_url='/not-authorized/')
def students_home(request):
    choices = ['APPROVED', 'PENDING', 'ARCHIVE']
    redirect_links = ['students-approved', 'students-pending', 'students-archive']
    context = {
        'units': list(zip(choices, redirect_links))
    }
    return render(request, 'dashboard/dashboard_home.html', context)

@user_passes_test(lambda u: u.is_superuser, login_url='/not-authorized/')
def students_approved(request):
    data = STUDENTINFO.objects.filter(is_approved=True).filter(cancelled=False)
    context = {
        'students': data
    }
    return render(request, 'dashboard/student.html', context)  


@user_passes_test(lambda u: u.is_superuser, login_url='/not-authorized/')
def students_unapproved(request):
    data = STUDENTINFO.objects.filter(is_approved=False).filter(cancelled=False)
    context = {
        'students': data
    }
    return render(request, 'dashboard/student.html', context)

@user_passes_test(lambda u: u.is_superuser, login_url='/not-authorized/')
def students_cancelled(request):
    data = STUDENTINFO.objects.filter(is_approved=False).filter(cancelled=True)
    context = {
        'students': data
    }
    return render(request, 'dashboard/student.html', context)


@user_passes_test(lambda u: u.is_superuser, login_url='/not-authorized/')
def exam_batch_approve(request, id):
    try:
        student = get_object_or_404(STUDENTINFO, id=id)
        student.is_approved = True
        student.cancelled = False
        student.save()
        return redirect(request.META.get('HTTP_REFERER'))
    except:
        return redirect('students-pending')


@user_passes_test(lambda u: u.is_superuser, login_url='/not-authorized/')
def exam_batch_delete(request, id):
    try:
        student = get_object_or_404(STUDENTINFO, id=id)
        student.cancelled = True
        student.is_approved = False
        student.save()
        return redirect(request.META.get('HTTP_REFERER'))
    except:
        return redirect(request.META.get('HTTP_REFERER'))
    
@user_passes_test(lambda u: u.is_superuser, login_url='/not-authorized/')
def create_card_bunit(request):
    try:
        if request.method == 'POST':
            form = CARD_FORM(request.POST)
            if form.is_valid():
                EXAM_BATCH_CARDS_BUNIT.objects.create(
                    title=form.cleaned_data['title'],
                    take_exam=form.cleaned_data['take_exam'],
                    drive_link=form.cleaned_data['drive_link']
                )
                return redirect('b-unit-home')
            else:
                # Form is invalid; display errors
                
                return render(request, 'dashboard/question/create-exam.html', {'form': form})
        else:
            # Display empty form
            
            form = CARD_FORM()
            return render(request, 'dashboard/question/create-exam.html', {'form': form})
    except Exception as e:
        return render(request, 'dashboard/question/create-exam.html', {'form': form, 'error': str(e)})


@user_passes_test(lambda u: u.is_superuser, login_url='/not-authorized/')
def create_card_cunit(request):
    try:
        if request.method == 'POST':
            form = CARD_FORM(request.POST)
            if form.is_valid():
                EXAM_BATCH_CARDS_CUNIT.objects.create(
                    title=form.cleaned_data['title'],
                    take_exam=form.cleaned_data['take_exam'],
                    drive_link=form.cleaned_data['drive_link']
                )
                return redirect('c-unit-home')
            else:
                # Form is invalid; display errors
                
                return render(request, 'dashboard/question/create-exam.html', {'form': form})
        else:
            # Display empty form
            
            form = CARD_FORM()
            return render(request, 'dashboard/question/create-exam.html', {'form': form})
    except Exception as e:
        return render(request, 'dashboard/question/create-exam.html', {'form': form, 'error': str(e)})

@user_passes_test(lambda u: u.is_superuser, login_url='/not-authorized/')    
def edit_card_bunit(request, id):
    item = get_object_or_404(EXAM_BATCH_CARDS_BUNIT, id=id)
    if request.method == 'GET':
        context = {
            'item': item,
            'form': EDIT_CARD_BUNIT(instance=item)
        }
        return render(request, 'dashboard/question/edit-card.html', context)
    else:
        posted_item = EDIT_CARD_BUNIT(request.POST, instance=item)
        posted_item.save()
        return redirect('b-unit-home')
    

@user_passes_test(lambda u: u.is_superuser, login_url='/not-authorized/')
def edit_card_cunit(request, id):
    item = get_object_or_404(EXAM_BATCH_CARDS_CUNIT, id=id)
    if request.method == 'GET':
        context = {
            'item': item,
            'form': EDIT_CARD_CUNIT(instance=item)
        }
        return render(request, 'dashboard/question/edit-card.html', context)
    else:
        posted_item = EDIT_CARD_CUNIT(request.POST, instance=item)
        posted_item.save()
        return redirect('c-unit-home')


@user_passes_test(lambda u: u.is_superuser, login_url='/not-authorized/')  
def delete_card_bunit(request, id):
    try:
        item = get_object_or_404(EXAM_BATCH_CARDS_BUNIT, id=id)
        if request.method == 'POST':
            item.delete()
            return redirect('b-unit-home')
    except:
        return redirect('b-unit-home')
    
@user_passes_test(lambda u: u.is_superuser, login_url='/not-authorized/')  
def delete_card_cunit(request, id):
    try:
        item = get_object_or_404(EXAM_BATCH_CARDS_CUNIT, id=id)
        if request.method == 'POST':
            item.delete()
            return redirect('c-unit-home')
    except:
        return redirect('c-unit-home')
    

# def bunit_per_exam_leaderboard(request, id):
#     try:
#         test = get_object_or_404(EXAM_BATCH_BUNIT, id=id)
        
#         scores = BUNITSCORESHEET.objects.filter(exam=test).order_by('-score')
#         print('okay')
#         scoresheet = [
#             {'key':index, 'score':score}
#                 for index, score in enumerate(scores)
#         ]
#         cache.set('scoresheet', scoresheet, timeout=3600)
#         context = {
#             'leaderboard_data': scoresheet
#         }
#         return render(request, 'dashboard/question/leader-board.html',context)
#     except:
#         return redirect('students-home')


# from django.shortcuts import render

# def view_scores_with_student_info(request, exam_id):
#     # Fetch all score sheets for the given exam
#     scoresheets = BUNITSCORESHEET.objects.filter(exam_id=exam_id).select_related('user')

#     # Collect data along with student info
#     data = []
#     for scoresheet in scoresheets:
#         student_info = None
#         if scoresheet.user:
#             try:
#                 student_info = scoresheet.user.studentinfo  # Access STUDENTINFO via User
#             except STUDENTINFO.DoesNotExist:
#                 student_info = None

#         data.append({
#             'score': scoresheet.score,
#             'user': scoresheet.user,
#             'student_info': student_info,
#         })

#     return render(request, 'scores_with_student_info.html', {'data': data})

