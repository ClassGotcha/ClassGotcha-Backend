from django.contrib import admin

from models import Comment


class CommentAdmin(admin.ModelAdmin):
	# The fields to be used in displaying the User model.
	# These override the definitions on the base UserAdmin
	# that reference specific fields on auth.User.
	list_display = ('creator', 'created')

# fields = ['group_type', 'members', 'classroom', 'get_members']
#
# list_filter = ['group_type']
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


admin.site.register(Comment, CommentAdmin)