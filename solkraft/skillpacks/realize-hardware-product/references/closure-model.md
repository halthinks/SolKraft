<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Closure model and claim boundary

## Evidence classes

| Code | Evidence | May support | Must not be called |
|---|---|---|---|
| `REQ` | User/product/software requirement | required behavior, envelope driver | selected hardware or proof |
| `MFR` | Manufacturer page, drawing, datasheet, CAD | nominal identity, interface, dimensions, ratings | received or installed measurement |
| `RCV` | Recorded inspection of a received serialized/lot sample | as-received dimensions, mass, revision | assembled performance |
| `CALC` | Reproducible calculation with inputs | predicted load, runtime, CG, stress/thermal estimate | measured performance |
| `CAD` | Checked assembly/PCB model | digital fit, route and keep-out status | physical fit or endurance |
| `TEST` | Recorded test on identified hardware | the tested result under stated conditions | broader untested conditions |

Every quantitative field in a realization package should identify one of these
classes or be explicitly `UNKNOWN`.

## Promotion rules

### SOURCE_BOUND

Critical purchased components must have:

- manufacturer and exact model/order identity, or a named procurement hold;
- controlled URL and document/CAD revision or access date;
- interface and nominal envelope evidence;
- lifecycle/availability status and an order path;
- conflicts and unverified assumptions recorded.

### DIGITAL_CLOSED

In addition to `SOURCE_BOUND`:

- all parts have positioned geometry in a single datum system;
- custom parts are dimensioned and exported;
- interfaces and connector orientations agree;
- PCB outline, placement, routing status, and keep-outs are released at the
  stated level;
- cable/flex bends and assembly/service paths are modeled;
- collision and balance studies are reproducible;
- thermal and power paths are complete calculations with limits;
- unresolved items cannot invalidate the current envelope.

### FIRST_ARTICLE_READY

In addition to `DIGITAL_CLOSED`:

- fabrication and purchasing outputs are revision-controlled;
- incoming inspection limits and deviation flow exist;
- assembly work instructions and tooling are defined;
- bring-up and acceptance tests include methods, conditions, limits, equipment,
  raw artifact paths, and disposition rules;
- any regulatory or supplier qualification hold is explicit.

### PHYSICALLY_VERIFIED

In addition to `FIRST_ARTICLE_READY`:

- actual sample/article IDs and revisions are recorded;
- required inspection/test rows are executed with dates and operators;
- instruments and calibration state are identified;
- raw evidence exists and is hash-bound where practical;
- failures/deviations have disposition and retest evidence;
- measured mass, CG/balance, thermal, runtime, fit, and retention are reported
  only for the configurations actually tested.

## Claim language

Prefer:

- “supplier nominal envelope” for datasheet/STEP geometry;
- “calculated” or “predicted” for analytical results;
- “digital interference check passed” for CAD results;
- “first-article test pending” for unexecuted validation;
- “measured on article GS-R09-EVT-001 under test GS-…” for physical proof.

Reject phrases such as “fully solved,” “production ready,” “validated hardware,”
or “measured balance” unless the manifest evidence actually supports them.
