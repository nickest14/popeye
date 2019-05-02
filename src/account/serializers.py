import re
from rest_framework.response import Response
from rest_framework import serializers
from popeye.libs import constants
from account.models import User


class MemberRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def to_internal_value(self, data):
        request = self.context.get('request')
        ret = super().to_internal_value(data)
        ret['password'] = request.data.get('password')
        ret['confirm_password'] = \
            request.data.get('confirm_password', None)
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
        if not data.get('password', None) == \
               data.get('confirm_password', None):
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


class TestSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username']
