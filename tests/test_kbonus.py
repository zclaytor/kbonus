import os
import pandas as pd
from astropy.table import Table
import lightkurve as lk

import kbonus as kb


def test_root_exists():
    assert os.path.exists(kb.root_dir)

def test_reader():
    assert isinstance(kb.read_input_catalog(), Table)
    assert isinstance(kb.read_input_catalog(reader="pandas"), pd.DataFrame)
    try:
        kb.read_input_catalog('pasta')
    except ValueError:
        pass

def test_resolve_filename():
    gaia = 2143858906058582784
    kic = 11282447
    fname = 'kic-011282447'
    f1 = kb.core.resolve_filename(gaia)
    f2 = kb.core.resolve_filename(kic)
    assert f1 == fname
    assert f2 == fname
    
def test_ETE():
    gaia = 2086636884980516352
    kic = 10407233
    for f in [gaia, kic, f"Gaiadr3{gaia}  ", f"   kic{kic}"]:
        l = kb.get_lightcurve(f)
        assert isinstance(l, lk.LightCurve)