import bcrypt
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User

# Create your views here.
def index(request):
    return render(request, 'index.html')

def process_registration(request):
    # pass the post data to the meathod we wrote and save the response in a variable called errors
    errors = User.objects.registration_validator(request.POST)
        # check if the errors dictionary has anything in it
    if len(errors) > 0:
        # if the errors dictionary contains crap, loop through it
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the blog to be updated, make the changes, and save
        return redirect('/')
    else:
        # If the errors object is empty, that means there were no errors!
        # retrieve the user to be updated, make the changes and save
    
        tempFirstName = request.POST['reg_first_name']
        tempLastName = request.POST['reg_last_name']
        tempEmail = request.POST['reg_email']
        tempPassword = request.POST['reg_password']
        tempConfrim = request.POST['reg_confirm']
        pw_hash = bcrypt.hashpw(tempPassword.encode(), bcrypt.gensalt()).decode()
        print(pw_hash)
        new_user = User.objects.create(first_name=tempFirstName, last_name=tempLastName, user_email=tempEmail, password=pw_hash)
        messages.success(request, "User Successfully Created")
        if 'user_id' not in request.session:
            request.session['user_id'] = new_user.id
        return redirect('/success')

def process_login(request):
    # see if the username exists within the database
    user = User.objects.filter(user_email=request.POST['login_email'])
    if user: # tests to see if user is true
        logged_user = user[0]
        print(logged_user.id)
        if bcrypt.checkpw(request.POST['login_password'].encode(), logged_user.password.encode()):
            # if we get true after checking the password, we may put the user id in session
            if 'user_id' not in request.session:
                request.session['user_id'] = logged_user.id
                return redirect('/success')
                # if user was not found
        else:
            messages.error(request, "Yo password does not match")
            return redirect('/')
    else:
        messages.error(request, "Yo email is not found")
        return redirect('/')

def success(request):
    context = {
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request,'success.html',context)

def logout(request):
    request.session.clear()
    return redirect('/')