from rest_framework import serializers

from .models import (User, InvestorUser, CompanyUser, AnalystUser, InvestorUserAddress,
                     IDVerification, InvestorVerification, VerificationCode, UserLog)

from ..companies.models import Company


class BasicCompanySerializer(serializers.ModelSerializer):
	class Meta:
		model = Company
		fields = ('id', 'name', 'logo', 'short_description', 'website',
		          'created', 'updated',)
		read_only_fields = ('created', 'updated',)


class FullUserSerializer(serializers.ModelSerializer):
	"""
	Full Serializer for User
	"""

	class Meta:
		model = User
		fields = ('id', 'email', 'phone_country_code', 'phone',
		          'last_login', 'last_login_ip', 'TOTP_enabled',
		          'is_investor', 'is_company_user', 'is_analyst', 'is_active',
		          'created', 'updated',)
		read_only_fields = ('created', 'updated',)


class BasicUserSerializer(serializers.ModelSerializer):
	"""
	Basic Serializer to build nested json feed for InvestorUser, CompanyUser and AnalystUser
	"""

	class Meta:
		model = User
		fields = ('id', 'email', 'phone_country_code', 'phone', 'TOTP_enabled',
		          'is_investor', 'is_company_user', 'is_analyst')


class BaseUserAddressSerializer(serializers.ModelSerializer):
	class Meta:
		model = InvestorUserAddress
		fields = ('address1', 'address2', 'city', 'state', 'zipcode', 'country',)


class CreateUserSerializer(serializers.ModelSerializer):
	"""
	Serializer for user sign up
	"""

	class Meta:
		model = User
		fields = ('id', 'email', 'password', 'refer_source', 'last_login_ip',)
		extra_kwargs = {'password': {'write_only': True}}

	def create(self, validated_data):
		user = User(
			email=validated_data['email'],
			last_login_ip=validated_data['last_login_ip'],
			refer_source=validated_data['refer_source']
		)
		user.set_password(validated_data['password'])
		user.save()
		user.update_last_login()

		return user


class FullInvestorUserSerializer(serializers.ModelSerializer):
	"""
	Full Serializer for InvestorUser
	"""
	user = BasicUserSerializer()
	address = BaseUserAddressSerializer(many=True)

	class Meta:
		model = InvestorUser
		fields = ('id', 'user',
		          'first_name', 'last_name', 'birthday', 'nationality', 'address',
		          'verification_level', 'id_verification', 'accredited_investor_verification',
		          'created', 'updated',)
		read_only_fields = ('created', 'updated',)


class FullCompanyUserSerializer(serializers.ModelSerializer):
	user = BasicUserSerializer()
	company = BasicCompanySerializer()

	class Meta:
		model = CompanyUser
		fields = ('user',
		          'company',
		          'created', 'updated',)
		read_only_fields = ('created', 'updated',)


class FullAnalystUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = AnalystUser
		fields = ('user',
		          'avatar', 'first_name', 'last_name',
		          'analyst_type',
		          'created', 'updated',)
		read_only_fields = ('created', 'updated',)


class FullIDVerificationSerializer(serializers.ModelSerializer):
	class Meta:
		model = IDVerification
		fields = ('investor_user',
		          'official_id_type', 'official_id_back_base64', 'official_id_front_base64', 'user_holding_official_id_base64',
		          'created', 'updated',)
		read_only_fields = ('created', 'updated',)


class FullInvestorVerificationSerializer(serializers.ModelSerializer):
	class Meta:
		model = InvestorVerification
		fields = ('doc_type', 'doc1', 'doc2',)


class FullVerificationCodeSerializer(serializers.ModelSerializer):
	class Meta:
		model = VerificationCode
		fields = ('user', 'code', 'expire_time',)
		read_only_fields = ('expire_time', 'code',)


class FullUserLogVerificationSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserLog
		fields = ('action', 'ip', 'device', 'datetime',)
		read_only_fields = ('action', 'ip', 'device', 'datetime',)


class BasicInvestorUserSerializer(serializers.ModelSerializer):
	# TODO get email, full name, eth amount, country
	class Meta:
		model = InvestorUser
		fields = ('full_name', 'email', 'nationality')
