from rest_framework import serializers
from .models import SignUp
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = SignUp
        fields = ('__all__')

    validators = [
            UniqueTogetherValidator(
                queryset=SignUp.objects.all(),
                fields=['Username']
            )
        ]
    extra_kwargs = {
            'Username' : {
                'validators' : [UniqueValidator(queryset = SignUp.objects.all())]
            }
    }
class LoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = SignUp
        fields = ('Userid','Username','Name','Email','Phone')
