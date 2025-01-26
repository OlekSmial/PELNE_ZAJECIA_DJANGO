from folder_aplikacji.models import osoba, Stanowisko
from folder_aplikacji.serializers import osobaSerializer, StanowiskoSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

# tworzmy sobie nowe obiekty 

stanowisko = Stanowisko.objects.create(nazwa = "Kierownik", opis = "Zarządza tymi co zarzadzaja")
Osoba = osoba.objects.create(imie = "Jan", nazwisko = "Malinowski", stanowisko = stanowisko, plec = 2)

# inicjalizacja serializera dla osoby 
Osoba_serializer = osobaSerializer(Osoba)
print(Osoba_serializer.data)

# format JSON tego samego 
osoba_json = JSONRenderer().render(osoba_serializer.data)


# (id 8)
import io 

# strumien danych JSON
stream = io.BytesIO(osoba_json)

# parsowanie JSON do slownika 
data = JSONParser().parse(stream)

# tqorzymy obiekt deserializera dla danych json
deserializer = OsobaSerializer(data = data)

# walidacja danych 
print(deserializer.is_valid())
print(deserializer.errors)
# oczekiwany wynik True

# ledne dane 
invalid_data = {'imie': 'Adam', 'nazwisko': 'Nowak', 'plec': 'nieznane', 'stanowisko' : stanowisko.id}

# stworzmy serializer z blednymi danami 
invalid_serializer = osobaSerializer(data = invalid_data)
print(invalid_serializer.is_valid())
print(invalid_serializer.errors)

# fALSE
# plec valid choice

# zapis do BD
if deserializer.is_valid():
    deserializer.save()

# inicjowanie  serializera dla stanowisko 
stanowisko_serializer = StanowiskoSerializer(stanowisko)
print(stanowisko_serializer.data)

# serializacja do JSON

stanowisko_json = JSONRenderer().render(stanowisko_serializer.data)
print(stanowisko_json)

# deserializacja z JSON

strwam = io.BytesIO(stanowisko_json)
data = JSONParser().parse(stream)

deserializer = StanowiskoSerializer(data = data)

print(deserializer.is_valid())

if deserializer.is_valid():
    deserializer.save()
