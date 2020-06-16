from django import forms
from django.contrib.auth.models import User
from api.models import Student, Teacher, Class, Assignment
import re

class UserUpdateForm(forms.ModelForm):

    username = forms.CharField(max_length=50, disabled=True)
    first_name = forms.CharField(max_length=50, disabled=True)
    last_name = forms.CharField(max_length=50, disabled=True)
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']

class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['git']

class TeacherUpdateForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['git']

class ClassCreationForm (forms.ModelForm):
    subject = forms.CharField(max_length=50)
    period = forms.IntegerField(min_value=0, max_value=9)
    description = forms.CharField(widget=forms.Textarea)
    unconfirmed = forms.ModelMultipleChoiceField(queryset=Student.objects.all(), label="Invite students")


    def clean_period(self):
        pd = self.cleaned_data['period']
        if pd < 1 or pd > 9:
            raise forms.ValidationError("Invalid period")
        return pd;

    def __init__(self, *args, **kwargs):
        super(ClassCreationForm, self).__init__(*args, **kwargs)
        self.fields['period'].widget.attrs['min'] = 0
        # Only in case we build the form from an instance
        # (otherwise, 'unconfirmed' list should be empty)
        if kwargs.get('instance'):
            # We get the 'initial' keyword argument or initialize it
            # as a dict if it didn't exist.
            initial = kwargs.setdefault('initial', {})
            # The widget for a ModelMultipleChoiceField expects
            # a list of primary key for the selected data.
            initial['unconfirmed'] = [t.pk for t in kwargs['instance'].unconfirmed.all()]

    # Overriding save allows us to process the value of 'unconfirmed' field
    def save(self, commit=True):
        # Get the unsave Pizza instance
        instance = forms.ModelForm.save(self, False)

        # Prepare a 'save_m2m' method for the form,
        old_save_m2m = self.save_m2m
        def save_m2m():
           old_save_m2m()
           # This is where we actually link the pizza with toppings
           instance.topping_set.clear()
           instance.topping_set.add(*self.cleaned_data['unconfirmed'])
        self.save_m2m = save_m2m

        # Do we need to save all changes now?
        if commit:
            instance.save()
            self.save_m2m()

        return instance

    class Meta:
        model = Class
        fields = ['subject', 'period', 'description', 'unconfirmed']
