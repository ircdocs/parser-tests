IRC Parser Tests
================
Tests for IRC parsers.

**Note:** This is nowhere near done or ready for much use at all for anyone but me yet. Feel free to submit PRs.


Testing
-------
The ``test.py`` script uses both the `ircreactor <https://github.com/mammon-ircd/ircreactor>`_ and `girc <https://github.com/DanielOaks/girc>`_ libraries as 'reference' implementations. Neither of these are on PyPi, and must be installed with ``python3 setup.py install`` on both of them.

After that, simply run ``python3 test.py``. This will test everything we can test, and show the output.


License
-------
Whatever belongs to me is released into the public domain, do whatever you want with it. Most of these originate from `grawity's tests <https://github.com/grawity/code/tree/master/lib/tests>`_ though, so they may be covered under that license.
