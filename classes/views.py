from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout

from .models import *
from .forms import *

def classroom_list(request):
	classrooms = Classroom.objects.all()
	context = {
		"classrooms": classrooms,
	}
	return render(request, 'classroom_list.html', context)


def classroom_detail(request, classroom_id):
	classroom_obj = Classroom.objects.get(id=classroom_id)
	student_obj= Student.objects.filter(classroom=classroom_obj).order_by("name","exam_grade")
	context = {
		"classroom": classroom_obj,
		"student": student_obj,
	}
	return render(request, 'classroom_detail.html', context)


def classroom_create(request):
	if request.user.is_anonymous:
		return redirect('signin')
	form = ClassroomForm()
	if request.method == "POST":
		form = ClassroomForm(request.POST, request.FILES or None)
		if form.is_valid():
			classroom=form.save(commit=False)
			classroom.teacher = request.user
			classroom.save()
			messages.success(request, "Successfully Created!")
			return redirect('classroom-list')
		print (form.errors)             
	context = {
	"form": form,
	}
	return render(request, 'create_classroom.html', context)


def classroom_update(request, classroom_id):
	if request.user.is_anonymous:
		return redirect('signin')
	classroom = Classroom.objects.get(id=classroom_id)
	form = ClassroomForm(instance=classroom)
	if request.method == "POST":
		form = ClassroomForm(request.POST, request.FILES or None, instance=classroom)
		if form.is_valid():
			form.save()
			messages.success(request, "Successfully Edited!")
			return redirect('classroom-list')
		print (form.errors)
	context = {
	"form": form,
	"classroom": classroom,
	}
	return render(request, 'update_classroom.html', context)


def classroom_delete(request, classroom_id):
	if request.user.is_anonymous:
		return redirect('signin')
	Classroom.objects.get(id=classroom_id).delete()
	messages.success(request, "Successfully Deleted!")
	return redirect('classroom-list')


def signup(request):
	form = SignupForm()    
	if request.method == 'POST':
		form = SignupForm(request.POST)    
		if form.is_valid():
			user = form.save(commit=False)
			user.set_password(user.password)
			user.save()
			login(request, user)
			return redirect("classroom-list")
	context = {
		"form":form,
	}
	return render(request, 'signup.html', context)     

def signin(request):                         
	form = SigninForm()
	if request.method == 'POST':
		form = SigninForm(request.POST)             
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			auth_user = authenticate(username=username, password=password)
			if auth_user is not None:
				login(request, auth_user) 
				return redirect('classroom-list')              
	context = {
		"form":form
	}
	return render(request, 'signin.html', context)     


def signout(request):
	logout(request)
	return redirect("signin")




# def student_list(request):
# 	student = Student.objects.all().order_by("name")
# 	context = {
# 		"student": student,
# 	}
# 	return render(request, 'student_list.html', context)



def student_create(request,classroom_id):
	if request.user.is_anonymous:
		return redirect('signin')
	form = Studentform()
	classroom_obj = Classroom.objects.get(id=classroom_id)   
	if request.method == "POST":
		form = Studentform(request.POST, request.FILES or None)  # what des or none do ??
		if form.is_valid():
			student=form.save(commit=False)
			student.classroom = classroom_obj     
			student.save()
			messages.success(request, "Successfully Created!")
			return redirect('classroom-detail' , classroom_obj.id )       
		print (form.errors)
	context = {
	"form": form,
	"classroom_obj":classroom_obj    
	}
	return render(request, 'create_student.html', context)


def student_update(request, student_id):
	if request.user.is_anonymous:
		return redirect('signin')
	student_obj = Student.objects.get(id=student_id)
	form = Studentform(instance=student_obj)
	if request.method == "POST":
		form = Studentform(request.POST, request.FILES or None, instance=student_obj)  # What does this do
		if form.is_valid():
			form.save()
			messages.success(request, "Successfully Updated!")
			return redirect('classroom-detail',  student_obj.classroom.id )     
		print (form.errors)
	context = {
	"form": form,
	"student_obj": student_obj,
	}
	return render(request, 'update_student.html', context)


def student_delete(request, student_id):
	if request.user.is_anonymous:
		return redirect('signin')
	student_obj=Student.objects.get(id=student_id)
	student_obj.delete()
	messages.success(request, "Successfully Deleted!")
	return redirect("classroom-detail", student_obj.classroom.id)
