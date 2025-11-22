# Zadanie 1
## Opis błędu
Po dodaniu nowego klienta przez formularz:
zdjęci
W logach pojawia się informacja kliencie
zdjęcia
Taka informacja nie jest w logach konieczna i mozna usunąć jej dodanie. Dane były logowane w klasie `Customer` w następującej lini:
``` python
print("Getting: " + str(self),flush=True)
```
Aby poprawić to nalezy zmodyfikować funkcje `__repr__` w klasie `Cusstomer` w np taki sposób
``` python
def __repr__(self):
        return f"Customer(ID: {self.id}, Name: ******, City: ******,, Age: ******,, Pesel: ******,, Street: ******, AppNo: ******)"
```
Wtedy w logach otrzymujemy:
zdjęcie
# Zadanie 2
Narzędzie `gitleak` wykryło 3 potencjalne podatności
zdjęcie podatności
Linki do podatności:
https://github.com/KarolZebala/kz-tbo-task2/blob/bc17b7ddc46f46fff175aed55d68e11bb48166cc/deployment.key#L1
https://github.com/KarolZebala/kz-tbo-task2/blob/de9d7b8cb63bd7ae741ec5c9e23891b71709bc28/deployment2.key#L1
https://github.com/KarolZebala/kz-tbo-task2/blob/bc17b7ddc46f46fff175aed55d68e11bb48166cc/awscredentials.json#L5

Wśród wykrytych problemów wszystkie wyglądają sensownie.

# Zadanie 3
W pakiecie jinja2 3.1.2 wykryto podatność pozwalającą na obejście sandboxa wykorzystując filtr `| atrt`, co moze prowadzić do wykonania dowolnego kodu Pythona.
 Aby móc wykorzystać podatność atakujący musi mieć mozliwość kontrolowania treści renderowanego szablonu, gdy aplikacja
 wykorzystuje jedynie szablony developerskie prawdopodobieństwo wykorzystanie podatności jet niewielkie.
 Podatność została naprawiona w wersji 3.1.6