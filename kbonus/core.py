import os
import warnings
from socket import gethostname
import pandas as pd
from astropy.table import Table, Row
from astropy.io import fits
from astropy.units import UnitsWarning
import lightkurve as lk
from lightkurve.utils import KeplerQualityFlags

if gethostname() == "Ultron":
    root_dir = "/home/zach/Projects/kbonus-bkg/"
else:
    root_dir = "/blue/jtayar/zclaytor/kbonus-bkg"
cat_dir = os.path.join(root_dir, "catalogs")
lcs_dir = os.path.join(root_dir, "lcs")


def read_catalog(cat="source", reader="fits", **kw):
    """Reads a KBONUS catalog from file.

    Args:
        cat (str): Which catalog to read.
            Options are "source", "kois-nns", "mstars", and "wd". Defaults to "source".
        reader (str): Which reader to use. 
            Options are 'fits' for `astropy.table.Table.read` 
            and 'pandas' for `pandas.DataFrame.read_csv`.
            Defaults to 'fits'.
        **kw: keyword arguments to be passed to the file reader.

    Returns:
        catalog: astropy Table or pandas DataFrame version of the catalog.
    """
    if "koi" in cat:
        # I don't want to type "kois-nns" every time I want the kois.
        cat = "kois-nns"
    elif cat == "input":
        # For the inevitable event that I forget that it's the "source" (not "input") catalog
        cat = "source"
    elif cat not in ["source", "mstars", "wd"]:
        raise ValueError("Argument `cat` must be one of 'source', 'kois-nns', 'mstars', or 'wd'.")
        
    if reader == "fits":
        with warnings.catch_warnings():
            # By default, AstroPy emits noisy warnings about units commonly used
            # in archived TESS data products (e.g., "e-/s" and "pixels").
            # We ignore them here because they don't affect Lightkurve's features.
            warnings.simplefilter("ignore", category=UnitsWarning)
            tab = Table.read(
                os.path.join(cat_dir, 
                    f"hlsp_kbonus-bkg_kepler_kepler_{cat}-catalog_kepler_v1.0_cat.fits"),
                format="fits",
                **kw)
            return tab
    elif reader == "pandas":
        return pd.read_csv(
            os.path.join(cat_dir, f"kbonus-bkg_{cat}-catalog_v1.0.csv"),
            **kw
        )
    else:
        raise ValueError("`reader` must be either 'fits' or 'pandas'.")
    
def read_source_catalog(reader="fits", **kw):
    """Reads the KBONUS Source Catalog from file.

    Args:
        reader (str): Which reader to use. 
            Options are 'fits' for `astropy.table.Table.read` 
            and 'pandas' for `pandas.DataFrame.read_csv`.
            Defaults to 'fits'.
        **kw: keyword arguments to be passed to the file reader.

    Returns:
        catalog: astropy Table or pandas DataFrame version of the catalog.
    """
    return read_catalog(cat="source", reader=reader, **kw)

def read_koi_catalog(reader="fits", **kw):
    """Reads the KBONUS KOI catalog from file.

    Args:
        reader (str): Which reader to use. 
            Options are 'fits' for `astropy.table.Table.read` 
            and 'pandas' for `pandas.DataFrame.read_csv`.
            Defaults to 'fits'.
        **kw: keyword arguments to be passed to the file reader.

    Returns:
        catalog: astropy Table or pandas DataFrame version of the catalog.
    """
    return read_catalog(cat="koi-nns", reader=reader, **kw)

def read_mstars_catalog(reader="fits", **kw):
    """Reads the KBONUS Mstars Catalog from file.

    Args:
        reader (str): Which reader to use. 
            Options are 'fits' for `astropy.table.Table.read` 
            and 'pandas' for `pandas.DataFrame.read_csv`.
            Defaults to 'fits'.
        **kw: keyword arguments to be passed to the file reader.

    Returns:
        catalog: astropy Table or pandas DataFrame version of the catalog.
    """
    return read_catalog(cat="mstars", reader=reader, **kw)

def read_wd_catalog(reader="fits", **kw):
    """Reads the KBONUS White Dwarf Catalog from file.

    Args:
        reader (str): Which reader to use. 
            Options are 'fits' for `astropy.table.Table.read` 
            and 'pandas' for `pandas.DataFrame.read_csv`.
            Defaults to 'fits'.
        **kw: keyword arguments to be passed to the file reader.

    Returns:
        catalog: astropy Table or pandas DataFrame version of the catalog.
    """
    return read_catalog(cat="wd", reader=reader, **kw)

def get_lightcurve(target, **kw):
    """Retrieve and read light curve of specified target.

    Args:
        target (int, str, astropy.table.[Row, Table], pandas.[Series, DataFrame]): 
            The specified target. If supplying an ID, `target` must be
            formatted as a KIC ID or Gaia DR3 ID, but can be of type `str` 
            or `int`. Acceptable formats include:
                `target=11282447` # KIC ID. KIC IDs are always <= 8 characters.
                `target="11282447"` # Same as above.
                `target="KIC 11282447"` # KIC ID formatted as str.
                `target="Gaia DR3 2143858906058582784"` # Gaia DR3 ID
                `target=2143858906058582784 # Gaia ID (always == 19 characters).
            `target` may also be a row from one of the source catalogs, as type
            astropy.table Row or Table (length=1), or pandas Series or 
            DataFrame (length=1).
            
        **kw:
            Keyword arguments to be passed to `lightkurve.read`.
        
    Returns:
        lightcurve (lightkurve.KeplerLightCurve):
            The Kepler light curve of the desired target.
    """
    filepath = get_target_path(target)
    if "flux_column" in kw:
        flux_column = kw.pop("flux_column")
        return lk.read(filepath, **kw).select_flux(flux_column)
    else:
        return lk.read(filepath, **kw)
    
def get_lightcurve_fits(target, **kw):
    filepath = get_target_path(target)
    if "flux_column" in kw:
        flux_column = kw.pop("flux_column")
    else:
        flux_column = "FLUX"

    if "quality_bitmask" in kw:
        quality_bitmask = kw.pop("quality_bitmask")
    else:
        quality_bitmask = "default"

    with fits.open(filepath) as f:
        data = f[1].data

        lc = lk.KeplerLightCurve(data=data,
            time=data["TIME"],
            flux=data[flux_column],
            flux_err=data[flux_column + "_ERR"])
        
        # Filter out poor-quality data
        quality_mask = KeplerQualityFlags.create_quality_mask(
            quality_array=lc["SAP_QUALITY"], bitmask=quality_bitmask
        )
        lc = lc[quality_mask]

        lc.meta["AUTHOR"] = "Kepler"
        lc.meta["TARGETID"] = lc.meta.get("KEPLERID")
        lc.meta["QUALITY_BITMASK"] = quality_bitmask
        lc.meta["QUALITY_MASK"] = quality_mask

    return lc

def get_quarter_lightcurves(target, **kw):
    """Retrieve and read quarter light curves of specified target.

    Args:
        target (int, str, astropy.table.[Row, Table], pandas.[Series, DataFrame]): 
            The specified target. If supplying an ID, `target` must be
            formatted as a KIC ID or Gaia DR3 ID, but can be of type `str` 
            or `int`. Acceptable formats include:
                `target=11282447` # KIC ID. KIC IDs are always <= 8 characters.
                `target="11282447"` # Same as above.
                `target="KIC 11282447"` # KIC ID formatted as str.
                `target="Gaia DR3 2143858906058582784"` # Gaia DR3 ID
                `target=2143858906058582784 # Gaia ID (always == 19 characters).
            `target` may also be a row from one of the source catalogs, as type
            astropy.table Row or Table (length=1), or pandas Series or 
            DataFrame (length=1).
    
        **kw:
            Keyword arguments to be passed to `lightkurve.KeplerLightCurve` constructor.

    Returns:
        lightcurves (lightkurve.LightCurveCollection):
            The Kepler light curves of the desired target.
    """    
    filepath = get_target_path(target)

    if "flux_column" in kw:
        flux_column = kw.pop("flux_column")
        if flux_column == "PSF_FLUX_NOVA":
            flux_err = "PSF_FLUX_ERR_NOVA"
        else:
            flux_err = flux_column + "_ERR"
    else:
        flux_column = "FLUX"
        flux_err = "FLUX_ERR"

    with fits.open(filepath) as f:
        lcs = []
        objname = f[0].header["OBJECT"]
        for hdu in f:
            extname = hdu.header["EXTNAME"]
            if "LIGHTCURVE_Q" in extname:
                q = extname[extname.find("Q")+1:]
                lc = lk.KeplerLightCurve(hdu.data, 
                    time=hdu.data["TIME"].astype(float),
                    flux=hdu.data[flux_column].astype(float),
                    flux_err=hdu.data[flux_err].astype(float),
                    label=f"{objname} Quarter {q}",
                    **kw)
                lcs.append(lc)
    if len(lcs) == 1:
        return lcs[0]
    return lk.LightCurveCollection(lcs)

def get_target_path(target):
    """Given a target, return the path to the target's light curve file.
    See the docstring for `get_lightcurve` for acceptable target formats.
    """
    fname = _get_filename(target).strip()
    if fname.startswith("kic"):
        id_str = fname[4:]
    elif fname.startswith("gaia"):
        id_str = fname[9:]
    first_four = id_str[:4]
    file_path = os.path.join(
        lcs_dir, first_four, id_str,
        f"hlsp_kbonus-bkg_kepler_kepler_{fname}_kepler_v1.0_lc.fits")
    return file_path

def _get_filename_int(target):
    """Helper function to retrieve the filename given integer target name.
    """
    if len(str(target)) == 19:
        # All Gaia IDs are 19 digits
        designation = f"Gaia DR3 {target}"
        c = "gaia_designation"
    else:
        # All Kepler IDs are 8 digits or less, but no need to be specific.
        designation = target
        c = "kic"

    return c, designation

def _get_filename(target):
    """Helper function to retrieve the target's designation as listed
    in the name of its file.
    """
    if isinstance(target, pd.Series) or isinstance(target, Row):
        return target["fname"]
    elif isinstance(target, pd.DataFrame) or isinstance(target, Table):
        assert len(target) == 1, "Cannot return light curves for multiple rows."
        if isinstance(target, Table):
            target = target[0]
        else:
            target = target.iloc[0]
        return target["fname"]
    
    names = _read_designations()

    if isinstance(target, int):
        c, designation = _get_filename_int(target)

    elif isinstance(target, str):
        target = target.lower().strip()
        if "gaia" in target:
            c = "gaia_designation"
            gaia_id = target[-19:]
            designation = f"Gaia DR3 {gaia_id}"
        elif "kic" in target:
            c = "kic"
            kic_id = target[target.find("kic")+3:]
            designation = int(kic_id)
        else:
            try:
                target = int(target)
            except ValueError:
                raise ValueError("'Gaia' or 'KIC' not in target name, and could not cast to int.")
            else:
                c, designation = _get_filename_int(target)

    # Make sure target is in the table
    assert designation in names[c], f"Object with {c}={designation} not found."
    row = names[names[c] == designation]
    # If multiple rows are returned, something went wrong.
    if len(row) > 1:
        raise RuntimeError(f"Multiple rows returned:\n{row}")
    
    fname = row["fname"][0]
    return fname

def _read_designations():
    """Read in the designation.fits file for name disambiguation.
    """
    return Table.read(os.path.join(cat_dir, "designations.fits"))