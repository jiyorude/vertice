from setuptools import setup, find_packages

setup(
    name='vertice',
    version='0.5.0',
    author='Jordy Veenstra / A Pixelated Point of View',
    author_email='jordy.gaptx@gmail.com',
    description='Quake III Map Boundary Analysis Tool',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/jiyorude/vertice',
    project_urls={
        "GitHub": "https://www.github.com/jiyorude/vertice",
        "PyPi": "#"
    },
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=[
       "reportlab",
       "py7zr",
       "rarfile"
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'vertice_run = vertice.vertice:exec',
        ],
    },
)