# Zad1

dane wrażliwe są wyświetlane tylko w przypadku wykonania operacji tworzenia nowego użytkownika. Logi pokazują wtedy dane wrażliwe jak pesel, miejsce zamieszkania.

log:
`Getting: Customer(ID: None, Name: imie, City: city, Age: 22, Pesel: 20001110, Street: street, AppNo: 40)`

### Poprawki:
Problem został naprawiony przez zastosowania wzorca projektowego read-once dla pól PESEL, street, appno.
Aby było to możliwe, została stworzona nowa klasa dla oddzielenia bazy danych (klasa CustomerDBModel) or klasy używanej przez backend (klasa Customer). Klasa Customer posiada pola typu read-once, które dla metody str() zwracają "Sensitive Data: ***".

log:
`Getting: Customer(Name: a, City: a, Age: 11, Pesel: Sensitive Data: ***, Street: Sensitive Data: ***, AppNo: Sensitive Data: ***)`

# Zad2

Git leaks znalazło 3 sekrety

### 1
Zcommitowany klucz prywatny RSA w pliku deployment.key,
dla commita:
`bc17b7ddc46f46fff175aed55d68e11bb48166cc`
link:
`https://github.com/Mixeway-Academy/task2/blob/bc17b7ddc46f46fff175aed55d68e11bb48166cc/deployment.key#L1`
### 2
Zcommitowany klucz prywatny RSA w pliku deployment2.key
dla commita:
`de9d7b8cb63bd7ae741ec5c9e23891b71709bc28`
link:
`https://github.com/Mixeway-Academy/task2/blob/de9d7b8cb63bd7ae741ec5c9e23891b71709bc28/deployment2.key#L1`

### 3
Zcommitowany klucz prywatny RSA w pliku awscredentials.json dla commita:
`bc17b7ddc46f46fff175aed55d68e11bb48166cc`
link:
`https://github.com/Mixeway-Academy/task2/blob/de9d7b8cb63bd7ae741ec5c9e23891b71709bc28/deployment2.key#L1`

# Zad 3

Przeanalizowałem exploit:

| jinja2                     | 3.1.2     | <3.1.5                   | 76378    |
+==============================================================================+
| An oversight in how the Jinja sandboxed environment detects calls to         |
| str.format allows an attacker who controls the content of a template to      |
| execute arbitrary Python code. To exploit the vulnerability, an attacker     |
| needs to control the content of a template. Whether that is the case depends |
| on the type of application using Jinja. This vulnerability impacts users of  |
| applications which execute untrusted templates. Jinja's sandbox does catch   |
| calls to str.format and ensures they don't escape the sandbox. However, it's |
| possible to store a reference to a malicious string's format method, then    |
| pass that to a filter that calls it. No such filters are built-in to Jinja,  |
| but could be present through custom filters in an application. After the     |
| fix, such indirect calls are also handled by the sandbox.                    |
+==============================================================================+

Oznacza on, że w tej wersji, jeżeli atakujący miał dostęp do niezabezpieczoego template (na przykład przy używaniu render_template_string) możliwe było wykonanie zdefiniowanego obiektu format dla obiektu string (przy użyciu metody set), następne, jeżeli deweloperzy aplikacji zdefiniowali własny filtr, (przy użyciu @blueprint.app_template_filter("name")), możliwe było wywołanie tego filtru z podaniem obiektu format jako argumentu. Jako że metoda filtr znajdywała się poza sandoxem Jinja, możliwe było dostanie się do atrybutów globalnych, i
zdalne wykonanie kodu.

W tej aplikacji, wykonanie tego exploitu nie jest możliwe, gdyż używa ona tylko metody render_template, która blokuje możliwość interpretowania otrzymanych danych jako template syntax.