from rest_framework import serializers
from account.models import User


class MemberRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',
                  'real_name',
                  'phone',
                  'withdraw_password',
                  'email',
                  'account_type',
                  'realname_repeated',
                  'referring_url')

    # def to_internal_value(self, data):
    #     request = self.context.get('request')
    #
    #     ret = super().to_internal_value(data)
    #     ret['password'] = request.data.get('password')
    #     ret['confirmation_password'] = \
    #         request.data.get('confirmation_password')
    #     ret['verification_code_0'] = request.data.get('verification_code_0')
    #     ret['verification_code_1'] = request.data.get('verification_code_1')
    #     ret['sms_code'] = request.data.get('sms_code', None)
    #     return ret

    # def validate(self, data):
    #     request = self.context.get('request')
    #     validated_data = {}
    #     if request.method == 'POST':
    #         if self.get_account_type(data) == ACCOUNT_TYPE_TRIAL_MEMBER:
    #             # skip validation for trial member creation
    #             return data
    #
    #         required_fields = (
    #             'username',
    #             'password',
    #             'confirmation_password',
    #             'real_name',
    #             'withdraw_password')
    #         RequiredFieldValidator.validate(data, required_fields)
    #
    #         # captcha or sms validate
    #         sms_enabled = GlobalPreferences.objects.get(
    #             key='sms_validation_enabled').value
    #         if sms_enabled == 'true':
    #             # check the sms code is valid
    #             sms_code = data.get('sms_code', None)
    #             phone = data.get('phone')
    #             if sms_code is not None:
    #                 code = cache.get(f'sms_code_{phone}', None)
    #                 if code is None:
    #                     raise serializers.ValidationError(
    #                         {constants.NOT_OK:
    #                              _('This phone does not have sms code yet')})
    #                 if str(code) != str(sms_code):
    #                     raise serializers.ValidationError(
    #                         constants.INVALID_SMS_CODE)
    #             else:
    #                 raise serializers.ValidationError(constants.LACK_SMS_CODE)
    #         else:
    #             # check if verification code is valid
    #             captcha = {
    #                 'verification_code_0': data.get('verification_code_0'),
    #                 'verification_code_1': data.get('verification_code_1')
    #             }
    #             verified = verification_codes(captcha)
    #             if verified is False:
    #                 raise serializers.ValidationError(
    #                     constants.INVALID_CAPTCHA)
    #
    #         # check if username is already in used
    #         user_check = User.objects.filter(username=data.get('username'))
    #
    #         if user_check:
    #             raise serializers.ValidationError({constants.FIELD_ERROR:
    #                                                constants.USERNAME_IN_USED})
    #         username = data.get('username')
    #         if not re.match('^[a-zA-Z0-9]{6,15}$', username):
    #             raise serializers.ValidationError({constants.FIELD_ERROR:
    #                                                constants.INVALID_USERNAME})
    #
    #         validated_data['username'] = username
    #
    #         # check if password and confirmation password matched
    #         if not data.get('password') == data.get('confirmation_password'):
    #             raise \
    #                 serializers.ValidationError({constants.FIELD_ERROR:
    #                                              constants.PASSWORD_NOT_MATCHED})
    #
    #         pattern = re.compile('^[a-zA-Z0-9]{6,15}$')
    #         msg = _('Password must be 6 to 15 alphanumeric characters')
    #         if not pattern.match(data.get('password')):
    #             raise serializers.ValidationError({constants.FIELD_ERROR: msg})
    #
    #         validated_data['password'] = data.get('password')
    #
    #         withdraw_password = data.get('withdraw_password')
    #         if not re.match('^[\d]{6}$', withdraw_password):
    #             raise serializers.ValidationError({constants.FIELD_ERROR:
    #                                                constants.INVALID_WITHDRAW_PASSWORD})
    #         validated_data['withdraw_password'] = withdraw_password
    #
    #         # Can't register without domain to prevent bot.
    #         if not self.__get_domain(request):
    #             raise serializers.ValidationError(constants.NOT_ALLOWED)
    #
    #         agent = self.get_agent(request)
    #
    #         validated_data['agent'] = agent
    #         validated_data['level'] = agent.default_member_lv
    #
    #         # real name
    #         real_name = data.get('real_name')
    #
    #         if not re.match('^[\u4e00-\u9fa5]{2,10}$', real_name):
    #             raise serializers.ValidationError({constants.FIELD_ERROR:
    #                                                constants.INVALID_REALNAME})
    #
    #         try:
    #             black_list = set(GlobalPreferences.objects.get(
    #                 key='register_black_list').value.split(','))
    #         except:
    #             black_list = set()
    #         if real_name in black_list:
    #             raise serializers.ValidationError(
    #                 {constants.NOT_OK: constants.REAL_NAME_NOT_ALLOWED})
    #
    #         try:
    #             allow_same_rname = GlobalPreferences.objects.get(
    #                 key='is_allow_register_same_real_name').value
    #         except:
    #             allow_same_rname = True
    #
    #         is_duplicated_name = \
    #             Member.objects.filter(real_name=real_name).exists()
    #
    #         if allow_same_rname == 'false' and is_duplicated_name:
    #             raise serializers.ValidationError(
    #                 {constants.FIELD_ERROR: constants.REALNAME_IN_USED})
    #
    #         validated_data['real_name'] = real_name
    #         if is_duplicated_name:
    #             validated_data['realname_repeated'] = True
    #
    #         validated_data['phone'] = data.get('phone')
    #         # validate phone
    #         if validated_data['phone'] and not re.match(
    #                 '^[1][3-9]\d{9}$', validated_data['phone']):
    #             raise serializers.ValidationError({
    #                 constants.FIELD_ERROR: constants.INVALID_PHONE})
    #
    #         # validate email
    #         email = data.get('email')
    #         if email:
    #             try:
    #                 validate_email(email)
    #             except:
    #                 raise serializers.\
    #                     ValidationError({constants.FIELD_ERROR:
    #                                      constants.INVALID_EMAIL})
    #             validated_data['email'] = email
    #
    #         # set status to active
    #         validated_data['status'] = 1
    #
    #         # get/set register_ip
    #         ipaddr = get_ip_addr(request)
    #         validated_data['register_ip'] = ipaddr
    #
    #         # check if register ip is already used
    #         ip_repeated = \
    #             Member.objects.filter(register_ip=ipaddr,
    #                                   ).exists()
    #         if ip_repeated:
    #             validated_data['ip_repeated'] = True
    #
    #         validated_data['account_type'] = \
    #             data.get('account_type', ACCOUNT_TYPE_REAL_MEMBER)
    #
    #         # Check the member is registered from pc or mobile
    #         is_pc = request.user_agent.is_pc
    #         validated_data['platform_registered'] = 'pc' if is_pc else 'mobile'
    #
    #         referring_url = data.get('referring_url')
    #         if referring_url:
    #             validated_data['referring_url'] = referring_url
    #
    #     return validated_data
    #
    #
    # def create(self, validated_data):
    #     """
    #     @fn create
    #     @brief
    #         Member registration serializer for standalone website.
    #         This cannot be used by API mode because some of Members
    #         fields are not applicable with that mode.
    #     """
    #
    #     account_type = self.get_account_type(validated_data)
    #     if account_type == ACCOUNT_TYPE_TRIAL_MEMBER:
    #         agent = Agent.objects.filter(pk=DEFAULT_AGENT_ID).first()
    #         validated_data['agent'] = agent
    #         validated_data['username'] = uuid.uuid4().hex
    #         validated_data['password'] = TRIAL_MEMBER_PASSWORD
    #         validated_data['real_name'] = _('Visitor')
    #
    #         try:
    #             validated_data.pop('verification_code_0')
    #         except KeyError:
    #             pass
    #         try:
    #             validated_data.pop('verification_code_1')
    #         except KeyError:
    #             pass
    #     password = validated_data.pop('password')
    #     # parameters are already validated at this point
    #     user = User.objects.create_user(username=validated_data['username'],
    #                                     password=password)
    #
    #
    #     return member