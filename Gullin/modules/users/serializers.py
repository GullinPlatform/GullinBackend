from rest_framework import serializers

from .models import User, InvestorUser, CompanyUser, AnalystUser, IDVerification, InvestorVerification, VerificationCode


class FullCompanySerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'name', 'logo', 'short_description', 'white_paper', 'website',
		          'token_detail',
		          'facebook', 'telegram', 'slack', 'twitter', 'medium',
		          'created', 'updated',)
		read_only_fields = ('created', 'updated',)

	# TODO
	def create(self, validated_data):
		pass

	# TODO
	def update(self, instance, validated_data):
		pass


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
