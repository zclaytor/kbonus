import os
import pandas as pd
from astropy.table import Table
from astropy.io import fits
import lightkurve as lk


root_dir = "/home/zach/Projects/kbonus-bkg/"


def read_input_catalog(reader="fits", **kw):
    """Reads the KBONUS Input Catalog from file.

    Args:
        reader (str): Which reader to use. 
            Options are 'fits' for `astropy.table.Table.read` 
            and 'pandas' for `pandas.DataFrame.read_csv`.
            Defaults to 'fits'.
        **kw: keyword arguments to be passed to the file reader.

    Returns:
        catalog: astropy Table or pandas DataFrame version of the catalog.
    """
    if reader == "fits":
        return Table.read(
            os.path.join(root_dir, 
                "hlsp_kbonus-bkg_kepler_kepler_source-catalog_kepler_v1.0_cat.fits"),
            format="fits",
            **kw)
    elif reader == "pandas":
        return pd.read_csv(
            os.path.join(root_dir, "kbonus-bkg_source_catalog_v1.0.csv"),
            **kw
        )
    else:
        raise ValueError("`reader` must be either 'fits' or 'pandas'.")