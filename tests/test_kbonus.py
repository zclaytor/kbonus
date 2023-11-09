import os
import pandas as pd
from astropy.table import Table

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
    