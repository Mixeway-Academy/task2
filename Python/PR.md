
# PR: Flask_Book_Library
 
## Zadanie 1 – wyciek danych wrażliwych w logach
 
### Znalezione wycieki
| # | Miejsce | Co trafia do logu |
|---|---|---|
| 1 | `customers/models.py` – `Customer.__init__` robi `print("Getting: " + str(self))`, a `__repr__` zwraca wszystkie pola | `Pesel: 90010112345, Street: Marszalkowska, AppNo: 12` przy **każdym** dodaniu klienta |
| 2 | `customers/views.py` – `print(f'Error creating customer: {str(e)}')` | wyjątek SQLAlchemy `IntegrityError` zawiera parametry zapytania: `[parameters: ('Jan Kowalski', 'Gdansk', '41', '83121254321', 'Dluga', '3')]`. Ten sam tekst wraca też do klienta w odpowiedzi HTTP 500 |
 
### Poprawka (format logów bez zmian)
- Nowy moduł `project/utils/masking.py`:
  - `mask(value)` zamienia każdy znak na `*` i zachowuje długość, np. `90010112345` → `***********`,
  - `redact(text, *values)` maskuje podane wartości w dowolnym tekście (np. w treści wyjątku).
- `Customer.__repr__` maskuje `pesel`, `street` i `appNo`. Maskowanie dotyczy tylko reprezentacji tekstowej, w bazie nadal zapisują się prawdziwe wartości (zweryfikowano).
- W `create_customer` komunikat wyjątku przechodzi przez `redact(...)` przed `print` i przed zwróceniem w JSON.
Przed → po:
```
Getting: Customer(ID: None, Name: Jan Kowalski, City: Warszawa, Age: 30, Pesel: 90010112345, Street: Marszalkowska, AppNo: 12)
Getting: Customer(ID: None, Name: Jan Kowalski, City: Warszawa, Age: 30, Pesel: ***********, Street: *************, AppNo: **)
 
[parameters: ('Jan Kowalski', 'Gdansk', '41', '83121254321', 'Dluga', '3')]
[parameters: ('Jan Kowalski', 'Gdansk', '41', '***********', '*****', '*')]
```
Po zmianie w całym logu nie występuje żaden PESEL ani żadna ulica z testu. Wszystkie 26 kodów HTTP są identyczne jak przed zmianą.
 
---
 
## Zadanie 2 – sekrety (gitleaks)
  
```
docker run -v <ścieżka>/task2:/path zricethezav/gitleaks:latest detect --source="/path" -v
```
Repozytorium zawiera katalog `.git`, więc gitleaks przeskanował **całą historię commitów**, a nie tylko bieżący stan plików.
 
### Wynik
Gitleaks zgłosił **3 wykrycia**, wszystkie regułą `private-key`:
 
| # | Plik | Linia | Commit | Data (UTC) | Entropia | Wykryta wartość (początek) |
|---|---|---|---|---|---|---|
| 1 | `deployment2.key` | 1 | `de9d7b8` | 2023-11-15 12:49:39 | 5.88 | `-----BEGIN RSA PRIVATE KEY-----` / `MIIBOgIBAAJBAKj34G...` |
| 2 | `deployment.key` | 1 | `bc17b7d` | 2023-11-15 12:52:32 | 5.88 | `-----BEGIN RSA PRIVATE KEY-----` / `MIIBOgIBAAJBAKj34G...` |
| 3 | `awscredentials.json` | 5 | `bc17b7d` | 2023-11-15 12:52:32 | 5.92 | `"private_key": "-----BEGIN PRIVATE KEY-----\nlRsGbRO/1A5L...` |
 
### Weryfikacja (TP / FP)
| # | Ocena | Uzasadnienie |
|---|---|---|
| 1 | **True positive** | Klucz prywatny RSA w formacie PEM (PKCS#1) zapisany wprost w repozytorium. Treść zaczyna się od `MIIBOgIBAAJBA`, czyli poprawnej struktury DER typowej dla klucza RSA 512-bit. Klucz 512-bit jest dodatkowo kryptograficznie słaby, ale nadal jest sekretem |
| 2 | **True positive** (ten sam klucz co #1) | Identyczny początek treści i identyczna entropia jak w #1, czyli najpewniej ten sam klucz zapisany w drugim pliku 3 minuty później. Oznacza to, że klucz występuje w historii w dwóch miejscach |
| 3 | **Prawdopodobny false positive** | Reguła dopasowała tylko nagłówek `-----BEGIN PRIVATE KEY-----`. Treść nie wygląda na prawdziwy klucz: poprawny klucz PKCS#8 w Base64 zaczyna się od `MII` (struktura DER), a tu zaczyna się od `lRsG...` i zawiera powtarzane wstawki `ASDASD`, typowe dla ręcznie wpisanych danych testowych. Mimo to nazwa `awscredentials.json` sugeruje plik z poświadczeniami, więc pozostałe pola pliku wymagają ręcznego przeglądu (gitleaks zgłosił tylko linię 5) |
 
W wynikach nie wystąpił opisany w instrukcji przypadek fałszywego pozytywu (słowo `password` jako nazwa zmiennej, a nie wartość). Wszystkie wykrycia dotyczą bloków kluczy prywatnych.
 
### Wnioski i rekomendacje (bez zmian w kodzie)
- Klucz z `deployment.key` / `deployment2.key` należy uznać za **skompromitowany**: unieważnić go i wygenerować nowy (min. RSA 2048/3072 lub Ed25519), a następnie wymienić go wszędzie, gdzie był używany.
- Samo usunięcie plików w nowym commicie nie wystarcza, bo klucz pozostaje w historii (commity `de9d7b8` i `bc17b7d`). Historię trzeba przepisać (`git filter-repo` lub BFG) i wymusić ponowne sklonowanie repozytorium. Jeśli repozytorium było publiczne, klucz trzeba traktować jako ujawniony niezależnie od przepisania historii.
- Plik `awscredentials.json` przejrzeć ręcznie w całości; jeśli zawiera prawdziwe poświadczenia, zrotować je tak jak klucz.
 
---
 
## Zadanie 3 – podatne biblioteki (safety)
 
```
docker run -it -v <ścieżka>/Python/Flask_Book_Library:/sources pyupio/safety safety check -r /sources/requirements-task.txt --full-report
```
Safety sprawdził **18 pakietów** z `requirements-task.txt` i zgłosił **17 podatności w 5 pakietach**:
 
| Pakiet | Wersja | Liczba | ID (safety) i zakres podatnych wersji | Typ podatności |
|---|---|---|---|---|
| werkzeug | 2.3.7 | 8 | 62019 (<2.3.8), 73969 (<3.0.6), 73889 (<3.0.6), 82196 (<3.1.4), 84324 (<3.1.5), 86908 (<3.1.6), 71595 (<=2.3.7), 71594 (>=0.3,<3.0.3) | DoS przy parsowaniu multipart, path traversal / DoS w `safe_join` (tylko Windows), RCE przez debugger |
| jinja2 | 3.1.2 | 5 | 64227 (<3.1.3), 71591 (<3.1.4), 76378 (<3.1.5), 75976 (<3.1.6), 74735 (>=3.0.0a1,<3.1.5) | XSS przez filtr `xmlattr`, ucieczka z sandboxa (wymaga kontroli nad treścią szablonu) |
| mako | 1.2.4 | 2 | 98067 (<1.3.12), 93670 (<=1.3.10) | path traversal w `TemplateLookup.get_template()` |
| flask | 2.3.3 | 1 | 86909 (<3.1.3) | ujawnienie informacji (brak nagłówka `Vary: Cookie`) |
| healpy | 1.8.0 | 1 | 61774 (<=1.16.6) | podatna wersja dołączonej biblioteki libcurl („high-severity”) |
 
Darmowa baza nie podaje w raporcie numerów CVE ani ocen CVSS. Do wyboru podatności o najwyższej krytyczności przypisano je na podstawie identyfikatorów safety i opisów: ID 61774 odpowiada **CVE-2023-38545**, a ID 71594 odpowiada **CVE-2024-34069**.
 
### Analiza podatności o najwyższej krytyczności
**`healpy 1.8.0` – CVE-2023-38545 (safety ID 61774), CVSS 3.1 = 9.8 CRITICAL (NVD)**
 
- **Opis:** przepełnienie bufora na stercie w **libcurl** (wersje 7.69.0–8.3.0) podczas handshake'u SOCKS5. `healpy` ≤ 1.16.6 dostarcza w wheelu własną kopię libcurl, której używa cfitsio do odczytu plików FITS spod URL-a.
- **Warunki wykorzystania:** wszystkie poniższe muszą być spełnione jednocześnie:
  1. kod wywołuje healpy/cfitsio z **adresem sieciowym** (np. `healpy.read_map("https://...")`),
  2. ruch idzie przez **proxy SOCKS5 z rozwiązywaniem nazw po stronie proxy** (`socks5h://` w zmiennej środowiskowej albo `CURLPROXY_SOCKS5_HOSTNAME`),
  3. atakujący kontroluje serwer, który przekierowuje na hostname dłuższy niż 255 bajtów, i spowalnia handshake.
- **Sytuacja w badanej aplikacji:**
  - `healpy` nie jest importowany w żadnym pliku `.py`,
  - aplikacja nie pobiera żadnych plików FITS ani niczego spod zewnętrznych URL-i,
  - pakiet jest tylko w `requirements-task.txt`; Dockerfile instaluje `requirements.txt`, więc **healpy w ogóle nie trafia do obrazu**,
  - nie jest skonfigurowane żadne proxy SOCKS.
- **Wniosek:** podatna funkcja nie jest osiągalna, więc prawdopodobieństwo wykorzystania jest **minimalne (praktycznie zerowe)**.
Dla porównania druga w kolejności: **Werkzeug CVE-2024-34069 (CVSS 7.5, RCE przez debugger)**. Wymaga włączonego debuggera (`debug=True` / `--debug`). Obraz uruchamia `flask run` bez debugu (`FLASK_ENV` jest ignorowany od Flask 2.3), więc w kontenerze ryzyko jest niskie. Realne ryzyko istnieje tylko przy lokalnym uruchomieniu przez `python app.py`, bo tam jest `app.run(debug=True)`.
 
### Rekomendacje (bez zmian w kodzie)
- Usunąć nieużywany pakiet `healpy` (albo, jeśli jest potrzebny, podnieść go do `healpy >= 1.17`).
- Usunąć `debug=True` z `app.py`.
- `python:3.9` jest EOL od 10.2025
- Podnieść pakiety do wersji bez znanych podatności:
  
| Pakiet | Obecnie | Rekomendowana |
|---|---|---|
| Flask | 2.3.3 | 3.1.3 |
| Werkzeug | 2.3.7 | 3.1.9 |
| Jinja2 | 3.1.2 | 3.1.6 |
| Mako | 1.2.4 | 1.3.12 (ostatnia wersja dla Pythona 3.9) |
| itsdangerous / blinker | 2.1.2 / 1.6.2 | 2.2.0 / 1.9.0 (wymagane przez Flask 3.1) |
 
