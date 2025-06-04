from eqrApp.models import Student 


objects_to_create = [
Student(enrol_no='test', first_name='rahul', dob='2001-08-20', branch='Computer Science & Business System')
]

Student.objects.bulk_create(objects_to_create)