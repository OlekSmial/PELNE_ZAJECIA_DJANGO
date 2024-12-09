 Zadanie 1 
 ```python
 from folder_aplikacji.models import osoba
 osoby = osoba.objects.all()
 print(osoby)
 ```

 Zadanie 2 
 ``` python
 osoba1 = osoba.objects.get(id=3)
 print(osoba1)
 ```

 Zadanie 3 
 ``` python
 osoba_z_N = osoba.objects.filter(imie__startswith = 'N')
 print(osoba_z_N)
 ```

Zadanie 4 (do sprawdzenia)
``` python
 stanowiska = osoba.objects.values('stanowisko').distinct()
 print(stanowiska)
```

Zadanie 5 
``` python
from folder_aplikacji.models import Stanowisko
Stanowisko.objects.values_list('nazwa', flat = True).order_by("-nazwa")
```

Zadanie 6
```python
osoba.objects.create( imie = "Jan", nazwisko = "Pawel", plec = 2, stanowisko = Stanowisko.objects.get(id = 1))
```