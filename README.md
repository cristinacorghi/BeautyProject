# La Profumeria

Sito web per la vendita di profumi.
* Funzione utente anonimo: visualizzare i prodotti disponibili e il relativo prezzo, navigare il sito, leggere le recensioni.
* Funzione utenti registrati: funzionalità dell'utente anonimo con l'aggiunta di:
  * poter scrivere le recensioni ai prodotti;
  * aggiungere i prodotti al carrello e acquistarli
  * pagina dedicata all'utente con la possibilità di inserire un'immagine del profilo;
  * nel caso in cui un prodotto fosse esaurito, possibilità di ricevere una email per la nuova disponibilità del prodotto.
* Funzione utente amministratore: è come un utente registrato ma può modificare i prodotti.
---
# Init Project
'django-admin startproject LaProfumeria'

# Init Applications
'django-admin startapp Store'
'django-admin startapp carts'

# Run Project
'python3 manage.py runserver'

# Test Project
'python3 manage.py test Store'
'python3 manage.py test carts'
---
Versione di Python utilizzata:
* Python 3.8.10