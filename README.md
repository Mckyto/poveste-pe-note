# Poveste pe Note

Pagină statică HTML, fără build sau dependențe. Pentru previzualizare locală:

```bash
python3 -m http.server 8000
```

Apoi deschide `http://localhost:8000`.

## Formularul de comandă

Adresa de contact se configurează în meta-tagul `order-email` din `index.html`:

```html
<meta name="order-email" content="povestepenote.comenzi@gmail.com" />
```

Adresa din meta-tag alimentează toate punctele de contact de pe pagină: linkurile `mailto:`, nota de confidențialitate și endpointul FormSubmit. Schimbi adresa într-un singur loc.

Formularul validează câmpurile în browser și trimite cererea direct din pagină, prin [FormSubmit](https://formsubmit.co), către adresa de mai sus. Vizitatorul nu mai are nevoie de o aplicație de e-mail: datele pleacă prin `POST` către `https://formsubmit.co/ajax/<adresa-din-meta>`, ca JSON. Site-ul rămâne static, fără build și fără chei secrete în HTML.

### Cum se activează FormSubmit

1. Prima trimitere către o adresă nouă nu ajunge ca cerere obișnuită: FormSubmit trimite **un e-mail de confirmare** la adresa respectivă, cu un link de activare. Deschide linkul, apoi retrimite o cerere de test.
2. Nu uita să verifici și folderul Spam; dacă nu confirmi, cererile viitoare nu sunt livrate.
3. Opțional, după activare FormSubmit îți oferă un **alias aleatoriu** (ex. `8f3c1d9a2b`). Îl poți pune în meta-tagul `order-email` în locul adresei, ca adresa reală să nu mai apară în pagină.
4. FormSubmit păstrează cererile până la 30 de zile într-o arhivă de siguranță (accesibilă și prin API-ul lor, cu limită de accesări pe zi), apoi le șterge. Acest lucru este menționat și în nota de confidențialitate.
5. Câmpul `_honey` din formular este capcana anti-spam recomandată de FormSubmit: dacă un bot îl completează, cererea este ignorată discret. Câmpul `email` devine Reply-To, deci poți răspunde direct clientului.

### Variantele de rezervă

Dacă trimiterea directă nu reușește (lipsă internet, blocare de către browser, răspuns de eroare, adresă neactivată sau neconfigurată), formularul păstrează toate variantele de rezervă: link `mailto:` (când mesajul încape într-un link), descărcare `.eml` și copierea detaliilor. Mesajul de pe ecran spune explicit că cererea nu a plecat. Dacă adresa din meta-tag nu este validă, se sare direct la variantele de rezervă, fără să se încerce trimiterea.

## Încărcarea pieselor demonstrative

Nu există un formular de upload public pentru vizitatori. Adaugă fișierele audio în repository, în `assets/audio/`, cu numele de mai jos:

- `locul-meu-e-langa-tine.mp3` — cardul Romantic pop
- `mama-primul-meu-acasa.mp3` — cardul Baladă emoționantă
- `legenda-din-gasca.mp3` — cardul Pop vesel

Playerul folosește automat fișierul MP3 dacă există; dacă lipsește, redă fragmentul sintetic de demonstrație. Pentru alte nume sau căi, schimbă proprietatea `audioFile` a piesei corespunzătoare din obiectul `tracks` din `index.html`. MP3 este formatul recomandat; păstrează fișierele comprimate și adaugă numai materiale pe care ai dreptul să le publici. Fișierele puse în repository vor fi publice împreună cu site-ul.

## Înainte de publicarea comercială

- Confirmă că inboxul din `order-email` există și este monitorizat, apoi **activează adresa în FormSubmit** (vezi mai sus) și trimite o cerere de test de pe pagina publicată.
- Verifică dacă pagina este servită prin HTTPS și de pe domeniul real: FormSubmit respinge trimiterile venite din fișiere deschise direct de pe disc (`file://`) sau fără un site valid.
- Completează identitatea legală a operatorului și verifică politicile afișate, condițiile comerciale, livrarea, anularea și drepturile asupra materialelor.
- Verifică prețurile și conținutul pachetelor.
- Publică pagina prin HTTPS.
