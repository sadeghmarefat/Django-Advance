from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


from ...models import User,Profile

class UserSerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField(max_length=128, write_only=True)
    class Meta:
        model = User
        fields = ['email', 'password', 'password_confirmation']


    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirmation']:
            raise serializers.ValidationError("Passwords do not match.")

        try:
            validate_password(attrs['password'])
        except DjangoValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirmation', None)
        validated_data.pop('password', None)
        return User.objects.create_user(**validated_data)



class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(
        label=_("email"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        username = attrs.get('email')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
            if not user.is_verified:
                msg = _('User is not verified.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['user_id'] = user.id
        token['email'] = user.email

        return token



    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        if not user.is_verified:
            msg = _('User is not verified.')
            raise serializers.ValidationError(
                msg,
                code='authorization'
            )

        data['user_id'] = user.id
        data['email'] = user.email

        return data


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        required=True,
        write_only=True,
        style = {'input_type': 'password'}
    )
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        style = {'input_type': 'password'}
    )
    confirm_password = serializers.CharField(
        required=True,
        write_only=True,
        style = {'input_type': 'password'}
    )

    def validate_old_password(self, value):
        user = self.context['request'].user

        if not user.check_password(value):
            raise serializers.ValidationError(
                'Current password is incorrect.'
            )

        return value

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({
                'confirm_password': 'Passwords do not match.'
            })

        validate_password(
            attrs['new_password'],
            user=self.context['request'].user
        )

        return attrs

class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        source='user.email',
        read_only=True
    )
    first_name = serializers.CharField(
        source='user.first_name'
    )

    class Meta:
        model = Profile
        fields = ['id', 'email', 'first_name', 'last_name','bio','profile_picture']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})

        instance.last_name = validated_data.get(
            'last_name',
            instance.last_name
        )
        instance.bio = validated_data.get(
            'bio',
            instance.bio
        )
        instance.profile_picture = validated_data.get(
            'profile_picture',
            instance.profile_picture
        )
        instance.save()

        if 'first_name' in user_data:
            instance.user.first_name = user_data['first_name']
            instance.user.save(update_fields=['first_name'])

        return instance


class ReSendActivationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError('User with this email does not exist.')
        return value