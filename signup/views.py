from django.shortcuts import render
from .models import SignUp
from rest_framework.views import APIView
from rest_framework.serializers import ValidationError
from requirements import success, error
from django.db import IntegrityError
from rest_framework.response import Response
from .serializers import SignUpSerializer,LoginSerializer
from django.shortcuts import get_object_or_404

import hashlib 
import re 
import datetime

class SignUpView(APIView):

    def post(self, request):
        try:
            if len(request.data['Password']) != 8:
                raise InvalidPassword("Password length must be 8")
            if bool(re.match('[a-zA-Z\s]+$', request.data['Name'])) is False:
                raise InvalidName("Name must contain only Alphabets and spaces")

            serializer = SignUpSerializer(data = request.data)
            _mutable = request.data._mutable
            request.data._mutable = True
            request.data['Password'] = hashlib.md5(request.data['Password'].encode('utf-8')).hexdigest()
            request.data._mutable = _mutable

            if serializer.is_valid(raise_exception = True):
                saved_object = serializer.save()
            success_message = "Data added successfully"
            response = success.APIResponse(201, success_message).respond()
        
        except ValidationError as validation_error:
            err = validation_error.__dict__
            response        = error.APIErrorResponse(409, err['detail']).respond()

        except IntegrityError:
            error_message = "Database integrity error occured"
            response      = error.APIErrorResponse(409, error_message).respond()
        
        except InvalidPassword as passwordError:
            response = error.APIErrorResponse(404, str(passwordError)).respond()

        except InvalidName as nameError:
            response = error.APIErrorResponse(404, str(nameError)).respond()

        except Exception as e:
            error_message   = "unexpected error occured"
            response        = error.APIErrorResponse(400, str(e), error_message).respond()

        finally:
            return Response(response)
    
class LoginView(APIView):
     def post(self, request):
        try:
            Password = hashlib.md5(request.data['Password'].encode('utf-8')).hexdigest()
            if(SignUp.objects.filter(Username=request.data['Username'],Password=Password).exists() is False):
                raise LoginFail("Invalid Login Credentials")
            queryset    = SignUp.objects.get(Username=request.data['Username'])
            serializer  = LoginSerializer(queryset)
            response = success.APIResponse(200, serializer.data).respond()
        
        except LoginFail as loginfail:
            response = error.APIErrorResponse(404, str(loginfail)).respond()

        except Exception as e:
            response = error.APIErrorResponse(400, str(e)).respond()
            return Response(response, status=400)

        finally:
            return Response(response)




class InvalidPassword(Exception):
    pass

class InvalidName(Exception):
    pass

class LoginFail(Exception):
    pass
