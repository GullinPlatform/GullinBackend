from rest_framework import serializers

from .models import Company, TokenDetail, PressRelease, CompanyMember


class FullCompanySerializer(serializers.ModelSerializer):
	class Meta:
		model = Company
		fields = ('id', 'name', 'logo', 'short_description', 'white_paper', 'website',
		          'token_detail',
		          'facebook', 'telegram', 'slack', 'twitter', 'medium',
		          'created', 'updated',)
		read_only_fields = ('created', 'updated',)


class FullTokenDetailSerializer(serializers.ModelSerializer):
	class Meta:
		model = TokenDetail
		fields = ('logo', 'code', 'is_finished',
		          'start_datetime', 'end_datetime',
		          'ico_token_type', 'ico_stage_type',
		          'init_price', 'current_price', 'total_token_supply', 'token_sold', 'soft_market_cap', 'hard_market_cap', 'market_cap_unit',
		          'wallet_address',
		          'created', 'updated',)
		read_only_fields = ('wallet_address', 'created', 'updated',)


class FullPressReleaseSerializer(serializers.ModelSerializer):
	class Meta:
		model = PressRelease
		fields = ('company',
		          'title', 'content', 'url',
		          'created', 'updated')
		read_only_fields = ('created', 'updated',)


class FullCompanyMemberSerializer(serializers.ModelSerializer):
	class Meta:
		model = CompanyMember
		fields = ('company',
		          'avatar', 'first_name', 'last_name', 'title', 'description', 'member_type'
		                                                                       'facebook', 'linkedin',
		          'created', 'updated')
		read_only_fields = ('created', 'updated',)
