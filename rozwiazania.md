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



