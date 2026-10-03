# DayQ ballistics adapter contract

Create a project-owned `IBallisticsBackend` or equivalent following actual DayQ naming conventions.

The boundary accepts versioned, vendor-neutral values for:

- shot authorization ID;
- weapon and barrel state reference;
- ammunition definition and unique cartridge/chamber mutation reference;
- authoritative muzzle transform and timestamp;
- shooter/owner identity;
- environment sample;
- projectile definition;
- collision/material query interface;
- server tick and rewind context;
- debug/evidence sink.

It returns vendor-neutral events for:

- projectile state samples;
- impact time and transform;
- material/layer interaction;
- retained energy/momentum abstractions;
- ricochet/penetration/stop/continuation;
- suppression and acoustic scheduling hooks;
- terminal damage inputs;
- correction and validation results;
- deterministic evidence identifiers.

Candidate objects, enums, structs, assets, and serialization must not cross the boundary. DayQ owns persistent weapon, ammunition, chamber, magazine, damage, wound, material, inventory, and journal state.

Use one adapter per candidate plus an internal control. Prove hot replacement at build/configuration time and migration-free removal from saved state.
