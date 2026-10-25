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

<div class="muted text-sm mb-6">will@durham:~$ ./colloquium --budget=0</div>

<h1 class="blink !text-5xl !mb-4">Doing Astrophysics<br>As A Cheapskate</h1>

<div class="text-lg mt-8">Will Roper</div>

<div class="muted text-sm mt-1">Durham Colloquium · 26 October 2026</div>

</div>

<img src="/img/oxford_logo.png" class="absolute left-6 bottom-6 h-16" alt="University of Oxford" />
<img src="/img/oxrse_logo.png" class="absolute right-6 bottom-6 h-16" alt="OxRSE" />

<!--
Title. Cheapskate framing: compute is the currency, and I'm going to show you how to spend less of it.
-->

---

# whoami

<div class="grid grid-cols-[1fr_auto] gap-10 items-center mt-4">
<div>

- **Research Software Engineer**, OxRSE, Oxford
- I run (and break) simulations
- SWIFT zooms, Synthesizer, too many CLI tools

<div class="term mt-10 text-sm">
<div class="muted">$ history | head</div>
music tech → touring band → chef → access course → MPhys → PhD (Sussex) → research fellow (Sussex) → OxRSE
</div>

</div>
<img src="/img/me.jpg" class="h-100 rounded-lg" alt="Will" />
</div>

<!--
Quick intro. I sit on both sides, astrophysics and research software, which is why this talk is about how we spend compute.
-->

---

# The Plan

<div class="term mt-6 text-lg leading-loose">
<div class="term-bar"><span /><span /><span /></div>

<div>$ cat talk.txt</div>
<div v-click><span class="accent">[1]</span> how astrophysics actually works</div>
<div v-click><span class="accent">[2]</span> what a Universe costs</div>
<div v-click><span class="accent">[3]</span> cheapskate trick #1: <strong>zoom simulations</strong></div>
<div v-click><span class="accent">[4]</span> making zooms cheap in <strong>SWIFT</strong></div>
<div v-click><span class="accent">[5]</span> cheapskate trick #2: <strong>Synthesizer</strong></div>

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
layout: full
class: full-bleed
---

<div class="absolute inset-0">
  <video src="/video/eagle_galaxy_evolution.mp4" autoplay loop muted playsinline class="w-full h-full object-cover"></video>
</div>

<div class="credit">EAGLE, 12.5 Mpc box: galaxy evolution</div>

---

# You Can't Have It All

<div class="grid grid-cols-[1fr_1.15fr] gap-10 mt-2 items-center">
<div>

- **Resolution**: the physics inside galaxies
- **Volume**: the rare objects and the statistics

<div class="term mt-10">cost ∝ N<sub>particles</sub> × N<sub>steps</sub><br><span class="warn">both grow with resolution <em>and</em> volume</span></div>

</div>
<img src="/img/volume_resolution.png" class="fig bg-white h-108 mx-auto" alt="simulation volume vs resolution" />
</div>

<div class="credit">Plot: Chris Lovell</div>

---

# The Price Of Admission

<table class="bill mt-2">
<thead><tr><th>simulation</th><th>box</th><th>particles</th><th class="r">cost</th></tr></thead>
<tbody>
<tr><td>EAGLE Ref-L100N1504</td><td>100 Mpc</td><td>2 × 1504³</td><td class="r">4.5 M</td></tr>
<tr><td>TNG100-1</td><td>111 Mpc</td><td>2 × 1820³</td><td class="r">18 M</td></tr>
<tr><td>FLAMINGO L2p8_m9</td><td>2.8 Gpc</td><td>2 × 5040³ + 2800³ ν</td><td class="r">31 M</td></tr>
<tr><td>TNG300-1</td><td>303 Mpc</td><td>2 × 2500³</td><td class="r">35 M</td></tr>
<tr><td>COLIBRE L200m6</td><td>200 Mpc</td><td>4 × 3008³</td><td class="r">72 M</td></tr>
<tr><td>TNG50-1</td><td>52 Mpc</td><td>2 × 2160³</td><td class="r">~130 M</td></tr>
<tr><td>MillenniumTNG</td><td>740 Mpc</td><td>2 × 4320³</td><td class="r">170 M</td></tr>
<tr class="node"><td>ASTRID</td><td>370 Mpc</td><td>2 × 5500³</td><td class="r">3 M node-h</td></tr>
<tr class="node"><td>Frontier-E (CRK-HACC)</td><td>4.7 Gpc</td><td>2 × 12600³</td><td class="r">1.7 M node-h</td></tr>
</tbody>
</table>

<div class="muted text-xs mt-2">core-hours unless stated · hydro runs · comoving boxes</div>

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
<LiveEmbed src="https://www.christopherlovell.co.uk/cosmo-carta/" fallback="/img/cosmo_carta_offline.png" />
</div>

<!--
Live: cosmo-carta. Walk through flagship volumes vs resolution. Points to hit: EAGLE, TNG, FLAMINGO, COLIBRE; where the gaps are.
-->

---

# Most Of The Universe Is Boring

<div class="grid grid-cols-[1fr_1fr] gap-10 mt-2 items-center">
<div>

- Voids, filaments, typical haloes: **boring**
- First massive galaxies, proto-clusters: **rare**

<div v-click class="mt-12 text-xl">So <span class="accent">only pay for the bits you care about.</span></div>

</div>
<img src="/img/flamingo.png" class="fig h-108 mx-auto" alt="FLAMINGO large-scale structure" />
</div>

<div class="credit">FLAMINGO project</div>

---
class: section-card
---

# ./zoom --only-the-good-bits

<div class="muted mt-4">cheapskate trick #1: zoom simulations</div>

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
layout: full
class: full-bleed
---

<div class="absolute inset-0">
  <video src="/video/flares_spheres.mp4" autoplay loop muted playsinline class="w-full h-full object-contain bg-black"></video>
</div>

<div class="credit">FLARES: 40 resimulated regions</div>

---

# FLARES: Zooming In On The First Galaxies

<div class="grid grid-cols-[1.1fr_1fr] gap-10 mt-2 items-center">
<div>

- **40 regions** from a (3.2 cGpc)³ parent
- Spanning the full range of **overdensity**, re-weighted to the global distribution
- EAGLE physics, EAGLE resolution, *way* more volume

<div class="muted text-sm mt-8"><a href="https://arxiv.org/abs/2004.07283" target="_blank">Lovell+21</a>, <a href="https://arxiv.org/abs/2008.06057" target="_blank">Vijayan+21</a></div>

</div>
<img src="/img/zoom_resolution_volume.png" class="fig h-108 mx-auto bg-white" alt="FLARES on the volume-resolution plane" />
</div>

<div class="credit">Plot: Stephen Wilkins</div>

<!--
Key point: the weighting. Because we know each region's overdensity from the parent, we can stitch the regions back into a representative global distribution function.
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
clicks: 4
---

# The TESSERA Pipeline

<div class="body">
<div class="flex flex-col gap-10 items-center">
  <div class="flex items-end gap-4">
    <div class="text-center"><img src="/tessera/image31.webp" class="h-52 rounded" alt="PM parent" /><div class="text-xs muted mt-1">pmwd PM parents · (1.6 Gpc/h)³</div></div>
    <span v-click="1" class="accent text-3xl mb-14">→</span>
    <div v-click="1" class="text-center"><img src="/tessera/image11.webp" class="h-52 rounded" alt="region selection" /><div class="text-xs muted mt-1">regions across δ</div></div>
    <span v-click="2" class="accent text-3xl mb-14">→</span>
    <div v-click="2" class="text-center"><img src="/tessera/zoom_cutout_P00485.webp" class="h-52 rounded" alt="SWIFT zoom region" /><div class="text-xs muted mt-1">SWIFT zooms · (50 Mpc/h)³ · 1 node each</div></div>
  </div>
  <div class="flex items-center gap-8">
    <div v-click="4" class="text-center"><img src="/img/synthesizer_logo.png" class="h-28 mx-auto" alt="Synthesizer" /><div class="text-xs muted mt-1">Synthesizer: emission</div></div>
    <span v-click="4" class="accent text-3xl">←</span>
    <div v-click="3" class="text-center"><img src="/tessera/shark.png" class="h-24 bg-white rounded p-1 mx-auto" alt="SHARK" /><div class="text-xs muted mt-1">SHARK: galaxies + SFHs</div></div>
  </div>
</div>

</div>

<div class="credit">Li+22 (pmwd), Lagos+18,23 (SHARK), <a href="https://arxiv.org/abs/2508.03888" target="_blank">Lovell+25</a>, <a href="https://arxiv.org/abs/2506.15811" target="_blank">Roper+26</a> (Synthesizer)</div>

---
layout: full
class: full-bleed
---

<div class="absolute inset-0">
  <img src="/tessera/mosaic_lowres.jpg" class="w-full h-full object-cover" alt="mosaic of 1024 TESSERA zooms" />
</div>

<div class="absolute bottom-6 left-6 term text-sm"><strong>1,024 zooms</strong> run so far, from an 8,192-point Sobol' design over cosmology + galaxy formation</div>

---

# Turns Out It Works

<div class="grid grid-cols-2 gap-4 mt-1 items-center">
  <img src="/tessera/hmf_suite_z0_z2.png" class="fig bg-white max-h-48 mx-auto" alt="halo mass functions" />
  <img src="/tessera/gsmf_suite_z0_z2.png" class="fig bg-white max-h-48 mx-auto" alt="galaxy stellar mass functions" />
  <img src="/tessera/lf_g_suite_z0.png" class="fig bg-white max-h-48 mx-auto" alt="g-band luminosity functions" />
  <img src="/tessera/colour_gr_suite_z0.png" class="fig bg-white max-h-48 mx-auto" alt="g-r colours" />
</div>

<div class="text-center mt-2 text-sm">Every zoom in <span class="theory">blue</span>, all regions combined in <span class="bad">red</span>.</div>

<div class="credit !bottom-0.5">HMF (SWIFT) · GSMF (SHARK) · LF + colours (Synthesizer)</div>

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

<div class="grid grid-cols-[1fr_1fr] gap-10 mt-2 items-center">
<div>

- SWIFT splits work over a **grid of cells**
- That needs work spread **uniformly**
- A zoom is the antithesis

<div v-click class="mt-10">Fix: a <strong>second grid</strong> of zoom cells, nested inside the background.</div>

</div>
<img src="/img/balancing_grid.png" class="h-108 mx-auto" alt="background grid with nested zoom cells" />
</div>

---

# Cell Construction: Three Kinds Of Cell

<img src="/img/cell_construction.png" class="h-108 mx-auto mt-2" alt="background, void and zoom cell hierarchy" />

<div class="text-center text-sm muted">background → void (holds the zoom region) → zoom cells, each with its own octree</div>

---

# Play With The Geometry

<ZoomCellExplorer class="mt-2" />

<!--
Interactive. Defaults are the real test zoom: 3.2 Gpc box, 63 background cells per side, a 30 Mpc region, depth 4 -> 16^3 zoom cells.
Show: more background cells -> smaller void -> finer zoom cells at fixed depth. Grow the region past a background cell and the void jumps to 2^3 cells. Depth sets the zoom cell size.
Toy model: the real code has more nuance (padding rules etc).
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

# Where Do All These Tasks Come From?

<div class="body"><PairTaskHistogram /></div>

<!--
Interactive, toy model: all pairs of 16^3 zoom cells (3.17 Mpc each) binned by their minimum separation. r_FMM fixed (illustrative, 9.5 Mpc).
Pairs closer than min(r_FMM, r_mesh) are pair tasks; between r_FMM and r_mesh they are multipole-only; beyond r_mesh the mesh does it all.
Presets: global 1024^3 mesh on 3.2 Gpc -> r_mesh 17.6 Mpc; adding a 512^3 zoom mesh -> 1.7 Mpc, leaving only neighbouring cells.
-->

---

# Have Less, Do Less -> Win

<div class="body">
<div class="grid grid-cols-[1fr_1.3fr] gap-8 mt-2 items-center">
<div>

- Pairs the mesh handles **exit immediately**
- So check the mesh *while* splitting
- **~90%** fewer pair tasks
- Up to **25%** faster, for *every* SWIFT run

</div>
<div class="relative h-100">
  <img v-click.hide src="/img/gravity_pair_tasks.png" class="absolute inset-0 m-auto max-h-full fig" alt="gravity pair tasks" />
  <img v-click src="/img/task_counts.png" class="absolute inset-0 m-auto max-h-full fig" alt="task counts before and after" />
</div>
</div>

</div>

<!--
The most cheapskate fix of all: the cheapest work is the work you never do.
-->

---

# The Unavoidable: Partitioning

<ZoomCommsExplorer class="mt-2" />

<!--
Interactive, toy 2D model: 32^2 background cells, one void cell holding 16^2 zoom cells. Ranks get equal angular wedges around the zoom region: balanced, but every rank owns part of the zoom region and the background around it.
Every cross-rank pair task is a comm: background neighbours, zoom pairs within r_mesh, and (worst case, global mesh only) the background cells around the void talk to every zoom cell.
Show global only, slide ranks up, then hit "+ zoom mesh". That's the motivation for the second mesh.
-->

---

# Fine… Maybe We Do Need A Second High-Res Mesh

<img src="/img/zoom_mesh_geometry.png" class="fig bg-white w-full mt-2" alt="global mesh, zoom mesh domain and cut-off radii" />

<div class="text-center mt-6 text-lg">r<sub>mesh</sub>: <span class="bad">17.6 Mpc</span> → <span class="accent">1.7 Mpc</span></div>

<!--
3.2 Gpc box, 63^3 background cells, global mesh 1024^3. Zoom mesh 512^3 over the zoom region + 1 background cell (0.30 Mpc mesh cells).
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

# It Genuinely Seems To Work…

<div class="grid grid-cols-[1fr_1.5fr] gap-8 mt-2 items-center">
<div>

- 3.2 Gpc parent, 30 Mpc zoom
- Boosted global mesh (1280³) vs global 1024³ + zoom 512³

<div class="big-num mt-8">~25%</div>
<div>less wall-clock</div>

</div>
<img src="/img/hr_mesh.png" class="fig bg-white max-h-108 mx-auto" alt="wall-clock time: global mesh vs global + zoom mesh" />
</div>

<!--
~700^3 particles, DMO. Read off the plot: ~17.9 h vs ~13.5 h cumulative wall-clock at a = 0.175.
-->

---

# Master Is Faster Too Now…

<div class="grid grid-cols-[1.4fr_1fr] gap-8 mt-2 items-center">
<img src="/img/master_faster.png" class="fig bg-white max-h-108 mx-auto" alt="zoom branch vs master runtime" />
<div>

<div class="big-num">~50%</div>
<div>faster than master</div>

<div class="muted mt-6 text-sm">(it was 70%... until the general fixes landed in master too)</div>

<img src="/img/zoom_scaling.png" class="fig bg-white h-44 mt-6" alt="strong scaling with physics" />

</div>
</div>

<!--
The gap shrank because the optimisations benefit every SWIFT run: being a cheapskate in a shared code helps everyone. Zooms scale with full physics, and MPI zoom runs are now possible.
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

# Simulations Don't Make Photons

<div class="grid grid-cols-[1fr_1.2fr] gap-8 mt-2 items-center">
<div>

- SPS, IMF, nebular, dust, AGN, instruments...
- **Every choice is a model**
- And you want to vary them all

<div v-click class="mt-10 text-lg">So: <strong>flexible</strong> <em>and</em> <strong>fast</strong>.</div>

</div>
<img src="/img/emission_tree.png" class="fig bg-white max-h-100 mx-auto" alt="an emission model tree" />
</div>

---

# Inference Eats Forward Models

<div class="body">
<div class="flex items-center justify-center gap-4 text-lg">
<div class="term text-center">θ<div class="text-xs muted">physics + model choices</div></div>
<span class="accent text-3xl">→</span>
<div class="term text-center" style="border-color: var(--warn)">forward model<div class="text-xs muted">Synthesizer</div></div>
<span class="accent text-3xl">→</span>
<div class="term text-center">x<div class="text-xs muted">photometry · spectra · images</div></div>
<span class="accent text-3xl">→</span>
<div class="term text-center">train<div class="text-xs muted">SBI</div></div>
</div>

<div v-click class="text-center mt-14 text-xl">× <span class="warn">millions</span> of (θ, x) pairs</div>

<div v-click class="text-center mt-4 muted">The forward model sets the budget.</div>

</div>

---

# Why Bother Being Fast?

<div class="body"><SpeedChart /></div>

<div class="credit">Synference: <a href="https://arxiv.org/abs/2511.10640" target="_blank">Harvey, Lovell et al. 2026</a> · timed on 3000 JADES galaxies with spectroscopic redshifts</div>

<!--
Interactive: drag to Euclid / Rubin. Amortised inference is milliseconds per object, but only because a fast forward model built the training set.
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
<div class="grid grid-cols-[1fr_auto_1fr_auto_1fr] gap-3 mt-10 items-center text-center">
<div class="term"><div class="accent">Galaxy</div><div class="text-sm muted mt-2">stars · gas · black holes<br>particle or parametric</div></div>
<div class="accent text-2xl">→</div>
<div class="term"><div class="accent">EmissionModel</div><div class="text-sm muted mt-2">grids (SPS + Cloudy)<br>extract · attenuate · combine</div></div>
<div class="accent text-2xl">→</div>
<div class="term"><div class="accent">Instruments</div><div class="text-sm muted mt-2">filters · resolution<br>PSFs · noise</div></div>
</div>

<div class="term mt-10 text-sm">
<div class="muted"># observables</div>
Sed · PhotometryCollection · ImageCollection · SpectralCube · LineCollection
</div>

<div class="text-center mt-8">One model, any galaxy, any instrument.</div>

</div>

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

<div class="grid grid-cols-2 gap-8 mt-2 items-center">
<div class="text-center">
<img src="/perf/nparticles_performance_spectra_nlam9244_nt32.png" class="fig bg-white max-h-80 mx-auto" alt="spectra runtime vs number of particles" />
<div class="text-sm mt-2">integrated spectra: <strong>~1 ms</strong>, 10³ → 10⁵ particles</div>
</div>
<div class="text-center">
<img src="/perf/exclusive_docs_int_spectra_cic_totThreads32_nstars1000000.png" class="fig bg-white max-h-80 mx-auto" alt="thread scaling of integrated spectra for 1e6 particles" />
<div class="text-sm mt-2">10⁶ particles: <strong>~12×</strong> on 32 threads</div>
</div>
</div>

<div class="credit">COSMA8 (2 × AMD EPYC 7763) · 9244 wavelength bins · <a href="https://synthesizer-project.github.io/synthesizer/performance/performance.html" target="_blank">synthesizer-project.github.io/synthesizer/performance</a></div>

---

# Throwing Nodes At It

<div class="grid grid-cols-[1fr_1.3fr] gap-8 mt-2 items-center">
<div class="text-center">
<img src="/perf/pipeline_timing_scaling.png" class="fig bg-white max-h-80 mx-auto" alt="Pipeline runtime vs particle count" />
<div class="text-sm mt-2">full Pipeline, everything on: <strong>O(n)</strong></div>
</div>
<div class="text-center">
<img src="/perf/mpi_strong_scaling.png" class="fig bg-white mx-auto" alt="MPI strong scaling of the Pipeline" />
<div class="text-sm mt-2">1,000 galaxies over MPI: <strong>near-ideal</strong> to 32 ranks</div>
</div>
</div>

<div class="credit">Pipeline: LOS optical depths, SFHs, spectra, photometry, lines, images (rest + observer frame) · 16 threads per rank, 4 COSMA8 nodes</div>

---

# Back To TESSERA

<div class="grid grid-cols-[1fr_1.3fr] gap-8 mt-2 items-center">
<div>

- Every galaxy, every zoom, a full SED
- LFs and colours emulated **as observables**
- Run as each zoom finishes

</div>
<img src="/tessera/lf_global_shark_g_z0.png" class="fig bg-white max-h-108 mx-auto" alt="global g-band LF" />
</div>

---

# Ongoing Work (i.e. The To-Do List)

<div class="grid grid-cols-2 gap-6 mt-4">
<div class="term"><div class="accent mb-1">Learning the Universe</div><div class="muted text-sm">picked up as the forward model for the collaboration</div></div>
<div class="term"><div class="accent mb-1">Radio</div><div class="muted text-sm">radio emission from star-forming regions</div></div>
<div class="term col-span-2"><div class="accent mb-1">Common ground</div><div class="muted text-sm">the same forward modelling choices across EAGLE, TNG, Simba, ASTRID, SC-SAM, L-Galaxies and SHARK, and inferring them back</div></div>
</div>

<div class="text-center mt-10"><strong>24 papers</strong> <span class="muted">already using Synthesizer, and many more in the works</span></div>

<div class="credit"><a href="https://synthesizer-project.github.io/synthesizer/publications/publications.html" target="_blank">synthesizer-project.github.io/synthesizer/publications</a></div>

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
  <div class="text-left text-sm leading-loose">
    <div><span class="accent">synthesizer</span> <a href="https://synthesizer-project.github.io/" target="_blank">synthesizer-project.github.io</a></div>
    <div><span class="accent">swift</span> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <a href="https://swift.strw.leidenuniv.nl/" target="_blank">swift.strw.leidenuniv.nl</a></div>
    <div><span class="accent">tessera</span> &nbsp;&nbsp;&nbsp; <a href="https://arxiv.org/abs/2604.17981" target="_blank">arXiv:2604.17981</a></div>
  </div>
</div>

<div class="flex justify-center gap-6 mt-10">
  <img src="/img/oxford_logo.png" class="h-14" alt="University of Oxford" />
  <img src="/img/oxrse_logo.png" class="h-14" alt="OxRSE" />
</div>
