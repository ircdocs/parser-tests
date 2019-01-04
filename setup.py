from contextlib import contextmanager
from pathlib import Path

from setuptools import setup

import parser_tests


@contextmanager
def link_tests():
    """
    Just a little bit of fuckery to symlink the data files in to the source tree
    """
    data_files = Path('tests').resolve()
    src_dir = Path('parser_tests').resolve()
    src_data = (src_dir / 'data')
    src_data.symlink_to(data_files, True)
    yield
    src_data.unlink()


with link_tests():
    setup(
        name="irc-parser-tests",
        # Generate the version string from __version__ tuple
        version='.'.join(map(str, parser_tests.__version__)),
        description="A library of tests for various IRC protocol parsers",
        url='https://github.com/ircdocs/parser-tests',
        author="linuxdaemon",
        author_email="linuxdaemonirc@gmail.com",
        classifiers=[
            'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        ],
        keywords='irc tests parser',
        packages=['parser_tests'],
        install_requires=[
            'PyYaml',
        ],
        include_package_data=True,
    )
