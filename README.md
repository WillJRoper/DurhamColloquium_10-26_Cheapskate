# Doing Astrophysics As A Cheapskate

Durham colloquium, 26 October 2026 (45 min). Slidev deck.

Live: <https://willjroper.github.io/DurhamColloquium_10-26_Cheapskate/>

Pushing to `main` rebuilds and redeploys the site (`.github/workflows/deploy.yml`).

```bash
npm install
npm run dev      # present at localhost:3030 (presenter view: /presenter)
npm run build    # static site in dist/
npm run export   # PDF
```

- `public/img`, `public/video`: assets mined from the old Keynote talks (and crops of their PDFs).
- `public/tessera`: figures from christopherlovell/tessera-talk-long.
- `components/SpeedChart.vue`: ported from christopherlovell/sbi_tutorial.
- The two live embeds (cosmo-carta, synthesizer-project.github.io) show a screenshot when offline.
