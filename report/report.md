
## Zadanie 1 - dane wrażliwe

W aplikacji Java podczas dodawania nowego studenta do logów trafiały wszystkie jego dane osobowe: imię i nazwisko, e-mail, data urodzenia oraz dokładny adres. Zgodnie z wymaganiem zadania format logu musiał pozostać bez zmian, dlatego dane osobowe zostały w nich zamaskowane.

**Logi przed zmianą:**

```text
2026-11-11 14:35:56.632  INFO 1 --- [nio-8080-exec-4] com.example.thymeleaf.entity.Student     : Created user Student{id='101224d1-f6e8-417b-af6e-504e29b3dc87', name='Mike Wazowski', email='mike@wazowski.pl', birthday=2026-11-11, createdAt=2026-11-11T14:35:56.632372, updatedAt=null, address=Address{id='null', zipCode='20040-020', street='Testowa', number='14', complement='', district='Dzielnica', city='Test', state='DE', createdAt=null, updatedAt=null}}
2026-11-11 14:40:16.027  INFO 1 --- [nio-8080-exec-7] com.example.thymeleaf.entity.Student     : Created user Student{id='44c86e80-e3c5-4cb7-863e-774c1834ad48', name='John Doe', email='john@doe.pl', birthday=2026-11-11, createdAt=2026-11-11T14:40:16.027284, updatedAt=null, address=Address{id='null', zipCode='00000-111', street='Test', number='11', complement='', district='Ooo', city='Ttt', state='DE', createdAt=null, updatedAt=null}}
```

**Logi po zmianie:**

```text
2026-11-11 14:58:55.341  INFO 1 --- [nio-8080-exec-3] com.example.thymeleaf.entity.Student     : Created user Student{id='a520a19f-9103-4ca7-9782-ac208eeb5793', name='***', email='***', birthday=***, createdAt=2026-11-11T14:58:55.341660, updatedAt=null, address=Address{id='null', zipCode='***', street='***', number='***', complement='***', district='***', city='***', state='***', createdAt=null, updatedAt=null}}
2026-11-11 14:59:43.116  INFO 1 --- [nio-8080-exec-6] com.example.thymeleaf.entity.Student     : Created user Student{id='f4628326-32e1-49f5-93a2-b99b64242914', name='***', email='***', birthday=***, createdAt=2026-11-11T14:59:43.116977, updatedAt=null, address=Address{id='null', zipCode='***', street='***', number='***', complement='***', district='***', city='***', state='***', createdAt=null, updatedAt=null}}
```

## Zadanie 2 - sekrety

Gitleaks wykrył 2 klucze prywatne w 3 różnych plikach. Plików z tymi kluczami nie ma już w kodzie, ale nadal są dostępne w historii gita. Nie są to fałszywe alarmy.

Przetestowałem też trochę gitleaks lokalnie i uważam, że w domyślnej konfiguracji nie zgłasza wielu fałszywie pozytywnych wyników. Narzędzie wykorzystuje to, że prawdziwe klucze i tokeny do konkretnych serwisów mają określony format, więc może mieć dla nich osobne reguły (np. `RuleID: stripe-access-token`). Przed fałszywie pozytywnymi wynikami w dużej mierze chroni reguła `generic-api-key`, która zgłasza tylko hasła o dużej entropii, czyli takie, które wyglądają na realnie używane. Właśnie dlatego nie zostały zgłoszone ani proste hasło `spring.database.password=1qaz@WSX` w `application.properties`, ani zmienna `String password = "";` w `StudentController`, która nie ma przypisanej żadnej wartości.

**Wynik gitleaks:**

```text
    ○
    │╲
    │ ○
    ○ ░
    ░    gitleaks

Finding:     -----BEGIN RSA PRIVATE KEY-----
MIIBOgIBAAJBAKj34GkxFhD90vcNLYLInFEX6Ppy1tPf9Cnzj4p4WGeKLs1Pt8Qu
KUp...
Secret:      -----BEGIN RSA PRIVATE KEY-----
MIIBOgIBAAJBAKj34GkxFhD90vcNLYLInFEX6Ppy1tPf9Cnzj4p4WGeKLs1Pt8Qu
KUp...
RuleID:      private-key
Entropy:     5.875154
File:        deployment.key
Line:        1
Commit:      bc17b7ddc46f46fff175aed55d68e11bb48166cc
Author:      Grzegorz Siewruk
Email:       gsiewruk@gmail.com
Date:        2023-11-15T12:52:32Z
Fingerprint: bc17b7ddc46f46fff175aed55d68e11bb48166cc:deployment.key:private-key:1
Link:        https://github.com/Sebastian-Abramowski/task2/blob/bc17b7ddc46f46fff175aed55d68e11bb48166cc/deployment.key#L1

Finding:     -----BEGIN RSA PRIVATE KEY-----
MIIBOgIBAAJBAKj34GkxFhD90vcNLYLInFEX6Ppy1tPf9Cnzj4p4WGeKLs1Pt8Qu
KUp...
Secret:      -----BEGIN RSA PRIVATE KEY-----
MIIBOgIBAAJBAKj34GkxFhD90vcNLYLInFEX6Ppy1tPf9Cnzj4p4WGeKLs1Pt8Qu
KUp...
RuleID:      private-key
Entropy:     5.875154
File:        deployment2.key
Line:        1
Commit:      de9d7b8cb63bd7ae741ec5c9e23891b71709bc28
Author:      Grzegorz Siewruk
Email:       gsiewruk@gmail.com
Date:        2023-11-15T12:49:39Z
Fingerprint: de9d7b8cb63bd7ae741ec5c9e23891b71709bc28:deployment2.key:private-key:1
Link:        https://github.com/Sebastian-Abramowski/task2/blob/de9d7b8cb63bd7ae741ec5c9e23891b71709bc28/deployment2.key#L1

Finding:     "private_key": "-----BEGIN PRIVATE KEY-----\nlRsGbRO/1A5LiQHjuR5SASDASDAiSMNeOYqna2R+HEalBoyISASDASD1Tgkj\n4CC02Uux+...\n",
Secret:      -----BEGIN PRIVATE KEY-----\nlRsGbRO/1A5LiQHjuR5SASDASDAiSMNeOYqna2R+HEalBoyISASDASD1Tgkj\n4CC02Uux+...
RuleID:      private-key
Entropy:     5.917361
File:        awscredentials.json
Line:        5
Commit:      bc17b7ddc46f46fff175aed55d68e11bb48166cc
Author:      Grzegorz Siewruk
Email:       gsiewruk@gmail.com
Date:        2023-11-15T12:52:32Z
Fingerprint: bc17b7ddc46f46fff175aed55d68e11bb48166cc:awscredentials.json:private-key:5
Link:        https://github.com/Sebastian-Abramowski/task2/blob/bc17b7ddc46f46fff175aed55d68e11bb48166cc/awscredentials.json#L5

3:17PM INF 5 commits scanned.
3:17PM INF scanned ~21991492 bytes (21.99 MB) in 1m7s
3:17PM WRN leaks found: 3
```

## Zadanie 3 - biblioteki OpenSource

Ze względu na problemy z uruchomieniem OWASP Dependency Check raport podatności wygenerowano inaczej niż w instrukcji. Wyniki: [sbom.json](./dependency-scan/sbom.json), [raport.html](./dependency-scan/raport.html).

**Wybrana podatność:** CVE-2025-24813 (krytyczna, CVSS 9.8 wg NIST NVD)

**Pakiet:** `org.apache.tomcat.embed:tomcat-embed-core:9.0.50`

**Analiza:** Podatność dotyczy `DefaultServlet`, czyli komponentu Tomcata, który udostępnia pliki statyczne. Domyślnie pozwala on tylko na ich odczyt (GET), a błąd ujawnia się dopiero przy żądaniach typu PUT: atakujący może wtedy wgrać na serwer spreparowany plik i w pewnych warunkach uruchomić na serwerze własny kod (RCE).

Tomcat jest wbudowany w aplikację (biblioteka `tomcat-embed-core` w JAR-ze), więc podatny kod jest obecny. Jednak w Spring Boot od wersji 2.4 `DefaultServlet` jest domyślnie wyłączony (`server.servlet.register-default-servlet=false`), dlatego w badanej aplikacji podatność nie występuje.
