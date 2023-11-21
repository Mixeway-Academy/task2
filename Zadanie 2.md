Uruchomiono w folderze Task2 skan za pomocą komendy:

docker run -v ${path_to_host_folder_to_scan}:/path zricethezav/gitleaks:latest detect --source="/path" -v 

Wyniki:

![Zadanie 2 - Część 1](https://github.com/PW-user/task2/assets/150120897/4f67c52d-5c6f-47d9-8c2b-118fc8b28938)

![Zadanie 2 - Część 2](https://github.com/PW-user/task2/assets/150120897/bef561ec-4af2-4927-a3f6-51724a5845da)

Zostały znalezione 4 wyniki o potencjalnych leakach haseł/kluczy. Dla dwóch pierwszych wyników znaleziono klucze prywatne (kolejno w plikach: deployment.key oraz deployment2.key) co nie ejst false-positivem. 

Dla trzeciego wyniku znaleziono id klucza co nie jest prawidłowo zarejestrowanym leakiem (False-positive), natomiast dla czwartego wynik zarejestrowano prywatny klucz co jest prawidłowo zarejestrowanym leakiem.

Należy unikać umieszczania haseł bezpośrednio w kodzie. Zamiast tego, zalecane jest używanie narzędzi do zarządzania hasłami, takich jak menedżery haseł lub systemy zarządzania konfiguracją. 
