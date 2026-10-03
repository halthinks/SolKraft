# Character Rig and Collision Contract

Require:

- stable skeleton, body-profile and physics-profile IDs with versions;
- real-world units, root orientation, pelvis height range and supported proportion bands;
- deform hierarchy, IK/weapon/helper bones and retarget chains;
- sockets for hands, back, belt, chest, head, feet, weapon support, packs, armor, medical interactions, ropes and exoskeleton interfaces;
- gameplay regions for head/neck, thorax, abdomen/pelvis, upper/lower arms, hands, upper/lower legs and feet, with explicit health-owner mapping;
- movement capsule and stance capsules independent from visual mesh;
- query shapes for hits and contacts, plus Physics Asset bodies and constraints for reactions/ragdoll;
- material/coverage mapping for skin, clothing, armor and equipment;
- skin weights, twist behavior, corrective shapes and extreme-pose acceptance;
- first-person and third-person parity without duplicated inventory or damage state;
- LOD/crowd physics and animation budgets;
- Blender/Unreal import, retarget, socket, collision and pose conformance tests.

Reject bodies whose proportions, collision, skeleton or sockets silently change gameplay capability.
