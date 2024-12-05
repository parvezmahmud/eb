from django import forms
from .models import Question

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


class CARD_FORM(forms.Form):
    title = forms.CharField(label="Class Name", widget=forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}))
    drive_link = forms.CharField(label="PDF File Link", widget=forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}))
    take_exam = forms.CharField(label="Exam Link", widget=forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}))