from django import forms
from .models import Question, UserAnswer, EXAM_BATCH_CARDS_BUNIT, EXAM_BATCH_CARDS_CUNIT

class CREATE_TEST(forms.Form):
    title = forms.CharField(label="Name of the Exam", widget=forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}))
    number_of_questions = forms.IntegerField(label='Number of Questions', min_value=1, widget=forms.NumberInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}))
    marks = forms.IntegerField(label="Total Marks", min_value=1, widget=forms.NumberInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}))
    time = forms.IntegerField(label="Time", widget=forms.NumberInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}))


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            'question_text', 
            'option1', 'option1_is_correct', 
            'option2', 'option2_is_correct', 
            'option3', 'option3_is_correct', 
            'option4', 'option4_is_correct',
        ]
        labels = {
            'question_text':'Question:',
            'option1':'First Choice',
            'option1_is_correct':'',
            'option2':'Second Choice',
            'option2_is_correct':'',
            'option3':'Third Choice',
            'option3_is_correct':'',
            'option4':'Fourth Choice',
            'option4_is_correct':'',
        }
        widgets = {
            'question_text': forms.Textarea(attrs={'class': 'form-textarea mt-1 block w-full'}),
            'option1': forms.TextInput(attrs={'class': 'form-input mt-1 block w-full'}),
            'option1_is_correct': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'option2': forms.TextInput(attrs={'class': 'form-input mt-1 block w-full'}),
            'option2_is_correct': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'option3': forms.TextInput(attrs={'class': 'form-input mt-1 block w-full'}),
            'option3_is_correct': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'option4': forms.TextInput(attrs={'class': 'form-input mt-1 block w-full'}),
            'option4_is_correct': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }
        def clean_option1(self):
            """Handle empty string for option1"""
            data = self.cleaned_data.get('option1')
            return data if data.strip() else None

        def clean_option2(self):
            """Handle empty string for option2"""
            data = self.cleaned_data.get('option2')
            return data if data.strip() else None

        def clean_option3(self):
            """Handle empty string for option3"""
            data = self.cleaned_data.get('option3')
            return data if data.strip() else None

        def clean_option4(self):
            """Handle empty string for option4"""
            data = self.cleaned_data.get('option4')
            return data if data.strip() else None

        def clean(self):
            """Custom validation for the entire form."""
            cleaned_data = super().clean()

            # Ensure all `option` fields with blank values are stored as None
            for field in ['option1', 'option2', 'option3', 'option4']:
                if not cleaned_data.get(field):
                    cleaned_data[field] = None

            return cleaned_data


class CARD_FORM(forms.Form):
    title = forms.CharField(label="Class Name", widget=forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}))
    drive_link = forms.CharField(label="PDF File Link", widget=forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}))
    take_exam = forms.CharField(label="Exam Link", widget=forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}))

class EDIT_CARD_BUNIT(forms.ModelForm):
    class Meta:
        model = EXAM_BATCH_CARDS_BUNIT
        fields = [
            'title',
            'drive_link',
            'take_exam',
        ]

class EDIT_CARD_CUNIT(forms.ModelForm):
    class Meta:
        model = EXAM_BATCH_CARDS_CUNIT
        fields = [
            'title',
            'drive_link',
            'take_exam',
        ]


class AnswerForm(forms.ModelForm):
    class Meta:
        model = UserAnswer
        fields = ['selected_option']

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question', None)
        super(AnswerForm, self).__init__(*args, **kwargs)
        if question:
            self.fields['selected_option'] = forms.ChoiceField(
                choices=[
                    (question.option1, question.option1),
                    (question.option2, question.option2),
                    (question.option3, question.option3),
                    (question.option4, question.option4),
                ],
                widget=forms.RadioSelect(attrs={'class': 'h-4 w-4'})
            )
            self.fields['selected_option'].label = question.question_text