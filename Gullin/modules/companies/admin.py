from django.contrib import admin

from .models import Company, CompanyMember, PressRelease, TokenDetail


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
	# List display Settings
	list_display = ('id', 'name', 'created', 'updated',)
	search_fields = ('name',)
	ordering = ('created',)

	# Detail Page Settings
	fieldsets = (
		('Company Info', {'fields': ('name', 'display_img', 'logo', 'short_description', 'white_paper', 'website',)}),
		('Token Detail', {'fields': ('token_detail',)}),
		('Social Media', {'fields': ('facebook', 'telegram', 'slack', 'twitter', 'medium',)}),
		('Timestamp', {'fields': ('created', 'updated',)}),
	)
	readonly_fields = ('created', 'updated', 'token_detail',)


@admin.register(CompanyMember)
class CompanyMemberAdmin(admin.ModelAdmin):
	# List display Settings
	list_display = ('id', 'company', 'full_name', 'title',)
	search_fields = ('company', 'first_name', 'last_name')
	list_filter = ('company',)
	ordering = ('created',)

	# Detail Page Settings
	fieldsets = (
		('Company Info', {'fields': ('company',)}),
		('Member Type', {'fields': ('member_type',)}),
		('Member Detail', {'fields': ('avatar', 'first_name', 'last_name', 'title', 'description',)}),
		('Social Media', {'fields': ('facebook', 'linkedin',)}),
		('Timestamp', {'fields': ('created', 'updated',)}),
	)
	readonly_fields = ('created', 'updated',)


@admin.register(PressRelease)
class PressReleaseAdmin(admin.ModelAdmin):
	# List display Settings
	list_display = ('id', 'title', 'created', 'updated',)
	search_fields = ('title',)
	ordering = ('created',)

	# Detail Page Settings
	fieldsets = (
		('Company Info', {'fields': ('company',)}),
		('Article Info', {'fields': ('title', 'url', 'content',)}),
		('Timestamp', {'fields': ('created', 'updated',)}),
	)
	readonly_fields = ('created', 'updated', 'company',)


@admin.register(TokenDetail)
class TokenDetailAdmin(admin.ModelAdmin):
	# List display Settings
	list_display = ('token_code', 'ico_token_type', 'ico_stage_type', 'created', 'updated',)
	search_fields = ('token_code',)
	ordering = ('created',)

	# Detail Page Settings
	fieldsets = (
		('Token Detail', {'fields': ('token_name', 'token_code', 'token_logo', 'erc20_compliant',)}),
		('ICO Type', {'fields': ('ico_token_type', 'ico_stage_type',)}),
		('ICO Time', {'fields': ('start_datetime', 'end_datetime', 'is_finished')}),
		('Tokenomics', {'fields': ('threshold', 'init_price', 'current_price', 'total_token_supply', 'token_sold', 'soft_market_cap', 'hard_market_cap', 'market_cap_unit')}),
		('Contract Address', {'fields': ('contract_address',)}),
		('ICO Stage', {'fields': ('is_finished',)}),
		('Timestamp', {'fields': ('created', 'updated',)}),
	)
	readonly_fields = ('created', 'updated',)
