"""
bitc, a python library for the Bayesian analysis of isothermal titration calorimetry experiments.
"""
from __future__ import print_function
import os
from os.path import relpath, join
import subprocess

from setuptools import setup, Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize


DOCLINES = __doc__.split("\n")


VERSION = "0.0.0"
ISRELEASED = False
__version__ = VERSION

CLASSIFIERS = """\
Development Status :: 3 - Alpha
Intended Audience :: Science/Research
Intended Audience :: Developers
License :: OSI Approved :: Lesser GNU Public License (LGPL)
Programming Language :: Python
Programming Language :: Python :: 3
Topic :: Scientific/Engineering :: Bio-Informatics
Topic :: Scientific/Engineering :: Chemistry
Operating System :: POSIX
Operating System :: Unix
Operating System :: MacOS
"""


# Writing version control information to the module


def git_version():
    # Return the git revision as a string
    # copied from numpy setup.py
    def _minimal_ext_cmd(cmd):
        # construct minimal environment
        env = {}
        for k in ['SYSTEMROOT', 'PATH']:
            v = os.environ.get(k)
            if v is not None:
                env[k] = v
        # LANGUAGE is used on win32
        env['LANGUAGE'] = 'C'
        env['LANG'] = 'C'
        env['LC_ALL'] = 'C'
        out = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, env=env).communicate()[0]
        return out

    try:
        out = _minimal_ext_cmd(['git', 'rev-parse', 'HEAD'])
        GIT_REVISION = out.strip().decode('ascii')
    except OSError:
        GIT_REVISION = 'Unknown'

    return GIT_REVISION


def write_version_py(filename='bitc/version.py'):
    cnt = """
# This file is automatically generated by setup.py
short_version = '%(version)s'
version = '%(version)s'
full_version = '%(full_version)s'
git_revision = '%(git_revision)s'
release = %(isrelease)s

if not release:
    version = full_version
"""
    # Adding the git rev number needs to be done inside write_version_py(),
    # otherwise the import of numpy.version messes up the build under Python 3.
    FULLVERSION = VERSION
    if os.path.exists('.git'):
        GIT_REVISION = git_version()
    else:
        GIT_REVISION = 'Unknown'

    if not ISRELEASED:
        FULLVERSION += '.dev-' + GIT_REVISION[:7]

    a = open(filename, 'w')
    try:
        a.write(cnt % {'version': VERSION,
                       'full_version': FULLVERSION,
                       'git_revision': GIT_REVISION,
                       'isrelease': str(ISRELEASED)})
    finally:
        a.close()

# USEFUL SUBROUTINES


def find_package_data(data_root, package_root):
    files = []
    for root, dirnames, filenames in os.walk(data_root):
        for fn in filenames:
            files.append(relpath(join(root, fn), package_root))
    return files


# SETUP

write_version_py()
setup(
    name='bitc',
    author='John Chodera, Bas Rustenburg',
    author_email='john.chodera@choderalab.org',
    description=DOCLINES[0],
    long_description="\n".join(DOCLINES[2:]),
    version=__version__,
    license='LGPL',
    url='https://github.com/choderalab/bayesian-itc',
    platforms=['Linux', 'Mac OS-X', 'Unix'],
    classifiers=CLASSIFIERS.splitlines(),
    package_dir={'bitc': 'bitc'},
    packages=['bitc'],
    package_data={'bitc': find_package_data('examples', 'bitc')},  # NOTE: examples installs to bitc.egg/examples/, NOT bitc.egg/bitc/examples/.  You need to do utils.get_data_filename("../examples/*/setup/").
    zip_safe=False,
    ext_modules=cythonize("bitc/*.pyx"),
    cmdclass={'build_ext': build_ext},
    install_requires=[
        'numpy',
        'pandas',
        'pymc',
        'pint',
        'docopt',
        'schema',
        'scikit-learn',
        'matplotlib',
        ],
    )
