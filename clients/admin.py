from django.contrib import admin

# Register your models here.
from .models import Clients


#admin.site.register(Clients)


class ClientsAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('name',
                       'lastname',
                       'identifier',
                       'physicalCode',
                       'mobileNumber',
                       'email',
                       'birthDate',
		       'inseach'
                       )
        }),
        ('Optional fields', {
            'classes': ('collapse',),
            'fields': (
                       'address',
                       'city',
                       'phoneNumber',
                       'postalCode',
                       'alergies',
                       'diseases',
                       'bloodType',
                       'contacts',
                       ),
        }),
    )

    filter_horizontal = ('contacts',)
    #search_fields = ['id']


admin.site.register(Clients, ClientsAdmin)
