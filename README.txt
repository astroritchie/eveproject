Goal: understand how magnetic flux that is reconnected in solar flares is related to flare intensity in different
wavelengths and emission measure. Find scaling laws.

ASTR 3760 Final Paper on this project's overview: 
https://github.com/astroritchie/eveproject/blob/master/ASTR3760RitchieFinalProject.pdf

Weekly Progress Log:

Week of 5/12 - 5/18: 
-Corrected background subtraction bugs in Python code
-Spearman correlation coefficients:
    -Peak EVL flux vs RibbonDB ribbon reconnection flux (phi_rbn)
    -Peak EVL flux vs RibbonDB peak x-ray flux (ixpeak)
    -Total EVL flux vs phi_rbn
    -Total EVL flux vs ixpeak
-Python Plots of Spearman correlation coefficients against EVE center line temperatures
-Began differential emission measure (DEM) inversion readings
-Ordered IDL license for DEM inversions

Week of 5/19 - 5/25:
-DEM mathematics background readings
-EVL flux txt files for AIA lines
-Corrected tstart,tfinal splicing for flux txt files
-Obtained IDL license, installed IDL87
-Found RibbonDB date errors, received new database
-Corrected nfiles algorithm in getEVLflux()
-Friday 5/24 off (traveling)

Week of 5/26 - 6/1:
-Monday 5/27 off (Memorial Day)
-SSW + CHIANTI setup
-Setup IDL pathing and startup file
-IDL session for REU students
-Background on ch_synethic.pro
-Began IDL code adjustments for local machine

Week of 6/2 - 6/8:
-Out most of week due to wisdom tooth extraction
-Finished IDL code adjustments for local machine
-Corrected ioneq and elemental abundance input files
-Created synthetic contribution functions via do_cont.pro
