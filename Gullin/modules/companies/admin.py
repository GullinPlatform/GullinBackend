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
		('Company Info', {'fields': ('name', 'logo', 'short_description', 'white_paper', 'website',)}),
		('Token Detail', {'fields': ('token_detail',)}),
		('Social Media', {'fields': ('facebook', 'telegram', 'slack', 'twitter', 'medium',)}),
		('Timestamp', {'fields': ('created', 'updated',)}),
	)
	readonly_fields = ('created', 'updated', 'token_detail',)


@admin.register(CompanyMember)
class CompanyMemberAdmin(admin.ModelAdmin):
	# List display Settings
	list_display = ('id', 'full_name', 'created', 'updated',)
	search_fields = ('name',)
	ordering = ('created',)

	# Detail Page Settings
	fieldsets = (
		('Company Info', {'fields': ('company',)}),
		('Member Type', {'fields': ('member_type',)}),
		('Member Detail', {'fields': ('avatar', 'first_name', 'last_name', 'title', 'description', )}),
		('Social Media', {'fields': ('facebook', 'linkedin',)}),
		('Timestamp', {'fields': ('created', 'updated',)}),
	)
	readonly_fields = ('created', 'updated', 'company',)


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
	list_display = ('code', 'type', 'created', 'updated',)
	search_fields = ('code',)
	ordering = ('created',)

	# Detail Page Settings
	fieldsets = (
		('Token Summary', {'fields': ('logo', 'code', 'type',)}),
		('ICO Time', {'fields': ('start_datetime', 'end_datetime',)}),
		('ICO Type', {'fields': ('ico_token_type', 'ico_stage_type',)}),
		('Tokenomics', {'fields': ('init_price', 'current_price', 'total_token_supply', 'token_sold', 'soft_market_cap', 'hard_market_cap', 'market_cap_unit')}),
		('ICO Destination', {'fields': ('ico_destination_address',)}),
		('ICO Stage', {'fields': ('is_finished',)}),
		('Timestamp', {'fields': ('created', 'updated',)}),
	)
	readonly_fields = ('created', 'updated',)
