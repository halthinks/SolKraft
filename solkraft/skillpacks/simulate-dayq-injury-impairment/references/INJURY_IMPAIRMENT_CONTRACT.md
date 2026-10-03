# Injury and Impairment Contract

Persist stable survivor/body ID, region, tissue-trauma band, bleeding rate, fracture state, pain, shock, consciousness, infection/contamination links, treatment, healing state and revision.

Project bounded values for:

- left/right leg support and propulsion;
- left/right arm reach, grip and weapon support;
- torso stability and breathing;
- head/neurological awareness and balance;
- overall blood-loss, shock, pain and consciousness constraints.

Movement consumes capability outputs; it does not inspect wound internals. Weapons consume grip/support/sway/reaction outputs. Traversal consumes grip, limb mobility, balance and consciousness. Animation consumes presentation tags and magnitudes. Exos consume fit/contact/pain and support requests.

Test single and combined injuries, treatment interruption, load, weather, fatigue, falls, weapon use, climbing, dragging, exoskeleton assistance, incapacity, disconnect, restart, migration and death/body transfer.
