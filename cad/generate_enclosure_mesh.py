from pathlib import Path


MM = 1.0


PARAMS = {
    "screen_outer_w": 149.86 * MM,
    "screen_outer_h": 66.04 * MM,
    "screen_t": 5.08 * MM,
    "outer_w": 205.0 * MM,
    "outer_d": 45.0 * MM,
    "outer_h": 84.0 * MM,
    "wall": 3.0 * MM,
    "clearance": 0.6 * MM,
    "runner_h": 2.4 * MM,
    "runner_w": 7.0 * MM,
    "face_t": 3.0 * MM,
    "bottom_t": 3.0 * MM,
    "pilot_hole": 4.6 * MM,
    "pilot_outer": 12.0 * MM,
    "pilot_depth": 8.0 * MM,
    "pilot_offset_x": 18.0 * MM,
    "pilot_offset_y": 10.0 * MM,
    "retain_t": 3.0 * MM,
    "retain_d": 6.0 * MM,
    "retain_overlap": 1.5 * MM,
    "retain_margin": 8.0 * MM,
    "vent_slot_len": 16.0 * MM,
    "vent_slot_h": 2.5 * MM,
    "vent_slot_gap": 7.0 * MM,
}

PARAMS["window_w"] = PARAMS["screen_outer_w"] - 4.0
PARAMS["window_h"] = PARAMS["screen_outer_h"] - 4.0
PARAMS["tray_w"] = PARAMS["outer_w"] - 2 * PARAMS["wall"] - 2 * PARAMS["clearance"]
PARAMS["tray_d"] = PARAMS["outer_d"] - PARAMS["face_t"] - PARAMS["clearance"] - 1.0
PARAMS["tray_h"] = PARAMS["outer_h"] - PARAMS["wall"] - PARAMS["runner_h"] - 2 * PARAMS["clearance"]


def tri(a, b, c):
    return (tuple(a), tuple(b), tuple(c))


def box(x0, y0, z0, dx, dy, dz):
    x1, y1, z1 = x0 + dx, y0 + dy, z0 + dz
    v000 = (x0, y0, z0)
    v100 = (x1, y0, z0)
    v110 = (x1, y1, z0)
    v010 = (x0, y1, z0)
    v001 = (x0, y0, z1)
    v101 = (x1, y0, z1)
    v111 = (x1, y1, z1)
    v011 = (x0, y1, z1)
    return [
        tri(v000, v100, v110), tri(v000, v110, v010),
        tri(v001, v011, v111), tri(v001, v111, v101),
        tri(v000, v001, v101), tri(v000, v101, v100),
        tri(v010, v110, v111), tri(v010, v111, v011),
        tri(v000, v010, v011), tri(v000, v011, v001),
        tri(v100, v101, v111), tri(v100, v111, v110),
    ]


def extrude_rects_with_holes(axis, start, end, outer_u0, outer_v0, outer_u1, outer_v1, holes):
    us = {outer_u0, outer_u1}
    vs = {outer_v0, outer_v1}
    for hu0, hv0, hu1, hv1 in holes:
        us.update([hu0, hu1])
        vs.update([hv0, hv1])

    us = sorted(us)
    vs = sorted(vs)
    tris = []

    for i in range(len(us) - 1):
        for j in range(len(vs) - 1):
            u0, u1 = us[i], us[i + 1]
            v0, v1 = vs[j], vs[j + 1]
            cu = (u0 + u1) / 2.0
            cv = (v0 + v1) / 2.0
            inside_outer = outer_u0 <= cu <= outer_u1 and outer_v0 <= cv <= outer_v1
            if not inside_outer:
                continue
            inside_hole = any(hu0 <= cu <= hu1 and hv0 <= cv <= hv1 for hu0, hv0, hu1, hv1 in holes)
            if inside_hole:
                continue

            if axis == "x":
                tris.extend(box(start, u0, v0, end - start, u1 - u0, v1 - v0))
            elif axis == "y":
                tris.extend(box(u0, start, v0, u1 - u0, end - start, v1 - v0))
            elif axis == "z":
                tris.extend(box(u0, v0, start, u1 - u0, v1 - v0, end - start))
            else:
                raise ValueError(f"bad axis {axis}")

    return tris


def build_base_tray():
    p = PARAMS
    tris = []

    left_hole = (
        p["pilot_offset_x"] - p["pilot_hole"] / 2,
        p["pilot_offset_y"] - p["pilot_hole"] / 2,
        p["pilot_offset_x"] + p["pilot_hole"] / 2,
        p["pilot_offset_y"] + p["pilot_hole"] / 2,
    )
    right_hole = (
        p["tray_w"] - p["pilot_offset_x"] - p["pilot_hole"] / 2,
        p["pilot_offset_y"] - p["pilot_hole"] / 2,
        p["tray_w"] - p["pilot_offset_x"] + p["pilot_hole"] / 2,
        p["pilot_offset_y"] + p["pilot_hole"] / 2,
    )

    tris.extend(
        extrude_rects_with_holes(
            "z",
            0,
            p["bottom_t"],
            0,
            0,
            p["tray_w"],
            p["tray_d"],
            [left_hole, right_hole],
        )
    )

    tris.extend(box(0, 0, p["bottom_t"], p["wall"], p["tray_d"], p["tray_h"] - p["bottom_t"]))
    tris.extend(box(p["tray_w"] - p["wall"], 0, p["bottom_t"], p["wall"], p["tray_d"], p["tray_h"] - p["bottom_t"]))

    cable_hole = (
        (p["tray_w"] - 16) / 2,
        0,
        (p["tray_w"] + 16) / 2,
        12,
    )
    tris.extend(
        extrude_rects_with_holes(
            "y",
            p["tray_d"] - p["wall"],
            p["tray_d"],
            0,
            p["bottom_t"],
            p["tray_w"],
            p["tray_h"],
            [cable_hole],
        )
    )

    for center_x in [p["pilot_offset_x"], p["tray_w"] - p["pilot_offset_x"]]:
        outer = (
            center_x - p["pilot_outer"] / 2,
            p["pilot_offset_y"] - p["pilot_outer"] / 2,
            center_x + p["pilot_outer"] / 2,
            p["pilot_offset_y"] + p["pilot_outer"] / 2,
        )
        inner = (
            center_x - p["pilot_hole"] / 2,
            p["pilot_offset_y"] - p["pilot_hole"] / 2,
            center_x + p["pilot_hole"] / 2,
            p["pilot_offset_y"] + p["pilot_hole"] / 2,
        )
        tris.extend(
            extrude_rects_with_holes(
                "z",
                -p["pilot_depth"],
                0,
                outer[0],
                outer[1],
                outer[2],
                outer[3],
                [inner],
            )
        )

    tris.extend(box(18, p["tray_d"] - 16, -2, 12, 10, 2))
    tris.extend(box(p["tray_w"] - 30, p["tray_d"] - 16, -2, 12, 10, 2))

    return tris


def build_sliding_lid():
    p = PARAMS
    tris = []

    screen_x0 = (p["outer_w"] - p["screen_outer_w"]) / 2
    screen_z0 = (p["outer_h"] - p["screen_outer_h"]) / 2
    window_x0 = (p["outer_w"] - p["window_w"]) / 2
    window_z0 = (p["outer_h"] - p["window_h"]) / 2

    window_hole = (
        window_x0,
        window_z0,
        window_x0 + p["window_w"],
        window_z0 + p["window_h"],
    )
    tris.extend(
        extrude_rects_with_holes(
            "y",
            0,
            p["face_t"],
            0,
            0,
            p["outer_w"],
            p["outer_h"],
            [window_hole],
        )
    )

    tris.extend(box(0, p["face_t"], 0, p["wall"], p["outer_d"] - p["face_t"], p["outer_h"]))

    vent_holes = []
    for i in range(4):
        y0 = 14 + i * p["vent_slot_gap"]
        z0 = 24 + i * 8
        vent_holes.append((y0, z0, y0 + p["vent_slot_len"], z0 + p["vent_slot_h"]))
    tris.extend(
        extrude_rects_with_holes(
            "x",
            p["outer_w"] - p["wall"],
            p["outer_w"],
            p["face_t"],
            0,
            p["outer_d"],
            p["outer_h"],
            vent_holes,
        )
    )

    tris.extend(box(0, p["face_t"], p["outer_h"] - p["wall"], p["outer_w"], p["outer_d"] - p["face_t"], p["wall"]))
    tris.extend(box(p["wall"], p["face_t"], 0, p["runner_w"], p["outer_d"] - p["face_t"] - 2, p["runner_h"]))
    tris.extend(box(p["outer_w"] - p["wall"] - p["runner_w"], p["face_t"], 0, p["runner_w"], p["outer_d"] - p["face_t"] - 2, p["runner_h"]))

    left_strip_x = screen_x0 - p["retain_t"]
    right_strip_x = screen_x0 + p["screen_outer_w"] - p["retain_overlap"]
    mid_z0 = screen_z0 + p["retain_margin"]
    mid_h = p["screen_outer_h"] - 2 * p["retain_margin"]
    tris.extend(box(left_strip_x, p["face_t"], mid_z0, p["retain_t"] + p["retain_overlap"], p["retain_d"], mid_h))
    tris.extend(box(right_strip_x, p["face_t"], mid_z0, p["retain_t"] + p["retain_overlap"], p["retain_d"], mid_h))

    inner_x0 = screen_x0 + p["retain_margin"]
    inner_w = p["screen_outer_w"] - 2 * p["retain_margin"]
    tris.extend(box(inner_x0, p["face_t"], screen_z0 - p["retain_t"], inner_w, p["retain_d"], p["retain_t"] + p["retain_overlap"]))
    tris.extend(box(inner_x0, p["face_t"], screen_z0 + p["screen_outer_h"] - p["retain_overlap"], inner_w, p["retain_d"], p["retain_t"] + p["retain_overlap"]))

    return tris


def write_ascii_stl(path, name, triangles):
    with open(path, "w", encoding="ascii") as f:
        f.write(f"solid {name}\n")
        for a, b, c in triangles:
            f.write("  facet normal 0 0 0\n")
            f.write("    outer loop\n")
            f.write(f"      vertex {a[0]:.6f} {a[1]:.6f} {a[2]:.6f}\n")
            f.write(f"      vertex {b[0]:.6f} {b[1]:.6f} {b[2]:.6f}\n")
            f.write(f"      vertex {c[0]:.6f} {c[1]:.6f} {c[2]:.6f}\n")
            f.write("    endloop\n")
            f.write("  endfacet\n")
        f.write(f"endsolid {name}\n")


def write_obj(path, triangles):
    with open(path, "w", encoding="ascii") as f:
        idx = 1
        for a, b, c in triangles:
            for v in (a, b, c):
                f.write(f"v {v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n")
            f.write(f"f {idx} {idx+1} {idx+2}\n")
            idx += 3


def main():
    out = Path(__file__).resolve().parent / "out"
    out.mkdir(parents=True, exist_ok=True)

    parts = {
        "pibar_base_tray": build_base_tray(),
        "pibar_sliding_lid": build_sliding_lid(),
    }

    for name, triangles in parts.items():
        write_ascii_stl(out / f"{name}.stl", name, triangles)
        write_obj(out / f"{name}.obj", triangles)
        print(f"wrote {name}: {len(triangles)} triangles")


if __name__ == "__main__":
    main()
