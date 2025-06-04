from secrets import choice
from django import forms
from numpy import require
from eqrApp import models
import qrcode

class SaveStudent(forms.ModelForm):
    enrol_no = forms.CharField(max_length=250, label="Enrollment No")
    first_name = forms.CharField(max_length=250, label="First Name")
    middle_name = forms.CharField(max_length=250, label="Middle Name", required=False)
    last_name = forms.CharField(max_length=250, label="Last Name")
    dob = forms.DateField(label="Birthday")
    gender = forms.ChoiceField(choices=[("Male","Male"), ("Female","Female")], label="Gender")
    contact = forms.CharField(max_length=250, label="Contact")
    email = forms.CharField(max_length=250, label="Email")
    address = forms.Textarea()
    branch = forms.CharField(max_length=250, label="Branch")
    semester = forms.CharField(max_length=250, label="Semester")
    avatar = forms.ImageField(label="Avatar")

    class Meta():
        model = models.Student
        fields = ('enrol_no',
                  'first_name',
                  'middle_name',
                  'last_name',
                  'dob',
                  'gender',
                  'contact',
                  'email',
                  'address',
                  'branch',
                  'semester',
                  'avatar', )

    def clean_student_code(self):
        id = self.data['id'] if self.data['id'] != '' else 0
        enrol_no = self.cleaned_data['enrol_no']
        try:
            if id > 0:
                student = models.student.exclude(id=id).get(enrol_no = enrol_no)
            else:
                student = models.student.get(enrol_no = enrol_no)
        except:
            return enrol_no
        return forms.ValidationError(f"{enrol_no} already exists.")

