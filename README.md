# kbonus

Read and interact with [KBONUS-BKG](https://archive.stsci.edu/hlsp/kbonus-bkg) light curves.

**Author: [Zachary R. Claytor](https://github.com/zclaytor)** (<zclaytor@ufl.edu>)

`kbonus` is designed primarily to work with the light curves downloaded on the University of Florida's HiPerGator computer, where the data are mirrored from the database at MAST. For more information about the data, see the paper by [Martinez-Palomera, Hedges, and Dotson (2023)](https://ui.adsabs.harvard.edu/abs/2023arXiv231017733M/abstract).

Citation information pending.

## Installation

For now, I recommend installing either from GitHub, or directly from the repository on HiPerGator.

**GitHub** installation will clone the repository into wherever your packages are saved:

```bash
pip install git+https://github.com/zclaytor/kbonus
```

**HiPerGator** installation is more space efficient, as it will source directly from the HPG repository. But note that you'll be trusting me to keep this version up to date and working.

```bash
pip install -e /blue/jtayar/zclaytor/kbonus-bkg/kbonus
```

## Usage

### Reading light curves

This package is designed to read a light curve without you having to worry about where the file is downloaded. All you have to do is supply a Kepler Input Catalog ID or Gaia DR3 designation. The file is read directly into a `lightkurve.KeplerLightCurve` object, so you'll want to familiarize yourself with `lightkurve` if you haven't already.

Here's an example:

```python
import kbonus as kb
kic = 10407233
lc = kb.get_lightcurve(kic)
lc
```

Output:

```output
<KeplerLightCurve length=63651 LABEL="KIC 10407233" AUTHOR=Kepler FLUX_ORIGIN=pdcsap_flux>
```

### Reading quarter light curves

The light curve files also include the individual quarter light curves, which are returned as a `lightkurve.LightCurveCollection`:

```python
lcs = kb.get_quarter_lightcurves(kic)
lcs
```

Output:

```output
LightCurveCollection of 17 objects:
    0: <KeplerLightCurve LABEL="KIC 10407233 Quarter 0">
    1: <KeplerLightCurve LABEL="KIC 10407233 Quarter 2">
    2: <KeplerLightCurve LABEL="KIC 10407233 Quarter 3">
    ...
```

But note that I'm not entirely sure the quarter light curves are properly corrected for systematics. Let me know if you find or think otherwise.

### Reading light curves from catalog row

You can also read light curves by supplying a catalog row. If you find a target you like, just pass the catalog row directly to the reader. For example:

```python
target = source_cat[source_cat["kic"] == 10407233] # `target` is an astropy Table
lc = kb.get_lightcurve(target)
```

### Reading the catalogs

`kbonus` also has readers for the various KBONUS-BKG catalogs, so you can see for yourself what targets are available. The available catalogs are the Source ("source"), M Stars ("mstars"), and White Dwarf ("wd") catalogs.

```python
cat = kb.read_catalog(cat="source")
cat
```

Output:

```output
<Table length=606900>
      gaia_designation               ra               dec        ...       kic_sep            kep_mag                 fname            
                                    deg               deg        ...        arcsec              mag                                    
          bytes28                 float64           float64      ...       float64            float64                bytes28           
---------------------------- ----------------- ----------------- ... -------------------- ---------------- ----------------------------
Gaia DR3 2049129000009122560 295.1368480059792 38.47822861016137 ...   0.6189198743541765 18.8530006408691 kic-003357387               
Gaia DR3 2049129000009123328 295.1291598452008 38.47715676860133 ...  0.17665367027730292 16.1299991607666 kic-003357360               
                         ...               ...               ... ...                  ...              ...                          ...
```

The default settings return an `astropy.table`, but a `pandas` version of each catalog is available as well. Just set `reader='pandas'` to get a `pandas.DataFrame` version of the table.
