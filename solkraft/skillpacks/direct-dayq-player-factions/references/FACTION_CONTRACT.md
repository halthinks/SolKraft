# DayQ player-origin contract

## Canon identities

| Origin ID | Canon name | Native trees | Player fantasy |
|---|---|---|---|
| `origin.warforge` | The Warforge Clans | Gunsmith, Dronewright, Ironmaker, Machine Hunter | Build and weaponize things |
| `origin.ash_hounds` | The Ash Hounds | Stalker, Climber, Outrider, Raider | Move, hunt, climb, ambush |
| `origin.bastion` | The Bastion Directorate | Bulwark, Combat Medic, Siegehand, Heavy Support | Hold ground and keep squads alive |
| `origin.ghostwire` | The Ghostwire Cells | Drone Commander, Signal Hunter, Intruder, War Companion | Control information, drones, and hostile systems |

Origin is chosen cultural training and history. It is permanent for the character and is not biological. Current clan, alliances, employers, reputation, and ideology may change without changing origin.

## Canon progression boundary

- T0 is the shared survivor baseline.
- Every character can see and train all sixteen trees through T5.
- Creation sets the four native trees to T1 and the other twelve to T0.
- Every character can cross-train every tree through T5.
- T6 is native-only, requires T5 plus a major origin mastery trial and physical requirements, and is never needed for a core action or required objective.
- Foreign T6 must not be sent as a locked node. The client receives no ID, name, icon, description, prerequisite, silhouette, localization key, asset reference, or discovery hint.
- Defection, clan transfer, manuals, trainers, agents, captured data, respecialization, rollback, migration, or forged requests cannot reveal or grant foreign T6.

## T6 registry

- Warforge: Black Forge, Machine Legion, Dreadplate, Dead Factory.
- Ash Hounds: Bloodtrail, No Ground, Beyond the Wire, Smoke Eater.
- Bastion: Last Wall, Death Denied, Citadel Seed, Siegebreaker.
- Ghostwire: Ghost Armada, Spectrum Dominion, Quantum Breach, Ghost in the Armor.

## Integration

Use stable IDs instead of display text. The server owns origin selection and authorizes native projections. The reputation system consumes origin context but owns relationship changes. Inventory resolves starter-package class grants transactionally. Progression consumes the native-tree map. Death/persistence determines which learned state survives death; this contract does not override that policy.

An ability node may grant only a bounded capability tag or recipe understood by the authoritative owner. It cannot mutate weapons, health, inventory, drones, agents, cyber targets, exos, mechs, or buildings directly.
