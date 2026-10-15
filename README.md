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

Formularul validează câmpurile în browser și trimite cererea **prin aplicația de e-mail a vizitatorului** (`mailto:`), către adresa de mai sus: la apăsarea butonului „Trimite cererea”, scriptul compune un link `mailto:` cu subiectul `Cerere melodie personalizată — <persoana>` și un corp formatat, apoi îl deschide în gestul utilizatorului. Nu există servicii intermediare (fără FormSubmit, fără reCAPTCHA): mesajul pleacă direct din aplicația de e-mail a vizitatorului, iar confirmarea o dăm noi personal, la răspuns.

### Cum decurge o trimitere

1. Vizitatorul completează formularul și apasă „Trimite cererea”. Scriptul validează câmpurile (cu mesaje în română și focus pe primul câmp greșit) și compune cererea: subiect cu persoana destinatar, corp cu nume, e-mail, ocazie, pachet (valoarea include prețul), persoană, stil, povestea, ce trebuie evitat și acordul pentru portofoliu.
2. Linkul `mailto:` se deschide sincron, în gestul utilizatorului, cu cererea completată către `order-email`. Pagina afișează „Ți-am deschis aplicația de e-mail” și îl îndrumă pe vizitator să verifice mesajul și să apese Trimite din aplicație.
3. Vizitatorul trimite mesajul din aplicația lui de e-mail; o copie rămâne la el (mesaje trimise sau ciornă). Noi răspundem personal pe adresa din formular, cu confirmarea pachetului, a prețului și a termenului.
4. Dacă aplicația de e-mail nu se deschide (nu există niciuna configurată), vizitatorul are sub formular variantele de rezervă.

Dacă mesajul este atât de lung încât linkul `mailto:` depășește pragul sigur (`MAILTO_LIMIT`, 1800 de caractere — unele sisteme trunchează sau nu deschid linkuri lungi), scriptul îl deschide oricum, dar afișează un avertisment și deschide automat blocul cu variantele de rezervă.

Fără JavaScript, formularul folosește atributul `action` (`mailto:...`, `method="post"`, `enctype="text/plain"`): se deschide tot aplicația de e-mail, iar câmpurile ajung ca text simplu (`nume=...`, `email=...`) în corpul mesajului. Subiectul nu poate fi presetat pe acest traseu; câmpurile ascunse nu mai sunt necesare.

### Variantele de rezervă

Blocul „Nu s-a deschis e-mailul? Trimite cererea manual” de sub formular păstrează toate variantele de rezervă: link `mailto:` (doar când mesajul încape într-un link), descărcare `.eml` și copierea detaliilor (cu casetă de copiere manuală când clipboard-ul nu este permis). Butoanele sunt dezactivate până când formularul este completat corect, se activează la fiecare trimitere, iar o nouă editare resetează starea. Dacă adresa din meta-tag lipsește, pagina sare direct la variantele de rezervă, fără să încerce deschiderea aplicației de e-mail.

### Teste înainte de lansare

1. Trimite o cerere de test: confirmă că se deschide aplicația de e-mail cu mesajul completat către `povestepenote.comenzi@gmail.com`, cu subiectul `Cerere melodie personalizată — <persoana>` și cu toate detaliile în corp.
2. Trimite mesajul din aplicație și confirmă că ajunge în inboxul din `order-email` (verifică și folderul Spam la prima trimitere). Răspunde clientului de test ca să confirmi fluxul complet.
3. Dezactivează temporar aplicația de e-mail implicită (sau testează pe un dispozitiv fără una): butonul trebuie să nu strice pagina, iar variantele de rezervă să funcționeze (`.eml`, copiere).
4. Completează o poveste lungă (spre 4000 de caractere): pagina trebuie să arate avertismentul despre linkul lung și să deschidă blocul de rezervă.
5. Trimite formularul gol: nimic nu pleacă, apar mesajele de validare, iar focusul ajunge pe primul câmp greșit.

Pentru verificări automate există o suită jsdom (rulată în afara repo-ului, ex. `/tmp/jstest`, cu `npm i jsdom`) care simulează trimiterea formularului: validare, deschiderea linkului `mailto:` cu subiectul și corpul corecte, starea de avertisment pentru mesaje lungi, variantele de rezervă, meta-tagul gol și editarea după trimitere.

## Încărcarea pieselor demonstrative

Nu există un formular de upload public pentru vizitatori. Adaugă fișierele audio în repository, în `assets/audio/`, cu numele de mai jos:

- `locul-meu-e-langa-tine.mp3` — cardul Romantic pop
- `mama-primul-meu-acasa.mp3` — cardul Baladă emoționantă
- `legenda-din-gasca.mp3` — cardul Pop vesel

Playerul folosește automat fișierul MP3 dacă există; dacă lipsește, redă fragmentul sintetic de demonstrație. Pentru alte nume sau căi, schimbă proprietatea `audioFile` a piesei corespunzătoare din obiectul `tracks` din `index.html`. MP3 este formatul recomandat; păstrează fișierele comprimate și adaugă numai materiale pe care ai dreptul să le publici. Fișierele puse în repository vor fi publice împreună cu site-ul.

## Înainte de publicarea comercială

- Confirmă că inboxul din `order-email` există și este monitorizat, apoi parcurge pașii de test de pe pagina publicată.
- Trimite o cerere de test de pe un telefon și de pe un calculator, ca să vezi cum se comportă aplicația de e-mail implicită pe fiecare dispozitiv.
- Verifică textele despre date din nota de confidențialitate: acum cererea pleacă din aplicația de e-mail a vizitatorului, fără servicii intermediare și fără confirmări automate.
- Completează identitatea legală a operatorului și verifică politicile afișate, condițiile comerciale, livrarea, anularea și drepturile asupra materialelor.
- Verifică prețurile și conținutul pachetelor.
- Publică pagina prin HTTPS.
