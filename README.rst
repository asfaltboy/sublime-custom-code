Custom Command
--------------

This is a fun excersize to show how to allow users to run arbitrary python
code in sublime, substituting variable text by prompting the
user for each "context variable" (i.e a simple template system).

Usage:

- define a custom command in your ``User.sublime-commands``:

  [
    {
      "caption": "custom: set git commit date",
      "command": "custom_code",
      "args": {
        "code": "import os\nos.environ.update(dict(GIT_COMMITTER_DATE='{{DATE}}', GIT_AUTHOR_DATE='{{DATE}}'))",
      }
    }
  ]