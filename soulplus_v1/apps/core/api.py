from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import (TokenAuthentication,
                                           SessionAuthentication)
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

import json
import random
from core.models import  UserProfile, Action, Notification, Comment, Like, PrivateGroup, CalendarAction, Friend
from django.contrib.auth.models import User
from django.core import serializers
from django.http import HttpResponse 

from django.core.validators import validate_email
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
 
from allauth.socialaccount import providers
from allauth.socialaccount.models import SocialLogin, SocialToken, SocialApp
from allauth.socialaccount.providers.facebook.views import fb_complete_login
from allauth.socialaccount.helpers import complete_social_login
import threading


class AccountSignup(APIView):
    #authentication_classes = (SessionAuthentication, TokenAuthentication)
    #permission_classes = (IsAuthenticated,)
    #renderer_classes = (JSONRenderer,)
    def post(self, request, format=None):
        """ sign up new account. """
        if request.META.get('CONTENT_TYPE') is None:
            return Response({'error':"invalid_header"},status=status.HTTP_400_BAD_REQUEST)
        else:
            if request.META.get('CONTENT_TYPE') == "application/json":
                if request.data['signup_type']:
                    if request.data['signup_type'] == "phone":
                        if UserProfile.objects.filter(phonenumber = request.data['phonenumber']).exists():
                            return Response({'status':'phone_existed'},status=802)
                        else:
                            newuser = User.objects.create_user(username=request.data['phonenumber'],password=request.data['password'])
                            UserProfile.objects.create(user=newuser,phonenumber=request.data['phonenumber'])
                            return Response({'status':"success"}, status=status.HTTP_200_OK)
                    if request.data['signup_type'] == "email":
                        if User.objects.filter(email = request.data['email']).exists():
                            return Response({'status':'email_existed'},status=801)
                        else:
                            newuser = User.objects.create_user(username=request.data['email'],email=request.data['email'],password=request.data['password'])
                            UserProfile.objects.create(user=newuser)
                            return Response({'status':"success"}, status=status.HTTP_200_OK)
                else: 
                    return Response({'error': "missing_or_invalid_params"}, status=402)
            else:
                return Response({'error':"unsupport_type"},status=403)
        
class AccountSignin(APIView):
    def post(self, request, format=None):
        """ sign up new account. """
        if not (("email" in request.data and "password" in request.data and "signin_type" in  request.data) or ("phonenumber" in request.data and "password" in request.data and "signin_type" in request.data)):
            return Response({'error': "missing_params"}, status=status.HTTP_400_BAD_REQUEST)

        if request.data['signin_type'] == "email":
            emailinput = str(request.data['email'])
            passwordinput = str(request.data['password'])
            print emailinput, passwordinput
            valid_email = True
            try:
                validate_email(emailinput)
                valid_email = True
            except :
                valid_email = False
            if ((len(passwordinput) < 3) or not valid_email):
                return Response({"error":"Invalid_password_or_email"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                if User.objects.get(email=emailinput).check_password(passwordinput):
                    return Response({'status':"success" ,'userid':User.objects.get(email=emailinput).pk}, status=status.HTTP_200_OK)

                else:
            
                    return Response({'status':"password_incorrect"}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error":"user_does_not_exist"},status=400)
        if request.data['signin_type'] == "phone":
            phonenumber = str(request.data['phonenumber'])
            password = str(request.data['password'])
            if len(password) < 3 or len(phonenumber) < 8 or len (phonenumber)>13:
                return Response({"error":"invalid_params"},status=400)
            try:
                if User.objects.get(username=phonenumber).check_password(password):
                    return Response({'status':"success" ,'userid':User.objects.get(username=phonenumber).pk}, status=status.HTTP_200_OK)

                else:
                    return Response({'status':"password_incorrect"}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error":"user_does_not_exist"},status=400)

class FacebookSignin(APIView):
   # permission_classes = (AllowAny,)
    
    # this is a public api!!!
   # authentication_classes = (EverybodyCanAuthentication,)
             
    def dispatch(self, *args, **kwargs):
        return super(FacebookSignin, self).dispatch(*args, **kwargs)
    
    def post(self, request):        
        data = JSONParser().parse(request)
        access_token = data.get('access_token', '')    
        
        try:
            app = SocialApp.objects.get(provider="facebook")
            token = SocialToken(app=app, token=access_token)
                            
            # check token against facebook                  
            login = fb_complete_login(app, token)
            login.token = token
            login.state = SocialLogin.state_from_request(request)
        
            # add or update the user into users table
            ret = complete_social_login(request, login)
 
            # if we get here we've succeeded
            return Response(status=200, data={
                'status': "success",
                'user_id': request.user.pk,
            })
            
        except:
 
            return Response(status=401 ,data={
                'status': "fail",
                'error': "Bad_Access_Token",
            })

class LostPassword(APIView):
    def post(self, request, format=None):
        return
class ListAction(APIView):
    def post(self, request, format=None):
        #actions = Action.objects.order_by('?')[:20]
        
        response_message = []
        sample = random.sample(xrange(Action.objects.count()),3)
        result = []
        try:
            result = [Action.objects.all()[i] for i in sample] 
            for j in range(0,3):
                action = result[j]
                resultjson = {'title':action.title,'content':action.content, 'actionid':action.pk, 'avatarurl':action.firstPicture.url}
                response_message.append(resultjson)
        #return HttpResponse(serializers.serialize("json", actions))
            response_message_json = {'status':"success",'action':response_message}
            return Response(status=200 ,data=response_message_json)
        except:
            return Response(status=401 ,data={'status': "fail"})

class GetNotifications(APIView):
    def post(self, request, format=None):
        userid = request.data['userid']
        return Response(status=200 ,data={'success': False})

class GetMyAction(APIView):
    def post(self, request, format=None):
        return Response(status=200 ,data={'success': False})
    
def createfriend(userid,friendid):
    Friend.objects.create(userid=userid,friendid=friendid)

class CreateFriend(APIView):
    def post(self, request, format=None):
        try:
            createfriend(request.data['userid'],request.data['friendid']) 
            return Response({'status':"success"},status=200)
        except:
            return Response({'status':"fail"},status=201)
def updatenotification(userpk,actionid):
    try:
        friends = Friend.objects.filter(userid=userpk)
        print "number of friend", friends.count()
        for friend in friends:
            print "creating notification"
            Notification.objects.create(userid=friend.friendid,notificationtype='Liked',friend_like_id=userpk,actionlikedid=actionid)
            print "success"
    except Exception as e:
        print e      
         
class LikeAction(APIView):
    def post(self, request, format=None):
        userpk = request.data["userpk"]
        actionpk = request.data["actionpk"]
        print userpk 
        try:
            Like.objects.create(userid=int(userpk),actionid=int(actionpk))
            t = threading.Thread(target=updatenotification(userpk=userpk,actionid=actionpk))
            t.start()
            return Response(status=200,data={'status':"success"})
        except Exception as e:
            print e
            return Response(status=400,data={'error': "fail"})

class GetLikesAction(APIView):
    def post(self, request, format=None):
        actionid = request.data["actionid"]
        try:
            result = Like.objects.filter(actionid=actionid)
            print result
            number_of_likes = result.count()
            print number_of_likes
            users_liked = []
            for i in range(0, number_of_likes):
                user_liked_id = result[i].userid
                try:
                    user_avatar = UserProfile.objects.get(pk=user_liked_id).avatar.url
                    user_liked_json={"userid":user_liked_id,"avatar":user_avatar}
                    users_liked.append(user_liked_json)
                except:
                    user_liked_json={"userid":user_liked_id}
                    users_liked.append(user_liked_json)
            
            return Response(status=200,data={'status':"success",'likes_number':number_of_likes,'users_liked':users_liked})
        except Exception as e:
            print e
            return Response(status=200 ,data={'status': "fail"})

class Comment(APIView):
    pass

class SendInvitation(APIView):
    pass

class AcceptInvitation(APIView):
    pass
