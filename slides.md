---
theme: default
title: Doing Astrophysics As A Cheapskate
info: Durham colloquium, 26 October 2026. Zoom simulations and Synthesizer.
author: Will Roper
colorSchema: dark
aspectRatio: 16/9
fonts:
  sans: JetBrains Mono
  mono: JetBrains Mono
  provider: none
transition: fade
mdc: true
routerMode: hash
layout: center
class: text-center
---

<video src="/video/title_bg.mp4" poster="/img/title_bg.png" autoplay loop muted playsinline class="title-bg"></video>

<div class="title-fg">

<div class="muted text-sm mb-6">will@durham:~$ ./colloquium --budget=0 --move-to-monday=1</div>

<h1 class="blink !text-5xl !mb-4">Doing Astrophysics<br>As A Cheapskate</h1>

<div class="text-lg mt-8">Will Roper</div>

<div class="muted text-sm mt-1">Durham Astronomy Colloquium · 26 October 2026</div>

</div>

<img src="/img/oxford_logo.png" class="absolute left-6 bottom-6 h-16" alt="University of Oxford" />
<img src="/img/oxrse_logo.png" class="absolute right-6 bottom-6 h-16" alt="OxRSE" />

<!--
Title. Cheapskate framing: compute is the currency, and I'm going to show you how to spend less of it.
-->

---

# Who Am I?

<div class="body"><div class="grid grid-cols-[1fr_auto] gap-10 items-center">
<div>

- **Research Software Engineer**, OxRSE, Oxford
- I develop and run (and break) simulations
- FLARES: high-z galaxy evolution
- SWIFT zooms, Synthesizer, too many CLI tools

</div>
<img src="/img/whoami_chibi.jpg" class="h-88 rounded-lg" alt="Chibi Will: laptop, galaxies, supercomputer, guitar, chef hat and a coin purse" />
</div></div>

<!--
Quick intro. I sit on both sides, astrophysics and research software, which is why this talk is about how we spend compute.
-->

---

# This Talk In A Nutshell

<div class="term mt-6 text-lg leading-loose">
<div class="term-bar"><span /><span /><span /></div>

<div>$ cat talk.txt</div>
<div v-click><span class="accent">[1]</span> studying the Universe with simulations</div>
<div v-click><span class="accent">[2]</span> what a Universe costs</div>
<div v-click><span class="accent">[3]</span> cheapskate trick #1: <strong>zoom simulations</strong></div>
<div v-click><span class="accent">[4]</span> cheapskate trick #2: <strong>Synthesizer</strong></div>

</div>

<div v-click class="mt-8 text-center muted">Being a cheapskate isn't doing less science. It's doing more with what you've got.</div>

---
clicks: 3
---

# Astronomy In A Nutshell…

<div class="mt-10">
<AstroFlowchart :step="Math.min($clicks, 2)" :highlight="$clicks >= 3 ? 'sims' : ''" />
</div>

<div v-click="3" class="text-center mt-4">Part one: the <span class="theory">Physics → Fields</span> step. Simulations.</div>

<div class="credit">Credit: Stephen Wilkins, Chris Lovell</div>

<!--
Click 1: theory direction, physics out to observations. Click 2: the inverse direction, what observers do. Click 3: highlight the simulation step.
-->

---
clicks: 3
---

# Building A Universe In A Box

<SimMachine :step="$clicks" class="mt-6" />

<!--
Click 1: initial conditions go in (these happen to be zoom ICs: high-res region in the middle, foreshadowing).
Click 2: the physics: gravity and hydrodynamics plus sub-grid models, solved by a code (SWIFT) on a machine (COSMA, a few floors from here).
Click 3: out comes a simulated universe (EAGLE).
-->

---

# You Can't Have It All

<div class="body text-xl"><div class="mx-auto w-fit">

- **Resolution**: the physics inside galaxies
- **Volume**: the rare objects and the statistics

<div class="term mt-12 text-lg w-fit">cost ∝ N<sub>particles</sub> × N<sub>steps</sub><br><span class="warn">both grow with resolution <em>and</em> volume</span></div>

</div></div>

---

# The Price Of Admission

<table class="bill mt-2">
<thead><tr><th>simulation</th><th>box</th><th>particles</th><th class="r">cost</th></tr></thead>
<tbody>
<tr><td>EAGLE Ref-L100N1504</td><td>100 Mpc</td><td>2 × 1504³</td><td class="r">4.5 M</td></tr>
<tr><td>TNG100-1</td><td>111 Mpc</td><td>2 × 1820³</td><td class="r">18 M</td></tr>
<tr><td>FLAMINGO L2p8_m9</td><td>2.8 Gpc</td><td>2 × 5040³ + 2800³ ν</td><td class="r">31 M</td></tr>
<tr><td>TNG300-1</td><td>303 Mpc</td><td>2 × 2500³</td><td class="r">35 M</td></tr>
<tr><td>COLIBRE L200m6</td><td>200 Mpc</td><td>5 × 3008³</td><td class="r">72 M</td></tr>
<tr><td>TNG50-1</td><td>52 Mpc</td><td>2 × 2160³</td><td class="r">~130 M</td></tr>
<tr><td>MillenniumTNG</td><td>740 Mpc</td><td>2 × 4320³</td><td class="r">170 M</td></tr>
<tr class="node"><td>ASTRID</td><td>250 Mpc/h</td><td>2 × 5500³</td><td class="r">3 M node-h</td></tr>
<tr class="node"><td>Frontier-E (CRK-HACC)</td><td>4.7 Gpc</td><td>~4 × 10¹²</td><td class="r">1.7 M node-h</td></tr>
</tbody>
</table>

<div class="muted text-xs mt-2">costs as reported in each paper · core-hours unless stated · hydro runs · comoving boxes</div>

<div class="credit"><a href="https://arxiv.org/abs/1407.7040" target="_blank">Schaye+15</a>, <a href="https://arxiv.org/abs/1707.03406" target="_blank">Pillepich+18</a>, <a href="https://arxiv.org/abs/1902.05553" target="_blank">Pillepich+19</a>, <a href="https://arxiv.org/abs/2306.04024" target="_blank">Schaye+23</a>, <a href="https://arxiv.org/abs/2508.21126" target="_blank">Schaye+25</a>, <a href="https://arxiv.org/abs/2210.10060" target="_blank">Pakmor+23</a>, <a href="https://arxiv.org/abs/2111.01160" target="_blank">Bird+22</a>, <a href="https://arxiv.org/abs/2510.03557" target="_blank">Frontiere+25</a></div>

<style>
.bill { width: 100%; border-collapse: collapse; font-size: 0.9rem; }
.bill th { text-align: left; color: var(--muted); font-weight: 400; border-bottom: 1px solid var(--line); padding: 4px 8px; }
.bill td { padding: 5px 8px; border-bottom: 1px solid var(--grid); }
.bill .r { text-align: right; }
.bill td.r { color: var(--warn); font-weight: 700; }
.bill tr.node td.r { color: var(--theory); }
</style>

<!--
Costs as published: EAGLE ~4.5M CPU hours (Schaye+15 §2.2); TNG Table 1 of Pillepich+18/19; FLAMINGO footnote 14 of Schaye+23 (includes lightcones); COLIBRE footnote 22 of Schaye+25; MTNG Pakmor+23 §2 (57 days on 122,880 cores); ASTRID Bird+22 (Frontera node-hours); Frontier-E Frontiere+25 (GPU node-hours, 9000 nodes, 196 h).
-->

---
layout: full
---

# How Much Is That Universe In The Window?

<div class="h-[86%]">
<LiveEmbed src="https://www.christopherlovell.co.uk/cosmo-carta/" fallback="/img/cosmo_carta_offline.png" :width="1920" />
</div>

<!--
Live: cosmo-carta. Walk through flagship volumes vs resolution. Points to hit: EAGLE, TNG, FLAMINGO, COLIBRE; where the gaps are.
-->

---
class: section-card
---

# ./zoom --only-the-good-bits

<div class="muted mt-4">cheapskate trick #1: zoom simulations</div>

---

# Most Of The Universe Is Boring

<div class="body">
<div class="grid grid-cols-[1fr_1fr] gap-10 mt-2 items-center">
<div>

- Any one science question only cares about **specific** objects
- First galaxies? **Overdense**, early-forming regions
- Milky Way analogues? **Local Group**-like haloes
- Clusters? The most **massive** haloes
- Everything else is, *for that question*, boring

<div v-click class="mt-10 text-xl">So <span class="accent">only pay for the bits your question cares about.</span></div>

</div>
<img src="/img/flamingo.png" class="fig h-108 mx-auto" alt="FLAMINGO large-scale structure" />
</div>

</div>

<div class="credit">FLAMINGO project</div>

---

# What Is A Zoom Simulation?

<div class="grid grid-cols-[1.2fr_1fr] gap-8 h-[86%] items-center">
<div class="h-full flex justify-center">
<ZoomCallouts />
</div>
<div>

- Cheap, low-res **parent** box
- Pick the regions you care about
- Re-run *only* those at **high resolution**

<div v-click class="mt-10 term text-sm">cost ≈ the bits you care about<br><span class="muted">+ a little low-res background</span></div>

</div>
</div>

<div class="credit">Schematic: Chris Lovell</div>

---

# FLARES: Zooming In On The First Galaxies

<div class="body">
<div class="grid grid-cols-[1.1fr_1fr] gap-10 mt-2 items-center">
<div>

- **40 regions** from a (3.2 cGpc)³ parent
- Spanning the full range of **overdensity**, re-weighted to the global distribution
- EAGLE physics, EAGLE resolution, *way* more volume

<div class="muted text-sm mt-8"><a href="https://arxiv.org/abs/2004.07283" target="_blank">Lovell+21</a>, <a href="https://arxiv.org/abs/2008.06057" target="_blank">Vijayan+21</a>, after GIMIC (<a href="https://arxiv.org/abs/0906.4350" target="_blank">Crain+09</a>)</div>

</div>
<img src="/img/zoom_resolution_volume.png" class="fig h-108 mx-auto bg-white" alt="FLARES on the volume-resolution plane" />
</div>

</div>

<div class="credit">Plot: Stephen Wilkins</div>

<!--
Key point: the weighting. Because we know each region's overdensity from the parent, we can stitch the regions back into a representative global distribution function.
-->

---
layout: full
class: full-bleed
---

<div class="absolute inset-0">
  <video src="/video/flares_spheres.mp4" autoplay loop muted playsinline class="w-full h-full object-contain bg-black"></video>
</div>

<div class="credit">FLARES: 40 resimulated regions</div>

---
clicks: 2
---

# Putting The Universe Back Together

<div class="body"><div class="grid grid-cols-[1fr_1fr] gap-8 items-center">
<div class="text-center">
  <div class="relative h-90">
    <img v-click.hide="1" src="/img/flares_sampling_bins.png" class="absolute inset-0 m-auto max-h-full fig bg-white" alt="overdensity PDF of the parent box vs the resimulated regions" />
    <img v-click="1" src="/img/flares_gsmf_delta.png" class="absolute inset-0 m-auto max-h-full fig bg-white" alt="stellar mass function split by region overdensity at z = 9" />
  </div>
  <div class="text-xs muted mt-2"><span v-if="$clicks < 1">parent box (dashed) vs our regions (solid): overdense regions <strong>oversampled</strong></span><span v-else>z = 9: strongly <strong>environment</strong>-dependent</span></div>
</div>
<div>

- Regions picked to **oversample** the rare, overdense ones
- So a naive average is biased high

<div v-click="2" class="mt-6">Fix: weight each region by how common its overdensity <em>really</em> is:</div>

<div v-click="2" class="text-sm mt-4">

$$
f_j = \sum_i \frac{w_{{\rm true},i}}{w_{{\rm sample},i}}\, w_{ij},
\qquad
\phi(X) = \sum_j f_j\, \phi_j(X)
$$

</div>

<div v-click="2" class="text-xs muted mt-3">i: overdensity bins in log(1+δ) · j: regions · w<sub>ij</sub>: fraction of region j in bin i</div>

</div>
</div></div>

<div class="credit"><a href="https://arxiv.org/abs/2004.07283" target="_blank">Lovell+21</a> (FLARES I), after GIMIC (<a href="https://arxiv.org/abs/0906.4350" target="_blank">Crain+09</a>)</div>

<!--
Click 0: the parent's overdensity PDF (log-normal, sigma ~0.05) vs the resimulated grid points: we deliberately oversample the high-overdensity tail (that's where the rare massive galaxies live).
Click 1: the GSMF depends strongly on overdensity, so you can't just stack regions.
Click 2: the weighting. Bin log(1+delta) into 50 bins; w_true,i is the parent fraction in bin i, w_sample,i the sum over regions of their fraction in bin i; each region j gets f_j = sum_i r_i w_ij with r_i = w_true/w_sample, and sum_j f_j = 1. The composite distribution function is the f_j-weighted sum. Same idea TESSERA uses, but with an emulator in place of the discrete sum.
-->

---

# FLARES Thus Far

<div class="text-center text-lg mb-5"><strong>23 papers</strong> <span class="muted">(FLARES I–XXII and counting)</span></div>

<div class="grid grid-cols-3 gap-4 text-sm">
<div class="term"><div class="accent mb-1">JWST observables</div><div class="muted">UV LFs, colours, [OIII] emitters, Balmer breaks, UV indices, the z&gt;10 frontier</div><div class="warn mt-2">6 papers</div></div>
<div class="term"><div class="accent mb-1">Dust, geometry &amp; sizes</div><div class="muted">massive dusty galaxies, star–dust geometry, compact galaxies, UV–dust offsets</div><div class="warn mt-2">6 papers</div></div>
<div class="term"><div class="accent mb-1">Environment &amp; method</div><div class="muted">environmental dependence, survey variance, galaxy–halo connection, SAM comparison</div><div class="warn mt-2">4 papers</div></div>
<div class="term"><div class="accent mb-1">Histories &amp; quenching</div><div class="muted">star formation &amp; enrichment histories, passive galaxies at z ≥ 5, RUBIES-UDS-QG-z7</div><div class="warn mt-2">3 papers</div></div>
<div class="term"><div class="accent mb-1">Black holes &amp; reionisation</div><div class="muted">SMBH properties, early AGN emissivities, SMBH mergers, LyC escape</div><div class="warn mt-2">4 papers</div></div>
<div class="term flex items-center justify-center text-center"><div>all from <strong>40 zooms</strong><br><span class="muted">run once, mined ever since</span></div></div>
</div>

<!--
Paper list (arXiv): I Lovell 2004.07283, II Vijayan 2008.06057, III Vijayan 2108.00830, IV Roper 2203.12627, V Wilkins 2204.09431, VI Wilkins 2207.10920, VII Wilkins 2208.00976, VIII Lovell 2211.07540, IX Roper 2301.05228, X Thomas 2301.09510, XI Wilkins 2301.13038, XII Vijayan 2303.04177, XIII Seeyave 2305.18174, XIV Wilkins 2305.18175, XV Wilkins 2404.02815, XVI Punyasheel 2408.11037, XVII Maltz 2410.24082, XVIII Wilkins 2505.05257, XIX Liao 2505.12591, XX Seeyave 2511.11982, XXI Sant Fournier 2605.13472, XXII Punyasheel 2605.27370, + Turner 2509.16111.
-->

---

# Now Do That… A Thousand Times

<div class="grid grid-cols-[1fr_1.15fr] gap-8 mt-2 items-center">
<div>

- Large volumes, across **cosmology** *and* **galaxy formation** parameters
- Inference wants *thousands* of simulations

<div v-click class="mt-8 text-sm">Emulate each region, integrate over the parent's overdensities:</div>

<div v-click class="mt-2 text-sm">

$$
\Phi_{\rm global}(m\,|\,\boldsymbol\theta) = \int \hat\Phi(m\,|\,\boldsymbol\theta,\delta)\, p(\delta\,|\,\boldsymbol\theta)\,\mathrm{d}\delta
$$

</div>

</div>
<div class="relative h-108">
  <img v-click.hide="1" src="/tessera/baryonic_volume_4_suites.png" class="absolute inset-0 m-auto max-h-full fig bg-white" alt="halo mass vs volume plane with parameter-variation suites" />
  <img v-click="1" src="/tessera/baryonic_volume_5_question.png" class="absolute inset-0 m-auto max-h-full fig bg-white" alt="the gap TESSERA aims at" />
</div>
</div>

<div class="credit">Proof of concept: <a href="https://arxiv.org/abs/2604.17981" target="_blank">arXiv:2604.17981</a></div>

---
layout: center
class: text-center
---

<img src="/tessera/tessera_dark.png" class="w-[70%] mx-auto" alt="TESSERA" />

<div class="muted mt-8 text-lg">a suite of zooms for emulation and inference</div>

---
clicks: 5
---

# The TESSERA Pipeline

<div class="body">
<div class="flex flex-col gap-6 items-center">
  <div class="flex items-end gap-4">
    <div class="text-center"><img src="/tessera/image31.webp" class="h-52 rounded" alt="PM parent" /><div class="text-xs muted mt-1">pmwd PM parents · (1.6 Gpc/h)³</div></div>
    <span v-click="1" class="accent text-3xl mb-14">→</span>
    <div v-click="1" class="text-center"><img src="/tessera/image11.webp" class="h-52 rounded" alt="region selection" /><div class="text-xs muted mt-1">regions across δ</div></div>
    <span v-click="2" class="accent text-3xl mb-14">→</span>
    <div v-click="2" class="text-center"><img src="/tessera/zoom_cutout_P00485.webp" class="h-52 rounded" alt="SWIFT zoom region" /><div class="text-xs muted mt-1">SWIFT zooms · (50 Mpc/h)³ · 1 node each</div></div>
  </div>
  <div v-click="3" class="accent text-3xl self-end -my-8" style="margin-right: 8.6rem">↓</div>
  <div class="flex items-center gap-8 self-end mr-6">
    <div v-click="5" class="text-center"><img src="/img/synthesizer_logo.png" class="h-28 mx-auto" alt="Synthesizer" /><div class="text-xs muted mt-1">Synthesizer: emission</div></div>
    <span v-click="5" class="accent text-3xl">←</span>
    <div v-click="4" class="text-center"><img src="/tessera/shark.png" class="h-24 bg-white rounded p-1 mx-auto" alt="SHARK" /><div class="text-xs muted mt-1">SHARK: galaxies + SFHs</div></div>
    <span v-click="4" class="accent text-3xl">←</span>
    <div v-click="3" class="text-center"><div class="h-32 flex justify-center"><MergerTree /></div><div class="text-xs muted mt-1">HBT-HERONS: subhaloes + merger trees</div></div>
  </div>
</div>

</div>

<div class="credit">Li+22 (pmwd), <a href="https://arxiv.org/abs/2502.06932" target="_blank">Forouhar Moreno+25</a> (HBT-HERONS), Lagos+18,23 (SHARK), <a href="https://arxiv.org/abs/2508.03888" target="_blank">Lovell+25</a>, <a href="https://arxiv.org/abs/2506.15811" target="_blank">Roper+26</a> (Synthesizer)</div>

---
layout: full
class: full-bleed
---

<div class="absolute inset-0">
  <img src="/tessera/mosaic_lowres.jpg" class="w-full h-full object-cover" alt="mosaic of 1024 TESSERA zooms" />
</div>

<div class="absolute bottom-6 left-6 term text-sm"><strong>1,024 zooms</strong> run so far, from an 8,192-point Sobol' design over cosmology + galaxy formation</div>

---

# A Thousand Zooms' Worth Of Distributions

<div class="grid grid-cols-2 gap-4 mt-1 items-center">
  <img src="/tessera/hmf_suite_z0_z2.png" class="fig bg-white max-h-48 mx-auto" alt="halo mass functions" />
  <img src="/tessera/gsmf_suite_z0_z2.png" class="fig bg-white max-h-48 mx-auto" alt="galaxy stellar mass functions" />
  <img src="/tessera/lf_g_suite_z0.png" class="fig bg-white max-h-48 mx-auto" alt="g-band luminosity functions" />
  <img src="/tessera/colour_gr_suite_z0.png" class="fig bg-white max-h-48 mx-auto" alt="g-r colours" />
</div>

<div class="text-center mt-2 text-sm">Every zoom in <span class="theory">blue</span>, all regions combined in <span class="bad">red</span>.</div>

<div class="credit !bottom-0.5">HMF (SWIFT) · GSMF (SHARK) · LF + colours (Synthesizer)</div>

---

# How Good Is The Emulator?

<div class="body">
<div class="grid grid-cols-3 gap-4">
  <div class="text-center"><div class="text-sm mb-2"><span class="accent">halo mass function</span> <span class="muted">· SWIFT</span></div><img src="/tessera/hmf_fractional_fof_z0.png" class="fig bg-white" alt="HMF emulator fractional error on held-out regions" /></div>
  <div class="text-center"><div class="text-sm mb-2"><span class="accent">stellar mass function</span> <span class="muted">· SHARK</span></div><img src="/tessera/smf_fractional_shark_z0.png" class="fig bg-white" alt="SMF emulator fractional error on held-out regions" /></div>
  <div class="text-center"><div class="text-sm mb-2"><span class="accent">g-band LF</span> <span class="muted">· Synthesizer</span></div><img src="/tessera/lf_fractional_shark_g_z0.png" class="fig bg-white" alt="g-band LF emulator fractional error on held-out regions" /></div>
</div>

<div class="text-center mt-6">Unseen regions: median error ≈ 0, scatter <strong>tracks the Poisson noise</strong>.</div>
</div>

<div class="credit">measured / emulated − 1 · band: 16–84% of held-out regions · dashed: Poisson 1σ for the median region · z = 0</div>

<!--
Fractional error of the emulator on regions it never saw in training (104 held-out regions for the HMF, 818 for SMF and LF). Median sits on zero; the 16-84% scatter tracks the Poisson noise of an individual region until the bright/massive end where there are only a handful of objects.
-->

---

# The Receipt

<div class="body">
<div class="grid grid-cols-2 gap-10 mt-8">
<div class="term">
<div class="term-bar"><span /><span /><span /></div>
<div class="muted">periodic, same resolution &amp; volume</div>

- one box: **~9 M core-hours**
- 1000 boxes: <span class="bad">**9 billion core-hours**</span>
- ~0.5 PB of snapshots *per box*

</div>
<div class="term">
<div class="term-bar"><span /><span /><span /></div>
<div class="muted">TESSERA so far</div>

- 1,024 zooms: <span class="accent">**< 1 M core-hours**</span>
- one node per zoom: fills the gaps
- ~17 GB per zoom after trees

</div>
</div>

<div v-click class="mt-12 text-center text-xl">Same statistics, <span class="warn">~10,000× cheaper</span>.</div>

</div>

<!--
9 billion vs under 1 million core hours. The PM parents are essentially free. 8192^3 periodic equivalent; 3.5 TB per snapshot x 140 snapshots. Each zoom ~100 GB with 140 outputs, ~17 GB after merger trees.
-->

---
class: section-card
---

# git log --grep="zoom"

<div class="muted mt-4">zooms are cheap... once someone has made them cheap</div>

---

# Why Zooms Are Hard: The Balancing Act

<div class="body">
<div class="grid grid-cols-[1fr_1fr] gap-10 mt-2 items-center">
<div>

- SWIFT splits work over a **grid of cells**
- That needs work spread **uniformly**
- A zoom is the antithesis

<div v-click class="mt-10">Fix: a <strong>second grid</strong> of zoom cells, nested inside the background.</div>

</div>
<img src="/img/balancing_grid.png" class="h-108 mx-auto" alt="background grid with nested zoom cells" />
</div>

</div>

---

# Cell Construction: Three Kinds Of Cell

<img src="/img/cell_construction.png" class="h-108 mx-auto mt-2" alt="background, void and zoom cell hierarchy" />

<div class="text-center text-sm muted">background → void (holds the zoom region) → zoom cells, each with its own octree</div>

---

# Exploring The Geometry

<div class="body"><ZoomCellExplorer /></div>

<!--
Interactive, follows zoom_init.c (zoom_region_init). The high-res particle extent is padded by region_pad_factor; the background grid is either set or auto-chosen (floor(L/max_dim), odd, shifted so the padded region sits inside one cell, min 8); the void is the background cells covering the padded region; the zoom region IS the void and its cells are the void cells split zoom_top_level_depth times.
Show: auto mode gives a single void cell. Turn auto off and pick an even cdim: the box centre lands on a cell edge, the void becomes 2^3 cells and the achieved pad factor doubles (warning). Shrink bkg cells relative to the region to hit the "too many zoom regions" warning/error.
-->

---

# We All Love Mesh Gravity

<div class="body"><div class="grid grid-cols-[1.9fr_1fr] gap-8 items-center">
<img src="/img/gravity_regimes.png" class="fig" alt="particle-particle, multipole, particle-mesh regimes" />
<div>

- Beyond r<sub>mesh</sub>: **no task at all**
- Coarse global mesh → *big* r<sub>mesh</sub>
- ...and the zoom region is tiny

</div>
</div></div>

---

# The Birds, The Bees, And The Gravity Tasks

<div class="body"><PairTaskHistogram /></div>

<!--
Interactive, toy model. 1 Gpc parent, the 30 Mpc zoom region from the geometry slide: 16^3 zoom cells of 2.16 Mpc. All pairs of zoom cells binned by minimum separation. The slider sets the FFT mesh side N; with SWIFT defaults r_mesh = 4.5 x 1.25 x L/N. Pairs closer than min(r_FMM, r_mesh) are pair tasks, between r_FMM and r_mesh multipole-only, beyond r_mesh the mesh does it all. r_FMM is illustrative (3 zoom cells).
Show: small mesh -> r_mesh bigger than the whole zoom region -> everything is a task. Push N up -> tasks fall. But you hit 1290 (N^3 > 2^31) without a distributed FFT. Leave that hanging: it is what the second mesh solves later.
-->

---

# Have Less, Do Less -> Win

<div class="body">
<div class="grid grid-cols-[1fr_1.3fr] gap-8 mt-2 items-center">
<div>

- Pairs the mesh handles **exit immediately**
- So check the mesh *while* splitting
- **70–90%** fewer pair tasks
- Up to **25%** faster, for *every* SWIFT run

</div>
<div class="relative h-100">
  <img v-click.hide="1" src="/img/gravity_pair_tasks.png" class="absolute inset-0 m-auto max-h-full fig" alt="gravity pair tasks" />
  <img v-click="1" src="/img/task_counts.png" class="absolute inset-0 m-auto max-h-full fig" alt="task counts before and after" />
</div>
</div>

</div>

<!--
The most cheapskate fix of all: the cheapest work is the work you never do.
-->

---

# Have Less, Do Less -> Win (For Everyone)

<div class="body"><div class="grid grid-cols-[1fr_1.2fr] gap-8 items-center">
<div>

- FLAMINGO-DMO-L1000N1800: **not a zoom**
- Run by Matthieu, not me <span class="muted"><s>lying</s></span> being selective
- Saving **grows with time** as the cell hierarchy gets deeper

</div>
<img src="/img/flamingo_dmo_speedup.png" class="fig bg-white max-h-108 mx-auto" alt="scale factor vs wall-clock time, master vs branch, FLAMINGO DMO L1000N1800" />
</div></div>

<!--
Same pair-task change on a big periodic DMO run: the branch reaches z = 0 in ~59 h, master is only at a ~ 0.67 by then. Being a cheapskate in shared code pays off for everyone.
-->

---

# Fine… Maybe We Do Need A Second High-Res Mesh

<img src="/img/zoom_mesh_geometry.png" class="fig bg-white w-full mt-2" alt="global mesh, zoom mesh domain and cut-off radii" />

<div class="text-center mt-6 text-lg">r<sub>mesh</sub>: <span class="bad">17.6 Mpc</span> → <span class="accent">1.7 Mpc</span></div>

<!--
3.2 Gpc box, 63^3 background cells, global mesh 1024^3. Zoom mesh 512^3 over the zoom region + 1 background cell (0.30 Mpc mesh cells).
-->

---

# It Genuinely Seems To Work…

<div class="body">
<div class="grid grid-cols-[1fr_1.5fr] gap-8 mt-2 items-center">
<div>

- 3.2 Gpc parent, 30 Mpc zoom
- Boosted global mesh (1280³) vs global 1024³ + zoom 512³

<div class="big-num mt-8">~25%</div>
<div>less wall-clock</div>

</div>
<img src="/img/hr_mesh.png" class="fig bg-white max-h-108 mx-auto" alt="wall-clock time: global mesh vs global + zoom mesh" />
</div>

</div>

<!--
~700^3 particles, DMO. Read off the plot: ~17.9 h vs ~13.5 h cumulative wall-clock at a = 0.175.
-->

---

# Biting The Bullet: Are We Still Correct?

<div class="body"><div class="grid grid-cols-[1.3fr_1fr] gap-8 items-center">
<img src="/img/accuracy.png" class="fig bg-white max-h-108 mx-auto" alt="force accuracy distributions" />
<div>

- Forces vs exact direct summation
- Zoom branch matches master

</div>
</div></div>

<!--
Hydro is isolated to the zoom region; baryons leaving it are converted to dark matter (if asked).
-->

---

# All That, For A 50% Speed Up…

<div class="body">
<div class="grid grid-cols-[1.4fr_1fr] gap-8 mt-2 items-center">
<img src="/img/master_faster.png" class="fig bg-white max-h-108 mx-auto" alt="zoom branch vs master runtime" />
<div>

<div class="big-num">~50%</div>
<div>faster than master</div>

<div class="muted mt-6 text-sm">(it was 70%... but the pair task improvements landed in master too and closed the gap)</div>
</div>
</div>

</div>

<!--
The gap shrank because the optimisations benefit every SWIFT run: being a cheapskate in a shared code helps everyone.
-->

---

# Zooms Scale!! With Physics And Everything

<div class="body"><div class="grid grid-cols-[1.4fr_1fr] gap-8 items-center">
<img src="/img/zoom_scaling.png" class="fig bg-white max-h-108 mx-auto" alt="MPI strong scaling of zoom runs, EAGLE physics and DMO" />
<div>

- Distributed zoom runs now work, with **full physics**
- Imbalance can reach **5%**, but often **~30%** on average
- The boundary exacerbates comms (next!)
- Better exchanges are in progress

</div>
</div></div>

<!--
Strong scaling, wall-clock vs MPI rank count, EAGLE-model hydro and DMO, against perfect scaling (dashed). Numbers on imbalance from the HPC Days 26 talk.
-->
---

# The Issues Still To Solve With Partitioning

<ZoomCommsExplorer class="mt-2" />

<!--
Interactive. Counts are 3D (scripts/zoom_comms.py): 32^3 background cells, the central void cell holds 16^3 zoom cells, ranks are equal azimuthal wedges around the zoom region, so every rank owns zoom cells and the background next to them (worst case). Every gravity pair closer than r split across ranks is a comm. The map is the mid-plane slice.
Show: at r = 17.6 Mpc (global mesh) the background cells overlapping the zoom region need comms with every off-rank zoom cell within r: background-zoom dominates. Slide r down to 1.7 Mpc (zoom mesh): it collapses. Then slide ranks up.
-->

---
class: section-card
---

# ./forward_model --fast --flexible

<div class="muted mt-4">cheapskate trick #2: Synthesizer</div>

---
clicks: 1
---

# Back To The Nutshell

<div class="mt-10">
<AstroFlowchart :step="2" :highlight="$clicks >= 1 ? 'forward' : ''" />
</div>

<div v-click="1" class="text-center mt-4">Simulations give masses, ages, metallicities. Telescopes see <span class="theory">photons</span>.</div>

<div class="credit">Credit: Stephen Wilkins, Chris Lovell</div>

---
clicks: 8
---

# Forward Modelling Isn't Cheap Either

<div class="body"><ForwardCost :step="$clicks" /></div>

<!--
Every step of a forward model is a modelling choice, and to be honest about the uncertainty you vary them. Click through (numbers are indicative: several of these, e.g. nebular parameters and escape fraction, are really continuous ranges, so this is a lower bound): each choice multiplies the number of model variations (4x4x3x3x3x3x4 = 5,184 by the end). The option lists are representative, not exhaustive. Last click: and every one of those has to be run over the simulation, N_gal x N_part x N_lambda. So it has to be flexible and cheap.
-->

---

# What Is Synthesizer?

<div class="grid grid-cols-[1.3fr_1fr] gap-10 mt-2 items-center">
<div>

- Open-source forward modelling
- **Python** on top, **C/C++** + **OpenMP** underneath
- Particle *and* parametric galaxies
- Swap any model in one line

<div class="mt-8 muted text-sm"><a href="https://arxiv.org/abs/2508.03888" target="_blank">Lovell+25</a>, <a href="https://arxiv.org/abs/2506.15811" target="_blank">Roper+26</a> · <a href="https://pypi.org/project/cosmos-synthesizer/" target="_blank">pip install cosmos-synthesizer</a></div>

</div>
<img src="/img/synthesizer_logo.png" class="h-90 mx-auto" alt="Synthesizer logo" />
</div>

---

# The Building Blocks

<div class="body">
<div class="grid grid-cols-[1fr_auto_1fr_auto_1fr_auto_1fr] gap-2 items-center text-center text-sm">
<div class="term"><div class="accent">Galaxy</div><div class="muted mt-2">stars · gas · BHs<br>particle · param.</div></div>
<div class="accent text-xl">→</div>
<div class="term"><div class="accent">EmissionModel</div><div class="muted mt-2">grids (SPS + Cloudy)<br>extract · attenuate</div></div>
<div class="accent text-xl">→</div>
<div class="term"><div class="accent">Emissions</div><div class="muted mt-2">Sed<br>LineCollection</div></div>
<div class="accent text-xl">→</div>
<div class="term"><div class="accent">Instruments</div><div class="muted mt-2">filters · resolution<br>PSFs · noise</div></div>
</div>

<div class="grid grid-cols-[1.35fr_1fr] gap-6 mt-8 text-sm">
<div class="term">
<div class="muted mb-1"># instrument → observable</div>
<table class="inst">
<tbody>
<tr><td>PhotometricInstrument</td><td>photometry</td></tr>
<tr><td>PhotometricImager</td><td>images (+ PSFs, noise)</td></tr>
<tr><td>SpectroscopicInstrument</td><td>spectra (+ noise)</td></tr>
<tr><td>IntegratedFieldUnit</td><td>data cubes (+ PSFs, noise)</td></tr>
<tr><td>LineImager</td><td>line maps (+ PSFs, noise)</td></tr>
</tbody>
</table>
</div>
<div class="term">
<div class="muted mb-1"># premade, ready to go</div>
<table class="inst">
<tbody>
<tr><td>JWST</td><td>NIRCam (W · M · N) · MIRI</td></tr>
<tr><td>HST</td><td>WFC3 UVIS · WFC3 IR · ACS WFC</td></tr>
<tr><td>Euclid</td><td>NISP · VIS</td></tr>
<tr><td>GALEX</td><td>FUV · NUV</td></tr>
</tbody>
</table>
<div class="muted text-xs mt-2">...or any SVO filter, top hats, your own</div>
<div class="warn text-xs mt-1">more premade instruments on the way</div>
</div>
</div>

<div class="text-center mt-6">One model, any galaxy, any instrument.</div>

<style>
.inst { width: 100%; border-collapse: collapse; }
.inst td { padding: 2px 4px; border-bottom: 1px solid var(--grid); }
.inst td:first-child { color: var(--accent); white-space: nowrap; padding-right: 12px; }
</style>

</div>

---

# The Building Blocks: EmissionModel

<div class="body">
<div class="grid grid-cols-[1fr_auto_1fr_auto_1fr_auto_1fr] gap-2 items-center text-center text-sm">
<div class="term" style="opacity:0.25"><div class="accent">Galaxy</div><div class="muted mt-2">stars · gas · BHs<br>particle · param.</div></div>
<div class="text-xl" style="color:#333">→</div>
<div class="term em-hot"><div class="warn">EmissionModel</div><div class="mt-2">grids (SPS + Cloudy)<br>extract · attenuate</div></div>
<div class="text-xl" style="color:#333">→</div>
<div class="term" style="opacity:0.25"><div class="accent">Emissions</div><div class="muted mt-2">Sed<br>LineCollection</div></div>
<div class="text-xl" style="color:#333">→</div>
<div class="term" style="opacity:0.25"><div class="accent">Instruments</div><div class="muted mt-2">filters · resolution<br>PSFs · noise</div></div>
</div>

<div class="grid grid-cols-4 gap-4 mt-12 text-sm text-center">
<div class="term"><div class="theory">extraction</div><div class="muted mt-1">pull spectra / lines from a grid</div></div>
<div class="term"><div style="color:#f472b6">generation</div><div class="muted mt-1">dust emission, AGN torus...</div></div>
<div class="term"><div class="warn">transformation</div><div class="muted mt-1">dust curves, IGM, escape fractions</div></div>
<div class="term"><div class="accent">combination</div><div class="muted mt-1">add emissions together</div></div>
</div>

<div class="text-center mt-10">Four operations, chained into a <strong>tree</strong>, any of them masked to a subset of particles.</div>
</div>

<style>
.em-hot { border-color: var(--warn); box-shadow: 0 0 18px color-mix(in srgb, var(--warn) 45%, transparent); transform: scale(1.08); }
</style>

<!--
Zoom in on the EmissionModel: everything is built from four operation types (extraction, generation, transformation, combination), linked into a tree. Any operation can take a property mask (e.g. young stars only) or wavelength mask. Next slide: a real one.
-->

---
clicks: 11
---

# Inside An Emission Model

<div class="body"><EmissionModelExplorer :step="$clicks" /></div>

<!--
Interactive. Click 0: the whole PacmanEmission tree (15 models). Clicks 1-10 walk up it one model at a time: extractions from the grid, escape fraction split, nebular, reprocessed, dust attenuation, emergent, energy-balance dust emission, total. Any node is also clickable.
Click 11: variation mode. Defaults fesc x2, tau_v x3 = the docs example: 6 combinations, 40 models instead of 90. Drag the sliders: extractions stay at 1, fesc-only models scale with n_fesc, everything downstream of tau_v scales with both.
-->

---

# What Can It Make?

<div class="wcm">
<section>
  <div class="sec"># spectra &amp; photometry</div>
  <figure><img src="/img/spectra.png" class="bg-white" alt="SED split into emission components" /><figcaption>SEDs, every component</figcaption></figure>
  <figure><img src="/img/spectra_vshift.png" class="bg-white" alt="spectra with and without velocity shifts" /><figcaption>+ velocity shifts</figcaption></figure>
  <figure><img src="/img/photometry_lfs.png" class="bg-white" alt="luminosity functions in four filters" /><figcaption>photometry in any filter</figcaption></figure>
</section>
<section>
  <div class="sec"># lines</div>
  <figure><img src="/img/line_profiles.png" class="bg-white" alt="nebular line luminosities" /><figcaption>line luminosities &amp; fluxes</figcaption></figure>
  <figure><img src="/img/bpt.png" class="bg-white" alt="BPT diagram" /><figcaption>ratios &amp; diagnostics</figcaption></figure>
</section>
<section class="wide">
  <div class="sec"># spatially resolved</div>
  <div class="grid3">
    <figure class="r1"><img src="/img/rgb_imgs.png" alt="RGB images" /><figcaption>images</figcaption></figure>
    <figure class="r1"><img src="/img/psf_one.png" class="fig" alt="image with PSF" /><figcaption>+ PSFs</figcaption></figure>
    <figure class="r1"><img src="/img/noise_one.png" class="fig" alt="image with noise" /><figcaption>+ noise</figcaption></figure>
    <figure class="r2"><img src="/img/line_map.png" class="bg-white" alt="H-alpha line map" /><figcaption>line maps</figcaption></figure>
    <figure class="r2"><img src="/img/data_cube.gif" alt="spectral data cube" /><figcaption>data cubes</figcaption></figure>
    <figure class="r3"><img src="/img/property_maps.jpeg" class="bg-white" alt="property maps" /><figcaption>property maps</figcaption></figure>
  </div>
</section>
</div>

<style>
.wcm { display: grid; grid-template-columns: 1fr 0.8fr 1.6fr; gap: 1.2rem; height: calc(100% - 4.6rem); }
.wcm section { display: flex; flex-direction: column; gap: 0.5rem; min-height: 0; border-left: 1px solid var(--line); padding-left: 0.8rem; }
.wcm .sec { color: var(--accent); font-size: 0.8rem; }
.wcm figure { flex: 1; min-height: 0; margin: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; }
.wcm figure img { max-width: 100%; min-height: 0; flex: 1; object-fit: contain; border-radius: 4px; }
.wcm figcaption { font-size: 0.62rem; color: var(--muted); margin-top: 2px; }
.wcm .grid3 { flex: 1; display: grid; grid-template-columns: repeat(6, 1fr); grid-template-rows: 1fr 1.15fr 1fr; gap: 0.6rem; min-height: 0; }
.wcm .r1 { grid-column: span 2; }
.wcm .r2 { grid-column: span 3; }
.wcm .r3 { grid-column: span 6; }
</style>

---

# Is It Actually Fast Though?

<div class="body"><div class="grid grid-cols-2 gap-10 items-start">
<div>
<div class="phead"># problem size: one galaxy, N stars</div>
<img src="/perf/nparticles_performance_spectra_nlam9244_nt32.png" class="fig bg-white max-h-76 mx-auto" alt="spectra runtime vs number of star particles" />
<div class="pcap">integrated spectrum: <strong>~1 ms</strong>, flat from 10³ to 10⁵ stars<br><span class="muted">per-particle spectra: grows linearly, still ≲ 0.1 s</span></div>
</div>
<div>
<div class="phead"># shared-memory (OpenMP) scaling: 10⁶ stars</div>
<img src="/perf/exclusive_docs_int_spectra_cic_totThreads32_nstars1000000.png" class="fig bg-white max-h-76 mx-auto" alt="thread scaling of integrated spectra for 10^6 star particles" />
<div class="pcap"><strong>~12×</strong> faster on 32 threads<br><span class="muted">top: time per kernel · bottom: speedup vs perfect (dash-dot)</span></div>
</div>
</div></div>

<div class="credit">one COSMA8 node (2 × AMD EPYC 7763) · 32 threads · 9,244 wavelength bins · <a href="https://synthesizer-project.github.io/synthesizer/performance/performance.html" target="_blank">synthesizer-project.github.io/synthesizer/performance</a></div>

---

# Throwing Nodes At It

<div class="body"><div class="grid grid-cols-[1.1fr_1.3fr] gap-8 items-start">
<div>
<div class="phead"># the full Pipeline, everything on</div>
<img src="/perf/pipeline_timing_scaling.png" class="fig bg-white max-h-76 mx-auto" alt="Pipeline runtime vs star particles per galaxy" />
<div class="pcap">10 galaxies · black: total · <strong>O(n)</strong> in particles<br><span class="muted">10⁴ stars each: ~5 s for all 10, on 32 threads</span></div>
<div class="pout">→ 220 spectra · 1,760 fluxes · 55,880 lines · 1,760 imgs</div>
</div>
<div>
<div class="phead"># distributed (MPI) strong scaling</div>
<img src="/perf/mpi_strong_scaling.png" class="fig bg-white mx-auto" alt="MPI strong scaling of the Pipeline and parallel efficiency" />
<div class="pcap">1,000 galaxies of 10⁴ stars, 16 threads per rank<br><strong>97%</strong> parallel efficiency at 32 ranks (4 nodes)</div>
<div class="pout">→ 22,000 spectra · 176,000 fluxes · 5.6M lines · 176,000 images</div>
</div>
</div></div>

<div class="credit">per galaxy: 11 PacmanEmission spectra (9,244 λ) × rest + obs · 8 NIRCam bands (L + F, + images) · 254 lines (L + F) · SFZH, SFH, LOS τ · COSMA8</div>

---

# So What Would Yours Cost?

<div class="body"><PipelineCost /></div>

<!--
Interactive, back of the envelope. Per-galaxy cost read off the full-Pipeline benchmark (10 galaxies, PacmanEmission + dust, photometry, lines, images, 32 threads), interpolated in particle number. Threads: Amdahl with a 95% parallel fraction (12x at 32, as measured). Ranks: 97% efficient. Particle mass sets the mean particles per galaxy via a z~0 Schechter GSMF (log M* 10.7, alpha -1.3) from 100 particles up to 1e12 Msun. Note the MPI benchmark's per-galaxy cost (with gas and BHs) is a few times higher than the Pipeline profile, so treat this as optimistic within a factor of a few.
Try: 1e5 galaxies at 1e6 Msun on a laptop vs 8 nodes.
Outputs per galaxy are what the benchmark actually produces: test grid (9,244 wavelengths, 254 lines), PacmanEmission with 11 saved emissions, JWST NIRCam wide (8 filters), images for every saved emission, rest + observer frame.
-->

---

# Ongoing Work (i.e. The To-Do List)

<div class="body">
<div class="grid grid-cols-2 gap-6 mt-4">
<div class="term"><div class="accent mb-1">Learning the Universe</div><div class="muted text-sm">picked up as the forward model for the collaboration</div></div>
<div class="term"><div class="accent mb-1">Radio</div><div class="muted text-sm">radio emission from star-forming regions</div></div>
<div class="term col-span-2"><div class="accent mb-1">Common ground</div><div class="muted text-sm">the same forward modelling choices across EAGLE, TNG, Simba, ASTRID, SC-SAM, L-Galaxies and SHARK, and inferring them back</div></div>
</div>

<div class="text-center mt-10"><strong>24 papers</strong> <span class="muted">already using Synthesizer, and many more in the works</span></div>

</div>

<div class="credit"><a href="https://synthesizer-project.github.io/synthesizer/publications/publications.html" target="_blank">synthesizer-project.github.io/synthesizer/publications</a></div>

---
clicks: 2
---

# Back To TESSERA

<div class="obs">
  <div v-for="col in [{ t: 'g-band luminosity function', k: 'lf', f: ['lf_regions_shark_g_z0.png', 'lf_global_shark_g_z0.png', 'lf_sweep_shark_g_z0.png'] }, { t: 'g − r colour', k: 'gr', f: ['pdf_regions_shark_g-r_z0.png', 'pdf_global_shark_g-r_z0.png', 'pdf_sweep_shark_g-r_z0.png'] }]" :key="col.k" class="col">
    <div class="text-sm mb-2 accent text-center">{{ col.t }}</div>
    <div class="frame">
      <img v-for="(f, i) in col.f" :key="f" :src="`tessera/${f}`" :class="['fig', 'bg-white', { on: i === Math.min($clicks, 2) }]" :alt="`${col.t}, stage ${i + 1}`" />
    </div>
  </div>
</div>

<div class="text-center text-sm mt-3">
<span v-if="$clicks === 0">Emulator vs <strong>held-out zooms</strong>: every galaxy forward modelled by Synthesizer</span>
<span v-else-if="$clicks === 1">Emulated <strong>global</strong> observables for new parameter draws (blue) vs the fiducial (grey)</span>
<span v-else>Sweep one parameter at a time: what each does to the <strong>observables</strong></span>
</div>

<style>
.obs { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; height: calc(100% - 7rem); }
.obs .col { display: flex; flex-direction: column; min-height: 0; }
.obs .frame { position: relative; flex: 1; min-height: 0; }
.obs .frame img { position: absolute; inset: 0; margin: auto; max-width: 100%; max-height: 100%; opacity: 0; transition: opacity 0.4s; }
.obs .frame img.on { opacity: 1; }
</style>

<!--
Synthesizer inside TESSERA: every galaxy in every zoom gets a full SED from SHARK's star formation histories, so luminosity functions and colours are emulated as observables directly.
Click 0: held-out regions, emulator (blue band) vs measured (points). Click 1: global LF / colour distribution for new parameter draws vs fiducial. Click 2: one-at-a-time parameter sweeps (cosmology + SHARK parameters).
-->

---
layout: full
---

# The Ecosystem

<div class="h-[86%]">
<LiveEmbed src="https://synthesizer-project.github.io/" fallback="/img/synthesizer_site_offline.png" />
</div>

<!--
Live: the project site. Docs, tutorials, grids, the wider set of tools around Synthesizer.
-->

---

# TL;DR

<div class="body">
<div class="term mt-6 text-lg leading-loose">
<div class="term-bar"><span /><span /><span /></div>

<div class="muted">$ cheapskate --summary</div>

- **Zooms**: pay only for the bits you care about
- Making them cheap took real work: **~50%** faster than master
- **Synthesizer**: forward model *everything*, fast

</div>

<div class="text-center mt-10 text-xl">Same budget, <span class="warn">more ambitious science</span>.</div>

</div>

---
layout: center
class: text-center
---

<h1 class="!text-5xl">Thanks!</h1>

<div class="flex justify-center items-center gap-10 mt-12">
  <div class="text-center">
    <img src="/img/qr_slides.png" class="h-36 rounded mx-auto" alt="QR code to these slides" />
    <div class="text-xs muted mt-1"><a href="https://willjroper.github.io/DurhamColloquium_10-26_Cheapskate/" target="_blank">these slides</a></div>
  </div>
  <div class="text-left text-sm leading-loose grid grid-cols-[auto_auto] gap-x-4 justify-items-start">
    <span class="accent">synthesizer</span><a href="https://synthesizer-project.github.io/" target="_blank">synthesizer-project.github.io</a>
    <span class="accent">swift</span><a href="https://swift.strw.leidenuniv.nl/" target="_blank">swift.strw.leidenuniv.nl</a>
    <span class="accent">tessera</span><a href="https://arxiv.org/abs/2604.17981" target="_blank">arXiv:2604.17981</a>
  </div>
</div>

<div class="flex justify-center gap-6 mt-10">
  <img src="/img/oxford_logo.png" class="h-14" alt="University of Oxford" />
  <img src="/img/oxrse_logo.png" class="h-14" alt="OxRSE" />
</div>
