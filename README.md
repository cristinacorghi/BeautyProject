# BeautyProject

Sito web per la vendita di profumi.
* Funzione utente anonimo: visualizzare i prodotti disponibili e il relativo prezzo, navigare il sito, leggere le recensioni.
* Funzione utenti registrati: funzionalità dell'utente anonimo con l'aggiunta di:
  * poter scrivere le recensioni ai prodotti;
  * aggiungere i prodotti al carrello e acquistarli
  * pagina dedicata all'utente con la possibilità di inserire un'immagine del profilo;
  * nel caso in cui un prodotto fosse esaurito, possibilità di ricevere una email per la nuova disponibilità del prodotto.
* Meccanismo di ricerca di un prodotto:
  * tramite la barra di ricerca;
  * tramite la selezione di diverse caratteristiche quali prezzo, marca, profumi uomo e profumi donna.
* Meccanismo di login e registrazione degli utenti.
---
# Init Project
'django-admin startproject BeautyProject'

# Init Applications
'django-admin startapp Store'
'django-admin startapp carts'
---
Versione di Python utilizzata:
* Python 3.8.10
# Run Project
'python3 manage.py runserver'
# Test Project