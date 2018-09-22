Custom Command
--------------

This is a fun excersize to show how to allow users to run arbitrary python
code in sublime text, substituting variable text by prompting the
user for each "context variable" (i.e a simple template system).

Usage:

- Drop the ``custom_code.py`` python module into your `Sublime user dir`_
- define a custom command in your ``Packages/User/User.sublime-commands``:

.. code-block:: javascript

    [
      {
        "caption": "custom: set git commit date",
        "command": "custom_code",
        "args": {
          "code": "import os\nos.environ.update(dict(GIT_COMMITTER_DATE='{{DATE}}', GIT_AUTHOR_DATE='{{DATE}}'))",
        }
      }
    ]

.. _Sublime user dir: http://docs.sublimetext.info/en/latest/customization/settings.html?highlight=Packages%2FUser
