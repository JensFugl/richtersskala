# Kammerkoret Richters Skala — Hjemmeside

## Hosting på GitHub Pages

1. Opret et nyt repository på GitHub
2. Upload alle filer i denne mappe (bevar struktur)
3. Settings → Pages → Branch: main → Save
4. Siden er live på https://<brugernavn>.github.io/<repo-navn>/

## Eget domæne (richtersskala.dk hos one.com)

Filen `CNAME` i roden fortæller GitHub Pages, at siden skal serveres på
richtersskala.dk. Derudover skal DNS hos one.com pege på GitHub:

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

- index.html — hjemmesiden (single-file React app)
- concerts.json — koncertdata synkroniseret fra Google Sheets
- recordings.json, videos.json — afspilningsdata hentet ved load
- assets/ — billeder og logo
