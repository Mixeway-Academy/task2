# Wrażliwe dane:
```
Getting: Customer(ID: None, Name: Andrzej, City: Warszawa, Age: 18, Pesel: 12345677, Street: Plac Politechniki, AppNo: 1)
```
W powyższym logu mamy adres oraz Pesel osoby zapisywane jawnie i niezaszyfrowane a także skojarzone z imieniem.
Pojawiają się one tylko w przypadku dodanie nowego gościa biblioteki, nie w przypadku wypożyczeń.

# Poprawki

```python
    def __repr__(self):
        return f"Customer(ID: {self.id}, Name: {self.name}, City: {self.city}, Age: {self.age}, Pesel: {self._mask_sensitive(self.pesel)}, Street: {self._mask_sensitive(self.street)}, AppNo: {self._mask_sensitive(self.appNo)})"
    
    def _mask_sensitive(self, value):
        """Mask sensitive data by replacing with asterisks"""
        if value:
            return '*' * len(str(value))
        return value
```
Dodano funkcję _mask_sensitive, która zamienia wybrane dane na "*".
Wynik:
```
Getting: Customer(ID: None, Name: Jan, City: Wawa, Age: 420, Pesel: *********, Street: ********, AppNo: **).
```
