from datetime import date
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

MONTHS = models.IntegerChoices('Miesiace', 'Styczeń Luty Marzec Kwiecień Maj Czerwiec Lipiec Sierpień Wrzesień Październik Listopad Grudzień')

PLCIE = models.IntegerChoices('PLEC', 'Kobieta Mężczyzna Inna')

KLASA_POSTACI = (
        ('W', 'Wojownik'),
        ('M', 'Mistyk'),
        ('B', 'Bandyta'),
    )


class Druzyna(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=80, unique=True)
    country = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.name}"


class Postacie(models.Model):

    nazwa_postaci = models.CharField(max_length=60)
    pseudonim_postaci = models.CharField(max_length=80, default='')
    klasa_postaci = models.CharField(max_length=1, choices=KLASA_POSTACI, default=KLASA_POSTACI[0][0])
    month_added = models.IntegerField(choices=MONTHS.choices, default=MONTHS.choices[0][0])
    druzyna = models.ForeignKey(Druzyna, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Person: {self.nazwa_postaci}, dodana w {self.month_added}, o klasie postaci {self.klasa_postaci}. \n"


class Osoba(models.Model):
    PLEC_CHOICES = (
        ("K", "Kobieta"),
        ("M", "Mężczyzna"),
        ("I", "Inna"),
    )
    
    imie = models.CharField(max_length=60, blank = False, null = False)
    nazwisko = models.CharField(max_length=100, blank = False, null = False)
    plec = models.IntegerField(choices=PLCIE.choices, default=PLCIE.choices[2][0])
    stanowisko = models.ForeignKey("Stanowisko", on_delete = models.CASCADE)
    data_dodania = models.DateField(default= date.today, blank=False, null=True)
    wlasciciel = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.imie} {self.nazwisko}'
    
    class Meta:
        ordering = ['nazwisko']
        permissions = [
            ("view_postacie_other_owner", "Pozwala zobaczyć modele Postacie innych właścicieli"),
        ]

class Stanowisko(models.Model):
    nazwa = models.CharField(max_length=80, blank = False, null = False)
    opis = models.TextField(blank = False, null = False, editable = True)

    def __str__(self):
        return self.nazwa

