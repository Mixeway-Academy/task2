## Zadanie 1
Podczas tworzenia nowego klienta - obiekt Customer - zostało zaobserwowane logowanie powstałego obiektu z widocznymi danymi wrażliwymi tj. pesel i adres.
![Logowanie peselu i adresu klienta](https://raw.githubusercontent.com/Yibux/task2/refs/heads/main/Logowanie_peselu_i_adresu.png)

### Poprawki w kodzie
Dodałem "maskę" w logowaniu peselu i adresu klienta.
![Logowanie peselu i adresu klienta po poprawie](https://raw.githubusercontent.com/Yibux/task2/refs/heads/main/Logowanie_peselu_i_adresu_po_poprawie.png)
## Zadanie 2
Gitleaks wykryło 3 wycieki secretów w repozytorium:
![Wycieki secretów](https://raw.githubusercontent.com/Yibux/task2/refs/heads/main/wycieki_secretow.png)

Każdy z wycieków to rodzaj `True Positive`, ponieważ zawiera klucze publiczne i prywatne. Gitleaks nie wykrył występowania zmiennych o nazwie `password`.
## Zadanie 3
1. Podatność w pakiecie werkzeug (ID: 73889)
W pakiecie werkzeug wykryto podatność typu Denial of Service (DoS) oznaczoną jako Wysoka. Wykorzystanie podatności jest możliwe po uruchomieniu metody parsującej z klasy werkzeug.formparser.MultiPartParser. Po analizie w badanej aplikacji klasa ta jest wykorzystywana (poprzez odwołania do request.form w plikach widoków, np. przy tworzeniu klientów), także prawdopodobieństwo wykorzystania tej podatności jest wysokie.

2. Podatność w pakiecie werkzeug (ID: 71594)
W pakiecie werkzeug wykryto podatność typu Remote Code Execution (RCE) oznaczoną jako Krytyczna. Wykorzystanie podatności jest możliwe po uruchomieniu debugera z klasy werkzeug.debug.DebuggedApplication (wystawionego publicznie). Po analizie w badanej aplikacji (plik app.py) tryb debugowania jest włączony (debug=True), zatem klasa ta jest wykorzystywana, a prawdopodobieństwo wykorzystania tej podatności (jeśli aplikacja jest dostępna z sieci) jest wysokie.

3. Podatność w pakiecie jinja2 (ID: 76378)
W pakiecie jinja2 wykryto podatność typu RCE (Sandbox Escape) oznaczoną jako Krytyczna. Wykorzystanie podatności jest możliwe po uruchomieniu metod formatowania ciągów znaków wewnątrz środowiska jinja2.sandbox.SandboxEnvironment. Po analizie w badanej aplikacji klasa SandboxEnvironment nie jest wykorzystywana (aplikacja korzysta ze standardowego, niesandboxowanego środowiska Jinja2 do renderowania zaufanych szablonów), także prawdopodobieństwo wykorzystania tej podatności w ten sposób jest minimalne.

4. Podatność w pakiecie healpy (ID: 61774)
W pakiecie healpy wykryto podatność typu Arbitrary Code Execution oznaczoną jako Krytyczna. Wykorzystanie podatności jest możliwe przy przetwarzaniu złośliwych danych przez bibliotekę libcurl wykorzystywaną przez ten pakiet. Po analizie w badanej aplikacji pakiet healpy znajduje się w pliku requirements.txt, ale jego funkcjonalności nie są importowane ani wykorzystywane w kodzie źródłowym projektu, także prawdopodobieństwo wykorzystania tej podatności jest minimalne.