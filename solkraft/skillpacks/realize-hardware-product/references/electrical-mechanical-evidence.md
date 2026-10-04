<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Electrical and mechanical evidence checklist

## PCB and high-speed interfaces

- Use manufacturer land patterns and connector STEP at the stated revision.
- Record stack-up, copper weight, finish, impedance targets, reference planes,
  via strategy, pair spacing, length/skew limits, and return-path transitions.
- Model connector bodies, latch travel, mating/unmating direction, cable exit,
  flex stiffener, installed bend radius, and tool/finger access.
- Report unrouted nets, DRC exclusions, unverified footprints, SI/PI status, and
  reference-design deviations independently.

## Batteries and source sharing

- A cell datasheet is not a protected pack specification.
- Define cell count/topology, qualified assembler, matched lot, insulation,
  spacing, compression/swell allowance, fuse, protector/gauge, charge control,
  thermistors, FETs, current/voltage thresholds, connector, harness, and label.
- Never tie raw packs directly together. Each source needs fault isolation and a
  controlled power path before sharing. Define hot-plug, inrush, reverse current,
  pack removal, one-source/two-source behavior, reserve priority, and telemetry.
- Derate contacts by installed temperature rise and unequal-current sensitivity;
  do not simply multiply catalog maximum current by contact count.

## Blind-mate contacts and mechanisms

- Define guiding features before electrical engagement, working travel,
  tolerance accumulation, wipe, spring force, last-mate/first-break sequencing,
  anti-short barriers, drainage, contamination control, target plating, cycle
  life, current derating, and service replacement.
- The latch carries mechanical pullout; contacts must not be retention members.
- Record latch material, spring, pivot, stops, capture, glove actuation, accidental
  release guard, and load cases.

## Sealing and thermal paths

- State the target, not an untested IP rating. Define gasket material, cross
  section, squeeze, gland fill, corners, fasteners/spacing, surfaces, vent, drain,
  cable/shaft seals, and service replacement.
- Use a complete junction-to-ambient thermal path for each major load. Include
  TIM thickness/compression, spreader, structural conduction, enclosure surface,
  solar/still-air/user-contact conditions, sensors, throttling, and safe shutdown.
- Vents do not replace a heat path. Sealed conduction designs still need pressure
  equalization and condensation/drain strategy.

## Collision and balance

- Label host, hand/glove, optic, magazine, accessory, cable, control, service,
  optical, and RF fixtures separately.
- AABB checks are early screening; final release uses solid/mesh interference and
  representative physical fixtures.
- Record whether each mass is manufacturer nominal, weighed, CAD-material,
  estimated, or allowance. Report CG in the product datum and the mounted host
  datum; include sensitivity for high-uncertainty masses.
