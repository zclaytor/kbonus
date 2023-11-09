import setuptools

# Load the __version__ variable without importing the package already
exec(open("kbonus/version.py").read())

setuptools.setup(
    name="kbonus",
    version=__version__,
    author="Zachary R. Claytor",
    author_email="zclaytor@ufl.edu",
    description="Utilities for reading kbonus-bkg light curves from HiPerGator",
    #long_description=open("README.md").read(),
    #long_description_content_type="text/markdown",
    url="https://github.com/zclaytor/kbonus",
    license="MIT",
    python_requires='>=3',
    install_requires=[
        'numpy', 'matplotlib', 'pandas', 'astropy', 'lightkurve'
    ],
    packages=setuptools.find_packages(),
    #include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Astronomy",
    ],
)
