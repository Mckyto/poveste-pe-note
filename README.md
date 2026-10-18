# Poveste pe Note

Pagină statică HTML, fără build sau dependențe. Pentru previzualizare locală:

```bash
python3 -m http.server 8000
```

Apoi deschide `http://localhost:8000`.

## Pachete și prețuri promoționale

Prețurile afișate în pagina publică sunt: Mini — **49 lei** (standard 79 lei), Poveste — **89 lei** (standard 149 lei) și Moment — **149 lei** (standard 249 lei). Valorile trebuie să rămână sincronizate între cardurile de preț, lista din formular și mesajul de comandă. Butonul fiecărui pachet selectează opțiunea cu prețul promoțional.

Pagina colectează cereri prin e-mail, nu plăți. Înainte de orice plată sau începerea lucrului, confirmăm în scris pachetul, suma finală, modalitatea de plată și termenul de livrare. Oferta nu afișează un termen-limită; nu adăuga un cronometru sau o dată de expirare fără confirmarea perioadei reale.

## Formularul de comandă

Adresa de contact se configurează în meta-tagul `order-email` din `index.html`:

```html
<meta name="order-email" content="povestepenote.comenzi@gmail.com" />
```

Adresa din meta-tag alimentează toate punctele de contact de pe pagină: nota de confidențialitate, blocul de trimitere manuală și atributul `action` al formularului (folosit fără JavaScript). Cu JavaScript activ, scriptul sincronizează și `action`-ul cu meta-tagul. Site-ul rămâne static, fără build, fără servicii externe și fără chei secrete în HTML.

Formularul validează câmpurile în browser și trimite cererea **direct prin Gmail**, către adresa de mai sus: la apăsarea butonului „Trimite cererea”, scriptul compune un link Gmail cu subiectul `Cerere melodie personalizată — <persoana>` și un corp formatat, apoi îl deschide într-o filă nouă, în browser, cu toate datele completate, fără nicio aplicație configurată pe dispozitiv. Nu există servicii intermediare (fără FormSubmit, fără reCAPTCHA): mesajul pleacă direct din contul Gmail al vizitatorului, iar confirmarea o dăm noi personal, la răspuns.

### Cum decurge o trimitere

1. Vizitatorul completează formularul și apasă „Trimite cererea”. Scriptul validează câmpurile (cu mesaje în română și focus pe primul câmp greșit) și compune cererea: subiect cu persoana destinatar, corp cu nume, e-mail, ocazie, pachet (valoarea include prețul), persoană, stil, povestea, ce trebuie evitat și acordul pentru portofoliu.
2. Linkul Gmail se deschide sincron, în gestul utilizatorului, cu cererea completată către `order-email`, într-o filă nouă. Pagina afișează „Cererea este gata de trimis” și îl îndrumă pe vizitator să verifice mesajul și să apese Trimite în Gmail. Imediat după fiecare apăsare, blocul „Nu s-a deschis Gmail?” se deschide automat, cu variantele de rezervă active.
3. Vizitatorul verifică mesajul în Gmail și apasă Trimite; o copie rămâne la el (mesaje trimise sau ciornă). Noi răspundem personal pe adresa din formular, cu confirmarea pachetului, a prețului și a termenului.

Linkul Gmail are o limită practică (`WEBMAIL_LIMIT`, 8000 de caractere); peste ea, butonul Gmail rămâne dezactivat și pagina îndrumă spre fișierul `.eml` sau copierea detaliilor, care acceptă povești de orice lungime.

Fără JavaScript, formularul folosește atributul `action` (`mailto:...`, `method="post"`, `enctype="text/plain"`): se deschide aplicația de e-mail ca rezervă, iar câmpurile ajung ca text simplu (`nume=...`, `email=...`) în corpul mesajului. Subiectul nu poate fi presetat pe acest traseu.

### Variantele de rezervă

Blocul „Nu s-a deschis Gmail? Folosește o variantă de rezervă” de sub formular păstrează toate variantele disponibile: compunere în **Gmail** (doar când mesajul încape într-un link), descărcare `.eml` și copierea detaliilor (cu casetă de copiere manuală când clipboard-ul nu este permis). Butoanele sunt dezactivate până când formularul este completat corect, se activează la fiecare trimitere, iar blocul se deschide automat după apăsarea butonului principal. O nouă editare resetează starea. Dacă adresa din meta-tag lipsește, pagina afișează un mesaj de avertizare și oferă direct variantele de rezervă.

Linkul Gmail este construit cu `encodeURIComponent` (spațiile devin `%20`) și se deschide cu `target="_blank"` și `rel="noopener noreferrer"`; nu necesită cont conectat în pagină, ci doar autentificarea obișnuită în Gmail, în browser.

### Teste înainte de lansare

1. Trimite o cerere de test: confirmă că se deschide Gmail într-o filă nouă, cu mesajul completat către `povestepenote.comenzi@gmail.com`, cu subiectul `Cerere melodie personalizată — <persoana>` și cu toate detaliile în corp.
2. În aceeași trimitere, confirmă că blocul de sub formular s-a deschis automat și că butoanele Gmail, `.eml` și copiere sunt active. Deschide Gmail: destinatarul, subiectul și corpul trebuie să fie completate, cu diacriticele intacte.
3. Trimite mesajul din Gmail și confirmă că ajunge în inboxul din `order-email` (verifică și folderul Spam la prima trimitere). Răspunde clientului de test ca să confirmi fluxul complet.
4. Completează o poveste lungă (spre 4000 de caractere): dacă linkul Gmail depășește `WEBMAIL_LIMIT`, butonul Gmail rămâne dezactivat și mesajul îndrumă spre `.eml` sau copiere.
5. Trimite formularul gol: nimic nu pleacă, apar mesajele de validare, iar focusul ajunge pe primul câmp greșit.
6. Alege fiecare pachet din card și din lista formularului: Gmail/.eml trebuie să conțină prețul promoțional corect (49, 89 sau 149 lei), nu prețul standard.

Pentru verificări automate există o suită jsdom (rulată în afara repo-ului, ex. `/tmp/jstest`, cu `npm i jsdom`) care simulează trimiterea formularului: validare, deschiderea linkului Gmail cu parametrii corecți, blocul de rezervă deschis după fiecare trimitere, mesajele lungi, meta-tagul gol și resetarea la editare.

## Încărcarea pieselor demonstrative

Nu există un formular de upload public pentru vizitatori. Adaugă fișierele audio în repository, în `assets/audio/`, cu numele de mai jos:

- `locul-meu-e-langa-tine.mp3` — cardul Romantic pop
- `mama-primul-meu-acasa.mp3` — cardul Baladă emoționantă
- `legenda-din-gasca.mp3` — cardul Pop vesel

Playerul folosește automat fișierul MP3 dacă există; dacă lipsește, redă fragmentul sintetic de demonstrație. Pentru alte nume sau căi, schimbă proprietatea `audioFile` a piesei corespunzătoare din obiectul `tracks` din `index.html`. MP3 este formatul recomandat; păstrează fișierele comprimate și adaugă numai materiale pe care ai dreptul să le publici. Fișierele puse în repository vor fi publice împreună cu site-ul.

## Înainte de publicarea comercială

- Confirmă că inboxul din `order-email` există și este monitorizat, apoi parcurge pașii de test de pe pagina publicată.
- Trimite o cerere de test de pe un telefon și de pe un calculator, ca să vezi cum se deschide Gmail pe fiecare dispozitiv; verifică și `.eml` și copierea ca alternative.
- Verifică textele despre date din nota de confidențialitate: acum cererea pleacă din contul Gmail al vizitatorului, fără servicii intermediare și fără confirmări automate.
- Completează identitatea legală a operatorului și verifică politicile afișate, condițiile comerciale, livrarea, anularea și drepturile asupra materialelor.
- Confirmă perioada reală a promoției, prețurile standard de referință, dacă sumele includ taxele aplicabile și condițiile de plată/livrare; aceste informații nu pot fi presupuse de cod.
- Reverifică în carduri, formular și e-mail că prețurile promoționale și conținutul pachetelor sunt sincronizate.
- Publică pagina prin HTTPS.
