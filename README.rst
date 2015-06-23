IRC Parser Tests
================
Tests for IRC parsers.

**Note:** This is still being written. Feel free to suggest or contribute tests - PRs are welcomed!


Testing
-------
The ``test.py`` script uses both the `ircreactor <https://github.com/mammon-ircd/ircreactor>`_ and `girc <https://github.com/DanielOaks/girc>`_ libraries as 'reference' implementations. Neither of these are on PyPi, and must be installed with ``python3 setup.py install`` on both of them.

The library `ircmatch <https://github.com/mammon-ircd/ircmatch>`_ is also used as a reference implementation. This is `on PyPi <https://pypi.python.org/pypi/ircmatch>`_, and can be installed with ``pip3 install ircmatch``.

After that, simply run ``python3 test.py``. This will test everything we can test, and show the output.


License
-------
Whatever belongs to me is released into the public domain, do whatever you want with it.

Some tests originate from `Mozilla's test vectors <https://dxr.mozilla.org/comm-central/source/chat/protocols/irc/test/test_ircMessage.js>`_, which are public domain.

Some tests originate from `grawity's test vectors <https://github.com/grawity/code/tree/master/lib/tests>`_ which are MIT licensed.
