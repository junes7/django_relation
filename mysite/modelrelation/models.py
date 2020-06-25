from django.db import models

# Create your models here.
class Doctor(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return f'{self.pk}의사 {self.name}'

class Patient(models.Model):
    name = models.CharField(max_length=20)
    # Manytomany는 복수형이고, 다수의 관계가 형성되기에 변수명을 복수형으로 정해주었다.
    # patient_set의 이름을 related_name옵션을 통해 환자명들이란 이름으로 변경해주면
    # 정해준 이름으로만 가져올 수 있다.
    # through='Reservation',
    doctors = models.ManyToManyField(Doctor, related_name="patients")
    def __str__(self):
        return f'{self.pk}번 환자, {self.name}'

# class Reservation(models.Model):
#     doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
#     patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

#     def __str__(self):
#         return f'{self.doctor}의 {self.patient}'
