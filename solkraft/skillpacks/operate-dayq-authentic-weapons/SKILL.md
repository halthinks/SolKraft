---
name: operate-dayq-authentic-weapons
description: Implement DayQ physical weapon handling, ammunition, ballistics, malfunctions, and persistent firearm state.
---

# Operate DayQ Authentic Weapons

Read [FULL_CONTRACT.md](references/FULL_CONTRACT.md) and [INTEGRATION.md](references/INTEGRATION.md). Create original DayQ gunplay from measurable behavioral targets; never copy DayZ/Arma code, assets, tuning, UI, audio, animations, or protected designs.

1. Preserve existing weapon/item identity, inventory, combat/damage/wounds, acoustic, armor, movement, exo/mech, authority, and persistence owners.
2. Keep a project-owned `IBallisticsBackend`-style boundary and internal solver. Do not import BulletForge, EasyBallistics, Terminal Ballistics, or their types; the separate bakeoff owns adoption.
3. Model physical component/action/ammunition/condition state, interruption, mass/inertia/envelope/support, causal recoil/sway, projectile/material response, sound/suppression, maintenance, and failure.
4. Server-authorize configuration, firing, chamber/feed, projectile/impact, damage, ammo, repairs, transactions, and persistence; prediction never grants hits or ammunition.
5. Build rifle/handgun/manual-action prototype with multiple ammunition, optics/suppressor, cover/materials/armor/wounds, AI hearing, two clients, latency/loss, persistence/restart, performance, exploit, accessibility, and regression evidence.
