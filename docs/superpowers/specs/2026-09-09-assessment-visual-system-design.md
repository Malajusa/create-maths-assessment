# Assessment visual system design

Date: 2026-09-09  
Status: proposed for user review  
Target baseline: Create Maths Assessment v3.4 visual-production branch

## Purpose

Create an executable visual standard for the Create Maths Assessment skill so that every generated assessment uses clear, mathematically accurate and purposeful visuals regardless of the generating model.

The system must govern more than image appearance. It must control whether a visual belongs in a question, what mathematical work it performs, how it is constructed, how it is placed on the page and how it is validated before release.

## Goals

- Establish one coherent visual language from Pre-primary to Year 7 while allowing age-appropriate complexity.
- Preserve the approved A4 assessment hierarchy and v3.4 visual-profile architecture.
- Make exact mathematical diagrams reproducible and editable.
- Permit contextual illustrations when they improve comprehension or carry necessary information.
- Preserve the reasoning demand of Q7 and Q8 rather than using visuals to pre-organise or solve the problem.
- Make student tests clear in colour and in ordinary greyscale photocopies.
- Keep marking-key additions visibly distinct without changing the underlying student assessment.
- Convert visual defects into objective, fail-closed release barriers where possible.
- Provide approved assets, complete-page exemplars and machine-readable evidence rather than relying on prose guidance alone.

## Non-goals

- Reproduce or distribute illustrations from the Junior Illustrated Maths Dictionary, NAPLAN papers or the supplied problem-solving card archive.
- Make assessment pages resemble commercial problem-solving cards or an illustrated dictionary.
- Add decoration to routine questions.
- Replace mathematical or pedagogical review with automated geometry or layout checks.
- Build the complete Pre-primary-to-Year-7 asset catalogue in the first implementation increment.
- Change the established question structure, 20-mark allocation, A4 output format or Q7/Q8 independence rules.

## Source synthesis

The design derives principles from five evidence groups.

### NAPLAN numeracy papers

Useful characteristics:

- restrained assessment presentation;
- compact, readable question hierarchy;
- diagrams sized according to their function;
- subdued grids and construction lines;
- clear proximity between labels and the represented information;
- colour used sparingly and not required for most questions;
- substantial variation in mathematical representations, including maps, nets, graphs, tables, spinners, shapes and measurement displays.

Characteristics not to preserve:

- legacy low-resolution artwork;
- inconsistent illustration styles across years;
- diagrams that are too small for the current assessment format;
- dated visual treatment.

### Junior Illustrated Maths Dictionary

Useful characteristics:

- conventional angle arcs, equality marks, parallel marks, vertices and leaders;
- recognisable real-world examples paired with abstract concepts;
- bold separation of important regions and faces;
- clear visual distinctions between examples and counterexamples;
- accessible representations of shapes, solids, measurement and data concepts.

Characteristics not to preserve:

- page-level density intended for a reference book;
- decorative or explanatory material unnecessary in an assessment;
- multiple unrelated illustration styles;
- source artwork, which remains subject to its licence and must not be bundled or reproduced.

### Problem-solving main and extension cards

Useful characteristics:

- one coherent situation per task;
- familiar contexts that make quantities and relationships meaningful;
- integrated prose and visual information;
- visuals that support interpretation without prescribing a solution method;
- extension demand created by changed relationships, inference or constraints rather than by visual clutter;
- natural data displays only where the scenario genuinely contains a graph, timetable, schedule or table.

Characteristics not to preserve:

- subject-colour borders, strategy icons, publisher branding and card chrome;
- saturated backgrounds and dated clip art;
- visible strategy cues;
- the paired main/extension structure as an assessment sequence. Q7 and Q8 remain independent problems even though the main cards calibrate Q7 demand and the extension cards calibrate Q8 demand.

### Approved base shape assets

The approved square, circle and equilateral triangle establish the base asset language:

- mathematically exact geometry;
- dark charcoal outlines;
- very light neutral fills;
- transparent outer backgrounds;
- consistent internal padding and apparent scale;
- SVG authority with high-resolution PNG fallbacks;
- no labels, shadows, gradients or decorative effects in canonical base assets.

### Existing assessment benchmarks

The Year 6 transformations benchmark demonstrates the desired page hierarchy, diagram prominence, visual variety and marking-key separation. The weaker transformation output demonstrates why prose-only styling is insufficient: compliant page bounds can still contain small, repetitive, low-contrast or mechanically selected visuals.

## Core principle

Every visual must have a declared mathematical or accessibility purpose.

A visual is justified when it does at least one of the following:

1. supplies information required to solve the question;
2. is itself the mathematical representation being interpreted, completed, measured or constructed;
3. makes a necessary context materially easier to understand;
4. reduces avoidable reading demand for the intended cohort without reducing mathematical demand;
5. provides an appropriate response surface.

If removing the visual leaves the task equally understandable and mathematically unchanged, the visual is normally unnecessary. A small contextual illustration for younger students is permitted only when the assessment blueprint records its accessibility purpose.

## Visual modes

The system uses two coordinated modes.

### Exact mathematical mode

Use for shapes, solids, graphs, grids, coordinate planes, nets, fraction models, number lines, scales and measurement instruments when the rendering carries mathematical information.

Requirements:

- exact or explicitly declared schematic geometry;
- editable native PowerPoint elements or approved SVG assets;
- deterministic labels and annotation placement;
- no perspective or scale distortion that changes the mathematics;
- no unnecessary texture, shadow or decoration;
- a declared scale status: `exact`, `to_scale`, `not_to_scale` or `schematic`.

### Contextual problem-solving mode

Use for original illustrations that establish a real-world situation, reduce avoidable language load or make relationships understandable.

Requirements:

- original or correctly licensed artwork;
- one coherent, age-appropriate illustration style;
- immediately recognisable objects and plausible proportions;
- only task-relevant detail;
- no strategy cue, labelled operation or visual decomposition that performs reasoning intended for the student;
- no decorative scene when a simpler mathematical representation is sufficient;
- exact dimensions only when students must use or measure them.

Both modes share typography, colour, accessibility, placement and release-QA rules.

## Visual families

Every visual representation must be assigned exactly one primary family in the assessment specification.

| Family | Purpose | Examples |
| --- | --- | --- |
| `canonical_figure` | Represent an abstract mathematical object | square, triangle, circle, prism |
| `mathematical_diagram` | Encode relationships or support construction | angle diagram, coordinate grid, number line, net |
| `data_display` | Present naturally structured information for interpretation | graph, timetable, table, map, spinner |
| `contextual_illustration` | Establish or clarify a meaningful situation | measuring jug, paving layout, recipe scene |
| `response_surface` | Provide a mathematically meaningful place to respond | grid to complete, blank graph axes, partitioned model |
| `marking_overlay` | Add solution evidence to the duplicated test | blue construction, answer label, mark annotation |

An element can have secondary roles, but its primary family determines its construction and validation rules.

## Purpose declaration

Extend each non-null `visual_spec` so it records:

- `family`;
- `purpose`;
- `information_carried`;
- `removal_effect`;
- `scale_status`;
- `student_action`;
- `strategy_reveal_risk`;
- `source_kind`;
- `asset_ids` or `constructor_id`;
- `accessibility_cues`;
- `editable_required`;
- `minimum_print_dimensions_mm`;
- `omission_reason` when no visual is used in a representationally expected item.

The blueprint and validators must reject generic entries such as `add a picture` or `use a diagram` without a declared information role.

## Problem-solving visual rules

Q7 and Q8 remain prose-first, independent, self-contained problems.

### Permitted supporting visuals

- a natural graph, schedule, map, price list or timetable that students must interpret;
- a geometric or measurement diagram that supplies mathematical evidence;
- a restrained contextual illustration that clarifies the physical situation;
- a response surface needed to construct or show a result.

### Prohibited supporting visuals

- a solution-ready table that extracts and categorises values from the prose;
- arrows, grouping, colour coding or labels that reveal the intended sequence of operations;
- decorative characters or objects that do not change comprehension;
- a visual that contradicts the written quantities;
- a diagram that converts a required inference into direct reading;
- strategy icons or named problem-solving procedures;
- reuse of Q7's visual, setting or data as the basis of Q8.

### Demand preservation check

For Q7 and Q8, the content validator must compare the task with and without the visual and answer:

1. What information becomes unavailable or harder to interpret when the visual is removed?
2. Does the visual disclose a relationship the student is intended to infer?
3. Does it pre-sort information into a calculation pathway?
4. Does it introduce irrelevant decoding or visual search?
5. Is the same mathematical demand retained in greyscale?

Any unjustified reduction or inflation of demand is a content barrier, not merely a formatting defect.

## Visual tokens

The existing `visual-profile` remains the assessment-level style authority. Extend it with references to versioned token sets rather than embedding every asset rule into agent prose.

The default token set should include:

- charcoal primary outline;
- very light neutral canonical fill;
- two stepped neutral face fills for 3D solids and overlapping regions;
- pale grid and construction-line colours;
- one assessment blue for marking overlays and permitted instructional emphasis;
- minimum contrast ratios;
- separate stroke widths for primary geometry, axes, grids, leaders, hidden edges and answer overlays;
- standard dash patterns;
- standard arrowheads, vertex points, angle arcs, tick marks and parallel marks;
- canonical padding and SVG view-box rules;
- minimum A4 print dimensions by visual family;
- greyscale equivalents.

Colour must never be the only method used to distinguish answer-critical categories. Use position, labels, shape, pattern or line style as a redundant cue.

## Canonical asset library

Approved reusable assets live under a versioned visual-assets directory and are indexed by a machine-readable manifest.

Each manifest entry should record:

- stable asset ID and version;
- display name and aliases;
- visual family;
- mathematical properties;
- year-band suitability;
- SVG path and optional PNG fallback;
- native view box and padding;
- default and permitted variants;
- label anchors;
- allowed transformations;
- whether aspect-ratio changes are forbidden;
- scale status;
- accessibility metadata;
- asset hash;
- validation status.

The SVG is authoritative. PNG exports are compatibility fallbacks and must be regenerated from the authoritative asset rather than edited independently.

Initial canonical assets should cover only the proof set:

- square, circle and equilateral triangle;
- right-angled or scalene labelled triangle;
- angle diagram;
- fraction region model;
- number line;
- coordinate grid;
- cube or rectangular prism;
- cylinder;
- object net;
- spinner;
- ruler or measuring container;
- simple graph.

The broader Pre-primary-to-Year-7 catalogue is added incrementally after the proof set passes.

## Construction hierarchy

When a question requires a visual, the builder must use this order:

1. reuse an approved asset without distortion;
2. compose approved assets and governed primitives using a registered constructor;
3. create a new exact mathematical asset under the standard;
4. create or source an original contextual illustration under the contextual specification;
5. record why the preceding options were unsuitable.

Unregistered ad hoc visual generation is not permitted in a release package.

## Mathematical conventions

The existing `mathematical-diagram-conventions.md` remains authoritative and is expanded, not duplicated.

The implementation must add rules for:

- equal-side, equal-angle, parallel and right-angle markers;
- visible and hidden 3D edges;
- consistent solid projection and circular-face ellipse ratios;
- dimension lines, extension lines and units;
- scale declarations;
- graph keys, legends and category labels;
- leader-line collision avoidance;
- context-object measurement points;
- marking-overlay construction lines.

Whole-shape identifiers remain lowercase and centred inside the shape unless that placement impedes solving. Vertex labels remain capital letters outside vertices, with correspondence and prime notation preserved.

## Layout integration

Visuals are placed as part of the question composition, not added after text layout.

Requirements:

- reserve the diagram and response regions before final text placement;
- keep related prose, labels and representations spatially integrated;
- give required diagrams visual priority on Pages 2 and 3;
- keep Q1-Q6 visuals large enough to interpret within the six-cell grid;
- avoid excessive blank space caused by undersized diagrams;
- avoid crowding caused by unnecessary diagrams;
- place dimensions beside their corresponding features;
- preserve adequate pencil-working clearance around response surfaces;
- use a natural table only when table interpretation is part of the mathematics.

## Marking-key behaviour

The marking key is generated from the completed student test.

- Every student visual and its placement remain unchanged.
- Solutions are added as `marking_overlay` elements in the approved blue.
- Overlay line style, labels or symbols must provide a non-colour distinction.
- Construction work is placed on the original response surface where practical.
- Teacher annotations must not obscure task information or shrink the student diagram.
- Test/key visual identity is checked structurally and through rendered comparison.

## Age calibration

The visual language remains stable across year levels; complexity changes rather than quality.

### Pre-primary to Year 1

- large concrete representations;
- low element count;
- familiar objects and strong separation;
- minimal labels;
- generous response surfaces.

### Years 2 to 4

- transition between concrete and abstract representations;
- familiar contexts paired with conventional diagrams;
- increasing use of scales, partitions and labels;
- restrained contextual illustration.

### Years 5 to 7

- greater abstraction and information density where mathematically justified;
- formal notation, coordinate systems and composite diagrams;
- natural data displays and multi-constraint situations;
- no unnecessary childish styling.

Age calibration must not change the mathematical meaning or introduce decorative complexity.

## Accessibility and print safety

Every released visual must:

- remain interpretable in greyscale;
- avoid colour-only distinctions;
- meet the profile's contrast thresholds;
- use labels that meet A4 print minimums;
- avoid visually dense textures and low-contrast shading;
- remain clear after ordinary photocopying;
- preserve aspect ratio;
- avoid raster enlargement beyond its validated resolution;
- use alternative cues for students with colour-vision differences;
- avoid relying on minute spatial differences that printing may obscure.

## Proof artefacts

Implementation should create two types of approved proof artefact.

### Asset proof sheets

A4 pages showing:

- canonical assets at normal and minimum permitted size;
- annotation and label conventions;
- solid projection and face treatments;
- colour and greyscale rendering;
- correct and rejected examples.

### Complete problem-page proofs

Full assessment-page prototypes showing:

- a contextual illustration integrated with prose;
- a scale or measurement diagram;
- a natural graph, table or timetable;
- a problem with a purposeful response surface;
- a complex problem for which no visual is the correct choice;
- corresponding marking-key overlays.

These pages validate visual reasoning and page composition, not only asset quality.

## Validation architecture

Validation operates at four levels.

### 1. Source and licence validation

- asset provenance is recorded;
- bundled assets are original, user-owned or compatible with distribution;
- personal-licence and assessment-source illustrations are never copied into the repository;
- externally sourced assets have required attribution.

### 2. Asset validation

- SVG parses successfully;
- geometry properties match the manifest;
- view box, padding, fill, stroke and aspect ratio match the token set;
- canonical assets contain no unexpected text, gradients, shadows or embedded raster images;
- PNG fallback dimensions and alpha channel are correct;
- asset hash matches the manifest.

### 3. Specification and semantic validation

- every visual has a valid family and purpose;
- the information role and removal effect are explicit;
- scale status is declared;
- Q7/Q8 visuals pass the demand-preservation check;
- representationally expected questions either include a purposeful visual or record a defensible omission reason;
- no contextual illustration is accepted solely as decoration.

### 4. Rendered-package validation

- required visuals meet minimum printed dimensions;
- labels do not collide with edges, points, dimensions or working areas;
- grids remain subordinate to the task object;
- no asset is distorted, blurry or clipped;
- greyscale rendering preserves all answer-critical distinctions;
- the page has balanced information density and sufficient working space;
- student test and marking key retain visual identity;
- the package is compared with approved asset and complete-page exemplars.

Automated success supplies evidence but does not replace independent pedagogical and visual review.

## Release barriers

The following are mandatory release barriers:

- inaccurate or distorted mathematical geometry;
- incorrect, ambiguous, colliding or undersized labels;
- blurry or under-resolution raster assets;
- unjustified decorative visuals;
- a visual that reveals or sequences the intended solution method;
- a visual that pre-organises Q7/Q8 prose into a solution-ready structure;
- a visual whose apparent scale contradicts the problem without a declaration;
- colour-dependent mathematical information;
- inconsistent representations of the same object without a mathematical reason;
- grids or backgrounds that overpower the mathematical content;
- unnecessary hidden edges or misleading 3D perspective;
- a marking overlay that changes or obscures the student assessment;
- mismatch between prose, diagram, answers and rationale;
- unrecorded asset provenance or incompatible licensing;
- failure of asset, semantic, greyscale, structural or rendered-page checks.

There is no advisory-only visual defect class.

## Repository integration

The implementation plan should make targeted changes to the existing v3.4 structure.

Proposed additions:

- `standards/visual-standard.md`;
- `references/contextual-illustration-standard.md`;
- expansion of `references/mathematical-diagram-conventions.md`;
- `assets/visual-tokens/assessment-visual-tokens-v1.json`;
- `assets/maths-visuals/v1/` for authoritative SVG and PNG assets;
- `assets/maths-visuals/v1/manifest.json`;
- proof sheets and complete-page visual exemplars under `assets/visual-benchmarks/`;
- schema extensions for `visual-profile` and `question.visual_spec`;
- asset, semantic and rendered-output validators;
- positive and negative regression fixtures;
- agent instructions linking question design, document construction and release QA to the new standard.

Existing `classic-assessment-v1.json` remains the default profile but gains a versioned reference to the new token and asset systems. Existing benchmark decks remain scoped exemplars.

## Agent responsibilities

### Assessment Blueprint Agent

- decides whether a visual is expected;
- records its family, role and accessibility purpose;
- prevents visual requirements from being added merely for decoration.

### Question Designer

- defines the information the visual carries;
- keeps text and visual information consistent;
- avoids strategy-revealing organisation.

### Complex Problem Specialist

- applies the Q7/Q8 demand-preservation check;
- ensures supporting displays are natural mathematical evidence;
- maintains Q7/Q8 independence.

### Maths Pedagogy Validator

- verifies mathematical accuracy, representation choice, age suitability and cognitive demand;
- treats any required correction as a content barrier.

### Document Builder

- resolves tokens and assets;
- uses the construction hierarchy;
- integrates diagrams before final page composition;
- records asset IDs, hashes, constructors, scale status and print dimensions in the design manifest.

### Independent Release QA

- inspects the rendered test, key and rationale;
- checks positive visual evidence rather than relying on absence of overflow;
- validates greyscale safety, purpose, demand preservation, asset integrity and test/key fidelity;
- releases only with zero barriers.

## Test strategy

### Contract tests

- visual profile references valid token and asset versions;
- every manifest asset conforms to schema;
- every declared asset path and hash resolves;
- required agent and standard links are present.

### Geometry tests

- canonical square sides are equal and angles are right angles;
- canonical circle uses equal radii;
- equilateral-triangle sides are equal within deterministic tolerance;
- solid and net components match their declared properties;
- transformations preserve declared vertex correspondence.

### Semantic fixtures

Positive fixtures:

- necessary exact diagram;
- natural data display;
- contextual illustration that reduces language load;
- justified no-visual complex problem;
- Q7/Q8 visual that preserves reasoning demand.

Negative fixtures:

- decorative clip art;
- solution-ready Q8 table;
- colour-only categories;
- distorted shape;
- unlabelled scale diagram;
- strategy-revealing arrows;
- undersized or low-resolution image;
- unlicensed copied illustration;
- marking key with moved or replaced student visual.

### Visual regression

- render proof assets at normal and minimum print size;
- render in colour and greyscale;
- compare stable regions with approved baselines;
- require human inspection for purposeful layout, visual hierarchy and age appropriateness;
- pilot the standard against transformations, volume/capacity and one early-years assessment.

## Rollout

### Increment 1: foundation and proof set

- add standard, tokens, schemas and manifest;
- add the approved square, circle and equilateral triangle;
- add the remaining small proof set;
- add semantic and asset validators;
- create asset and page-level proof artefacts.

### Increment 2: assessment integration

- update agent contracts and pipeline hand-offs;
- extend the design manifest and package audit;
- add Q7/Q8 demand-preservation validation;
- run the three pilot assessments.

### Increment 3: catalogue expansion

- add visual families required across Pre-primary to Year 7;
- add constructors for repeated diagrams;
- add further page-level benchmarks by curriculum domain;
- version all additions without silently changing established assets.

## Acceptance criteria

The design is successfully implemented when:

1. the standard is authoritative and linked by every relevant agent;
2. the default visual profile resolves a versioned token set and asset manifest;
3. the proof assets pass deterministic geometry and rendering checks;
4. Q7/Q8 visual purpose and demand preservation are validated explicitly;
5. complete-page proof artefacts demonstrate both exact and contextual modes;
6. student pages remain clear in colour, greyscale and 100%-scale A4 renders;
7. marking overlays preserve the test layout and remain distinguishable without colour alone;
8. negative regression fixtures fail for the intended reason;
9. transformations, volume/capacity and early-years pilots pass independent release QA with zero barriers;
10. none of the protected reference-source artwork is included in distributable skill assets.

## Decisions fixed by this design

- Use the executable-system approach rather than a prose-only guide or asset-only library.
- Use two coordinated visual modes: exact mathematical and contextual problem-solving.
- Treat visual purpose and demand preservation as content concerns.
- Keep Q7 and Q8 independent even though main and extension cards calibrate their respective demand.
- Use original, distributable assets and derive only principles from protected references.
- Extend the existing v3.4 profile architecture rather than create a competing visual system.
- Validate complete assessment pages as well as individual assets.
- Expand the catalogue incrementally after a representative proof set passes.
