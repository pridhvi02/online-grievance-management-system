from django.contrib import admin
from .models import Complaint,Branch,Category,Student,Hod

class ComplaintAdmin(admin.ModelAdmin):
    fields = []
    readonly_fields = ['complaint_details' , 'branch' , 'category','status']
    list_display = ['category' , 'branch' ,'status']
    #def has_add_permission(self, request):
      #  return False
    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_save_and_add_another': False,
            'show_save_and_continue': False,
        })
        return super().render_change_form(request, context, add, change, form_url, obj)

    

class BranchAdmin(admin.ModelAdmin):
    fields = []
    #readonly_fields = ['branch']
class CategoryAdmin(admin.ModelAdmin):
    fields = []
    #readonly_fields = ['category']   
# Register your models here.
admin.site.register(Branch, BranchAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Student)
admin.site.register(Hod)



