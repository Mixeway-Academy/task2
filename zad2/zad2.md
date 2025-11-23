# Wyniki użycia programu gitleaks
Znaleziono 3 secrety:
```

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
Link:        https://github.com/PawelMurdzek/task2/blob/bc17b7ddc46f46fff175aed55d68e11bb48166cc/deployment.key#L1

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
Link:        https://github.com/PawelMurdzek/task2/blob/de9d7b8cb63bd7ae741ec5c9e23891b71709bc28/deployment2.key#L1

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
Link:        https://github.com/PawelMurdzek/task2/blob/bc17b7ddc46f46fff175aed55d68e11bb48166cc/awscredentials.json#L5
```

# Wycieki bezpieczeństwa:
Gitleaks wykrył **3 prawdziwe wycieki sekretów** w historii repozytorium Git:

1. **deployment.key** - klucz prywatny RSA (commit: bc17b7d, data: 15.11.2023)
2. **deployment2.key** - klucz prywatny RSA (commit: de9d7b8, data: 15.11.2023)
3. **awscredentials.json** - klucz prywatny w formacie JSON (commit: bc17b7d, data: 15.11.2023)

## Weryfikacja:

Pliki **NIE istnieją** w obecnym kodzie - zostały usunięte. Jednak **nadal są dostępne w historii Git**, co stanowi zagrożenie bezpieczeństwa.

## Wnioski:

- Wykrycia są **prawdziwe** (nie false positive)
- Klucze prywatne były commitowane do publicznego repozytorium
- Mimo usunięcia z kodu, klucze pozostają w historii i można je odzyskać
- Klucze należy uznać za skompromitowane i wymienić na nowe. W środowisku produkcyjnym powinny zostać natychmiast zdeaktywowane.

