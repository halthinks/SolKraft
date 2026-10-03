# Ground Locomotion Contract

## States

Support standing, crouched, prone, walking, jogging, sprinting, strafing, backpedaling, falling, landing, stumbling, swimming/wading where adopted, dragging, assisted carry and incapacitated transitions.

## Authoritative inputs

Desired direction/speed; stance; facing/aim relationship; slope and surface; traction; gravity; wind; supported and unsupported mass; load offsets/bulk; stamina/fatigue; pain; limb mobility; footwear/clothing restriction; hands; weapon support; exoskeleton assistance; collisions and moving base.

## Outputs

Actual acceleration, speed, velocity, rotation, capsule/stance, jump/step capability, turn rate, braking, noise, exertion, stumble risk, transition permission and reason codes.

## Required curves

- acceleration/braking versus stance, direction and load;
- speed and turn response versus unsupported mass and injury;
- stamina use/recovery versus gait, grade, temperature and assistance;
- jump/step/landing envelope versus load, fatigue and limb state;
- traction and slip versus surface, footwear, precipitation and slope;
- weapon-ready movement versus supported mass and hand occupancy.

## Network gates

Run 0/50/100/200 ms RTT with jitter/loss, input reordering, time manipulation, impossible acceleration, stance collision abuse, moving surfaces, knockback, disconnect and late join. Record correction frequency/magnitude, bandwidth and server cost.
