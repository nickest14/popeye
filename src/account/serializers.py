import re
from rest_framework.response import Response
from rest_framework import serializers
from popeye.libs import constants
from account.models import User


class MemberRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'line', 'phone', 'nickname']

    def to_internal_value(self, data):
        request = self.context.get('request')
        ret = super().to_internal_value(data)
        ret['password'] = request.data.get('password')
        ret['confirm_password'] = request.data.get('confirm_password', None)
        return ret

    def validate(self, data):
        username = data.get('username')
        if not re.match('^[a-zA-Z0-9]{4,15}$', username):
            raise serializers.ValidationError(f'{constants.FIELD_ERROR}: '
                                              f'{constants.USERNAME_ERROR}')
        password_pattern = re.compile('^[a-zA-Z0-9]{6,15}$')
        if not password_pattern.match(data.get('password')):
            raise serializers.ValidationError(f'{constants.FIELD_ERROR}: '
                                              f'{constants.PASSWORD_ERROR}')
        # check if password and confirmation password matched
        if not data.get('password') == data.get('confirm_password', None):
            raise serializers.ValidationError(
                f'{constants.FIELD_ERROR}: {constants.PASSWORD_NOT_MATCH}')
        data.pop('confirm_password')
        nickname = data.get('nickname', None)
        if not nickname or not re.match(
                '^[a-zA-Z0-9\u4e00-\u9fa5]{2,10}$', nickname):
            raise serializers.ValidationError({constants.FIELD_ERROR:
                                               constants.INVALID_REALNAME})
        phone = data.get('phone', None)
        if phone and not re.match('^[0-9]{10}$', phone):
            raise serializers.ValidationError({
                constants.FIELD_ERROR: constants.INVALID_PHONE})
        return data

    def create(self, validated_data):
        """
        @brief
            Member registration serializer
        """

        user = User.objects.create_user(**validated_data)
        return user


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'line', 'phone', 'nickname']

    def to_internal_value(self, data):
        request = self.context.get('request')
        ret = super().to_internal_value(data)
        if request.data.get('username'):
            ret.pop('username')
        if request.data.get('role'):
            ret.pop('role')
        if request.data.get('password'):
            ret['password'] = request.data.get('password')
            ret['confirm_password'] = request.data.get('confirm_password', None)
        return ret

    def validate(self, data):
        print(data)
        password = data.get('password')
        password_pattern = re.compile('^[a-zA-Z0-9]{6,15}$')
        if password and not password_pattern.match(password):
            raise serializers.ValidationError(f'{constants.FIELD_ERROR}: '
                                              f'{constants.PASSWORD_ERROR}')
        # check if password and confirmation password matched
        password = data.get('password')
        if password and not password == data.get('confirm_password', None):
            raise serializers.ValidationError(
                f'{constants.FIELD_ERROR}: {constants.PASSWORD_NOT_MATCH}')
        data.pop('confirm_password')
        nickname = data.get('nickname', None)
        if not nickname or not re.match(
                '^[a-zA-Z0-9\u4e00-\u9fa5]{2,15}$', nickname):
            raise serializers.ValidationError({constants.FIELD_ERROR:
                                               constants.INVALID_REALNAME})
        phone = data.get('phone', None)
        if phone and not re.match('^[0-9]{10}$', phone):
            raise serializers.ValidationError({
                constants.FIELD_ERROR: constants.INVALID_PHONE})
        return data

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        password = validated_data.get('password')
        if password:
            instance.set_password(password)
            instance.save()
        return instance


class TestSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username']
