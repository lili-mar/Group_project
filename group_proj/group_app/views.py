from django.shortcuts import render, HttpResponse, redirect
from .models import *  # import ALL models
from django.contrib import messages  # validation
import bcrypt  # password encryption
from django.conf import settings  # map settings
from datetime import datetime  # events/activities date -time


def index(request):
    request.session.flush()
    return render(request, 'index.html')


def login(request):
    if request.method == 'POST':
        print(request.POST)  # should see QueryDict

        errors = User.objects.login_validator(request.POST)
        print(errors)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)

            return render(request, 'partialMsgs.html')  # AJAX!!!
            # return redirect('/ABC')    #redirect the user back to the form to fix the errors
        else:

            this_user = User.objects.get(email=request.POST['email'])
            request.session['user_id'] = this_user.id
            # messages.success(request, "You have successfully logged in!")
            return redirect('/ABC/myEvents')


def regForm(request):
    # request.session.flush()
    return render(request, 'regForm.html')


def register(request):
    if request.method == 'POST':
        print(request.POST)  # should see QueryDict

        errors = User.objects.reg_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return render(request, 'partialMsgs.html')  # AJAX!!!
            # return redirect('/ABC/regForm')    #redirect the user back to the form to fix the errors
        else:
            hashed_pw = bcrypt.hashpw(
                request.POST['password'].encode(), bcrypt.gensalt()).decode()
            new_user = User.objects.create(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                email=request.POST['email'],
                password=hashed_pw)
            request.session['user_id'] = new_user.id
            # messages.success(request, "You have successfully registered!")
            return redirect('/ABC/dashboard')


def childForm(request):
    if 'user_id' not in request.session:
        return redirect('/ABC')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user,
    }
    return render(request, 'childForm.html', context)


def regChild(request):
    # see "register" -here it needs the Child model
    if request.method == "POST":
        # class Child(models.Model):
        # def child_validator(self, postData):
        errors = Child.objects.child_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            # redirect the user back to the form to fix the errors
            return redirect('/ABC/childForm')

        else:
            user = User.objects.get(id=request.session['user_id'])

            Child.objects.create(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                birth_date=request.POST['birth_date'],
                gender=request.POST['child_gender'],
                grade=request.POST['child_grade'],
                parent_child=user,
            )

    # when successful Register a Child is click redirect back to myProfile
    return redirect('/ABC/myProfile')


def myProfile(request):
    if 'user_id' not in request.session:
        return redirect('/ABC')
    user = User.objects.get(id=request.session['user_id'])
    children = user.enrolled_parent.all()
    context = {
        'user': user,
        'children': children,
    }
    return render(request, 'myProfile.html', context)


def update_myProfile(request):
    if request.method == "POST":
        hashed_pw = bcrypt.hashpw(
            request.POST['password'].encode(), bcrypt.gensalt()).decode()
        user = User.objects.get(id=request.session['user_id'])
        user.password = hashed_pw
        user.save()
        return redirect('/ABC/dashboard')


def remove_child_myProfile(request):
    if 'user_id' not in request.session:
        return redirect('/ABC')
    else:
        if request.method == "POST":
            child = Child.objects.get(id=request.POST['child_id'])
            child.delete()
            return redirect('/ABC/myProfile')
        else:
            return redirect('/ABC')


def myEvents(request):
    if 'user_id' not in request.session:
        return redirect('/ABC')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user,
    }
    return render(request, 'myEvents.html', context)


def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/ABC')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user,
    }
    return render(request, 'dashboard.html', context)


def newJoin(request, id):
    if 'user_id' not in request.session:
        return redirect('/ABC')
    user = User.objects.get(id=request.session['user_id'])
    children = user.enrolled_parent.all()
    events = Event.objects.get(id=id)
    context = {
        'user': user,
        'children': children,
        'events': events,
    }
    return render(request, 'newJoin.html', context)


def confirmJoin(request):
    if 'user_id' not in request.session:
        return redirect('/ABC')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user,
    }
    return render(request, 'confirmJoin.html', context)


def logout(request):
    request.session.clear()
    return redirect('/ABC')
