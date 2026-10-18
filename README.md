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

Adresa din meta-tag alimentează toate punctele de contact de pe pagină: linkurile `mailto:`, nota de confidențialitate, blocul de trimitere manuală și atributul `action` al formularului (folosit fără JavaScript). Cu JavaScript activ, scriptul sincronizează și `action`-ul cu meta-tagul. Site-ul rămâne static, fără build, fără servicii externe și fără chei secrete în HTML.

Formularul validează câmpurile în browser și trimite cererea **prin aplicația de e-mail a vizitatorului** (`mailto:`), către adresa de mai sus: la apăsarea butonului „Trimite cererea”, scriptul compune un link `mailto:` cu subiectul `Cerere melodie personalizată — <persoana>` și un corp formatat, apoi îl deschide în gestul utilizatorului. Imediat sub formular apar și variantele **Gmail** și **Outlook**, care deschid compunerea direct în browser, cu aceleași date completate, fără nicio aplicație configurată pe dispozitiv. Nu există servicii intermediare (fără FormSubmit, fără reCAPTCHA): mesajul pleacă direct din contul vizitatorului, iar confirmarea o dăm noi personal, la răspuns.

### Cum decurge o trimitere

1. Vizitatorul completează formularul și apasă „Trimite cererea”. Scriptul validează câmpurile (cu mesaje în română și focus pe primul câmp greșit) și compune cererea: subiect cu persoana destinatar, corp cu nume, e-mail, ocazie, pachet (valoarea include prețul), persoană, stil, povestea, ce trebuie evitat și acordul pentru portofoliu.
2. Linkul `mailto:` se deschide sincron, în gestul utilizatorului, cu cererea completată către `order-email`. Pagina afișează „Cererea este gata de trimis” și îl îndrumă pe vizitator să verifice mesajul și să apese Trimite. Pentru că browserul nu poate confirma dacă aplicația de e-mail s-a deschis, mesajul nu pretinde că s-a întâmplat: imediat după fiecare apăsare, blocul „Nu s-a deschis e-mailul?” se deschide automat, cu toate variantele active.
3. Dacă aplicația de e-mail nu se deschide (nu există niciuna configurată), vizitatorul apasă „Deschide în Gmail” sau „Deschide în Outlook”: compunerea se deschide într-o filă nouă, direct în browser, cu destinatarul, subiectul și tot corpul completate, și merge fără nimic configurat pe dispozitiv.
4. Vizitatorul trimite mesajul din aplicație sau din webmail; o copie rămâne la el (mesaje trimise sau ciornă). Noi răspundem personal pe adresa din formular, cu confirmarea pachetului, a prețului și a termenului.

Dacă mesajul este atât de lung încât linkul `mailto:` depășește pragul sigur (`MAILTO_LIMIT`, 1800 de caractere — unele sisteme trunchează sau nu deschid linkuri lungi), scriptul îl deschide oricum, dar afișează un avertisment și deschide automat blocul cu variantele de rezervă. Linkurile Gmail/Outlook au și ele o limită practică (`WEBMAIL_LIMIT`, 8000 de caractere); peste ea, butoanele webmail rămân dezactivate și pagina îndrumă spre fișierul `.eml` sau copierea detaliilor, care acceptă povești de orice lungime.

Fără JavaScript, formularul folosește atributul `action` (`mailto:...`, `method="post"`, `enctype="text/plain"`): se deschide tot aplicația de e-mail, iar câmpurile ajung ca text simplu (`nume=...`, `email=...`) în corpul mesajului. Subiectul nu poate fi presetat pe acest traseu; câmpurile ascunse nu mai sunt necesare.

### Variantele de rezervă

Blocul „Nu s-a deschis e-mailul? Alege cum trimiți” de sub formular păstrează toate variantele: link `mailto:` (doar când mesajul încape într-un link), compunere în **Gmail**, compunere în **Outlook**, descărcare `.eml` și copierea detaliilor (cu casetă de copiere manuală când clipboard-ul nu este permis). Butoanele sunt dezactivate până când formularul este completat corect, se activează la fiecare trimitere, iar blocul se deschide automat după apăsarea butonului principal. O nouă editare resetează starea. Dacă adresa din meta-tag lipsește, pagina sare direct la variantele de rezervă, fără să încerce deschiderea aplicației de e-mail.

Linkurile Gmail/Outlook sunt construite cu `encodeURIComponent` (spațiile devin `%20`, nu `+`) și se deschid cu `target="_blank"` și `rel="noopener noreferrer"`; nu necesită cont conectat în pagină, ci doar autentificarea obișnuită în serviciul respectiv, în browser.

### Teste înainte de lansare

1. Trimite o cerere de test: confirmă că se deschide aplicația de e-mail cu mesajul completat către `povestepenote.comenzi@gmail.com`, cu subiectul `Cerere melodie personalizată — <persoana>` și cu toate detaliile în corp.
2. În aceeași trimitere, confirmă că blocul de sub formular s-a deschis automat și că butoanele Gmail, Outlook, `.eml` și copiere sunt active. Deschide Gmail și Outlook într-o filă nouă: destinatarul, subiectul și corpul trebuie să fie completate, cu diacriticele intacte.
3. Trimite mesajul din aplicație sau din webmail și confirmă că ajunge în inboxul din `order-email` (verifică și folderul Spam la prima trimitere). Răspunde clientului de test ca să confirmi fluxul complet.
4. Dezactivează temporar aplicația de e-mail implicită (sau testează pe un dispozitiv fără una): butonul principal nu trebuie să strice pagina, iar Gmail/Outlook trebuie să deschidă compunerea completă în browser; verifică și `.eml` și copierea.
5. Completează o poveste lungă (spre 4000 de caractere): pagina trebuie să arate avertismentul despre linkul lung și să deschidă blocul de rezervă. Dacă linkurile webmail depășesc `WEBMAIL_LIMIT`, butoanele Gmail/Outlook rămân dezactivate și mesajul îndrumă spre `.eml` sau copiere.
6. Trimite formularul gol: nimic nu pleacă, apar mesajele de validare, iar focusul ajunge pe primul câmp greșit.

Pentru verificări automate există o suită jsdom (rulată în afara repo-ului, ex. `/tmp/jstest`, cu `npm i jsdom`) care simulează trimiterea formularului: validare, deschiderea linkului `mailto:` cu subiectul și corpul corecte, linkurile Gmail/Outlook cu parametrii corecți, blocul de rezervă deschis după fiecare trimitere, mesajele lungi, meta-tagul gol și resetarea la editare.

## Încărcarea pieselor demonstrative

Nu există un formular de upload public pentru vizitatori. Adaugă fișierele audio în repository, în `assets/audio/`, cu numele de mai jos:

- `locul-meu-e-langa-tine.mp3` — cardul Romantic pop
- `mama-primul-meu-acasa.mp3` — cardul Baladă emoționantă
- `legenda-din-gasca.mp3` — cardul Pop vesel

Playerul folosește automat fișierul MP3 dacă există; dacă lipsește, redă fragmentul sintetic de demonstrație. Pentru alte nume sau căi, schimbă proprietatea `audioFile` a piesei corespunzătoare din obiectul `tracks` din `index.html`. MP3 este formatul recomandat; păstrează fișierele comprimate și adaugă numai materiale pe care ai dreptul să le publici. Fișierele puse în repository vor fi publice împreună cu site-ul.

## Înainte de publicarea comercială

- Confirmă că inboxul din `order-email` există și este monitorizat, apoi parcurge pașii de test de pe pagina publicată.
- Trimite o cerere de test de pe un telefon și de pe un calculator, ca să vezi cum se comportă aplicația de e-mail implicită pe fiecare dispozitiv; repetă testul cu Gmail și Outlook, ca alternative care nu depind de nicio aplicație configurată.
- Verifică textele despre date din nota de confidențialitate: acum cererea pleacă din contul vizitatorului (aplicație de e-mail sau webmail), fără servicii intermediare și fără confirmări automate.
- Completează identitatea legală a operatorului și verifică politicile afișate, condițiile comerciale, livrarea, anularea și drepturile asupra materialelor.
- Verifică prețurile și conținutul pachetelor.
- Publică pagina prin HTTPS.
