# Poveste pe Note

Pagină statică HTML, fără build sau dependențe. Pentru previzualizare locală:

```bash
python3 -m http.server 8000
```

Apoi deschide `http://localhost:8000`.

## Formularul de comandă

Adresa de contact se configurează în meta-tagul `order-email` din `index.html`:

```html
<meta name="order-email" content="comenzi@povesteapenote.ro" />
```

Formularul validează câmpurile și pregătește un mesaj de e-mail cu toate detaliile. Vizitatorul trebuie să apese „Trimite” în aplicația sa de e-mail. Dacă nu are un client de e-mail configurat sau mesajul este prea lung pentru un link `mailto:`, poate descărca un fișier `.eml` ori copia textul. Site-ul static nu transmite și nu stochează comenzile pe un server.

Pentru trimitere automată, fără aplicația de e-mail a vizitatorului, este necesar un serviciu/backend de e-mail configurat pentru domeniu; cheile și secretele nu trebuie puse în HTML-ul public.

## Încărcarea pieselor demonstrative

Nu există un formular de upload public pentru vizitatori. Adaugă fișierele audio în repository, în `assets/audio/`, cu numele de mai jos:

- `locul-meu-e-langa-tine.mp3` — cardul Romantic pop
- `mama-primul-meu-acasa.mp3` — cardul Baladă emoționantă
- `legenda-din-gasca.mp3` — cardul Pop vesel

Playerul folosește automat fișierul MP3 dacă există; dacă lipsește, redă fragmentul sintetic de demonstrație. Pentru alte nume sau căi, schimbă proprietatea `audioFile` a piesei corespunzătoare din obiectul `tracks` din `index.html`. MP3 este formatul recomandat; păstrează fișierele comprimate și adaugă numai materiale pe care ai dreptul să le publici. Fișierele puse în repository vor fi publice împreună cu site-ul.

## Înainte de publicarea comercială

- Confirmă că inboxul din `order-email` există și este monitorizat.
- Completează identitatea legală a operatorului și verifică politicile afișate, condițiile comerciale, livrarea, anularea și drepturile asupra materialelor.
- Verifică prețurile și conținutul pachetelor.
- Publică pagina prin HTTPS.
