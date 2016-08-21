IRC Parser Tests
================
Tests for IRC parsers.

**Note:** This is still being written. Feel free to suggest or contribute tests - PRs are welcomed!


Testing
-------
The ``test.py`` script uses the `girc <https://github.com/DanielOaks/girc>`_ and `ircmatch <https://github.com/mammon-ircd/ircmatch>`_ libraries as reference implementations.

To install these libraries, run ``pip3 install --upgrade girc ircmatch``.

After that, simply run ``python3 test.py``. This will test everything we can test, and show the output.


Sources
-------
Some tests originate from `Mozilla's test vectors <https://dxr.mozilla.org/comm-central/source/chat/protocols/irc/test/test_ircMessage.js>`_, which are public domain.

Some tests originate from `grawity's test vectors <https://github.com/grawity/code/tree/master/lib/tests>`_ which were WTFPL v2 licensed when they were retrieved.
