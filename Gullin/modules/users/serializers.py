from rest_framework import serializers

from .models import User, InvestorUser, CompanyUser, AnalystUser, IDVerification, InvestorVerification, VerificationCode


class FullUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'email', 'phone_country_code', 'phone',
		          'last_login', 'last_login_ip', 'TOTP_enabled',
		          'is_investor', 'is_company', 'is_analyst', 'is_active',
		          'created', 'updated',)
		read_only_fields = ('created', 'updated',)


class CreateUserSerializer(serializers.ModelSerializer):
	"""
	Serializer for user sign up
	"""

	class Meta:
		model = User
		fields = ('id', 'email', 'password', 'last_login_ip',)
		extra_kwargs = {'password': {'write_only': True}}

	def create(self, validated_data):
		user = User(
			email=validated_data['email'],
			last_login_ip=validated_data['last_login_ip']
		)
		user.set_password(validated_data['password'])
		user.save()
		user.update_last_login()
		return user


class FullInvestorUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = InvestorUser
		fields = ('user',
		          'avatar', 'first_name', 'last_name', 'nationality',
		          'verification_level', 'id_verification', 'accredited_investor_verification',
		          'created', 'updated',)
		read_only_fields = ('created', 'updated',)


class FullCompanyUserSerializer(serializers.ModelSerializer):
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
		fields = ('official_id_type', 'official_id', 'nationality')
		read_only_fields = ('official_id_type', 'official_id',)


class FullInvestorVerificationSerializer(serializers.ModelSerializer):
	class Meta:
		model = InvestorVerification
		fields = ('doc_type', 'doc1', 'doc2')


class FullVerificationCodeSerializer(serializers.ModelSerializer):
	class Meta:
		model = VerificationCode
		fields = ('user', 'code', 'expire_time')
		read_only_fields = ('expire_time', 'code',)
