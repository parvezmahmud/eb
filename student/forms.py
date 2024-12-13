from .models import STUDENT, STUDENTINFO
from django import forms

class SignUpForm(forms.ModelForm):
    class Meta:
        model = STUDENT
        fields = [
            'email',
            'password',
            'confirm_password',
        ]
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'appearance-none block w-full bg-gray-100 text-gray-700 border border-gray-300 rounded-md py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-teal-500',
                'placeholder': 'Enter a valid E-mail'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'appearance-none block w-full bg-gray-100 text-gray-700 border border-gray-300 rounded-md py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-teal-500',
                'placeholder': 'Enter a password'
            }),
            'confirm_password': forms.PasswordInput(attrs={
                'class': 'appearance-none block w-full bg-gray-100 text-gray-700 border border-gray-300 rounded-md py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-teal-500',
                'placeholder': 'Password again'
            }),
        }

class StudentInfoForm(forms.ModelForm):
    class Meta:
        model = STUDENTINFO
        fields = [
            'name',
            'college',
            'phone',
            'bkash_number',
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'appearance-none block w-full bg-gray-100 text-gray-700 border border-gray-300 rounded-md py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-teal-500',
                'placeholder': 'Enter your full name'

            }),
            'college':forms.TextInput(attrs={
                'class': 'appearance-none block w-full bg-gray-100 text-gray-700 border border-gray-300 rounded-md py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-teal-500',
                'placeholder': 'Enter your college name'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'appearance-none block w-full bg-gray-100 text-gray-700 border border-gray-300 rounded-md py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-teal-500',
                'placeholder': 'Enter your phone number'
            }),
            'bkash_number':forms.TextInput(attrs={
                'class': 'appearance-none block w-full bg-gray-100 text-gray-700 border border-gray-300 rounded-md py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-teal-500',
                'placeholder': 'Your Bkash/Nagad/Rocket account number'
            })
        }