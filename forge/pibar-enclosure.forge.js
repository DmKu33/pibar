const displayMode = Param.choice("Display Mode", "exploded", ["assembled", "exploded"]);
const showScreen = Param.bool("Show Screen Reference", true);
const showComponents = Param.bool("Show Mock Components", false);

const screenW = Param.number("Screen Width", 149.86, { min: 140, max: 190, step: 0.1, unit: "mm" });
const screenH = Param.number("Screen Height", 66.04, { min: 60, max: 90, step: 0.1, unit: "mm" });
const screenT = Param.number("Screen Thickness", 5.08, { min: 3, max: 10, step: 0.1, unit: "mm" });

const wall = Param.number("Wall", 3.0, { min: 2, max: 6, step: 0.1, unit: "mm" });
const bottomT = Param.number("Base Thickness", 3.0, { min: 2, max: 6, step: 0.1, unit: "mm" });
const enclosureDepth = Param.number("Enclosure Depth", 42.0, { min: 30, max: 70, step: 0.5, unit: "mm" });
const sideMargin = Param.number("Side Margin", 14.0, { min: 8, max: 28, step: 0.5, unit: "mm" });
const topMargin = Param.number("Top Margin", 10.0, { min: 5, max: 20, step: 0.5, unit: "mm" });
const bottomMargin = Param.number("Bottom Margin", 9.0, { min: 5, max: 20, step: 0.5, unit: "mm" });

const windowLip = Param.number("Window Lip", 4.0, { min: 1.5, max: 8, step: 0.1, unit: "mm" });
const screenShelfDepth = Param.number("Screen Shelf Depth", 6.0, { min: 3, max: 12, step: 0.1, unit: "mm" });
const screenShelfThickness = Param.number("Screen Shelf Thickness", 2.0, { min: 1, max: 4, step: 0.1, unit: "mm" });
const screenTopCapture = Param.number("Screen Top Capture", 2.0, { min: 0.5, max: 5, step: 0.1, unit: "mm" });
const screenSupportMargin = Param.number("Screen Support Margin", 8.0, { min: 2, max: 20, step: 0.1, unit: "mm" });
const screenSetback = Param.number("Screen Setback", 0.8, { min: 0.3, max: 3, step: 0.1, unit: "mm" });

const lidT = Param.number("Lid Thickness", 2.4, { min: 1.5, max: 5, step: 0.1, unit: "mm" });
const lidClearance = Param.number("Lid Clearance", 0.35, { min: 0.1, max: 1, step: 0.05, unit: "mm" });
const lidRailWidth = Param.number("Lid Rail Width", 2.4, { min: 1.5, max: 5, step: 0.1, unit: "mm" });
const lidPullout = Param.number("Lid Pullout", 28.0, { min: 0, max: 80, step: 0.5, unit: "mm" });

const cableGapW = Param.number("Cable Gap Width", 24.0, { min: 10, max: 60, step: 0.5, unit: "mm" });
const cableGapH = Param.number("Cable Gap Height", 10.0, { min: 4, max: 20, step: 0.5, unit: "mm" });
const cableGapZ = Param.number("Cable Gap Z", 12.0, { min: 4, max: 28, step: 0.5, unit: "mm" });

const footScrewPilot = Param.number("Foot Screw Pilot", 4.2, { min: 3, max: 6, step: 0.1, unit: "mm" });
const footBossDia = Param.number("Foot Boss Dia", 12.0, { min: 8, max: 18, step: 0.1, unit: "mm" });
const footBossDrop = Param.number("Foot Boss Drop", 8.0, { min: 4, max: 16, step: 0.1, unit: "mm" });
const footInsetX = Param.number("Foot Inset X", 18.0, { min: 10, max: 30, step: 0.1, unit: "mm" });
const footInsetY = Param.number("Foot Inset Y", 10.0, { min: 6, max: 20, step: 0.1, unit: "mm" });

const ventSlotLength = Param.number("Vent Slot Length", 16.0, { min: 8, max: 28, step: 0.1, unit: "mm" });
const ventSlotHeight = Param.number("Vent Slot Height", 2.5, { min: 1.5, max: 5, step: 0.1, unit: "mm" });
const ventSlotCount = Param.number("Vent Slot Count", 3, { min: 2, max: 8, step: 1, integer: true });
const ventSlotGap = Param.number("Vent Slot Gap", 5.5, { min: 3, max: 12, step: 0.1, unit: "mm" });

const piW = Param.number("Pi Width", 85.0, { min: 70, max: 100, step: 0.1, unit: "mm" });
const piH = Param.number("Pi Height", 56.0, { min: 45, max: 70, step: 0.1, unit: "mm" });
const piT = Param.number("Pi Depth", 17.0, { min: 10, max: 25, step: 0.1, unit: "mm" });

const driverW = Param.number("Driver Width", 70.0, { min: 50, max: 95, step: 0.1, unit: "mm" });
const driverH = Param.number("Driver Height", 56.0, { min: 40, max: 75, step: 0.1, unit: "mm" });
const driverT = Param.number("Driver Depth", 14.0, { min: 8, max: 25, step: 0.1, unit: "mm" });

const breadW = Param.number("Breadboard Width", 48.0, { min: 30, max: 80, step: 0.1, unit: "mm" });
const breadH = Param.number("Breadboard Height", 35.0, { min: 20, max: 55, step: 0.1, unit: "mm" });
const breadT = Param.number("Breadboard Depth", 10.0, { min: 5, max: 20, step: 0.1, unit: "mm" });

const outerW = screenW + 2 * sideMargin;
const outerH = bottomMargin + screenH + topMargin;
const outerD = enclosureDepth;
const innerW = outerW - 2 * wall;
const innerD = outerD - 2 * wall;

const outerX0 = -outerW / 2;
const innerX0 = outerX0 + wall;
const innerRightX = outerX0 + outerW - wall;

const screenX0 = -screenW / 2;
const screenZ0 = bottomMargin;
const windowW = screenW - 2 * windowLip;
const windowH = screenH - 2 * windowLip;
const windowX0 = -windowW / 2;
const windowZ0 = screenZ0 + windowLip;

const lidTrackBottomZ = outerH - lidT - lidClearance;
const lidRailDrop = lidT + lidClearance;
const lidPanelW = innerW - 2 * lidClearance;
const lidPanelD = innerD - 2 * lidClearance;
const lidX0 = -lidPanelW / 2;
const lidY0 = wall + lidClearance;
const lidOffsetY = displayMode === "exploded" ? lidPullout : 0;

verify.greaterThan("Window width stays positive", windowW, 20);
verify.greaterThan("Window height stays positive", windowH, 20);
verify.greaterThan("Inner width stays positive", innerW, 60);
verify.greaterThan("Inner depth stays positive", innerD, 20);
verify.greaterThan("Lid panel width stays positive", lidPanelW, 40);
verify.greaterThan("Lid panel depth stays positive", lidPanelD, 20);
verify.greaterThan("Top lid track stays above screen", lidTrackBottomZ, screenZ0 + screenH + 4);
verify.greaterThan("Cable gap clears the floor", cableGapZ, bottomT + 2);

scene({
  background: { top: "#131210", bottom: "#0B0A09" },
  camera: { position: [250, -165, 135], target: [0, 22, 34], fov: 46 },
  ground: { visible: true, color: "#141310", offset: 2 },
  lights: [
    { type: "ambient", color: "#efe7db", intensity: 0.48 },
    { type: "directional", position: [120, -100, 180], color: "#fff4dd", intensity: 1.15 },
    { type: "point", position: [-130, 90, 100], color: "#d9cab3", intensity: 1.1, distance: 600 },
  ],
  postProcessing: { toneMappingExposure: 1.12 },
});

function placedBox(width, depth, height, x0, y0, z0) {
  return box(width, depth, height).moveTo(x0, y0, z0);
}

function centeredCylinder(height, diameter, cx, cy, z0) {
  return cylinder(height, diameter / 2).translate(cx, cy, z0);
}

function buildMainBody() {
  const floor = placedBox(outerW, outerD, bottomT, outerX0, 0, 0);

  const frontWallRaw = placedBox(outerW, wall, outerH, outerX0, 0, 0);
  const windowCut = placedBox(windowW, wall + 2, windowH, windowX0, -1, windowZ0);
  const frontWall = frontWallRaw.subtract(windowCut);

  let leftWall = placedBox(wall, outerD, outerH, outerX0, 0, 0);
  let rightWall = placedBox(wall, outerD, outerH, outerX0 + outerW - wall, 0, 0);

  const ventStackH = ventSlotCount * ventSlotHeight + (ventSlotCount - 1) * ventSlotGap;
  const ventStartZ = outerH * 0.52 - ventStackH / 2;
  const ventY0 = wall + (innerD - ventSlotLength) / 2;
  const leftVentCuts = [];
  const rightVentCuts = [];

  for (let i = 0; i < ventSlotCount; i += 1) {
    const slotZ0 = ventStartZ + i * (ventSlotHeight + ventSlotGap);
    leftVentCuts.push(placedBox(wall + 2, ventSlotLength, ventSlotHeight, outerX0 - 1, ventY0, slotZ0));
    rightVentCuts.push(
      placedBox(wall + 2, ventSlotLength, ventSlotHeight, outerX0 + outerW - wall - 1, ventY0, slotZ0)
    );
  }

  leftWall = leftWall.subtract(...leftVentCuts);
  rightWall = rightWall.subtract(...rightVentCuts);

  const backWallRaw = placedBox(outerW, wall, outerH, outerX0, outerD - wall, 0);
  const lidSlotCut = placedBox(
    lidPanelW + 2 * lidClearance,
    wall + 2,
    lidT + 2 * lidClearance,
    lidX0 - lidClearance,
    outerD - wall - 1,
    lidTrackBottomZ - lidClearance
  );
  const cableGapCut = placedBox(cableGapW, wall + 2, cableGapH, -cableGapW / 2, outerD - wall - 1, cableGapZ);
  const backWall = backWallRaw.subtract(lidSlotCut, cableGapCut);

  const leftRail = placedBox(lidRailWidth, innerD, lidRailDrop, innerX0, wall, outerH - lidRailDrop);
  const rightRail = placedBox(lidRailWidth, innerD, lidRailDrop, innerRightX - lidRailWidth, wall, outerH - lidRailDrop);

  const screenSupportW = screenW - 2 * screenSupportMargin;
  const bottomScreenShelf = placedBox(
    screenSupportW,
    screenShelfDepth,
    screenShelfThickness,
    -screenSupportW / 2,
    wall,
    screenZ0 - screenShelfThickness
  );
  const topScreenBar = placedBox(
    screenSupportW,
    screenShelfDepth,
    screenShelfThickness,
    -screenSupportW / 2,
    wall,
    screenZ0 + screenH - screenTopCapture
  );

  const leftBoss = centeredCylinder(footBossDrop, footBossDia, outerX0 + footInsetX, footInsetY, -footBossDrop);
  const rightBoss = centeredCylinder(footBossDrop, footBossDia, outerX0 + outerW - footInsetX, footInsetY, -footBossDrop);

  let body = union(
    floor,
    frontWall,
    leftWall,
    rightWall,
    backWall,
    leftRail,
    rightRail,
    bottomScreenShelf,
    topScreenBar,
    leftBoss,
    rightBoss
  );

  const leftFootHole = centeredCylinder(
    bottomT + footBossDrop + 2,
    footScrewPilot,
    outerX0 + footInsetX,
    footInsetY,
    -footBossDrop - 1
  );
  const rightFootHole = centeredCylinder(
    bottomT + footBossDrop + 2,
    footScrewPilot,
    outerX0 + outerW - footInsetX,
    footInsetY,
    -footBossDrop - 1
  );

  body = body.subtract(leftFootHole, rightFootHole);
  return body;
}

function buildSlidingLid() {
  return placedBox(lidPanelW, lidPanelD, lidT, lidX0, lidY0, lidTrackBottomZ);
}

function buildScreenRef() {
  return placedBox(screenW, screenT, screenH, screenX0, wall + screenSetback, screenZ0);
}

function buildComponentRefs() {
  const boardBaseZ = bottomT + 4;
  const pi = placedBox(piW, piT, piH, innerX0 + 5, wall + 8, boardBaseZ);
  const driver = placedBox(driverW, driverT, driverH, innerRightX - driverW - 5, wall + 8, boardBaseZ);
  const bread = placedBox(breadW, breadT, breadH, -breadW / 2, outerD - wall - breadT - 4, bottomT + 3);
  return { pi, driver, bread };
}

const body = buildMainBody().color("#C6C0B7");
const lid = buildSlidingLid().translate(0, lidOffsetY, 0).color("#8F877B");

const output = [
  { name: "Main Body", shape: body },
  { name: "Sliding Lid", shape: lid },
];

if (showScreen) {
  output.push({
    name: "Screen Reference",
    shape: buildScreenRef().color("#0C0C0C"),
  });
}

if (showComponents) {
  const refs = buildComponentRefs();
  output.push({ name: "Raspberry Pi 3 Ref", shape: refs.pi.color("#355C7D") });
  output.push({ name: "Driver Board Ref", shape: refs.driver.color("#6C7A52") });
  output.push({ name: "Mini Breadboard Ref", shape: refs.bread.color("#8B6F52") });
}

return output;
