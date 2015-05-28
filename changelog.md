# PyADAPT Changelog

## Currently Supported Datastreams and Variables:
### as of current version (v0.1.0)
 * `aos`       - Aerosol Backscatter
    * 1um  total light scattering coefficient
    * 10um total light scattering coefficient
    * plots: Aerosol scattering coefficient at 1um and 10um cutoff for all three
      color channels (R, G, B)
 * `aosccn`    - CCN Number Concentration
    * number concentration
    * supersaturation
 * `sfcmet`    - Surface Meteorology
    * temperature
    * wind speed
    * precip rate
 * `sondewnpn` - Radiosonde
 	* temperature
 	* dewpoint temperature

##v0.1.0 (January 21 2015)
Tested with a handful of GRW and ENA files

 * added support for CCN datastream (`aosccn`)
 * added support for Surface Meteorology datastream (`sfcmet`)
 * added support for the Radiosonde datastream (`sondewnpn`)
 * added support for the Aerosol Nephelometer datastream (`aos`)
 * make plots! for more details about the
   specific type of plot each datastream will make, check out
   the examples directory. There are examples of each type of
   plot in there.
 * automatically detect which type of datastream you are trying
   to make a plot of
 *
