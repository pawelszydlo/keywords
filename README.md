Generator słów kluczowych
==============================
*Zadanie rekrutacyjne.*

Czytelność kodu
---------------
Starałem się zachować równowagę pomiędzy czytelnością kodu a "pythonizacją". Można łatwo uprościć czytanie, np. rozwijając skomplikowane list comprehensions.

Wydajność
---------
Z punktu widzenia wydajności najsłabszym ogniwem projektu są listy słów odczytywane z dysku (ze względu na ich łatwą dostepność). Docelowo powinno się je umieścić w bazie danych, lub cache'u.
W przypadku generatora wykorzystującego API Calais wąskim gardłem jest oczywiście zapytanie zdalnego serwera.

Słowa kluczowe
--------------
Samo zagadnienie wyszukiwania słów kluczowych jest nielada wyzwaniem. Wyniki możnaby znacznie poprawić przez:
* Obszerne tablice stopwords
* Generatory rdzeni słów
* Lepsze klasyfikatory niż tylko częstość wystepowania (analiza leksykalna)
