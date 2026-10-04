<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Surfable item production contract

## Required domains

| Domain | Required content |
|---|---|
| Physical | dimensions, dry/saturated mass, construction, materials, center of mass, inertia, strength |
| Water | displacement, waterline, buoyancy regions, planing surfaces, drag axes, edge behavior, absorption |
| Control | pitch/roll/yaw authority, propulsion or tow behavior, assist limits, failure/recovery |
| Rider | rider, seat/stand, hand, foot, leash, tow, propulsion, camera, VFX and audio sockets as applicable |
| Asset | hero mesh, mobile-aware LODs, collision proxies, UVs, materials, moving/breakable parts |
| States | dry, wet, soaked, damaged, foam-contact, plus object-specific powered or flooded states |
| Runtime | named regions, hydrodynamics metadata, engine export, performance budgets |
| QA | scale, turntable, collision, waterline, buoyancy, planing, steering, crash, damage, performance |

## Metadata minimum

```json
{
  "asset_id": "three_seat_couch",
  "mass_dry_kg": 92,
  "mass_saturated_kg_range": [115, 160],
  "water_absorption_rate": 0.018,
  "flexibility": 0.21,
  "planing_surfaces": ["underside_main"],
  "buoyancy_regions": ["left_cushion", "center_cushion", "right_cushion", "back_frame"],
  "drag": {"longitudinal": 0.68, "lateral": 0.91},
  "control_authority": {"pitch": 0.34, "roll": 0.22, "yaw": 0.16},
  "assist_limits": {"stability": 0.28, "wave_face_attraction": 0.12, "self_righting": 0.08}
}
```

## Category adjustments

- Deformables: specify lattice/skeletal deformation, fold limits, damping, rebound, and permanent damage.
- Powered boards/craft: specify thrust curve, steering pivot, intake, exhaust, fuel/energy, cooling, failure, spray, and audio.
- Boats: specify hull compartments, flooding, passenger sockets, trim, capsize, and propulsion damage.
- Tow-in: specify rope tension, release timing, attachment failure, driver/rider coordination, and high-speed entry.
- Body surfing: replace asset mesh requirements with character pose, contact surfaces, breath, fatigue, injury, and wave-force tuning.
