# Kammerkoret Richters Skala — Hjemmeside

## Hosting på GitHub Pages

1. Opret et nyt repository på GitHub
2. Upload alle filer i denne mappe (bevar struktur)
3. Settings → Pages → Branch: main → Save
4. Siden er live på https://<brugernavn>.github.io/<repo-navn>/

## Eget domæne (richtersskala.dk hos one.com)

Filen `CNAME` i roden fortæller GitHub Pages, hvilket domæne siden serveres
på (www.richtersskala.dk — GitHub omdirigerer selv richtersskala.dk dertil).
Derudover skal DNS hos one.com pege på GitHub:

1. Log ind på one.com → Domæner → richtersskala.dk → **DNS-indstillinger**
2. Fjern eksisterende A-records for `@` (roddomænet), og opret disse fire:
   - `@` A `185.199.108.153`
   - `@` A `185.199.109.153`
   - `@` A `185.199.110.153`
   - `@` A `185.199.111.153`
3. Ret/opret `www` som CNAME der peger på `jensfugl.github.io`
   (GitHub omdirigerer selv www → richtersskala.dk)
4. På GitHub: Settings → Pages → tjek at "Custom domain" viser
   richtersskala.dk, og slå **Enforce HTTPS** til, når DNS-tjekket er grønt
   (DNS-ændringer kan tage op til et par timer)

## Struktur

- index.html — hjemmesiden (single-file React app). Markup skrives med
  [htm](https://github.com/developit/htm), der ligner JSX men kører direkte i
  browseren uden kompilering: brug `${...}` i stedet for `{...}`, og
  `<${Komponent}>…<//>` for egne komponenter
- concerts.json — koncertdata synkroniseret fra Google Sheets
- recordings.json, videos.json — afspilningsdata hentet ved load
- assets/ — billeder og logo. Hvert foto findes i to størrelser: `navn.jpg`
  (maks. 2400 px bred) og `navn-1200.jpg` (1200 px bred, til mobil og
  galleri-miniaturer). Nye fotos skal også have begge udgaver
- robots.txt, sitemap.xml — til søgemaskiner

## SEO

Titel, beskrivelse, delings-billede (Open Graph) og struktureret data om koret
ligger i `<head>` i index.html. Struktureret data for koncerterne (MusicEvent)
genereres automatisk ud fra concerts.json, så de kan vises i Googles
koncert-/begivenhedsresultater.
