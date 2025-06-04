from distutils.command.upload import upload
from email.policy import default
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
import qrcode
from PIL import Image

# Create your models here.
class Student(models.Model):
    enrol_no = models.CharField(max_length=100)
    first_name = models.CharField(max_length=250)
    middle_name = models.CharField(max_length=250, null=True)
    last_name = models.CharField(max_length=250)
    gender = models.CharField(max_length=50, choices=(("Male","Male"), ("Female","Female")), default="Male")
    dob = models.DateField(max)
    contact = models.CharField(max_length=100)
    email = models.CharField(max_length=250, blank=True)
    address = models.TextField(null=True, blank=True)
    branch = models.TextField(null=True, blank=True)
    semester = models.TextField(null=True, blank=True)
    avatar = models.ImageField(upload_to = "student-avatars/",null=True, blank=True)
    date_added = models.DateTimeField(default = timezone.now)
    date_created = models.DateTimeField(auto_now = True)

    def __str__(self):
        return str(f"{self.enrol_no} - {self.first_name}"+ (f"{self.middle_name} {self.last_name}" if not self.middle_name == "" else f"{self.last_name}") )
    def name(self):
        return str(f"{self.first_name} "+ (f"{self.middle_name} {self.last_name}" if not self.middle_name == "" else f"{self.last_name}") )
    def data(self):
        return str(f"Enrollment No. {self.enrol_no} Name {self.first_name} "+ (f"{self.middle_name} {self.last_name} Branch {self.branch} Semester {self.semester} DOB {self.dob} Contact {self.contact} Mail {self.email} Address {self.address}" if not self.middle_name == "" else f"{self.last_name} Branch {self.branch} Semester {self.semester} DOB {self.dob} Contact {self.contact} Mail {self.email} Address {self.address}") )


    def save(self, *args, **kwargs):
        super(Student, self).save(*args, **kwargs)
        print(self.avatar)
        imag = Image.open(self.avatar.path)
        if imag.width > 200 or imag.height> 200:
            output_size = (200, 200)
            imag.thumbnail(output_size)
            imag.save(self.avatar.path)