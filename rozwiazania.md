# Rozwiązanie laboratorium

## Zadanie 1 - Weryfikacja wycieku wrażliwych danych
Wybrałem technologię Python i uruchomiłem aplikację biblioteki. Po wypełnieniu formularzy na stronie \customers dodałem użytkownika (rysunek poniżej).

<img width="1158" height="700" alt="image" src="https://github.com/user-attachments/assets/146106dd-bbad-452f-94b9-f9e88a054aca" />
<br>
<br>

Niestety w logach w terminalu wyświetlone zostały jawnym tekstem wszystkie podane przeze mnie dane.

<img width="810" height="241" alt="logi" src="https://github.com/user-attachments/assets/6a5378a9-cde4-4931-a685-d372db2d6712" />

Aby zapobiec potencjalnemu wyciekowi danych poufnych (podawany tam był między innymi numer PESEL) wprowadziłem poprawkę maskującą dane znakami **'*'**. Zmianę zaimplementowano w pliku `Flask_Book_Library/project/customers/models.py`. 

```
# Dodanie funkcji masked w pliku customers/models.py

def masked(data):
    if data:
        return '*' * len(data)
    return none

# (...)

 def __repr__(self):
        return f"Customer(ID: {self.id}, Name: {masked(self.name)}, City: {masked(self.city)}, Age: {masked(self.age)},
Pesel: {masked(self.pesel)}, Street: {masked(self.street)}, AppNo: {masked(self.appNo)})"

```

Po wprowadzeniu poprawek dane wszystkich pól poza ID są maskowane, co uniemożliwia odczytanie ich bezpośrednio z logów. Wszystkie znaki zostały zastąpione przez **'*'** w odpowiedniej ilości.
<img width="1042" height="222" alt="image" src="https://github.com/user-attachments/assets/464a28b9-42bf-474c-bfd1-f853bb2735a6" />

## Zadanie 2 - weryfikacja wycieku sekretów

W tym zadaniu należało przeskanować używane repozytorium przy pomocy aplikacji **gitleaks**. Uruchomiono aplikację w folderze Task2 i w wyniku skanowania plików otrzymano 3 alarmy:
- klucz prywatny RSA w pliku `deployment.key`
- ten sam klucz, ale w pliku `deployment2.key`
- klucz prywatny w pliku `awscredentials.json`

Użycie aplikacji pozwoliło na znalezienie i bezproblemowe odczytanie sekretów. Zwrócone przez program wyniki nie były alarmami false-positive. Dodatkowo w terminalu pojawiają się dane autora oraz link do znalezionego pliku w repozytorium.

<img width="1088" height="757" alt="tbo2zad2" src="https://github.com/user-attachments/assets/854f264c-7f33-4aa4-a5da-c286a616b891" />

## Zadanie 3 - weryfikacja bezpieczeństwa bibliotek OpenSource wykorzystywanych w projekcie
Zweryfikowałem biblioteki wykorzystywane w projekcie Python/Flask_Book_Library. W wyniku skanowania `safety` w terminalu pojawił się raport ze znalezionymi lukami bezpieczeństwa.

<img width="1085" height="746" alt="image" src="https://github.com/user-attachments/assets/5b4e477b-fa0f-4be0-b190-d5c592788108" />

Pełny raport:

```
+==============================================================================+
| REPORT                                                                       |
| checked 18 packages, using free DB (updated once a month)                    |
+============================+===========+==========================+==========+
| package                    | installed | affected                 | ID       |
+============================+===========+==========================+==========+
| flask                      | 2.3.3     | <3.1.3                   | 86909    |
+==============================================================================+
| Affected versions of the Flask package are vulnerable to Information         |
| Disclosure due to missing cache-variation headers when the session object is |
| accessed via certain code paths. In Flask’s session handling, accessing      |
| flask.session is intended to set a Vary: Cookie response header, but session |
| key-only access patterns (such as using the Python in operator to test for a |
| key without reading or mutating session values) can bypass the logic that    |
| adds the header.                                                             |
+==============================================================================+
| jinja2                     | 3.1.2     | <3.1.3                   | 64227    |
+==============================================================================+
| Jinja is an extensible templating engine. Special placeholders in the        |
| template allow writing code similar to Python syntax. It is possible to      |
| inject arbitrary HTML attributes into the rendered HTML template,            |
| potentially leading to Cross-Site Scripting (XSS). The Jinja `xmlattr`       |
| filter can be abused to inject arbitrary HTML attribute keys and values,     |
| bypassing the auto escaping mechanism and potentially leading to XSS. It may |
| also be possible to bypass attribute validation checks if they are           |
| blacklist-based.                                                             |
+==============================================================================+
| jinja2                     | 3.1.2     | <3.1.4                   | 71591    |
+==============================================================================+
| Jinja is an extensible templating engine. The `xmlattr` filter in affected   |
| versions of Jinja accepts keys containing non-attribute characters. XML/HTML |
| attributes cannot contain spaces, `/`, `>`, or `=`, as each would then be    |
| interpreted as starting a separate attribute. If an application accepts keys |
| (as opposed to only values) as user input, and renders these in pages that   |
| other users see as well, an attacker could use this to inject other          |
| attributes and perform XSS. The fix for CVE-2024-22195 only addressed spaces |
| but not other characters. Accepting keys as user input is now explicitly     |
| considered an unintended use case of the `xmlattr` filter, and code that     |
| does so without otherwise validating the input should be flagged as          |
| insecure, regardless of Jinja version. Accepting _values_ as user input      |
| continues to be safe.                                                        |
+==============================================================================+
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
| jinja2                     | 3.1.2     | <3.1.6                   | 75976    |
+==============================================================================+
| Prior to 3.1.6, an oversight in how the Jinja sandboxed environment          |
| interacts with the |attr filter allows an attacker that controls the content |
| of a template to execute arbitrary Python code. To exploit the               |
| vulnerability, an attacker needs to control the content of a template.       |
| Whether that is the case depends on the type of application using Jinja.     |
| This vulnerability impacts users of applications which execute untrusted     |
| templates. Jinja's sandbox does catch calls to str.format and ensures they   |
| don't escape the sandbox. However, it's possible to use the |attr filter to  |
| get a reference to a string's plain format method, bypassing the sandbox.    |
| After the fix, the |attr filter no longer bypasses the environment's         |
| attribute lookup. This vulnerability is fixed in 3.1.6.                      |
+==============================================================================+
| jinja2                     | 3.1.2     | >=3.0.0a1,<3.1.5         | 74735    |
+==============================================================================+
| A vulnerability in the Jinja compiler allows an attacker who can control     |
| both the content and filename of a template to execute arbitrary Python      |
| code, bypassing Jinja's sandbox protections. To exploit this vulnerability,  |
| an attacker must have the ability to manipulate both the template's filename |
| and its contents. The risk depends on the application's specific use case.   |
| This issue affects applications that render untrusted templates where the    |
| attacker can determine the template filename, potentially leading to severe  |
| security breaches.                                                           |
+==============================================================================+
| mako                       | 1.2.4     | <1.3.12                  | 98067    |
+==============================================================================+
| Affected versions of the Mako package are vulnerable to Path Traversal due   |
| to a mismatch between the posixpath-based URI normalisation used in          |
| TemplateLookup.get_template() and the Windows-native ntpath path resolution  |
| used by os.path.isfile() and os.path.normpath() in Template.__init__(). The  |
| get_template() method normalises the URI using posixpath, which treats       |
| backslashes as literal characters and thus fails to detect directory         |
| traversal sequences embedded via backslash separators, while                 |
| os.path.normpath() in Template.__init__() resolves backslash-based ..        |
| sequences to a form that bypasses the startswith("..") guard. An attacker    |
| who can supply a user-controlled template name or include path to            |
| TemplateLookup.get_template() on a Windows host can read arbitrary files     |
| outside the configured template directory, and if the targeted file contains |
| Mako or Python template syntax, it may additionally be parsed and executed   |
| as a template.                                                               |
+==============================================================================+
| mako                       | 1.2.4     | <=1.3.10                 | 93670    |
+==============================================================================+
| Affected versions of the Mako package are vulnerable to Path Traversal due   |
| to inconsistent stripping of leading slashes between                         |
| TemplateLookup.get_template() and Template.init when resolving a template    |
| URI. TemplateLookup.get_template() strips all leading forward slashes before |
| joining the URI with the template directory via posixpath.join, while        |
| Template.init strips only a single leading slash before calling normpath, so |
| a URI beginning with a double slash is resolved to an absolute path like     |
| /etc/passwd that bypasses the subsequent startswith traversal check. An      |
| attacker who can pass untrusted input to TemplateLookup.get_template() can   |
| exploit this to read arbitrary files readable by the process and have their  |
| contents returned as rendered template output, resulting in unauthorized     |
| arbitrary file disclosure.                                                   |
+==============================================================================+
| werkzeug                   | 2.3.7     | <2.3.8                   | 62019    |
+==============================================================================+
| Werkzeug 3.0.1 and 2.3.8 include a security fix: Slow multipart parsing for  |
| large parts potentially enabling DoS attacks.                                |
| https://github.com/pallets/werkzeug/commit/b1916c0c083e0be1c9d887ee2f3d69692 |
| 2bfc5c1                                                                      |
+==============================================================================+
| werkzeug                   | 2.3.7     | <3.0.6                   | 73969    |
+==============================================================================+
| Affected versions of Werkzeug are vulnerable to Path Traversal (CWE-22) on   |
| Windows systems running Python versions below 3.11. The safe_join() function |
| failed to properly detect certain absolute paths on Windows, allowing        |
| attackers to potentially access files outside the intended directory. An     |
| attacker could craft special paths starting with "/" that bypass the         |
| directory restrictions on Windows systems. The vulnerability exists in the   |
| safe_join() function which relied solely on os.path.isabs() for path         |
| validation. This is exploitable on Windows systems by passing paths starting |
| with "/" to safe_join(). To remediate, upgrade to the latest version which   |
| includes additional path validation checks.                                  |
| NOTE: This vulnerability specifically affects Windows systems running Python |
| versions below 3.11 where ntpath.isabs() behavior differs.                   |
+==============================================================================+
| werkzeug                   | 2.3.7     | <3.0.6                   | 73889    |
+==============================================================================+
| Affected versions of Werkzeug are potentially vulnerable to resource         |
| exhaustion when parsing file data in forms. Applications using               |
| 'werkzeug.formparser.MultiPartParser' to parse 'multipart/form-data'         |
| requests (e.g. all flask applications) are vulnerable to a relatively simple |
| but effective resource exhaustion (denial of service) attack. A specifically |
| crafted form submission request can cause the parser to allocate and block 3 |
| to 8 times the upload size in main memory. There is no upper limit; a single |
| upload at 1 Gbit/s can exhaust 32 GB of RAM in less than 60 seconds.         |
+==============================================================================+
| werkzeug                   | 2.3.7     | <3.1.4                   | 82196    |
+==============================================================================+
| Affected versions of the Werkzeug package are vulnerable to Denial of        |
| Service (DoS) due to improper handling of Windows special device names in    |
| the safe_join function. In Werkzeug versions before 3.1.4, safe_join permits |
| path segments such as “CON” or “AUX” to pass validation, allowing            |
| send_from_directory to construct a path that resolves to a Windows device    |
| file, which opens successfully but then blocks indefinitely when read.       |
+==============================================================================+
| werkzeug                   | 2.3.7     | <3.1.5                   | 84324    |
+==============================================================================+
| Affected versions of the Werkzeug package are vulnerable to Improper         |
| Handling of Windows Device Names due to incomplete validation of Windows     |
| reserved device names in user-controlled path segments. In                   |
| werkzeug.security.safe_join, path components ending with special device      |
| names (for example CON or AUX) are not reliably rejected when they include   |
| compound extensions (for example CON.txt.html) or trailing spaces, and       |
| werkzeug.utils.send_from_directory relies on safe_join when resolving a      |
| requested filename.                                                          |
+==============================================================================+
| werkzeug                   | 2.3.7     | <3.1.6                   | 86908    |
+==============================================================================+
| Affected versions of the Werkzeug package are vulnerable to Denial of        |
| Service (DoS) due to improper handling of Windows special device names in    |
| path joining logic. The safe_join() function fails to reject device-name     |
| path segments when they are preceded by other segments (for example,         |
| example/NUL), and send_from_directory() relies on safe_join() when resolving |
| user-supplied file paths.                                                    |
+==============================================================================+
| werkzeug                   | 2.3.7     | <=2.3.7                  | 71595    |
+==============================================================================+
| Werkzeug is a comprehensive WSGI web application library. If an upload of a  |
| file that starts with CR or LF and then is followed by megabytes of data     |
| without these characters: all of these bytes are appended chunk by chunk     |
| into internal bytearray and lookup for boundary is performed on growing      |
| buffer. This allows an attacker to cause a denial of service by sending      |
| crafted multipart data to an endpoint that will parse it. The amount of CPU  |
| time required can block worker processes from handling legitimate requests.  |
+==============================================================================+
| werkzeug                   | 2.3.7     | >=0.3,<3.0.3             | 71594    |
+==============================================================================+
| Werkzeug is a comprehensive WSGI web application library. The debugger in    |
| affected versions of Werkzeug can allow an attacker to execute code on a     |
| developer's machine under some circumstances. This requires the attacker to  |
| get the developer to interact with a domain and subdomain they control, and  |
| enter the debugger PIN, but if they are successful it allows access to the   |
| debugger even if it is only running on localhost. This also requires the     |
| attacker to guess a URL in the developer's application that will trigger the |
| debugger.                                                                    |
+==============================================================================+
| healpy                     | 1.8.0     | <=1.16.6                 | 61774    |
+==============================================================================+
| Healpy 1.16.6 and prior releases ship with a version of 'libcurl' that has a |
| high-severity vulnerability.                                                 |
+==============================================================================+

```
### Analiza podatności
Raport zgłosił 17 pakietów, między innymi **healpy**, **werkzeug** oraz **jinja2**. W pakiecie Jinja2 (wersja 3.1.2) wykryto podatność typu RCE (Arbitrary Python Code Execution / Sandbox Escape). W raporcie reprezentują ją błędy o ID: 75976, 76378 oraz 74735. Ze względu na możliwość wykonania dowolnego kodu na serwerze, jest to luka o najwyższej krytyczności. 

Podatność wynika z niedopatrzenia w mechanizmie sandbox używanym przez silnik Jinja2 do renderowania szablonów aplikacji. Środowisko to nie filtruje w pełni niebezpiecznych odwołań przy wykorzystaniu filtra `|attr` lub metody `str.format`. Teoretycznie możliwe jest zatem przejście z bezpiecznego środowiska do właściwego, dzięki wstrzyknięciu złośliwego kodu Python, co prowadzi do ataku Server-Side Template Injection (SSTI). Jednak żeby wykorzystanie tej podatności było fizycznie możliwe, atakujący musiałby mieć możliwość kontrolowania zawartości lub struktury pliku szablonu. W przypadku analizowanego frameworku Flask szablony widoków (na przykład interfejsy dodawania książek czy klientów) są w nim zdefiniowane na stałe w kodzie źródłowym backendu, do którego użytkownik końcowy nie ma dostępu. Sprawia to, że prawdopodobieńśtwo wykorzystania omawianej podatności jest minimalne.

Aby zneutralizować tą podatność, należy zaktualizować bibliotekę do wersji co najmniej 3.1.6, gdyż w opisie podatności napisano, że od tej wersji została ona usunięta.
