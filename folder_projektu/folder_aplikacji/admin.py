from django.contrib import admin

from .models import Druzyna, Postacie, Osoba, Stanowisko

admin.site.register(Druzyna)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['nazwa_postaci', 'klasa_postaci', 'druzyna']
    list_filter = ['druzyna']
admin.site.register(Postacie, PersonAdmin)
class StanowiskoAdmin(admin.ModelAdmin):
    list_display = ['nazwa', 'opis']
    list_filter = ['nazwa']
    
admin.site.register(Stanowisko, StanowiskoAdmin)
class OsobaAdmin(admin.ModelAdmin):
    @admin.display(description= "Stanowisko (ID)")
    def stanowisko_with_id(self, obj):
        if obj.stanowisko:
            return f'{obj.stanowisko.nazwa} ({obj.stanowisko.id})'
        return "Brak stanowsika"
    
    list_display = ['imie', 'nazwisko', 'plec', 'stanowisko_with_id', 'data_dodania']
    list_filter = ['stanowisko', 'data_dodania']
    
admin.site.register(Osoba, OsobaAdmin)
