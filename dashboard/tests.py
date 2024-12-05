from django.test import TestCase, Client
from dashboard.models import EXAM_BATCH_BUNIT, Question, EXAM_BATCH_CUNIT, EXAM_BATCH_CARDS_BUNIT, EXAM_BATCH_CARDS_CUNIT
import uuid
from django.urls import reverse
from dashboard.forms import CREATE_TEST, QuestionForm
from django.forms import formset_factory
from unittest.mock import patch


print("Running Test for B UNIT test")
class EXAM_BATCH_BUNITTestCase(TestCase):
    def setUp(self):
        # Create Question objects with the required fields
        self.question1 = Question.objects.create(
            question_text="What is Django?",
            option1="A framework",
            option1_is_correct=True,
            option2="A database",
            option3="A language",
            option4="A text editor",
        )
        self.question2 = Question.objects.create(
            question_text="What is Python?",
            option1="A programming language",
            option1_is_correct=True,
            option2="A framework",
            option3="A tool",
            option4="A CMS",
        )

        # Create an EXAM_BATCH_BUNIT instance
        self.exam_batch = EXAM_BATCH_BUNIT.objects.create(
            title="Sample Exam Batch",
            number_of_questions=2,
            marks=100.0,
            time=120
        )

        # Associate questions with the exam batch
        self.exam_batch.questions.set([self.question1, self.question2])

    def test_exam_batch_creation(self):
        # Check that the EXAM_BATCH_BUNIT object is created
        self.assertIsInstance(self.exam_batch, EXAM_BATCH_BUNIT)

    def test_defaults(self):
        # Check default values
        self.assertEqual(self.exam_batch.unit, "B-UNIT")
        self.assertEqual(self.exam_batch.number_of_questions, 2)  # Overridden default
        self.assertEqual(self.exam_batch.marks, 100.0)
        self.assertEqual(self.exam_batch.time, 120)

    def test_id_is_uuid(self):
        # Check that `id` is a UUID
        self.assertIsInstance(self.exam_batch.id, uuid.UUID)

    def test_many_to_many_relationship(self):
        # Check questions associated with the EXAM_BATCH_BUNIT
        self.assertEqual(self.exam_batch.questions.count(), 2)
        self.assertIn(self.question1, self.exam_batch.questions.all())
        self.assertIn(self.question2, self.exam_batch.questions.all())

    def test_question_ordering(self):
        # Check that questions are ordered by the `order` field
        self.question1.order = 1
        self.question1.save()
        self.question2.order = 0
        self.question2.save()

        # Retrieve the questions in order
        ordered_questions = Question.objects.all()
        self.assertEqual(ordered_questions[0], self.question2)
        self.assertEqual(ordered_questions[1], self.question1)

    def test_str_representation(self):
        # Optionally, test the string representation if defined
        self.assertEqual(str(self.exam_batch), self.exam_batch.title)


print("Running Test for C UNIT test")
class EXAM_BATCH_CUNITTestCase(TestCase):
    def setUp(self):
        # Create Question objects with the required fields
        self.question1 = Question.objects.create(
            question_text="What is Django?",
            option1="A framework",
            option1_is_correct=True,
            option2="A database",
            option3="A language",
            option4="A text editor",
        )
        self.question2 = Question.objects.create(
            question_text="What is Python?",
            option1="A programming language",
            option1_is_correct=True,
            option2="A framework",
            option3="A tool",
            option4="A CMS",
        )

        # Create an EXAM_BATCH_BUNIT instance
        self.exam_batch = EXAM_BATCH_CUNIT.objects.create(
            title="Sample Exam - 002",
            number_of_questions=2,
            marks=100.0,
            time=120
        )

        # Associate questions with the exam batch
        self.exam_batch.questions.set([self.question1, self.question2])

    def test_exam_batch_creation(self):
        # Check that the EXAM_BATCH_BUNIT object is created
        self.assertIsInstance(self.exam_batch, EXAM_BATCH_CUNIT)

    def test_defaults(self):
        # Check default values
        self.assertEqual(self.exam_batch.unit, "C-UNIT")
        self.assertEqual(self.exam_batch.number_of_questions, 2)  # Overridden default
        self.assertEqual(self.exam_batch.marks, 100.0)
        self.assertEqual(self.exam_batch.time, 120)

    def test_id_is_uuid(self):
        # Check that `id` is a UUID
        self.assertIsInstance(self.exam_batch.id, uuid.UUID)

    def test_many_to_many_relationship(self):
        # Check questions associated with the EXAM_BATCH_BUNIT
        self.assertEqual(self.exam_batch.questions.count(), 2)
        self.assertIn(self.question1, self.exam_batch.questions.all())
        self.assertIn(self.question2, self.exam_batch.questions.all())

    def test_question_ordering(self):
        # Check that questions are ordered by the `order` field
        self.question1.order = 1
        self.question1.save()
        self.question2.order = 0
        self.question2.save()

        # Retrieve the questions in order
        ordered_questions = Question.objects.all()
        self.assertEqual(ordered_questions[0], self.question2)
        self.assertEqual(ordered_questions[1], self.question1)

    def test_str_representation(self):
        # Optionally, test the string representation if defined
        self.assertEqual(str(self.exam_batch), self.exam_batch.title)

print("Running Test for B UNIT Cards")
class EXAM_BATCH_BUNIT_CARDS_TEST(TestCase):
    def setUp(self):
        self.bunit_cards = EXAM_BATCH_CARDS_BUNIT.objects.create(
            title = "Sample Test B Unit Card",
            drive_link = "https://www.youtube.com/watch?v=jGB-16XbpmA",
            take_exam = "https://www.youtube.com/watch?v=jGB-16XbpmA"
        )
    def test_creation(self):
        self.assertIsInstance(self.bunit_cards, EXAM_BATCH_CARDS_BUNIT)
    
    def test_defaults(self):
        self.assertEqual(self.bunit_cards.title, "Sample Test B Unit Card")
        self.assertEqual(self.bunit_cards.unit, 'B-UNIT')
        self.assertEqual(self.bunit_cards.drive_link, "https://www.youtube.com/watch?v=jGB-16XbpmA")
        self.assertEqual(self.bunit_cards.take_exam, "https://www.youtube.com/watch?v=jGB-16XbpmA")
    def test_str(self):
        self.assertEqual(str(self.bunit_cards), self.bunit_cards.title)

    def test_uuid(self):
        self.assertIsInstance(self.bunit_cards.id, uuid.UUID)

print("Running Test Dashboard Home")
class DashboardHomeViewTest(TestCase):
    def setUp(self):
        # Set up the test client
        self.client = Client()
        self.url = reverse('dashboard-home')  # Replace 'dashboard-home' with the actual URL name of your view

    def test_dashboard_home_view_status_code(self):
        # Test if the view returns a 200 status code
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_dashboard_home_view_template(self):
        # Test if the correct template is used
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'dashboard/dashboard_home.html')

    def test_dashboard_home_view_context(self):
        # Test if the correct context is passed to the template
        response = self.client.get(self.url)
        self.assertIn('units', response.context)
        self.assertEqual(
            response.context['units'],
            [
                ('B-UNIT', 'b-unit-home'),
                ('C-UNIT', 'c-unit-home'),
                ('STUDENTS', 'students-home')
            ]
        )


print("Running Test for B UNIT")
class DashboardBUnitViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('b-unit-home')

        self.card1 = EXAM_BATCH_CARDS_BUNIT.objects.create(
            title="Card 01",
            drive_link = "https://www.youtube.com/watch?v=jGB-16XbpmA",
            take_exam = "https://www.youtube.com/watch?v=jGB-16XbpmA"
        )  # Add required fields
        self.card2 = EXAM_BATCH_CARDS_BUNIT.objects.create(
            title="Card 02",
            drive_link = "https://www.youtube.com/watch?v=jGB-16XbpmA",
            take_exam = "https://www.youtube.com/watch?v=jGB-16XbpmA"
        )
        self.exam1 = EXAM_BATCH_BUNIT.objects.create(
            title="Sample Exam - 002",
            number_of_questions=2,
            marks=100.0,
            time=120
        )
        self.exam2 = EXAM_BATCH_BUNIT.objects.create(
            title="Sample Exam - 004",
            number_of_questions=2,
            marks=100.0,
            time=120
        )

    def test_bunit_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_bunit_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'dashboard/unit.html')

    def test_bunit_view_context(self):
        response = self.client.get(self.url)
        self.assertIn('cards', response.context)
        self.assertEqual(list(response.context['cards']), [self.card2, self.card1])
        self.assertIn('exams', response.context)
        self.assertEqual(list(response.context['exams']), [self.exam2, self.exam1])
        self.assertEqual(response.context['create_card'], 'card-bunit')
        self.assertEqual(response.context['create_question'], 'create-question-bunit')
        self.assertEqual(response.context['edit_test'], 'edit-test-bunit')
        self.assertEqual(response.context['topic'], 'B-UNIT')


print("Running Test for C UNIT")
class DashboardCUnitViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('c-unit-home')

        self.card1 = EXAM_BATCH_CARDS_CUNIT.objects.create(
            title="Card 01",
            drive_link = "https://www.youtube.com/watch?v=jGB-16XbpmA",
            take_exam = "https://www.youtube.com/watch?v=jGB-16XbpmA"
        )  # Add required fields
        self.card2 = EXAM_BATCH_CARDS_CUNIT.objects.create(
            title="Card 02",
            drive_link = "https://www.youtube.com/watch?v=jGB-16XbpmA",
            take_exam = "https://www.youtube.com/watch?v=jGB-16XbpmA"
        )
        self.exam1 = EXAM_BATCH_CUNIT.objects.create(
            title="Sample Exam - 002",
            number_of_questions=2,
            marks=100.0,
            time=120
        )
        self.exam2 = EXAM_BATCH_CUNIT.objects.create(
            title="Sample Exam - 004",
            number_of_questions=2,
            marks=100.0,
            time=120
        )

    def test_bunit_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_bunit_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'dashboard/unit.html')

    def test_bunit_view_context(self):
        response = self.client.get(self.url)
        self.assertIn('cards', response.context)
        self.assertEqual(list(response.context['cards']), [self.card2, self.card1])
        self.assertIn('exams', response.context)
        self.assertEqual(list(response.context['exams']), [self.exam2, self.exam1])
        self.assertEqual(response.context['create_card'], 'card-cunit')
        self.assertEqual(response.context['create_question'], 'create-question-cunit')
        self.assertEqual(response.context['edit_test'], 'edit-test-cunit')
        self.assertEqual(response.context['topic'], 'C-UNIT')

print("Running test for Create Exam B Unit")
class CreateExamBUnitViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('create-exam-bunit')  # Update with the correct URL name for the view

    def test_create_exam_bunit_view_get(self):
        # Test GET request to render the form
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/question/create-exam.html')
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], CREATE_TEST)

    def test_create_exam_bunit_view_post_valid_data(self):
        # Test POST request with valid data
        valid_data = {
            'title': 'Sample Exam',
            'number_of_questions': 10,
            'marks': 100,
            'time': 60,
        }
        response = self.client.post(self.url, data=valid_data)
        # Check that the user is redirected
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('create-question-bunit'))  # Update with the actual URL name

        # Check session data
        session = self.client.session
        self.assertEqual(session['title'], 'Sample Exam')
        self.assertEqual(session['number_of_questions'], 10)
        self.assertEqual(session['marks'], 100)
        self.assertEqual(session['time'], 60)

    def test_create_exam_bunit_view_post_invalid_data(self):
        # Test POST request with invalid data
        invalid_data = {
            'title': '',  # Missing title
            'number_of_questions': -5,  # Invalid number of questions
            'marks': 'not_a_number',  # Invalid marks
            'time': -30,  # Invalid time
        }
        response = self.client.post(self.url, data=invalid_data)
        self.assertEqual(response.status_code, 200)  # Should render the form again
        self.assertTemplateUsed(response, 'dashboard/question/create-exam.html')
        self.assertIn('form', response.context)
        self.assertIn('invalid_data', response.context)
        self.assertEqual(response.context['invalid_data'], "Data is not valid")
        self.assertIsInstance(response.context['form'], CREATE_TEST)
        self.assertFalse(response.context['form'].is_valid())



# class CreateQuestionsBUnitViewTest(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.url = reverse('create-question-bunit')  # Update with the correct URL name

#         # Set up session data
#         session = self.client.session
#         session['title'] = 'Sample Exam'
#         session['number_of_questions'] = 5
#         session['marks'] = 100
#         session['time'] = 60
#         session.save()

#     def test_create_questions_bunit_view_get(self):
#         # Test GET request to render the formset
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'dashboard/question/create-question.html')
#         self.assertIn('formset', response.context)
#         self.assertEqual(len(response.context['formset']), 5)  # Ensure 5 formsets are generated (based on the session)

#     def test_create_questions_bunit_view_post_valid_data(self):
#         # Prepare valid POST data
#         valid_data = {
#             'form-0-question_text': 'Question 1',
#             'form-0-option1': 'Option 1',
#             'form-0-option1_is_correct': 'on',
#             'form-0-option2': 'Option 2',
#             'form-0-option2_is_correct': '',
#             'form-1-question_text': 'Question 2',
#             'form-1-option1': 'Option 1',
#             'form-1-option1_is_correct': 'on',
#             'form-1-option2': 'Option 2',
#             'form-1-option2_is_correct': '',
#             # Add form data for other forms (total of 5 based on the session)
#         }

#         response = self.client.post(self.url, data=valid_data)

#         # Check if EXAM_BATCH_BUNIT and Questions were created
#         self.assertEqual(response.status_code, 302)  # Should redirect
#         self.assertRedirects(response, reverse('b-unit-home'))

#         # Check that the exam was created
#         exam = EXAM_BATCH_BUNIT.objects.first()
#         self.assertEqual(exam.title, 'Sample Exam')
#         self.assertEqual(exam.number_of_questions, 5)
#         self.assertEqual(exam.marks, 100)
#         self.assertEqual(exam.time, 60)

#         # Check if questions were added to the exam
#         self.assertEqual(exam.questions.count(), 5)

print('Running Test For Create Questions B-Unit')
class CreateQuestionsBUnitViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('create-question-bunit')

        # Set up session data
        session = self.client.session
        session['title'] = 'Sample Exam'
        session['number_of_questions'] = 5
        session['marks'] = 100
        session['time'] = 60
        session.save()

    def test_create_questions_bunit_view_post_valid_data(self):
        valid_data = {
            'form-0-question_text': 'Question 1',
            'form-0-option1': 'Option 1',
            'form-0-option1_is_correct': 'on',
            'form-0-option2': 'Option 2',
            'form-0-option2_is_correct': '',
            'form-0-option3': 'Option 3',
            'form-0-option3_is_correct': '',
            'form-0-option4': 'Option 4',
            'form-0-option4_is_correct': '',
        }

        response = self.client.post(self.url, data=valid_data)

        # Assert redirect after valid form submission
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('b-unit-home'))