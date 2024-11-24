## Zadanie 1 - Weryfikacja wycieku wrażliwych danych
 Podczas "przeklikiwania się" przez aplikacje można było zauważyć, że w zakładce *Customers* opcja dodawania nowego klienta prosi o podanie danych wrażliwych takich jak np. PESEL. Wpisane w aplikacje dane są widoczne w logach. 

![Alt text](https://raw.githubusercontent.com/jagoda9/task2/refs/heads/main/z1_wyciek_logow.jpg "a title")

W kodzie aplikacji dodane zostały odpowiednie działania w wyniku których część danych została zamaskowana przy pomycy znaków *. 

![Alt text](https://raw.githubusercontent.com/jagoda9/task2/refs/heads/main/z1_wyciek_logow2.jpg)
## Zadanie 2 - weryfikacja wycieku sekretów

Widzimy, że w aplikacji *gitleaks* wykryte zostały wycieki sekretów. Po przyjrzeniu się im bliżej można uznać, że są to wykrycia realnych danych (nie są to wykrycia fałszywie pozytywne). Wśród skompromitowanych danych możemy zauważyć 4 wyniki dotyczące kluczy prywatnych. 
![Alt text](https://raw.githubusercontent.com/jagoda9/task2/refs/heads/main/wynik_gitleaks.jpg)
## Zadanie 3 - weryfikacja bezpieczeństwa bibliotek OpenSource wykorzystywanych w projekcie
Fragment raportu:

![Alt text](https://raw.githubusercontent.com/jagoda9/task2/refs/heads/main/fragment_raportu.jpg)

Po wykonaniu podanej w instrukcji komendy uzyskany został raport zawierający informacje o podatnościach. Widzimy, że znajdują się tu informacje odnoszące się do trzech pakietów:
- jinja2
- werkzeug
- healpy

W ramach zadania wybrany został pakiet jinja2 zawierający podatność związaną z atakiem typu Server-Side Template Injection (SSTI). Jest ona dość istotna, ponieważ pozwala na wstrzyknięcie atakującemu własnego kodu do szablonu strony. W ten sposób kod może zostać wykonany na serwerze powodując poważne szkody. 

Podatna w tym pakiecie jest funkcja *from_string* która przyjmuje parametr jako obiekt szablonu, renderuje go a następnie zwraca wynik. To dzięki niej atakujący może dokonać modyfikacji. W aplikacji nie zostało zauważone użycie tej funkcji, co sprawia, że wykorzystanie podatności jest mało prawdopodobne.
