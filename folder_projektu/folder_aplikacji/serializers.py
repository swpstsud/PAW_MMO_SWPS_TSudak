from rest_framework import serializers
from .models import Postacie, Druzyna, MONTHS, KLASA_POSTACI, Stanowisko, Osoba
from datetime import date


class PostacieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    nazwa_postaci = serializers.CharField(required=True)
    klasa_postaci = serializers.ChoiceField(choices=KLASA_POSTACI, default=KLASA_POSTACI[0][0])
    month_added = serializers.ChoiceField(choices=MONTHS.choices, default=MONTHS.choices[0][0])

    druzyna = serializers.PrimaryKeyRelatedField(queryset=Druzyna.objects.all())
    
    pseudonim = serializers.CharField(required = False)
    
    def validate_name(self, value):

        if not value.istitle():
            raise serializers.ValidationError(
                "Nazwa osoby powinna rozpoczynać się wielką literą!",
            )
        return value

    def create(self, validated_data):
        return Postacie.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.nazwa_postaci = validated_data.get('name', instance.nazwa_postaci)
        instance.klasa_postaci = validated_data.get('klasa_postaci', instance.klasa_postaci)
        instance.month_added = validated_data.get('month_added', instance.month_added)
        instance.druzyna = validated_data.get('druzyna', instance.druzyna)
        instance.pseudonim = validated_data.get('pseudonim', instance.pseudonim)
        instance.save()
        return instance
    
    
# class PersonModelSerializer(serializers.ModelSerializer):
#     class Meta:
#         # musimy wskazać klasę modelu
#         model = Person
#         # definiując poniższe pole możemy określić listę właściwości modelu,
#         # które chcemy serializować
#         fields = ['id', 'name', 'month_added', 'shirt_size', 'team', 'pseudonim']
#         # definicja pola modelu tylko do odczytu
#         read_only_fields = ['id']

class StanowiskoSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    nazwa = serializers.CharField(max_length = 80)
    opis = serializers.CharField()
    
    def create(self, validated_data):
        return Stanowisko.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.nazwa = validated_data.get('nazwa', instance.nazwa)
        instance.opis = validated_data.get('opis', instance.opis)
        instance.save()
        return instance
    
class DruzynaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Druzyna
        fields = ['id', 'name', 'country']
        read_only_fields = ['id']
        
class OsobaSerializer(serializers.ModelSerializer):
    def validate_imie(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("Pole 'imie' musi zawierać tylko litery!!!")
        return value
    
    def validate_nazwisko(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("Pole 'nazwisko' musi zawierać tylko litery!!!")
        return value
    
    def validate_data_dodania(self, value):
        if value > date.today():
            raise serializers.ValidationError("Pole 'data_dodania' nie może być z przyszłości!!!")
        return value
    
    class Meta:
        model = Osoba
        fields = ['id', 'imie', 'nazwisko','plec', 'stanowisko', 'data_dodania']
        read_only_fields = ['id']