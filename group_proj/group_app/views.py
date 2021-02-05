from django.shortcuts import render, HttpResponse, redirect
from .models import *  # import ALL models
from django.contrib import messages  # validation
import bcrypt  # password encryption
from django.conf import settings  # map settings
from datetime import datetime  # events/activities date -time


def index(request):
    request.session.flush()
    return render(request, 'index.html')

def logout(request):
    request.session.flush()
    return redirect('/ABC')

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
    if request.method == "POST":

        errors = Child.objects.child_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/ABC/childForm')  # redirect the user back to the form to fix the errors

        else:
            user = User.objects.get(id=request.session['user_id'])

            Child.objects.create(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                birth_date=request.POST['birth_date'],
                gender=request.POST['child_gender'],
                age=request.POST['child_age'],
                program=request.POST['child_program'],
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
        errors = User.objects.password_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/ABC/myProfile')
        else:
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

def remove_event_myEvents(request):
    # if 'event_id' not in request.session:
    #     return redirect('/ABC/myEvents')
    # else:
    if request.method == "POST":
        event= Event.objects.get(id=request.POST['event_id'])
        event.delete()
        return redirect('/ABC/myEvents')
    else:
        return redirect('/ABC')

def myEvents(request):
    if 'user_id' not in request.session:
        return redirect('/ABC')
    user = User.objects.get(id=request.session['user_id'])
    past_events=Event.objects.filter(event_date__lte = datetime.today())
    future_events=Event.objects.filter(event_date__gte = datetime.today())
    context = {
        'user': user,
        'past_events': past_events,
        'future_events':future_events,
    }
    return render(request, 'myEvents.html', context)


def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/ABC')
    user = User.objects.get(id=request.session['user_id'])
    events = Event.objects.all()

    context = {
        'user': user,
        'events': events,
        # 'total_num': total_num,
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


# ----Lily's work in progress ---------------------------------------

def confirmJoin(request, event_id):
    this_event = Event.objects.filter(id=event_id)  #d_id comes from the urls.py parm.  FILTER is SO important here -do not use GET!       
    if len(this_event) != 1:
        return redirect('/ABC/dashboard')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'one_event': this_event[0],  #need this because it is a list.  grab "value" to initially populate record for the update/view
        'user': user,
        'api_key': settings.SECRET_KEY2,  #if inspect -unfortunately you can still see the key!
        'messages_list': this_event[0].eventmessages_join.all(), #only messages for this SPECIFIC event
    }
    return render(request, 'confirmJoin.html', context) 


def create_msg(request, event_id):
    this_event = Event.objects.filter(id=event_id) 
    Message.objects.create(
        msg_content=request.POST['msg_content'],
        msg_UsrJoin=User.objects.get(id=request.session['user_id']),  #comes from the login 
        msg_EventJoin=this_event[0], 
        )
    return redirect(f'/ABC/{event_id}/confirmJoin')

def create_comment(request, msg_id):
    this_msg = Message.objects.get(id=msg_id)
    Comment.objects.create(com_content=request.POST['com_content'],
        com_UserJoin=User.objects.get(id=request.session['user_id']), #c#comes from the login 
        msg_CommJoin=this_msg,  #join the comment with the message
        )
    return redirect('/ABC/<int:event_id>/confirmJoin')

def delete_comment(request, comm_id):
    this_comm = Comment.objects.get(id=comm_id)
    this_Logged_user = User.objects.get(id=request.session['user_id'])

    if this_comm.com_UserJoin ==  this_Logged_user:  #only owner of comment can delete OR in html -just show "delete" to owner.  
        this_comm.delete()       
    return redirect('/ABC/<int:event_id>/confirmJoin')

def add_like(request, msg_id):
    liked_message = Message.objects.get(id=msg_id)
    user_liking = User.objects.get(id=request.session['user_id'])
    liked_message.user_likes.add(user_liking)
    return redirect('/ABC/<int:event_id>/confirmJoin')
def remove_like(request, msg_id):
    liked_message = Message.objects.get(id=msg_id)
    user_liking = User.objects.get(id=request.session['user_id'])
    liked_message.user_likes.remove(user_liking)
    return redirect('/ABC/<int:event_id>/confirmJoin')



