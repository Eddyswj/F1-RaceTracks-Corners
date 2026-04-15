# Model’s key visual signals

1. **Track geometry**
- Corner sequences (S-curves, chicanes)
- Elevation changes (Spa is unique here)
- Corner radius (tight vs flowing)
  1. Action:
    - Include aerial + wide-angle shots
    - Do NOT rely only on onboard views

2. **Kerbs and run-off areas**
- Kerb colours (very distinctive)
- Runoff patterns (Paul Ricard is extreme)
- Painted asphalt
  1. Action:
    - Ensure kerbs are visible in many samples
    - Include close-up and mid-range shots

3. **Surroundings / environment**
- City vs forest vs desert
- Buildings, barriers, lighting
- Night vs day races
  1. Action:
    - Include environment, but do not rely on it alone
    - Avoid dataset bias (e.g. “night = Singapore only”)

4. **Track surface & colour tone**
- Some tracks look darker/lighter
- Asphalt texture differs
- Painted sponsor logos
  1. Action:
    - Include multiple lighting conditions to avoid overfitting

---
## Mistakes to take note not to do. 

1. Cars
  - Different teams, colours, liveries
  - Completely irrelevant to the track
  1. Fix:
    - Include images with different cars or no cars at all

2. Weather / lighting shortcuts
  - “Night = Singapore”
  - “Bright desert = Bahrain”
  1. Fix:
    - Add counterexamples (e.g. sunset, cloudy, rain but with good visibility of the track)

3. Track and corners
  - Spa = only Eau Rouge
  - Monza = only Parabolica
  - Long straights (look identical globally)
  - Tight close-ups (no context)
  1. Fix:
    - Cover entire track layouts

