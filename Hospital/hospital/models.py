from django.db import models

# Create your models here.
class Nurse(models.Model):
	NID = models.CharField(max_length=5)
	Name = models.CharField(max_length = 20)
	Sex = models.CharField(max_length = 10)
	Contact_no = models.IntegerField()
	def __str__(self):
		return "[{} {}]".format(self.NID,self.Name)

class Patient(models.Model):
    PID = models.CharField(max_length = 5)
    Name = models.CharField(max_length = 25)
    Sex = models.CharField(max_length = 10)
    Address = models.CharField(max_length = 20)
    Contact_no = models.IntegerField()
    Record_no = models.CharField(max_length = 5)
    Description = models.CharField(max_length=30)
    Email=models.CharField(max_length=20)
    Password = models.CharField(max_length=15)
    def __str__(self):
    	return "[{} {} {} {}]".format(self.PID,self.Name,self.Contact_no,self.Record_no)

class Doctor(models.Model):
	Doc_id = models.ForeignKey(Nurse,on_delete=models.CASCADE)
	Type = models.CharField(max_length=10)
	Email=models.CharField(max_length=20)
	Password = models.CharField(max_length=15)
	def __str__(self):
		return "\n---------------------\nNID-{}\nName-{}\nContact-{}\n---------------------".format(self.Doc_id.NID,self.Doc_id.Name,self.Doc_id.Contact_no,self.Type)
		
class Treatment(models.Model):
	Treatment = models.CharField(max_length=20)
	Amount = models.IntegerField()
	
	def __str__(self):
		return "[{} {}]".format(self.Treatment,self.Amount)
		
class Bill(models.Model):
	PID = models.ForeignKey(Patient,on_delete=models.CASCADE)
	Treatment = models.CharField(max_length = 20)
	Amount = models.IntegerField()
	Medicine = models.CharField(max_length = 20)
	
	def __str__(self):
		return "[{} {}]".format(self.PID,self.Amount)

class Attends(models.Model):
    PID = models.ForeignKey(Patient,on_delete=models.CASCADE)
    Doc_id = models.ForeignKey(Doctor,on_delete=models.CASCADE)
    
    def __str__(self):
        return '[{} {}]'.format(self.PID.PID,self.Doc_id.Doc_id)

class Medicine(models.Model):
	Code = models.IntegerField()
	Quantity = models.CharField(max_length=3,default='')
	Price = models.IntegerField()
	Name = models.CharField(max_length=20,default='')
	def __str__(self):
		return "[{} {} {}]".format(self.Code,self.Name,self.Price)

class Rooms(models.Model):
	Room_ID = models.CharField(max_length=3)
	Room_type = models.CharField(max_length=1)
	Room_period = models.CharField(max_length=2,default='')
	#PID = models.ForeignKey(Patient,on_delete=models.CASCADE)
	
	def __str__(self):
		return "[{} {}]".format(self.Room_ID,self.Room_type,self.Room_period)
		
class Assigned(models.Model):
	PID = models.ForeignKey(Patient,on_delete=models.CASCADE)
	Room_ID = models.ForeignKey(Rooms,on_delete=models.CASCADE)
	def __str__(self):
		return "[{} {}]".format(self.PID.PID,self.Room_ID.Room_ID)
		
class Governs(models.Model):
	NID = models.ForeignKey(Nurse,on_delete=models.CASCADE)
	Room_ID = models.ForeignKey(Rooms,on_delete=models.CASCADE)
	
	def __str__(self):
		return "[{} {}]".format(self.NID.NID,self.Room_ID.Room_ID)
		

class Employee(models.Model):
	EID = models.CharField(max_length=5)
	NID = models.ForeignKey(Nurse,on_delete=models.CASCADE)
	Email = models.CharField(max_length=20)
	Salary = models.IntegerField()
	
	def __str__(self):
		return "{} {}".format(self.EID,self.NID.Name)
	
		
class Pdetails(models.Model):
	PID = models.ForeignKey(Patient,on_delete=models.CASCADE)
	Admit_date = models.CharField(max_length=20,default='')
	Discharge_date = models.CharField(max_length=20,default='')
	#Description = models.CharField(max_length=30) 
	
	def __str__(self):
		return "{} {} {}".format(self.PID.PID,self.Admit_date,self.Discharge_date)
		
class Appointment(models.Model):
	PID = models.ForeignKey(Patient,on_delete=models.CASCADE)
	Doc_id = models.ForeignKey(Doctor,on_delete=models.CASCADE)
	Date = models.DateField()
	Description = models.CharField(max_length=30)

	def __str__(self):
		return "{} {}".format(self.PID.PID,self.Doc_id.Doc_id)
		
class Record(models.Model):
	Record_no = models.IntegerField()
	PID = models.ForeignKey(Patient,on_delete=models.CASCADE)
	Appointment = models.CharField(max_length=50)
	Description = models.CharField(max_length=30)
	def __str__(self):
		return "{} {}".format(self.Record_no,self.PID.PID)		
		
class Receptionist(models.Model):
	NID = models.ForeignKey(Nurse,on_delete=models.CASCADE)
	R_ID = models.CharField(max_length=5)
	Record_no = models.ForeignKey(Record,on_delete=models.CASCADE)
	
	def __str__(self):
		return "{} {} {}".format(self.NID.NID,self.R_ID,self.Record_no.Record_no)
		
class Maintains(models.Model):
	R_ID = models.ForeignKey(Receptionist,on_delete=models.CASCADE)
	Record_no = models.ForeignKey(Record,on_delete=models.CASCADE)
	
	def __str__(self):
		return "{} {}".format(self.R_ID.R_ID,self.Record_no.Record_no)
		
class Trainee(models.Model):
	TID = models.ForeignKey(Doctor,on_delete=models.CASCADE)
	
	def __str__(self):
		return "{} {}".format(self.TID.Doc_id.NID,self.TID.Doc_id.Name)
	
class Visiting(models.Model):
	VID = models.ForeignKey(Doctor,on_delete=models.CASCADE)
	
	def __str__(self):
		return "{} {}".format(self.VID.Doc_id.NID,self.VID.Doc_id.Name)

class Permanent(models.Model):
	ID = models.ForeignKey(Doctor,on_delete=models.CASCADE)
	
	def __str__(self):
		return "{} {}".format(self.ID.Doc_id.NID,self.ID.Doc_id.Name)	
		
		

		

