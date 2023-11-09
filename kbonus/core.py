import os
import pandas as pd
from astropy.table import Table
from astropy.io import fits
import lightkurve as lk


root_dir = "/home/zach/Projects/kbonus-bkg/"


def read_input_catalog(reader="fits", **kw):
    if reader == "fits":
        return Table.read(
            os.path.join(root_dir, 
                "hlsp_kbonus-bkg_kepler_kepler_source-catalog_kepler_v1.0_cat.fits"),
            format="fits",
            **kw)
    elif reader == "pandas":
        return pd.read_csv(
            os.path.join(root_dir, "kbonus-bkg_source_catalog_v1.0.fits"),
            **kw
        )