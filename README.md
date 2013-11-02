Generator słów kluczowych
==============================
*Zadanie rekrutacyjne.*

Wymagania
---------
* Python 2.7 (ze względu na dict comprehensions)
* nltk > 2.0

Metody znajdywania słów kluczowych
----------------------------------
* W oparciu o bilbiotekę NLTK - usunięcie stop words, analiza częstotliwości występowania słów, wyszukanie bi-gramów.
* Prosta - usunięcie stop words, analiza częstotliowści wystepowania słów. Brak zewnętrznych zależności (poza plikami stop words).
* Calais - zapytanie o tagi sieciowego API serwisu OpenCalais (http://www.opencalais.com/). Brak obsługi języka polskiego.

Metody NLTK i prosta wykrywają język tekstu celem wczytania odpowiednich stop words.

Czytelność kodu
---------------
Starałem się zachować równowagę pomiędzy czytelnością kodu a "pythonizacją". Można łatwo uprościć czytanie, np. rozwijając skomplikowane list comprehensions.

Większość funkcji nie wymagała szerszych komentarzy, szczegółowe docstringi ograniczyłem do metod "publicznych".

Zastosowałem zawijanie linii do 99 znaków.

Wydajność
---------
Z punktu widzenia wydajności najsłabszym ogniwem projektu są listy słów odczytywane z dysku (ze względu na ich łatwą dostepność). Docelowo powinno się je umieścić w cache'u.

W przypadku generatora wykorzystującego API Calais wąskim gardłem jest oczywiście zapytanie zdalnego serwera.

Słowa kluczowe
--------------
Samo zagadnienie wyszukiwania słów kluczowych jest złożone. Wyniki możnaby znacznie poprawić przez:
* Obszerne tablice stopwords
* Generatory rdzeni słów
* Lepsze klasyfikatory niż tylko częstość wystepowania (analiza leksykalna)
* Stworzenie indeksu wszystkich tekstów danego projektu i wyszukiwanie słów wyjątkowych w tym kontekście
