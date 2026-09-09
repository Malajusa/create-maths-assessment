# Assessment visual standard

This standard governs every student-facing visual and marking-key overlay.
It extends the resolved visual profile; it does not change curriculum, question
content, marks or the required assessment structure.

## Purpose gate

Every visual must have a declared purpose. A visual is permitted only when it:

- supplies information needed to solve the question;
- is a representation students must interpret, complete, measure or construct;
- makes a necessary context materially easier to understand;
- reduces avoidable reading demand without reducing mathematical demand; or
- provides a mathematically meaningful response surface.

If removing a visual leaves the task equally understandable and mathematically
unchanged, omit it. Decoration is not a valid purpose.

## Two coordinated modes

### Exact mathematical mode

Use exact mathematical mode for shapes, solids, graphs, grids, coordinate
planes, nets, fraction models, number lines, scales and measurement instruments
when the rendering carries mathematical information.

- Prefer an approved SVG or an editable registered constructor.
- Preserve aspect ratio and mathematically meaningful proportions.
- Declare the scale as `exact`, `to_scale`, `not_to_scale` or `schematic`.
- Use conventional labels and markers from
  `references/mathematical-diagram-conventions.md`.
- Do not add texture, shadow, perspective or detail that changes interpretation.

### Contextual problem-solving mode

Use contextual problem-solving mode only when an original or distributable
illustration establishes a meaningful situation or reduces avoidable language
load. Follow `references/contextual-illustration-standard.md`.

- Keep the situation coherent, recognisable and age-appropriate.
- Include only task-relevant detail.
- Do not reveal an operation, sequence or relationship students must infer.
- Do not convert prose information into a solution-ready display.

## Visual families

Every non-null `visual_spec` declares one primary family:

- `canonical_figure` - an abstract shape or object;
- `mathematical_diagram` - a relationship, construction or model;
- `data_display` - a natural graph, table, timetable, schedule or map;
- `contextual_illustration` - a meaningful real-world situation;
- `response_surface` - a grid, model or axes on which students respond;
- `marking_overlay` - solution evidence added to the duplicated test.

## Colour and print

- Resolve colours and strokes from the profile's versioned token set.
- Use charcoal outlines and very light neutral fills for canonical figures.
- Keep grids and construction lines subordinate to the mathematical object.
- Reserve assessment blue for marking-key overlays and specifically authorised
  emphasis.
- Colour must not be the only answer-critical cue. Use a label, line style,
  pattern, position or shape as a redundant distinction.
- Inspect every page in colour and greyscale at 100% A4 print scale.

## Geometry and assets

- SVG is authoritative for canonical assets.
- Reuse an approved asset before constructing a new visual.
- Use a registered constructor when approved primitives must be composed.
- Record asset IDs, versions and hashes in the design manifest.
- Never stretch, skew or independently edit a PNG fallback.
- Create a new asset only when an approved asset or constructor cannot express
  the required mathematics.

## Layout

- Reserve diagram and response regions before finalising text placement.
- Place prose, labels and visuals close enough to avoid split attention.
- Give required diagrams visual priority, especially on Pages 2 and 3.
- Use only the grid, table or response structure the mathematics requires.
- Preserve clear pencil-working space around student response surfaces.
- Avoid both undersized diagrams surrounded by empty space and unnecessary
  visuals that compress working space.

## Q7 and Q8

Q7 and Q8 remain independent, prose-first problems. Supporting visuals may
provide mathematical evidence or necessary context but must not pre-sort values,
name the strategy, sequence operations or disclose a relationship students are
expected to infer.

For each supporting visual, the content validator records:

1. what information the visual carries;
2. what changes if it is removed;
3. whether it reveals or organises the strategy;
4. whether it introduces irrelevant visual search; and
5. whether its demand survives greyscale reproduction.

The main problem cards calibrate Q7 demand and the extension cards calibrate Q8
demand. Their artwork, card chrome, strategy icons and paired task structure are
not part of this standard.

## Marking keys

- Build the marking key from the finished student test.
- Keep every student visual in the same position and at the same size.
- Add answers and constructions as named `marking_overlay` elements.
- Use assessment blue plus a non-colour cue such as line weight, dash or label.
- Do not obscure task information or shrink the original student diagram.

## Age calibration

Keep one visual language across year levels while changing complexity:

- Pre-primary-Year 1: large concrete representations, few elements and generous
  response surfaces;
- Years 2-4: deliberate transitions between concrete and abstract models;
- Years 5-7: formal notation, natural data displays and denser composite
  representations only when mathematically justified.

Younger visuals must not become decorative or babyish. Older visuals must not
become unnecessarily small or austere.

## Release barriers

Each of the following is a release barrier:

- inaccurate, distorted or contradictory geometry;
- incorrect, ambiguous, colliding or undersized labels;
- a blurry or under-resolution raster asset;
- an unjustified decorative visual;
- a visual that reveals or sequences the solution method;
- a solution-ready Q7 or Q8 display made from prose values;
- misleading scale or undeclared scale status;
- colour-dependent mathematical information;
- an inconsistent representation without mathematical reason;
- a grid or background that overpowers the task;
- misleading 3D perspective or unnecessary hidden edges;
- a marking overlay that moves, changes or obscures the student visual;
- mismatch between prose, visual, answer or rationale;
- missing provenance or incompatible licence; or
- failure of asset, semantic, greyscale, structural or rendered-page checks.

There is no advisory-only visual defect class.
