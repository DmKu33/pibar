// pibar enclosure - first-pass parametric concept
// Units: mm
//
// This file is meant for refinement and export to STL.
// Current screen numbers come from the latest message, but they conflict
// with the stated 6.9" diagonal. Re-measure the real panel before printing.

screen_outer_w = 149.86;
screen_outer_h = 66.04;
screen_t       = 5.08;

outer_w        = 205;
outer_d        = 45;
outer_h        = 84;

wall           = 3;
clearance      = 0.6;
runner_h       = 2.4;
runner_w       = 7;
face_t         = 3;
bottom_t       = 3;

window_w       = screen_outer_w - 4;
window_h       = screen_outer_h - 4;

tray_w         = outer_w - 2 * wall - 2 * clearance;
tray_d         = outer_d - face_t - clearance - 1.0;
tray_h         = outer_h - wall - runner_h - 2 * clearance;

pilot_hole     = 4.6;
pilot_outer    = 12;
pilot_depth    = 8;
pilot_offset_x = 18;
pilot_offset_y = 10;

retain_t       = 3;
retain_d       = 6;
retain_overlap = 1.5;
retain_margin  = 8;

vent_slot_w    = 16;
vent_slot_h    = 2.5;
vent_gap       = 7;

module base_tray() {
    difference() {
        union() {
            cube([tray_w, tray_d, bottom_t]);
            translate([0, 0, bottom_t])
                cube([wall, tray_d, tray_h - bottom_t]);
            translate([tray_w - wall, 0, bottom_t])
                cube([wall, tray_d, tray_h - bottom_t]);

            translate([0, tray_d - wall, bottom_t])
                difference() {
                    cube([tray_w, wall, tray_h - bottom_t]);
                    translate([(tray_w - 16) / 2, -0.1, 0])
                        cube([16, wall + 0.2, 12]);
                }

            translate([pilot_offset_x - pilot_outer / 2, pilot_offset_y - pilot_outer / 2, -pilot_depth])
                difference() {
                    cube([pilot_outer, pilot_outer, pilot_depth]);
                    translate([(pilot_outer - pilot_hole) / 2, (pilot_outer - pilot_hole) / 2, -0.1])
                        cube([pilot_hole, pilot_hole, pilot_depth + 0.2]);
                }

            translate([tray_w - pilot_offset_x - pilot_outer / 2, pilot_offset_y - pilot_outer / 2, -pilot_depth])
                difference() {
                    cube([pilot_outer, pilot_outer, pilot_depth]);
                    translate([(pilot_outer - pilot_hole) / 2, (pilot_outer - pilot_hole) / 2, -0.1])
                        cube([pilot_hole, pilot_hole, pilot_depth + 0.2]);
                }

            translate([18, tray_d - 16, -2])
                cube([12, 10, 2]);
            translate([tray_w - 30, tray_d - 16, -2])
                cube([12, 10, 2]);
        }

        translate([pilot_offset_x - pilot_hole / 2, pilot_offset_y - pilot_hole / 2, -0.1])
            cube([pilot_hole, pilot_hole, bottom_t + 0.2]);
        translate([tray_w - pilot_offset_x - pilot_hole / 2, pilot_offset_y - pilot_hole / 2, -0.1])
            cube([pilot_hole, pilot_hole, bottom_t + 0.2]);
    }
}

module sliding_lid() {
    screen_x0 = (outer_w - screen_outer_w) / 2;
    screen_z0 = (outer_h - screen_outer_h) / 2;
    window_x0 = (outer_w - window_w) / 2;
    window_z0 = (outer_h - window_h) / 2;

    difference() {
        union() {
            difference() {
                cube([outer_w, face_t, outer_h]);
                translate([window_x0, -0.1, window_z0])
                    cube([window_w, face_t + 0.2, window_h]);
            }

            translate([0, face_t, 0])
                cube([wall, outer_d - face_t, outer_h]);

            translate([outer_w - wall, face_t, 0])
                difference() {
                    cube([wall, outer_d - face_t, outer_h]);
                    for (i = [0:3]) {
                        translate([-0.1, 14 + i * vent_gap, 24 + i * 8])
                            cube([wall + 0.2, vent_slot_w, vent_slot_h]);
                    }
                }

            translate([0, face_t, outer_h - wall])
                cube([outer_w, outer_d - face_t, wall]);

            translate([wall, face_t, 0])
                cube([runner_w, outer_d - face_t - 2, runner_h]);

            translate([outer_w - wall - runner_w, face_t, 0])
                cube([runner_w, outer_d - face_t - 2, runner_h]);

            translate([screen_x0 - retain_t, face_t, screen_z0 + retain_margin])
                cube([retain_t + retain_overlap, retain_d, screen_outer_h - 2 * retain_margin]);

            translate([screen_x0 + screen_outer_w - retain_overlap, face_t, screen_z0 + retain_margin])
                cube([retain_t + retain_overlap, retain_d, screen_outer_h - 2 * retain_margin]);

            translate([screen_x0 + retain_margin, face_t, screen_z0 - retain_t])
                cube([screen_outer_w - 2 * retain_margin, retain_d, retain_t + retain_overlap]);

            translate([screen_x0 + retain_margin, face_t, screen_z0 + screen_outer_h - retain_overlap])
                cube([screen_outer_w - 2 * retain_margin, retain_d, retain_t + retain_overlap]);
        }
    }
}

// Uncomment one at a time for export:
// base_tray();
// sliding_lid();
