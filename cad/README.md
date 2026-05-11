# pibar enclosure CAD draft

This folder contains a first-pass enclosure model for the current pibar concept:

- `pibar_enclosure.scad` — parametric source model
- `generate_enclosure_mesh.py` — pure-Python mesh exporter
- `out/` — generated `STL` and `OBJ` files for import into Tinkercad or other tools

## Current assumptions

This model is based on the latest dimensions you gave:

- screen overall size: `149.86 x 66.04 x 5.08 mm`
- Raspberry Pi 3: `85 x 56 x 17 mm`
- driver board: assumed `70 x 56 x 14 mm`
- mini breadboard: assumed `48 x 35 x 10 mm`

Important: the screen numbers are internally inconsistent with a true `6.9"` diagonal.

- `149.86 x 66.04 mm` works out to about `6.45"` diagonal
- earlier notes referenced roughly `181 x 67 mm`

So this is a **layout draft**, not a final print file. Before printing, update the screen values after measuring the real panel with calipers.

## Model intent

- two-part enclosure
  - `base tray`
  - `sliding lid`
- lid has:
  - front display window
  - screen-retention blocks behind the window
  - vent slots on one side
- base tray has:
  - internal cavity for Pi + driver board + mini breadboard
  - rear cable notch
  - front screw-post holes/bosses for adjustable feet

## Current outer size

- overall enclosure target: `205 x 45 x 84 mm`

Axis convention in the model:

- `X` = left to right across the long face
- `Y` = front to back depth
- `Z` = bottom to top height

## Files to import into Tinkercad

Use either:

- `out/pibar_base_tray.stl`
- `out/pibar_sliding_lid.stl`

or the matching `.obj` files.

`STL` is the safest target for Tinkercad import. `OBJ` is also included.

## Regenerate

Run:

```bash
python3 cad/generate_enclosure_mesh.py
```

## What still needs tuning

- exact screen outer size and visible area
- exact driver-board footprint and connector positions
- ribbon cable bend path
- whether the screw feet should be `M4` or `M5`
- whether the screw holes should stay printed as pilot holes or become full through-holes
- whether the vent pattern should move to the back instead of the side
