# Lab 2 - Mateusz Orzełowski

Autor: Mateusz Orzełowski

## Zadanie 1 - dane osobowe w logach

Wybrałem aplikację Python. Odtworzyłem problem przez `POST /customers/create` z fikcyjnymi danymi, a następnie ponowiłem żądanie z tą samą nazwą klienta. Przy dodaniu `Customer.__init__()` wypisywał reprezentację obiektu, a `Customer.__repr__()` zawierał imię i nazwisko, miasto, wiek, PESEL, ulicę i numer lokalu. Przy duplikacie `create_customer()` wypisywał także treść wyjątku SQLAlchemy z parametrami zapytania i zwracał ją w odpowiedzi HTTP.

![Log przed poprawką](https://raw.githubusercontent.com/morzelowski/task2/main/docs/evidence/logs-before.png)

Zachowałem układ logu `Customer(...)`, ale zastąpiłem wszystkie pola podane przez klienta stałymi maskami. W obsłudze błędów tworzenia i edycji klienta usunąłem surową treść wyjątku z logu lub odpowiedzi HTTP.

![Log po poprawce](https://raw.githubusercontent.com/morzelowski/task2/main/docs/evidence/logs-after.png)

Sprawdziłem tworzenie, listę, edycję i usuwanie klienta. Po poprawce testowe wartości nie występują w logu, a próba utworzenia duplikatu zwraca ogólny komunikat bez danych osobowych. Żądania tworzenia i edycji nadal kończą się przekierowaniem `302`, a lista zwraca `200`.

## Zadanie 2 - sekrety w historii repozytorium

Uruchomiłem Gitleaks na historii repozytorium z opcją `--redact=100`, aby nie pokazywać wartości sekretów. Skan obejmował 5 commitów i wykrył 3 wpisy reguły `private-key`.

![Wynik Gitleaks z ukrytymi sekretami](https://raw.githubusercontent.com/morzelowski/task2/main/docs/evidence/gitleaks.png)

| Plik w historii | Commit | Weryfikacja |
| --- | --- | --- |
| `deployment.key` | `bc17b7d` | Poprawny klucz prywatny RSA. `openssl rsa -check` kończy się powodzeniem. |
| `deployment2.key` | `de9d7b8` | Poprawny klucz prywatny RSA. To ta sama zawartość co w `deployment.key`, więc nie jest drugim niezależnym sekretem. |
| `awscredentials.json` | `bc17b7d` | Pole `private_key` przypomina PEM, ale jego treść ma niepoprawne kodowanie Base64 i nie daje się odczytać jako klucz. To fałszywie dodatnie wykrycie użytecznego klucza. |

Pliki usunięto z bieżącej wersji repozytorium w commicie `fd67400`, ale nadal są w historii. Nie da się ustalić z samego skanu, czy klucz RSA był używany; jeśli tak, należy go unieważnić i wymienić. Ręczny przegląd bieżących plików pokazał również stały `SECRET_KEY` Flaska oraz `ENV PASSWORD` w Dockerfile, których Gitleaks nie zgłosił. Przed użyciem produkcyjnym `SECRET_KEY` powinien pochodzić z bezpiecznej konfiguracji, a nieużywany `PASSWORD` należy usunąć z obrazu.

## Zadanie 3 - bezpieczeństwo zależności

Uruchomiłem Safety na `Python/Flask_Book_Library/requirements-task.txt`. Raport obejmuje 18 pakietów i zawiera 17 zgłoszeń. Do szczegółowej analizy wybrałem `healpy==1.8.0`, dla którego Safety zgłasza podatną wersję dołączonej biblioteki `libcurl` pod identyfikatorem `61774`.

![Wynik Safety dla healpy](https://raw.githubusercontent.com/morzelowski/task2/main/docs/evidence/safety.png)

Analizowana podatność `libcurl` to [CVE-2023-38545](https://curl.se/docs/CVE-2023-38545.html), oceniana jako wysoka przez autorów curl i jako [9,8 w CVSS 3.1](https://ubuntu.com/security/CVE-2023-38545). Może powodować przepełnienie bufora podczas negocjacji z proxy SOCKS5, gdy klient przekazuje przez proxy bardzo długą nazwę hosta. Wymaga podatnej wersji `libcurl`, odpowiedniego ustawienia proxy i nazwy hosta oraz wystąpienia określonego przebiegu negocjacji.

W badanej aplikacji wykorzystanie tego zgłoszenia jest mało prawdopodobne: `healpy` występuje tylko w pliku `requirements-task.txt` użytym do skanu. Dockerfile instaluje `requirements.txt`, w którym nie ma `healpy`; potwierdziłem też brak pakietu w uruchomionym kontenerze i brak importów w kodzie aplikacji. Wynik Safety dotyczy więc skanowanej listy, ale nie zależności faktycznie uruchomionej aplikacji. Jeśli pakiet ma być używany w przyszłości, trzeba ponownie sprawdzić wersję dołączonej `libcurl` i zaktualizować zależność.
