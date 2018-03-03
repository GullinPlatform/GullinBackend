from django.contrib import admin

from .models import Company, CompanyMember, PressRelease, TokenDetail, Document


class CompanyMemberInline(admin.TabularInline):
	model = CompanyMember
	show_change_link = True
	fields = ('avatar', 'first_name', 'last_name',
	          'title', 'description', 'member_type',
	          'facebook', 'linkedin', 'website',
	          'created', 'updated',)
	readonly_fields = ('created', 'updated',)
	extra = 0


class DocumentInline(admin.TabularInline):
	model = Document
	show_change_link = True
	fields = ('title', 'url',)
	readonly_fields = ('created',)
	extra = 0


class PressReleaseInline(admin.TabularInline):
	model = PressRelease
	show_change_link = True
	fields = ('title', 'brief', 'url',
	          'created',)
	extra = 0


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
	# List display Settings
	list_display = ('id', 'name', 'created', 'updated',)
	search_fields = ('name',)
	ordering = ('created',)

	# Detail Page Settings
	fieldsets = (
		('Published', {'fields': ('published',)}),
		('Company Info', {'fields': ('name', 'display_img', 'logo', 'short_description', 'website',)}),
		('Description', {'fields': ('description',)}),
		('Token Detail', {'fields': ('token_detail',)}),
		('Social Media', {'fields': ('youtube', 'ama', 'facebook', 'telegram', 'slack', 'twitter', 'medium',)}),
		('Timestamp', {'fields': ('created', 'updated',)}),
	)
	readonly_fields = ('created', 'updated',)

	inlines = [CompanyMemberInline, DocumentInline, PressReleaseInline, ]


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
		('Social Media', {'fields': ('facebook', 'linkedin', 'website')}),
		('Timestamp', {'fields': ('created', 'updated',)}),
	)
	readonly_fields = ('created', 'updated',)


@admin.register(PressRelease)
class PressReleaseAdmin(admin.ModelAdmin):
	# List display Settings
	list_display = ('id', 'title', 'created',)
	search_fields = ('title',)
	ordering = ('created',)

	# Detail Page Settings
	fieldsets = (
		('Company Info', {'fields': ('company',)}),
		('Article Info', {'fields': ('title', 'url', 'brief',)}),
		('Timestamp', {'fields': ('created',)}),
	)
	readonly_fields = ('created',)


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
		('Tokenomics', {'fields': ('price', 'total_token_supply', 'soft_market_cap', 'hard_market_cap', 'market_cap_unit', 'token_distribution')}),
		('Investment', {'fields': ('threshold', 'bonus', 'restrictions', 'restricted_country_list', 'accredited_investors', 'accredited_investors_country_list')}),
		('Smart Contract Info', {'fields': ('crowd_sale_contract_address', 'token_address', 'decimals',)}),
		('ICO Stage', {'fields': ('is_finished',)}),
		('Timestamp', {'fields': ('created', 'updated',)}),
	)
	readonly_fields = ('created', 'updated',)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
	# List display Settings
	list_display = ('id', 'title', 'created',)
	search_fields = ('title',)
	ordering = ('created',)

	# Detail Page Settings
	fieldsets = (
		('Company Info', {'fields': ('company',)}),
		('Article Info', {'fields': ('title', 'url',)}),
		('Timestamp', {'fields': ('created',)}),
	)
	readonly_fields = ('created',)
