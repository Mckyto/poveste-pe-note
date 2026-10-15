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

Adresa din meta-tag alimentează toate punctele de contact de pe pagină: linkurile `mailto:`, nota de confidențialitate, blocul de trimitere manuală și endpointul FormSubmit. Pentru traseul fără JavaScript există și atributul `action` al formularului (`https://formsubmit.co/<adresa>`), care trebuie ținut în pas cu meta-tagul; cu JavaScript activ, scriptul îl sincronizează singur.

Formularul validează câmpurile în browser și trimite cererea prin [FormSubmit](https://formsubmit.co), către adresa de mai sus, pe **traseul clasic** (POST `multipart/form-data` către `https://formsubmit.co/<adresa>`), nu prin AJAX. Motivul: FormSubmit documentează că `_autoresponse` — e-mailul de confirmare trimis automat clientului — **nu funcționează la trimiterile AJAX și nici cu reCAPTCHA dezactivat**. Nu reveni la `fetch`/AJAX și nu adăuga `_captcha=false`, altfel clientul nu mai primește confirmarea. Site-ul rămâne static, fără build și fără chei secrete în HTML.

### Cum decurge o trimitere

1. Vizitatorul apasă „Trimite cererea”. Scriptul deschide o **fereastră separată** (pe telefon, un tab nou), setează `form.target` către ea din JavaScript (nu din HTML) și trimite formularul acolo; pagina rămâne deschisă și afișează „Se trimite cererea…”, cu un buton care readuce fereastra în față.
2. În fereastră, FormSubmit cere o scurtă verificare anti-robot (Google reCAPTCHA), apoi trimite cererea pe adresa ta și confirmarea pe adresa clientului.
3. FormSubmit redirecționează fereastra către `_next`: aceeași pagină, fără hash, cu parametrul `?cerere=ok` (calculat la trimitere; valoarea statică din HTML, pentru traseul fără JavaScript, este URL-ul publicat pe GitHub Pages). Pagina de întoarcere anunță pagina principală prin `postMessage({ type: 'poveste-pe-note:cerere-trimisa' })`, acceptat doar de pe același origin, așteaptă confirmarea de primire și se închide singură.
4. Pagina principală arată „Cererea a fost trimisă ✓”, cu mesajul că am trimis o confirmare pe adresa clientului (și că poate verifica folderul Spam). Dovada este fie mesajul de mai sus, fie URL-ul ferestrei care conține `cerere=ok` (citit doar pe același origin); o pagină externă încărcată în fereastră nu contează ca succes.
5. Dacă fereastra se închide fără dovadă sau trec 2 minute fără ea (limita e generoasă, pentru că reCAPTCHA poate cere rezolvarea unui test), pagina arată **„Verifică-ți e-mailul”** și deschide automat blocul „Nu s-a trimis? Trimite cererea manual”. Dacă dovada vine totuși mai târziu, starea trece la „trimisă ✓”.
6. Dacă browserul blochează fereastra, formularul pleacă ca pagină întreagă (`target` `_self`), exact ca fără JavaScript: vizitatorul trece prin verificare și revine pe `?cerere=ok`, unde pagina arată confirmarea (fără fereastră părinte, parametrul este eliminat din URL ca să nu reapară la reîncărcare).

Câmpurile trimise au nume lizibile în e-mail: `nume`, `email` (Reply-To și adresa pe care pleacă confirmarea), `ocazie`, `pachet` (valoarea include prețul), `pentru`, `stil`, `povestea`, `evita`, `drepturi`, `acord-confidentialitate`, `portofoliu` (checkbox-uri cu `value="Da"`). Câmpurile ascunse: `_subject` (actualizat la trimitere: `Cerere melodie personalizată — <persoana>`), `_template: table`, `_next`, `_autoresponse` (mesajul de confirmare pentru client, editabil direct în `index.html`) și `_honey` (capcana anti-spam, ascunsă vizual, trimisă goală).

### Cum se activează FormSubmit

1. Prima trimitere către o adresă nouă nu ajunge ca cerere obișnuită: FormSubmit trimite **un e-mail de activare** la adresa respectivă, cu un link de confirmare. Deschide linkul (verifică și folderul Spam), apoi retrimite o cerere de test. Până la activare, cererile nu sunt livrate, iar clientul nu primește confirmarea.
2. Opțional, după activare FormSubmit îți oferă un **alias aleatoriu** (ex. `8f3c1d9a2b`). Pune-l în meta-tagul `formsubmit-address` (lăsat gol implicit) și în atributul `action` al formularului; `order-email` rămâne adresa reală pentru `mailto:`, `.eml` și nota de confidențialitate.
3. FormSubmit păstrează cererile până la 30 de zile într-o arhivă de siguranță (accesibilă și prin API-ul lor, cu limită de accesări pe zi), apoi le șterge. Acest lucru este menționat și în nota de confidențialitate, împreună cu verificarea reCAPTCHA și confirmarea automată trimisă clientului.
4. Câmpul `_honey` este capcana anti-spam recomandată de FormSubmit: dacă un bot îl completează, cererea este ignorată discret. Câmpul `email` devine Reply-To, deci poți răspunde direct clientului.

### Variantele de rezervă

Blocul „Nu s-a trimis? Trimite cererea manual” de sub formular păstrează toate variantele de rezervă: link `mailto:` (doar când mesajul încape într-un link), descărcare `.eml` și copierea detaliilor (cu casetă de copiere manuală când clipboard-ul nu este permis). Butoanele sunt dezactivate până când formularul este completat corect, se activează la fiecare trimitere, iar o nouă editare resetează starea. Dacă adresa din meta-tag lipsește sau nu este validă, se sare direct la variantele de rezervă, fără să se încerce trimiterea. În aceste cazuri mesajul pleacă din aplicația clientului, iar confirmarea automată nu se mai trimite.

### Teste înainte de lansare

Pe pagina publicată (HTTPS, nu `file://`):

1. Trimite o cerere de test cu o adresă de client pe care o poți citi. Confirmă că fereastra de verificare apare, că după reCAPTCHA se închide singură și că pagina arată „Cererea a fost trimisă ✓”.
2. Verifică inboxul tău (subiect `Cerere melodie personalizată — <persoana>`, tabel cu câmpurile de mai sus, Reply-To către client) și inboxul clientului de test (confirmarea cu mesajul din `_autoresponse` și copia cererii; verifică și Spam).
3. Închide fereastra de verificare înainte de a termina: pagina trebuie să arate „Verifică-ți e-mailul” și să deschidă blocul manual.
4. Blochează ferestrele pop-up în browser și retrimite: pagina trebuie să treacă prin FormSubmit ca pagină întreagă și să revină cu confirmarea.
5. Trimite formularul gol: nimic nu pleacă, apar mesajele de validare, iar focusul ajunge pe primul câmp greșit.

Pentru verificări automate există o suită jsdom (rulată în afara repo-ului, ex. `/tmp/jstest`, cu `npm i jsdom`) care simulează `form.submit()`, fereastra de verificare și timerele scurtate: trimitere confirmată prin `postMessage`, prin URL-ul ferestrei, expirare, fereastră închisă, pagină externă (fără succes prematur), fereastră blocată, validare, meta-tag gol, pagina de întoarcere și traseul fără JavaScript.

## Încărcarea pieselor demonstrative

Nu există un formular de upload public pentru vizitatori. Adaugă fișierele audio în repository, în `assets/audio/`, cu numele de mai jos:

- `locul-meu-e-langa-tine.mp3` — cardul Romantic pop
- `mama-primul-meu-acasa.mp3` — cardul Baladă emoționantă
- `legenda-din-gasca.mp3` — cardul Pop vesel

Playerul folosește automat fișierul MP3 dacă există; dacă lipsește, redă fragmentul sintetic de demonstrație. Pentru alte nume sau căi, schimbă proprietatea `audioFile` a piesei corespunzătoare din obiectul `tracks` din `index.html`. MP3 este formatul recomandat; păstrează fișierele comprimate și adaugă numai materiale pe care ai dreptul să le publici. Fișierele puse în repository vor fi publice împreună cu site-ul.

## Înainte de publicarea comercială

- Confirmă că inboxul din `order-email` există și este monitorizat, apoi **activează adresa în FormSubmit** (vezi mai sus) și parcurge pașii de test de pe pagina publicată.
- Dacă publici pe alt domeniu decât GitHub Pages, actualizează valoarea statică a câmpului `_next` din `index.html` (folosită doar fără JavaScript; cu JavaScript se calculează din URL-ul curent).
- Verifică dacă pagina este servită prin HTTPS și de pe domeniul real: FormSubmit respinge trimiterile venite din fișiere deschise direct de pe disc (`file://`) sau fără un site valid.
- Recitește mesajul din `_autoresponse` (confirmarea primită de client) și textele despre reCAPTCHA din nota de confidențialitate.
- Completează identitatea legală a operatorului și verifică politicile afișate, condițiile comerciale, livrarea, anularea și drepturile asupra materialelor.
- Verifică prețurile și conținutul pachetelor.
- Publică pagina prin HTTPS.
