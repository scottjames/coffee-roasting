
# Coffee Color

notes about measuring color and different color scales used.

## Color Scale

Artisan 4.0 supports four different color scale systems.

### Tonino

### ColorTest

### Colorette

### ColorTrack

### Agtron

ChatGTP compare/contrast:

These five scales are not interchangeable, even though all are intended to quantify coffee roast color.
The biggest source of confusion is that some scales run higher = lighter, while ColorTrack
runs higher = darker, and the instruments use different optical methods and sample preparation.

| Scale / system     | Typical range | Higher number means | Measurement method               | Typical sample       | Best use                          |
| ------------------ | ------------: | ------------------- | -------------------------------- | -------------------- | --------------------------------- |
| **Agtron Gourmet** |         0–100 | Lighter             | Spectroscopic/NIR reflectance    | Ground coffee        | Industry/SCA reference            |
| **Tonino**         |        50–130 | Lighter             | 64-channel true-color reflection | Ground coffee        | Small roaster, easy repeatability |
| **ColorTest II**   |         0–200 | Lighter             | Monochromatic reflectance        | Ground coffee        | Industrial QC                     |
| **Colorette**      |         0–200 | Lighter             | Red + near-IR reflectance        | Ground coffee        | Industrial QC                     |
| **ColorTrack**     |         ~0–80 | **Darker**          | 780-nm laser reflectometry       | Whole bean or ground | Roasting process control          |

The published literature specifically cautions that a reading such as Agtron 40 cannot simply be assumed to equal 40 on another instrument; the scales are instrument-specific



1. Agtron

Agtron is the closest thing to the industry reference scale.

The important distinction is that there are multiple Agtron scales, particularly:

Agtron Gourmet — approximately 0–100
Agtron Commercial — approximately 0–75

For the Gourmet scale:

Higher = lighter roast

So approximately:

70–80 → light
60–70 → medium-light
50–60 → medium
40–50 → medium-dark
30–40 → dark
20–30 → very dark

The SCA roast-color system is historically tied to Agtron, which is one reason Agtron values appear so frequently in roasting literature and cupping standards.

Important limitation

Agtron is not just a "color number." It is the output of a particular optical measurement system. Consequently:

Agtron 60 ≠ necessarily Tonino 60 ≠ Colorette 60.

That's one of the most important points when comparing meters.

2. Tonino

Tonino is probably the most interesting system for a small/specialty roaster.

It uses a 64-channel true-color photodetector and four full-spectrum white LEDs. It measures reflected light from a relatively small sample of finely ground coffee.

Its scale is approximately:

50–130

with:

Higher = lighter

Tonino publishes an approximate conversion to Agtron Gourmet:

Tonino	Approx. Agtron	Roast
125–130	80–90	Very light
115–125	70–80	Light
100–115	60–70	Medium-light
85–100	50–60	Medium
75–85	40–50	Medium-dark
60–75	30–40	Dark
50–60	20–30	Extremely dark

However, Tonino itself explicitly warns that this Agtron conversion is an approximation, based on a limited set of samples.

Tonino's major advantage

It is inexpensive and convenient compared with laboratory instruments, while giving you a continuous numerical measurement.

For home/small-batch roasting, that is a big advantage.

It also supports custom scales, so you can define your own roast targets.

3. ColorTest II

ColorTest is the Neuhaus Neotec system.

This one is considerably older and more industrial than Tonino.

The ColorTest II uses:

monochromatic illumination
a semiconductor light source
reflected-light measurement
averaging of many measurements

rather than attempting to reproduce human-visible color directly.

Its scale is:

0–200

where:

0 = black / very dark
200 = white / very light

So again:

higher = lighter

A published description of the Neuhaus Colortest scale explicitly defines it as a linear 0–200 scale from black to white.

Why ColorTest can look strange compared with Agtron

A medium roast might have a ColorTest number around 100 while the corresponding Agtron value might be around 60.

The numerical values therefore aren't intended to be directly compared.

4. Colorette

Colorette is the PROBAT system.

It is also fundamentally an industrial QC instrument.

PROBAT specifies:

Colorette scale: 0–200
CIELAB L*a*b*
user-defined scales
approximately ±1% accuracy on its Colorette scale.

The interesting thing about Colorette is that it gives you more than just its proprietary roast number.

It can provide:

Colorette → L*a*b*

That makes it potentially more useful if you're doing your own color analysis.

Published research reports Colorette values decreasing as coffee becomes darker, with commercial coffee commonly occupying approximately 60–150, depending on the coffee and measurement conditions.

Again:

higher = lighter

5. ColorTrack

ColorTrack is the odd one out.

Its number goes in the opposite direction:

Higher ColorTrack = darker coffee

The current ColorTrack system uses 780-nm laser reflectometry. Loring specifies a measurement range of 0–80, with most coffees falling approximately between 30 and 75. It can measure whole beans or ground coffee.

For example, one published ColorTrack reference chart gives approximately:

ColorTrack	Approx. Agtron	General interpretation
15	80	Very light
30	60–70	Light/medium-light
50	50–55	Medium
60	40–45	Medium-dark
65	35–40	Dark
70	30–35	Dark
75	25–30	Very dark
80	15–25	Extremely dark

That makes ColorTrack particularly useful for roasting process control, because the system is designed around measuring many points across the coffee sample. The manufacturer describes its laser module as collecting roughly 10,000 readings during a one-second scan.

The really important difference: what they're actually measuring

This is where comparing the scales gets more interesting.

#### Tonino

Visible-spectrum reflection

64-channel true-color sensor + white LEDs.

It is relatively close to measuring the actual optical color of the coffee.

#### ColorTest

Monochromatic reflected light

It isn't trying to reproduce human color perception. It's measuring reflected optical energy and mapping that to its proprietary scale.

#### Colorette

Red + near-infrared reflection

It has a roast-color-specific optical response and can additionally provide CIELAB values.

#### ColorTrack

780-nm laser reflectometry

Very narrow optical measurement with a laser, specifically optimized for roasted coffee.

#### Agtron

Spectroscopic/NIR reflectance

Agtron's system is particularly interesting because it is intended to relate optical response to chemical changes associated with roasting rather than simply asking "what RGB color does this coffee look like?"

Why two meters can disagree

This is extremely important if you're trying to establish roast targets.

Imagine you roast a batch and get:

Tonino = 95

You cannot automatically conclude:

Agtron = 55

even if a conversion table says something approximately like that.

There are several variables:

- Wavelength
- Illumination geometry
- Sensor technology
- Whole bean vs. ground coffee
- Grind size
- Sample packing
- Bean density
- Origin
- Roast development
- Surface vs. interior roast color

ColorTrack, for example, specifically samples the physical coffee surface, while ground-coffee instruments expose a much larger cross-section of the bean.

This is why published cross-meter conversions should be considered calibration relationships, not mathematical conversions.

The SCA/CoffeeMind comparison is a good illustration: one particular study found approximately:

±4 Agtron Gourmet ≈ ±4.5 Tonino ≈ ±1.5 ColorTrack

but the authors explicitly noted that the comparison was based on only one coffee and was not exhaustive.

A useful way to think about the scales

If your goal is roasting consistency, I'd group them like this:

Tier 1 — Industry/reference language

#### Agtron

Best when you want to communicate:

"This coffee is Agtron 62."

That number has the greatest recognition among professional roasters, researchers and SCA-related material.

Tier 2 — Practical small-roaster measurement

#### Tonino

Excellent if you want:

"My espresso blend should always be Tonino 92–95."

It's compact, inexpensive relative to industrial instruments, and easy to use repeatedly.

Tier 3 — Industrial QC

#### ColorTest / Colorette

Excellent for production environments where color measurement is part of formal quality control.

Tier 4 — Automated roasting/process control

#### ColorTrack

Particularly interesting if you want to integrate color measurement into the roasting process itself rather than simply check the finished batch.

One major issue for your application

Given that you're using Artisan + a small 500-g-class roaster, I would not recommend trying to convert every roast into an absolute "Agtron equivalent" unless you have a reason to.

A much better approach is:

Pick one instrument → establish your own target numbers → use those numbers consistently.

For example:

| Roast target | Tonino example | ColorTrack example |
| ------------ | -------------: | -----------------: |
| Light        |            110 |                ~30 |
| Medium-light |            103 |                ~40 |
| Medium       |             93 |                ~50 |
| Medium-dark  |             82 |                ~60 |
| Dark         |             70 |                ~70 |


Those are illustrative starting points, not universal conversions.

The most useful measurement for your roaster would actually be something like:

"This particular bean tastes best at Tonino 91 ± 2."

rather than:

"I need to achieve Agtron 58."

Color is an excellent repeatability metric, but it doesn't uniquely determine flavor. Two coffees can reach the same color through different time/temperature profiles and have different internal physical and chemical development. ColorTrack's own technical material makes essentially this point.



#### For your Artisan setup

If your ultimate goal is to correlate roast profile → final color → flavor, I would favor Tonino over trying to reproduce Agtron numerically.

You could record in Artisan:

Bean: Ethiopia ...
Charge: ...
FC: ...
Drop: ...
DTR: ...
Weight loss: ...
Tonino: 94

After 10–20 roasts of the same bean, you can start building a very useful relationship between Tonino color, weight loss, FC timing, development time, and cup results.

That would be considerably more useful for dialing in your Skywalker than treating the Agtron scale as an absolute roast endpoint.

