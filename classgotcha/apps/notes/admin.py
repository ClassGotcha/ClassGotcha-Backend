from django.contrib import admin

from models import Note, Rate


class NoteAdmin(admin.ModelAdmin):
	# The fields to be used in displaying the User model.
	# These override the definitions on the base UserAdmin
	# that reference specific fields on auth.User.
	list_display = ('creator', 'classroom', 'rating')
# list_filter = ('is_admin', 'school_year')
# fieldsets = (
#     (None, {'fields': ('email', 'username', 'password')}),
#     ('Personal info', {'fields': ('first_name', 'last_name', 'gender', 'school_year', 'major', 'avatar')}),
#     ('Permissions', {'fields': ('is_admin', 'is_student', 'is_professor')}),
# )
# readonly_fields = ('created', 'updated')
# # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
# # overrides get_fieldsets to use this attribute when creating a user.
# add_fieldsets = (
#     (None, {
#         'classes': ('wide',),
#         'fields': ('email', 'username', 'password1', 'password2')}
#      ),
# )
# search_fields = ('email', 'username')
# ordering = ('email',)
# filter_horizontal = ()


class RateAdmin(admin.ModelAdmin):
	list_display = ('creator', 'num', 'note')


admin.site.register(Note, NoteAdmin)
admin.site.register(Rate, RateAdmin)