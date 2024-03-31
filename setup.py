import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    # Metadata
    name='copernicusmarine_local',
    version='0.1',
    description='Fetch data from a local copy of CMEMS',
    url='https://github.com/jiho/copernicusmarine_local',
    author='Jean-Olivier Irisson',
    author_email='irisson@normalesup.org',
    license='GPLv3',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha'
    ],
    # Content
    python_requires='>=3.9',
    install_requires=[
    ],
)
