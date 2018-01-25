from rest_framework import serializers

from .models import Company, TokenDetail, PressRelease, CompanyMember


class FullTokenDetailSerializer(serializers.ModelSerializer):
	class Meta:
		model = TokenDetail
		fields = ('token_code', 'token_logo', 'erc20_compliant',
		          'start_datetime', 'end_datetime', 'is_finished',
		          'ico_token_type', 'ico_stage_type',
		          'threshold', 'init_price', 'current_price', 'total_token_supply', 'token_sold', 'soft_market_cap', 'hard_market_cap', 'market_cap_unit',
		          'contract_address',
		          'created', 'updated',)
		read_only_fields = ('contract_address', 'created', 'updated',)


class MiniTokenDetailSerializer(serializers.ModelSerializer):
	class Meta:
		model = TokenDetail
		fields = ('is_finished', 'start_datetime', 'end_datetime')


class BalanceTokenDetailSerializer(serializers.ModelSerializer):
	class Meta:
		model = TokenDetail
		fields = ('token_code', 'token_name', 'token_logo', 'contract_address')


class FullCompanyMemberSerializer(serializers.ModelSerializer):
	class Meta:
		model = CompanyMember
		fields = ('company',
		          'avatar', 'first_name', 'last_name',
		          'title', 'description', 'member_type', 'facebook', 'linkedin',
		          'created', 'updated')
		read_only_fields = ('created', 'updated',)


class FullCompanySerializer(serializers.ModelSerializer):
	token_detail = FullTokenDetailSerializer()
	members = FullCompanyMemberSerializer(many=True)

	class Meta:
		model = Company
		fields = ('id', 'name', 'logo', 'short_description', 'white_paper', 'website',
		          'token_detail',
		          'facebook', 'telegram', 'slack', 'twitter', 'medium',
		          'created', 'updated',)
		read_only_fields = ('created', 'updated',)


class ListCompanySerializer(serializers.ModelSerializer):
	token_detail = MiniTokenDetailSerializer(allow_null=True)

	class Meta:
		model = Company
		fields = ('id', 'name', 'token_detail', 'display_img', 'short_description')


class FullPressReleaseSerializer(serializers.ModelSerializer):
	class Meta:
		model = PressRelease
		fields = ('company',
		          'title', 'content', 'url',
		          'created', 'updated')
		read_only_fields = ('created', 'updated',)
