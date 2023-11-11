import os

from .core import read_catalog, cat_dir

def _convert_fits_to_pandas(cat):
    """Given the name of a catalog, convert it to pandas and save to csv.
    """
    if "koi" in cat:
        # I don't want to type "kois-nns" every time I want the kois.
        cat = "kois-nns"
    elif cat == "input":
        # For the inevitable event that I forget that it's the "source" (not "input") catalog
        cat = "source"
    elif cat not in ["source", "mstars", "wd"]:
        raise ValueError("Argument `cat` must be one of 'source', 'kois-nns', 'mstars', or 'wd'.")
    
    table = read_catalog(cat, reader="fits")
    table.convert_bytestring_to_unicode()
    table = table.to_pandas()

    newname = os.path.join(cat_dir, f"kbonus-bkg_{cat}-catalog_v1.0.csv")
    table.to_csv(newname, index=False)