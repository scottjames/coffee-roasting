
# coffee notes on development


 - https://shungrill.com/article/how-long-to-roast-coffee-development

 - longer development makes more bitterness, bigger/stronger flavor.
 - sugars burn 210-220c making bitter notes

 - average roast time is 12:00 minutes. can range 8:00 to 20:00.

 - grassy/hay flavors: to short roast time, or need longer devel time. 
 - kenya is high acid, may *seem* under developed due to acid taste.

 - Underdevelopment occurs when a bean has not been thoroughly roasted,
   leading to grassy and hay-like flavours.
 - Overdevelopment, can result in a burnt-sugar bitterness.

 - https://oilslickcoffee.com/roasting/ways-to-achieve-flavor-complexity/

 - In general; low and slow produces a smaller difference between ground
   and whole-bean color and hot and fast produces a larger difference between
   ground and whole-bean color.
 - lighter/brighter cup, we should ensure our roast is hot and fast...
   to preserve more of the brighter flavors still present in the
   less-cooked center of the bean.
 - For a darker/heavier cup, slow things down and spend more time in
   the Maillard’s sweet spot (~150°-190°C), to generate more caramelly,
   malty, nutty flavors
 - For a complex, light/bright coffee: roast hotter and faster
 - For a complex, dark/heavy coffee: roast slower and lower


https://chatgpt.com/share/68ba421b-fd20-800b-9ff2-589d5f38f90c


## Notes on DTR

 - https://millcityroasters.com/blogs/coffee-articles/whats-the-best-development-time-dtr-and-finish-temperature

 - Dry (when T < 150c) (aim for < 50% of time)
 - Browning, between DE and FCS. (around 150c - 175c)
 - Development - After FCS, aim for 20% - 25% time
 - At around 190c acids break down rapidly. (Darker roasts are less acidic)
 - DTR: 50 / 30 / 20 => 5 min, 3 min, 2 min (10 min duration)
 - DTR: 50 / 33 / 17 => 6 min, 4 min, 2 min (12 min duration)

 - Finish temp is 70% of flavor, determines color.
 - color shows DROP temp. partial indicator of flavor.

"""
Your finish temp is the point of greatest velocity of chemical change in the coffee. Successfully hitting your roast flavor target means discharging the coffee into the cooling tray at the exact instant your inner and outer seed development best contributes to your choice of flavor in the cup.

It's not catching a speeding bullet. It’s catching an accelerating bullet.
"""

## Crash and Flick

 - https://www.beanscenemag.com.au/cropster-adds-flick-prediction-to-its-ai-roasting-program/
 - software cropster.com added AI prediction for "crash and flick" after FCS.
 - it's the 'flick' causing Roasty flavors, not high DTR.

## Rob Hoos on Roasting
 - Rob Hoos -- https://www.youtube.com/watch?v=GaxiRQ5BxWs
 - Coffee is the business of Flavor. Keep it consistent and good.
 - Moisture requires more energy to crack. (11-12% is high)
 - Low Alt has more Tipping vs High Altitude.
 - High Alt has more sugar, more acidity in general.
 - High Density can usually take more heat faster.
 - Air flow temp good indicator of things are properly set.
 - Preheat long time to let metal parts heat up (not just air temp).
 - Lower Drum speed (beans lay on metal longer) Lower RPM = longer roast + scorching.
 - Faster Dump speed, faster heat effects beans faster (speed up profile)
 - Too fast bean stay stuck to drum wall.
 - Set RPM constant for your style, dont change during roast. set and forget.
 - Airflow, set and forget. However, can be useful (if cold day, less input)
 - Airflow 25% heavy scorching. 50% faster, 75% or 100% roast fastest.
 - Good: Air 50% until max ROR, then 100% Air for ROR bump, then slow air until FCs.
 - Measure air flow with magnahelic flow meter. Adjust airflow to constant volume (for weather effects)
 - Consistency? +/- 10 secs for target times (FCs), and +/- 2 'C; Agtron +/- 3; Weight Loss +/- 0.25% (more than 0.5% is way different color/flavor)
 - BT probe is actually Bean + Air temp.
 - Flavor is from: 80% color, devel 10%, FC time 10%
 - *ALWAYS* take weight loss measurement (ITS FREE!) and very insightful.
 - Weight Loss: Too Light <11%; Light 11-13%; Med 14-16%; Dark 17-18%; Very Dark 19-21%; Too Dark >21%
 - Color sensors: further from sample are "lighter" read, closer = Darker read.  Distance matters.
 - Color readings for Whole Bean "WB" maybe 34, but Ground "GR" might be 104 colors - measure both.
 - Always use consistent Grind setting, it can vary the GR color.
 - Every brew is a chance to rate the flavor. Rotate brewing through all beans, not just favorites.
 - Measure post-grind. Grind particle size distribution, color.
 - Industry uses 16:1 cupping ratio (water:coffee) (instead of 18:1) -- keep consistent ratio.
 - Measure total disolved solids (TDS) and solubility (for lab metrics)
 - Provide brewing instructions/guides along with coffee (help people get best flavor)

## Mike at Virtual Coffee Lab

 - https://www.youtube.com/watch?v=0sDGXYvQBk0
 - Early FC is evidence of Roasting going too fast. Run away roast!
 - if FC starts at lower temp, it's runaway momentum.
 - Drying Phase sets up momentum and pace for roast - it is important.
 - Sometimes SC starts, and we think it's FC continuing - runaway momentum.
 - Very Dark roast swells up very Large beans.
 - Increase air flow as emergency brake to slow down runaway temp rise.
 - ET shows thermal runaway, want slow gentle slope.
 - Plan the Dry phase, with intentional actions.

 - About turning point https://www.youtube.com/watch?v=Mu9vbybQLUc
 - TP affected by Ambient temp, Charge amount.
 - Notice TP Time and Temp - both useful.
 - Charge temp choice validation (based on Ambient temp)
 - How beans response to heat - high vs. low density, moving quick/slowly.
 - Notice roasting defects, scorching, tipping.
 - Slope of curve could be useful [SJ]
 - Indicates bean density.
 - Second chance to correct - notice TP if bean is fast/slow. indicates heat adjustments.
 - Notice TP difference in consecutive roasts (background previous roast).
 - Suggests Dry End behavior and FC. Washed Dense coffee ~30sec, Dry Process Low Density is faster.
 - Suggests FC behavior: fast/slow, heavy/light
 - Reveals pace of the roast, both indicator and control. high/low TP temp means fast/slow roast time.
 - Want to avoid fast under-devel (bitter), and long slow over-devel (flat).

 - Putting together a coffee roasting plan https://www.youtube.com/watch?v=-7Z3fAIvs7U
 - **GOOD TIPS FOR PLANNING**
 - longer time in BRN phase makes even thorough flavor profile (2,3,4 mins)
 - Flavor influenced by: 1) Color, 2) FC time, 3) DEV time
 - Charge Temp: (around 150C - 200C) bean density, total roast duration, time for FC
 - 400 gm beans, medium density, use 170C charge temp. for 5:15 to DE
 - **MEASURE PRIOR DE** to figure out DE profile for charge temp.
 - target FC around 2x DE time: (5:00 DE, then 10:00 FC) + 2 mins DEVEL, 12:00 total
 - Color: medium, drop ~200c.
 - Preheat roaster 10+ mins.

 - Bold Roast without the Char  https://www.youtube.com/watch?v=AFeiYj5oqKU
 - Fresh Roast to do 180 gm beans (same beans as above)
 - Target 3:00 DE, 7:00 FC, 9:00 DROP; Medium Roast, 15% loss weight.
 - Air roaster, can lower 2 mins (Convection Air faster than conduction in drum)
 - 






