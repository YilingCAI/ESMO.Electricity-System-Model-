from __future__ import division, absolute_import

from setuptools import setup, find_packages

setup(
    name='ESMO',
    version='1.0',
    author='CAI Yiling, Francois-Marie BREON',
    author_email='yiling.cai@lsce.ipsl.fr',
    description=
    'Variable Renewable Energy Sources Penetration in the Changing Climate: A Long-Term Electricity System Capacity Expansion MOdel (ESMO)',
    long_description='README.md',
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=[
        'numpy', 'pandas', 'matplotlib', 'pyomo', 'seaborn', 'plotly'
    ],
    classifiers=[
        'Developement Status :: 3-Alpha', 'Natural Language :: English'
    ])
