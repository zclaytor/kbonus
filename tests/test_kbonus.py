import os
import pandas as pd
from astropy.table import Table
import lightkurve as lk

import kbonus as kb


def test_root_exists():
    assert os.path.exists(kb.root_dir)

def test_reader():
    assert isinstance(kb.read_catalog(), Table)
    assert isinstance(kb.read_catalog(reader="pandas"), pd.DataFrame)
    try:
        kb.read_catalog('pasta')
    except ValueError:
        pass

def test_catalogs_fits(reader="fits"):
    assert len(kb.read_source_catalog(reader)) == 606900, \
        "Length of source catalog does not match expectation (606900)."
    assert len(kb.read_koi_catalog(reader)) == 35639, \
        "Length of koi catalog does not match expectation (35639)."
    assert len(kb.read_mstars_catalog(reader)) == 29800, \
        "Length of mstars catalog does not match expectation (29800)."
    assert len(kb.read_wd_catalog(reader)) == 91, \
        "Length of wd catalog does not match expectation (91)."
    
def test_catalogs_pandas():
    test_catalogs_fits(reader="pandas")

def test_lazy_catalog_reader():
    assert len(kb.read_catalog("koi")) == 35639, \
        "Lazy KOI reader does not return the KOI catalog."
    assert len(kb.read_catalog("input")) == 606900, \
        "Reading for 'input' does not return the Source catalog."

def test_resolve_filename():
    gaia = 2143858906058582784
    kic = 11282447
    fname = 'kic-011282447'
    f1 = kb.core._get_filename(gaia)
    f2 = kb.core._get_filename(kic)
    assert f1 == fname
    assert f2 == fname
    
def test_ETE():
    gaia = 2086636884980516352
    kic = 10407233
    for f in [gaia, kic, f"Gaiadr3{gaia}  ", f"   kic{kic}"]:
        l = kb.get_lightcurve(f)
        assert isinstance(l, lk.LightCurve)

def test_collection():
    kic = 10407233
    lcs = kb.get_quarter_lightcurves(kic)
    assert isinstance(lcs, lk.LightCurveCollection)