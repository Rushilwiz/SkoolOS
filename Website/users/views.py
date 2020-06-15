import json
import requests

from django.shortcuts import render, redirect

from requests_oauthlib import OAuth2Session
from django.contrib import messages

from .models import Token
from api.models import Student, Teacher

from .forms import UserCreationForm

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import os

# Create your views here.
# Thanks Django, what would I do without this comment

client_id = r'QeZPBSKqdvWFfBv1VYTSv9iFGz5T9pVJtNUjbEr6'
client_secret = r'0Wl3hAIGY9SvYOqTOLUiLNYa4OlCgZYdno9ZbcgCT7RGQ8x2f1l2HzZHsQ7ijC74A0mrOhhCVeZugqAmOADHIv5fHxaa7GqFNtQr11HX9ySTw3DscKsphCVi5P71mlGY'
redirect_uri = 'http://localhost:8000/callback/'
token_url = 'https://ion.tjhsst.edu/oauth/authorize/'
scope=["read"]

def register(request):
    oauth = OAuth2Session(client_id=client_id, redirect_uri=redirect_uri, scope=scope)
    authorization_url, state = oauth.authorization_url("https://ion.tjhsst.edu/oauth/authorize/")

    return render(request,"users/register.html", {"authorization_url": authorization_url})

def callback (request):
        if request.method == "GET":
            code = request.GET.get('code')
            state = request.GET.get("state")
            # Then if we get a response from Ion with the authorization code
            if code is not None and state is not None:
                print ("made it")
                # We send it back to fetch the acess_token
                payload = {'grant_type':'authorization_code','code': code,'redirect_uri':redirect_uri,'client_id':client_id,'client_secret':client_secret, 'csrfmiddlewaretoken': state}
                token = requests.post("https://ion.tjhsst.edu/oauth/token/", data=payload).json()
                headers = {'Authorization': f"Bearer {token['access_token']}"}
                print(token)

                # And finally get the user's profile!
                profile = requests.get("https://ion.tjhsst.edu/api/profile", headers=headers).json()
                print(profile)
                username = profile['ion_username']
                email = profile['tj_email']
                first_name = profile['first_name']
                last_name = profile['last_name']
                isStudent = profile['is_student']
                grade = profile['grade']['number']

                if User.objects.filter(username=username).count() != 0:
                    messages.success(request, "This user already exists!")
                    return redirect('/login/')
                else:
                    token = Token(username = username, email = email, first_name = first_name, last_name = last_name, isStudent = isStudent, grade=grade)
                    token.save()
                    tokenHash = token.token
                    print(f'/create_account/?token={tokenHash}')
                    return redirect(f'/create_account/?token={tokenHash}')


        messages.warning(request, "Invalid Callback Response")
        return redirect('/register/')


def create_account (request):
    if request.method == "POST":
        print("POSTPOSTPOSTPOSTPOSTPOSTPOSTPOST")
        form = UserCreationForm(request.POST)
        print(form.is_valid())
        print(request.POST)
        cleaned_data = form.clean()
        if cleaned_data.get('password') == cleaned_data.get('confirm_password'):
            token = Token.objects.get(token=cleaned_data.get('token'))
            username = token.username
            email = token.email
            first_name = token.first_name
            last_name = token.last_name
            isStudent = token.isStudent
            grade = token.grade
            git = cleaned_data.get('git')
            password = cleaned_data.get('password')



            user = User.objects.create_user(username=username,
                                            email=email,
                                            first_name=first_name,
                                            last_name=last_name,
                                            password=password)
            user.save()
            token.delete()

            if isStudent:
                profile = Student(user=user, git=git, grade=grade)
            else:
                profile = Teacher(user=user, git=git)

            profile.save()

            print (user)
            messages.success(request, "Your SkoolOS account has successfully been created")
            return redirect(f'/login/?username={username}')
        else:
            print(form.errors)
            Token.objects.get(token=request.GET.get('token')).delete()
            messages.warning(request, "Passwords did not match!")
            return redirect('/register/')

    if request.method == "GET" and Token.objects.filter(token=request.GET.get('token')).count() == 1:
        print("GETGETGETGETGETGET")
        token = Token.objects.get(token=request.GET.get('token'))
        username = token.username
        email = token.email
        first_name = token.first_name
        last_name = token.last_name
        isStudent = token.isStudent
        grade = token.grade

        initial = {
            'username': username,
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'grade': grade,
            'isStudent': isStudent,
            'token': token.token,
        }
        form  = UserCreationForm(initial=initial)
        return render(request, 'users/create_account.html', {'form': form})

    messages.warning(request, "Invalid token")
    return redirect('/register/')


@login_required
def logout(request):
    auth_logout(request)
    messages.success(request, "You've been logged out!")
    return redirect("/login")
