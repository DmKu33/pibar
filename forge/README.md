# ForgeCAD enclosure model

This folder holds the first ForgeCAD version of the pibar enclosure.

Main file:

- `forge/pibar-enclosure.forge.js`

## What it models

- main enclosure body with:
  - front display window
  - top-access sliding lid
  - simple internal screen shelf and top capture bar
  - vents on both side walls
  - rear cable gap
- optional reference blocks for:
  - Raspberry Pi 3
  - HDMI driver board
  - mini breadboard
- underside front screw bosses / pilot holes for adjustable front feet

## Current assumptions

This draft uses your latest screen dimensions:

- width: `149.86 mm`
- height: `66.04 mm`
- thickness: `5.08 mm`

That does **not** match a true 6.9" diagonal, so treat this as a parametric fit study until you measure the real panel and visible area.

## Run

```bash
forgecad run forge/pibar-enclosure.forge.js
forgecad render 3d forge/pibar-enclosure.forge.js
forgecad render section forge/pibar-enclosure.forge.js --plane XZ
forgecad export stl forge/pibar-enclosure.forge.js
forgecad export step forge/pibar-enclosure.forge.js
```

## Parameters you will likely change first

- `Screen Width`
- `Screen Height`
- `Screen Thickness`
- `Driver Width`
- `Driver Height`
- `Driver Depth`
- `Enclosure Depth`
- `Foot Screw Pilot`
- `Lid Pullout`

## Suggested next validation loop

1. Run:

```bash
forgecad run forge/pibar-enclosure.forge.js
```

2. Then render:

```bash
forgecad render 3d forge/pibar-enclosure.forge.js
forgecad render section forge/pibar-enclosure.forge.js --plane XZ
```

3. If the body, lid, or screen fit look wrong, send me:
   - the `forgecad run` output
   - a screenshot or the rendered PNG
