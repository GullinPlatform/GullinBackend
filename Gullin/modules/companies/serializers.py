from rest_framework import serializers

from .models import Company, TokenDetail, PressRelease, CompanyMember, Document


class FullTokenDetailSerializer(serializers.ModelSerializer):
	class Meta:
		model = TokenDetail
		fields = ('token_code', 'token_logo', 'erc20_compliant',
		          'start_datetime', 'end_datetime', 'is_finished',
		          'ico_token_type', 'ico_stage_type',
		          'price', 'price_unit', 'total_token_supply', 'soft_market_cap', 'hard_market_cap', 'market_cap_unit', 'token_distribution',
		          'threshold', 'restrictions', 'bonus', 'restricted_country_list',
		          'crowd_sale_contract_address', 'token_address', 'decimals',
		          'created', 'updated',)
		read_only_fields = ('contract_address', 'created', 'updated',)


class MiniTokenDetailSerializer(serializers.ModelSerializer):
	class Meta:
		model = TokenDetail
		fields = ('is_finished', 'ico_stage_type', 'ico_token_type', 'start_datetime', 'end_datetime',)


class BalanceTokenDetailSerializer(serializers.ModelSerializer):
	class Meta:
		model = TokenDetail
		fields = ('token_code', 'token_name', 'token_address', 'decimals', 'price', 'price_unit')


class FullPressReleaseSerializer(serializers.ModelSerializer):
	class Meta:
		model = PressRelease
		fields = ('title', 'brief', 'url',
		          'created',)
		read_only_fields = ('created',)


class FullDocumentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Document
		fields = ('title', 'url',
		          'created',)
		read_only_fields = ('created',)


class FullCompanyMemberSerializer(serializers.ModelSerializer):
	class Meta:
		model = CompanyMember
		fields = ('company',
		          'avatar', 'full_name',
		          'title', 'description', 'member_type',
		          'facebook', 'linkedin', 'website',
		          'created', 'updated',)
		read_only_fields = ('created', 'updated', 'full_name',)


class FullCompanySerializer(serializers.ModelSerializer):
	token_detail = FullTokenDetailSerializer()
	members = FullCompanyMemberSerializer(many=True)
	documents = FullDocumentSerializer(many=True)
	press_releases = FullPressReleaseSerializer(many=True)

	class Meta:
		model = Company
		fields = ('id', 'name', 'logo', 'short_description', 'website',
		          'description',
		          'token_detail', 'members', 'documents', 'press_releases',
		          'youtube', 'ama', 'facebook', 'telegram', 'slack', 'twitter', 'medium',
		          'created', 'updated',)
		read_only_fields = ('created', 'updated',)


class ListCompanySerializer(serializers.ModelSerializer):
	token_detail = MiniTokenDetailSerializer(allow_null=True)

	class Meta:
		model = Company
		fields = ('id', 'name', 'token_detail', 'display_img', 'short_description',)
