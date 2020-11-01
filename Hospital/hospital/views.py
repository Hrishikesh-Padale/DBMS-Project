from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponse
import random
from datetime import date

# Create your views here.
def homepage(request):
	return render(request,'hospital/home.html')


def appoint_doctor(request,Doctor_ID):
	attends = Attends.objects.filter(Doc_id__Doc_id__NID = Doctor_ID)
	context = {'patients':[]}

	for i in attends:
		context['patients'].append([i.PID.PID,i.PID.Name,i.PID.Sex,i.PID.Description])
		#print(i.PID.Name)
	print('context',context)
	return render(request,'hospital/show_appointments.html',context)

def discharge(request,Doctor_ID,Patient_ID):
	#discharge/05273/
	path = request.path
	appointment = Appointment.objects.get(Doc_id__Doc_id__NID=Doctor_ID)
	attends = Attends.objects.get(Doc_id__Doc_id__NID=Doctor_ID)
	print(appointment,attends)
	appointment.delete()
	attends.delete()
	return redirect(path[:len(path)-16])


def doctor_dashboard(request,credentials):
	doctor=Doctor.objects.filter(Email=credentials['Email'])
	context = {'doctor':[doctor[0].Doc_id.NID,doctor[0].Doc_id.Name]}
	return render(request,'hospital/doctor_dashboard.html',context)

def appointment(request,Patient_ID):
	appointment = request.POST
	if appointment:
		Doc_id = appointment['Doc_id']
		doctor = Doctor.objects.filter(Doc_id__NID=Doc_id)
		patient=Patient.objects.filter(PID=Patient_ID)
		Date = date.today()
		new_appointment=Appointment(Doc_id=doctor[0],PID=patient[0],Date=Date,Description=patient[0].Description)
		new_attends = Attends(PID=patient[0],Doc_id=doctor[0])
		record = Record.objects.filter(PID__PID=Patient_ID)
		print(Date)
		record[0].Appointment+= doctor[0].Doc_id.NID+' '+patient[0].PID+' '+str(Date)+' '+patient[0].Description
		new_appointment.save()
		print(record)
		record[0].save()
		new_attends.save()
		return redirect(request.path[:len(request.path)-8])

def patient_dashboard(request,Patient_ID):
	#print(request.POST)
	patient=Patient.objects.filter(PID=Patient_ID)
	if ',' in patient[0].Description:
		Description=patient[0].Description.split(',')
	else:
		Description=patient[0].Description.split()

	context = {'patient':[patient[0].PID,patient[0].Name],'doctors':[],'Description':Description}
	all_doctors = Doctor.objects.all()
	for doc in all_doctors:
		context['doctors'].append([doc.Doc_id.Name,doc.Doc_id.NID])	
	return render(request,'hospital/patient_dashboard.html',context)	


def doctor_login(request):
	credentials = request.POST
	if credentials:
		Email=credentials['Email'].strip()
		Password=credentials['password'].strip()
		profile=Doctor.objects.filter(Email=Email)
		try:
			if profile[0].Password == Password:
				return doctor_dashboard(request,credentials)
			else:
				return HttpResponse('Invalid credentials')
		except:
			return HttpResponse('Invalid credentials')
	return render(request,'hospital/doctor_login.html')

def patient_login(request):
	credentials = request.POST
	if credentials:
		Email=credentials['Email'].strip()
		Password=credentials['password']
		profile=Patient.objects.filter(Email=Email)
		try:
			if profile[0].Password == Password:
				path=request.path
				path=path[1:]
				path+=profile[0].PID
				return redirect(path)
			else:
				return HttpResponse('Invalid credentials')
		except:
			return HttpResponse('Invalid credentials')

	return render(request,'hospital/patient_login.html')

def patient_logout(request,Patient_ID):
	path = 'http://127.0.0.1:8000/hospital/patient_login/'
	return redirect(path)

def add_doctor(request):
	NID = ''
	context = {'rooms':[]}
	all_rooms = Rooms.objects.all()
	for room in all_rooms:
		context['rooms'].append('Room no {}'.format(room.Room_ID))
	#print(context)
	#print(request.path)
	doctor = request.POST
	if doctor:
		Doctors = Nurse.objects.all()
		if Doctors:
			search_done = False
			while not search_done:
				for i in range(5):
					NID += str(random.randrange(0,9))
			
				for Doc in Doctors:
					if NID == Doc.NID:
						NID = ''
				if NID:
					search_done = True
		else:
			for i in range(5):
				NID += str(random.randrange(0,9))

		Name = doctor['Name'].strip()
		Sex = doctor['Sex'].strip()
		Contact_no = doctor['Contact_no'].strip()
		Type = doctor['Type'].strip()
		Room_ID = doctor['Room_ID'].strip()
		Room_ID = Room_ID[-3:]
		Email = doctor['Email']
		Password = doctor['password']
		new_nurse = Nurse(NID = NID,Name=Name,Sex=Sex,Contact_no = Contact_no)	
		new_doctor = Doctor(Doc_id = new_nurse,Type = Type,Email=Email,Password=Password)
		new_nurse.save()
		new_doctor.save()

		Room_ID=Rooms.objects.filter(Room_ID=Room_ID)
		new_governs = Governs(NID =new_nurse,Room_ID=Room_ID[0])

		new_governs.save()
		if Type == 'Trainee':
			new_trainee = Trainee(TID = new_doctor)
			new_trainee.save()
		elif Type == 'Visitor':
			new_visitor = Visiting(VID = new_doctor)
			new_visitor.save()
		elif Type == 'Permanent':
			new_permanent = Permanent(ID = new_doctor)
			new_permanent.save()
		#print(new_doctor)
	return render(request,'hospital/add_doctor.html',context)


def staff_view(request):
    return render(request,'hospital/staff_management.html')

		

def patient_registration(request):	
	PID = ''
	all_doctors = Doctor.objects.all()
	context = {'doctors':[]}
	for d in all_doctors:
		context['doctors'].append(d.Doc_id.Name)
	#print(context)
	patient = request.POST
	if patient:
		Patients = Patient.objects.all()
		if Patients:
			search_done = False
			while not search_done:
				for i in range(5):
					PID += str(random.randrange(0,9))

				for pat in Patients:
					if PID == pat.PID:
						PID = ''

				if PID:
					search_done = True


		else:
			for i in range(5):
				PID += str(random.randrange(0,9))
		Name = patient['Name'].strip()
		Sex = patient['Sex'].strip()
		Address = patient['Address'].strip()
		Contact_no = patient['Contact_no'].strip()
		Description = patient['Description'].strip()
		#Appointment_doctor = patient['Appointment'].strip()
		Email=patient['Email'].strip()
		Password=patient['password']
		for pat in Patients:
			if pat.Email == Email:
				return HttpResponse('Email already exists')
		
		all_recs = Record.objects.all()
		if all_recs:
			last_rec_no = all_recs[len(all_recs)-1].Record_no
			Record_no = last_rec_no+1
		else :
			Record_no = 1
		new_patient = Patient(PID=PID,Name=Name,Sex=Sex,Address=Address,Contact_no=Contact_no,Record_no=Record_no,Description=Description,Email=Email,Password=Password)
		new_record = Record(Record_no=Record_no,PID=new_patient,Description=Description)
		new_patient.save()
		new_record.save()

	return render(request, 'hospital/add_patient.html',context)	 

def show_doctors(request):
	all_doctors = Doctor.objects.all()
	context = {'doctors':[]}
	for doc in all_doctors:
		context['doctors'].append([doc.Doc_id.NID,doc.Doc_id.Name,doc.Doc_id.Contact_no,doc.Doc_id.Sex,doc.Email])
	#print(context)
	#print('Request in show doctors:',request,request.path)
	return render(request,'hospital/show_doctors.html',context)

def show_employees(request):
	all_employees = Employee.objects.all()
	context = {'employees':[]}
	for emp in all_employees:
		context['employees'].append([emp.EID,emp.NID.NID,emp.NID.Name,emp.Email,emp.Salary])
	#print(context)
	return render(request,'hospital/show_employees.html',context)

def show_patients(request):
	all_patients = Patient.objects.all()
	#print(all_patients)
	context = {'patients':[]}
	for pat in all_patients:
		context['patients'].append([pat.PID,pat.Name,pat.Sex,pat.Address,pat.Contact_no])
	
	return render(request,'hospital/show_patients.html',context)

def show_rooms(request,Patient_ID=None):
	all_rooms = Rooms.objects.all()
	all_assigned = Assigned.objects.all()
	context={'rooms':[]}
	patient='No patient'
	for room in all_rooms:
		if room.Room_period:
			availability = 'Not Available'
		else :
			availability = 'Available'
		for i in all_assigned:
			if room.Room_ID == i.Room_ID.Room_ID:
				patient = i.PID.PID
				break
			else:
				patient = 'No patient'
		context['rooms'].append([room.Room_ID,room.Room_type,room.Room_period,availability,patient])
	#print(context)
	return render(request,'hospital/show_rooms.html',context)

def show_medicines(request):
	all_meds = Medicine.objects.all()
	context = {'medicines':[]}
	for med in all_meds:
		context['medicines'].append([med.Code,med.Name,med.Price])

	return render(request,'hospital/show_medicines.html',context)

def show_treatments(request):
	all_treats = Treatment.objects.all()
	context = {'treatments':[]}
	for t in all_treats:
		context['treatments'].append([t.Treatment,str(t.Amount)+'/-'])

	return render(request,'hospital/show_treatments.html',context)


def new_employee(request):
	NID = ''
	EID = ''
	employee = request.POST
	context = {'rooms':[]}
	all_rooms = Rooms.objects.all()
	for room in all_rooms:
		context['rooms'].append('Room no {}'.format(room.Room_ID))
	#print(employee)
	if employee:
		emps = Nurse.objects.all()
		all_employees = Employee.objects.all()
		if emps:
			search_done = False
			while not search_done:
				for i in range(5):
					NID += str(random.randrange(0,9))
				for emp in emps:
					if NID == emp.NID :
						NID = ''			
				if NID:
					search_done=True

		else:
			for i in range(5):
				NID += str(random.randrange(0,9))
		
		if all_employees:
			search_done = False
			while not search_done:
				for i in range(5):
					EID += str(random.randrange(0,9))
				for emp in all_employees:
					if EID == emp.EID :
						EID = ''
				if EID:
					search_done = True
		else:
			for i in range(5):
				EID += str(random.randrange(0,9))

		Name = employee['Name'].strip()
		Sex = employee['Sex'].strip()
		Contact_no = employee['Contact_no'].strip()
		Email = employee['email'].strip()
		Salary=employee['salary'].strip()
		Room_ID=employee['Room_ID'].strip()
		Room_ID=Room_ID[-3:]
		new_nurse = Nurse(NID = NID,Name=Name,Sex=Sex,Contact_no = Contact_no)	
		new_employee = Employee(NID = new_nurse,EID=EID,Email=Email,Salary=Salary)
		Room_ID=Rooms.objects.filter(Room_ID=Room_ID)
		new_governs = Governs(NID =new_nurse,Room_ID=Room_ID[0])
		new_nurse.save()
		new_employee.save()
		new_governs.save()
		
	return render(request,'hospital/new_employee.html',context)

def doct_remove(request,Doctor_ID):
	all_doctors = Doctor.objects.all()
	doct = None
	for doc in all_doctors:
		if doc.Doc_id.NID == Doctor_ID:
			doct = doc
			break
	if doct:
		N = Nurse.objects.filter(NID=doct.Doc_id.NID)
		N.delete()
	#print(request.path[-13:])
	path = request.path[:len(request.path)-13]
	return redirect(path)

def emp_remove(request,Emp_ID):
	all_employees = Employee.objects.all()
	emp = None
	for i in all_employees:
		if i.NID.NID == Emp_ID:
			emp = i
			break
	if emp:
		N = Nurse.objects.filter(NID=emp.NID.NID)
		N.delete()

	path = request.path[:len(request.path)-13]
	return redirect(path)

def patient_discharge(request,Patient_ID):
	all_patients = Patient.objects.all()
	pat = None
	for i in all_patients:
		if i.PID == Patient_ID:
			pat = i
			break
	if pat:
		P = Patient.objects.filter(PID=pat.PID)[0]
		for i in Assigned.objects.all():
			if i.PID.PID == P.PID:
				room = i.Room_ID
				room.Room_period =''
				room.save()
				for i in Assigned.objects.all():
					if i.PID.PID == P.PID:
						i.delete()

		P.delete()
	path = request.path[:len(request.path)-16]
	return redirect(path)


def new_receptionist(request):
	RID = ''
	NID = ''
	all_recps = Receptionist.objects.all()
	all_nurses = Nurse.objects.all()
	all_records = Record.objects.all()
	receptionist = request.POST
	search_done = False
	context = {'rooms':[]}
	all_rooms = Rooms.objects.all()
	for room in all_rooms:
		context['rooms'].append('Room no {}'.format(room.Room_ID))
	if receptionist:
		if all_recps:
			while not search_done:
				for i in range(5):
					RID += str(random.randrange(0,9))

				for R in all_recps:
					if RID == R.R_ID:
						RID = ''

				if RID:
					search_done = True
		else :
			for i in range(5):
				RID += str(random.randrange(0,9))

		search_done = False		
		if receptionist:
			if all_nurses:
				while not search_done:
					for i in range(5):
						NID += str(random.randrange(0,9))

					for N in all_nurses:
						if NID == N.NID:
							NID = ''

					if NID:
						search_done = True
			else :
				for i in range(5):
					NID += str(random.randrange(0,9))

		all_rec_nos = []
		for i in all_records:
			all_rec_nos.append(i.Record_no)

		Record_no = int(receptionist['Record_no'].strip())
		if Record_no not in all_rec_nos:
			return HttpResponse('No such ({}) record number is in the database'.format(Record_no))

		for i in all_records:
			if Record_no == i.Record_no:
				Record_no = i
				break

		Name = receptionist['Name'].strip()
		Sex = receptionist['Sex'].strip()
		Contact_no = receptionist['Contact_no'].strip()
		Room_ID=receptionist['Room_ID'].strip()
		Room_ID=Room_ID[-3:]
		new_nurse = Nurse(NID=NID,Name=Name,Sex=Sex,Contact_no=Contact_no)
		new_receptionist = Receptionist(NID= new_nurse,R_ID=RID,Record_no=Record_no)
		new_maintains = Maintains(R_ID=new_receptionist,Record_no=Record_no)
		Room_ID=Rooms.objects.filter(Room_ID=Room_ID)
		new_governs = Governs(NID =new_nurse,Room_ID=Room_ID[0])
		new_nurse.save()
		new_receptionist.save()
		new_maintains.save()
		new_governs.save()

	return render(request,'hospital/add_receptionist.html',context)

def new_drug(request):

	medicine = request.POST
	all_meds = Medicine.objects.all()
	if medicine:
		Code = medicine['Code'].strip()
		Name = medicine['Name'].strip()
		Price = medicine['Price'].strip()
		if all_meds:
			for i in all_meds:
				if i.Code == Code:
					return HttpResponse('Code already exists in database')
		new_medicine = Medicine(Code=Code,Price=Price,Name=Name)
		new_medicine.save()

	return render(request,'hospital/add_drug.html')	

def prescription(request,Doctor_ID,Patient_ID):
	all_meds = Medicine.objects.all()
	all_treats = Treatment.objects.all()
	all_rooms = Rooms.objects.all()
	context = {'meds':[],'treats':[],'rooms':[]}
	for i in all_meds:
		context['meds'].append(i.Name)
	for i in all_treats:
		context['treats'].append(i.Treatment)	
	for i in all_rooms:
		if not i.Room_period:
			context['rooms'].append(i.Room_ID)
	return render(request,'hospital/prescription.html/',context)

def save_prescription(request,Doctor_ID,Patient_ID):
	if request.POST:
		P = request.POST
		medicine = P['Medicine'].strip()
		Quantity = P['Quantity'].strip()
		treatment = P['Treatment'].strip()
		admit = P['Admit'].strip()
		#print(medicine,Quantity,Treatment)
		patient=Patient.objects.get(PID=Patient_ID)
		med = Medicine.objects.get(Name=medicine)
		T = Treatment.objects.get(Treatment=treatment)
		total_bill = med.Price*int(Quantity) + T.Amount
		room = P['room'].strip()
		period = P['Duration'].strip()

		if admit == 'Yes':
			Date = date.today()
			Date = [Date.day,Date.month,Date.year]
			new_detail = Pdetails(PID=patient,Admit_date=Date)
			new_detail.save()

		if room != 'Do not assign room' and admit !='no':
			for r in Rooms.objects.all():
				if room == r.Room_ID:
					r.Room_period = period
					r.save()
					new_assign = Assigned(Room_ID=r,PID=patient)
					new_assign.save()			
					break

		medicine += 'x'+str(Quantity) 
		patient_is_fresh=1
		for i in Bill.objects.all():
			if i.PID.PID == Patient_ID:
				patient_is_fresh=0
				break

		if patient_is_fresh:
			new_bill = Bill(PID=patient,Treatment=treatment,Amount=total_bill,Medicine=medicine)
			new_bill.save()
		else:
			for i in Bill.objects.all():
				if i.PID.PID == Patient_ID:
					i.Amount += total_bill
					i.save()
					break
		path = request.path[:len(request.path)-37]
		
	return redirect(path)

def make_querry(request):
	querry = request.POST
	print(querry)
	if querry:
		value=querry['value']
		Entity = querry['Entity Name']
		Attribute = querry['Attribute']
		if Entity == 'Doctor':
			if Attribute == 'ID':
				try:
					doc = Doctor.objects.get(Doc_id__NID=value)
					print(doc)
				except:
					return HttpResponse('No Record Found')


			elif Attribute == "Staff Name":
				try:
					doc = Doctor.objects.get(Doc_id__Name=value)
					print(doc)
				except:
					return HttpResponse('No Record Found')


			elif Attribute == "Staff Email":
				try:
					doc = Doctor.objects.get(Email=value)
					print(doc)
				except:
					return HttpResponse('No Record Found')

		elif Entity == 'Nurse':
			if Attribute == 'ID':
				try:
					nurse = Nurse.objects.get(NID=value)
					print(nurse)
				except:
					return HttpResponse('No Record Found')


			elif Attribute == "Staff Name":
				try:
					nurse = Nurse.objects.get(Name=value)
					print(nurse)
				except:
					return HttpResponse('No Record Found')


			elif Attribute == "Staff Email":
				try:
					nurse = Nurse.objects.get(Email=value)
					print(nurse)
				except:
					return HttpResponse('No Record Found')
		elif Entity == 'Employee':
			if Attribute == 'ID':
				try:
					employee = Employee.objects.get(EID=value)
					print(employee)
				except:
					return HttpResponse('No Record Found')


			elif Attribute == "Staff Name":
				try:
					employee = Employee.objects.get(Name=value)
					print(employee)
				except:
					return HttpResponse('No Record Found')


			elif Attribute == "Staff Email":
				try:
					employee = Employee.objects.get(Email=value)
					print(employee)
				except:
					return HttpResponse('No Record Found')

	return render(request,'hospital/search.html')
