from rest_framework import serializers
from .models import Person, Team, MONTHS, SHIRT_SIZES, Stanowisko, osoba
from datetime import date


class PersonSerializer(serializers.Serializer):

    # pole tylko do odczytu, tutaj dla id działa też autoincrement
    id = serializers.IntegerField(read_only=True)

    # pole wymagane
    name = serializers.CharField(required=True)

    # pole mapowane z klasy modelu, z podaniem wartości domyślnych
    # zwróć uwagę na zapisywaną wartość do bazy dla default={wybór}[0] oraz default={wybór}[0][0]
    # w pliku models.py SHIRT_SIZES oraz MONTHS zostały wyniesione jako stałe do poziomu zmiennych skryptu
    # (nie wewnątrz modelu)
    shirt_size = serializers.ChoiceField(choices=SHIRT_SIZES, default=SHIRT_SIZES[0][0])
    month_added = serializers.ChoiceField(choices=MONTHS.choices, default=MONTHS.choices[0][0])

    # odzwierciedlenie pola w postaci klucza obcego
    # przy dodawaniu nowego obiektu możemy odwołać się do istniejącego poprzez inicjalizację nowego obiektu
    # np. team=Team({id}) lub wcześniejszym stworzeniu nowej instancji tej klasy
    team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())

    pseudonim = serializers.CharField(max_length=100, allow_blank = True)

# fragment klasy PersonSerializer

# walidacja wartości pola name
    def validate_name(self, value):

        if not value.istitle():
            raise serializers.ValidationError(
                "Nazwa osoby powinna rozpoczynać się wielką literą!",
            )
        return value


    # przesłonięcie metody create() z klasy serializers.Serializer
    def create(self, validated_data):
        return Person.objects.create(**validated_data)

    # przesłonięcie metody update() z klasy serializers.Serializer
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.shirt_size = validated_data.get('shirt_size', instance.shirt_size)
        instance.month_added = validated_data.get('month_added', instance.month_added)
        instance.team = validated_data.get('team', instance.team)
        instance.pseudonim = validated_data.get('pseudonim', instance.pseudonim)
        instance.save()
        return instance
    

# class PersonModelSerializer(serializers.ModelSerializer):
#     class Meta:
#         # musimy wskazać klasę modelu
#         model = Person
#         # definiując poniższe pole możemy określić listę właściwości modelu,
#         # które chcemy serializować
#         fields = ['id', 'name', 'miesiac_dodania', 'shirt_size', 'team']
#         # definicja pola modelu tylko do odczytu
#         read_only_fields = ['id']

class StanowiskoSerializer(serializers.Serializer):
    nazwa = serializers.CharField(max_length = 80)
    opis = serializers.CharField()

    def create(self, validated_data):
        return Stanowisko.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.nazwa = validated_data.get('nazwa', instance.nazwa)
        instance.opis = validated_data.get('opis', instance.opis)
        instance.save()
        return instance
    
class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'country']
        read_only_fields = ['id']

class osobaSerializer(serializers.ModelSerializer) :
    def validate_imie(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("Pole 'imie' musi zawierac tylko litery!!!")
        return value
    
    def validate_nazwisko(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("Pole 'nazwisko' musi zawierac tylko litery!!!")
        return value
    
    def validate_data_dodania(self, value):
        if value > date.today():
            raise serializers.ValidationError("Pole 'data_dodania' nie moze być z przyszlosci!!!")
        return value
    
    class Meta:
        model = osoba 
        fields = ['id', 'imie', 'nazwisko', 'stanowisko', 'data_dodania', 'plec']
        read_only_fields = ['id', 'data_dodania']