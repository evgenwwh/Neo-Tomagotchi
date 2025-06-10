Neo Tamagotchi

Prosty projekt typu Tamagotchi napisany w Pythonie.
Użytkownik wybiera zwierzaka, nadaje mu imię i dba o jego energię oraz nastrój. Zwierzak umiera, jeśli jego poziom energii lub nastroju spadnie do 0.

Autorzy:
Yevhen Babalyk,Ivan Smirnov



Jak uruchomić grę?:

1.Upewnij się, że masz zainstalowane wymagane biblioteki:

    pip install customtkinter pillow


2.Uruchom grę:

    python src/pixel_pet_game.py


Jak wygenerować dokumentację?

1.Przejdź do katalogu docs/:

    cd docs

2.Wygeneruj dokumentację HTML:

    make.bat html (.\make.bat html)

lub alternatywnie:

    python -m sphinx -b html . _build/html

Gotową dokumentację znajdziesz tutaj:

    docs/_build/html/index.html

Możesz ją otworzyć w przeglądarce.

Uwagi:

Projekt zawiera dokumentację generowaną automatycznie przy użyciu Sphinx.

Wszystkie klasy i funkcje są opatrzone docstringami w języku polskim.

Obrazki zwierzaków (assets/) są używane w interfejsie graficznym gry.