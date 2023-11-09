import os
import kbonus as kb

def test_root_exists():
    assert os.path.exists(kb.root_dir)