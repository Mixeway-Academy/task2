# Task 1
Zidentyfikowano logi aplikacji, które udostępniają dane wraliwe. Po utworzeniu Customer aplikacja wyświetla w logach

```
Customers page accessed
Getting: Customer(ID: None, Name: loanCustomer, City: loanCity, Age: 200, Pesel: 012345678911, Street: loanStreetName, AppNo: 22)
```

Problem w aplikacji pytnowej występuje w module `project/customers/models.py`. Z uwagi na to, ze chcemy zachować format logów, dodano metodę `_mask()` w tym moduke, która maskuje wrazliwy output w metodzie `__repr__`

```python
def __mask(value):
    return '*' * len(str(value)) if value else value

```

# Task 2

Wykryto 3 wycieki credentiali, z czego 1 został przeze mnie zakwalifikowany jako false positive.

## deployment.key

Dla jego commith hash `bc17b7ddc46f46fff175aed55d68e11bb48166cc` znaleziono plik deployment.key.

Uzyto komenty `git show bc17b7d:deployment.key` do podświetlenia zawartości - wygląda na klucz prywatny

## deployment2.key

Analogicznie dla commith hash `de9d7b8cb63bd7ae741ec5c9e23891b71709bc28`

## awscredentials.json

Ten plik wygląda na false positive, po podświetleniu jego zawartości widać w pliku krotkę `"project_id": "test-project"`, dodatkowo zawiera informacje wskazujące na Google Services `app@test-project.iam.gserviceaccount.com`

# Task 3 

Po przeskanowaniu zależności z pliku `requirements-task.txt` narzędziem `safety` wykryto podatności w 5 pakietach (`flask`, `jinja2`, `mako`, `werkzeug`, `healpy`).
## healpy (v 1.8.0) - najwyższa krytyczność wg zasad zadania
W pakiecie `healpy` (ID `61774`) wykryto podatność o wysokiej/krytycznej wadze związaną z zaszytą wewnątrz biblioteką `libcurl` (CVE-2023-38545 - przepełnienie bufora na stercie mogące prowadzić do RCE). Na szczęście pakiet `healpy` w ogóle nie jest nigdzie importowany, występuje wyłącznie w `requirements-task.txt`. Prawdopodobieństwo wykorzystania tej podatności w badanej aplikacji jest więc zerowe.
