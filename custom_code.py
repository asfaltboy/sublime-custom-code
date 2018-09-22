"""
This is a fun excersize to show how to run arbitrary code
in sublime, substituting variable text (i.e template system)
prompting the user for each variable.

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
"""
import ast
import re

import sublime
from sublime_plugin import WindowCommand


class CustomCodeCommand(WindowCommand):
    def prompt_all(self, prompts, args, callback):
        if not prompts:
            return callback(args)

        prompt_argument = prompts.pop()
        caption = "Code argument for %s: " % prompt_argument

        def prompt_again(argument_name, response):
            args.append((argument_name, response))
            self.prompt_all(prompts, args, callback)

        window = sublime.active_window()
        window.show_input_panel(
            caption,
            '',
            lambda res: prompt_again(prompt_argument, res),
            None, None,
        )

    @staticmethod
    def run_custom_code(code, args=[]):
        for name, value in args:
            code = code.replace(name, value)
        tree = ast.parse(code)
        # None at [0] so we can index lines from 1
        lines = [None] + code.splitlines()
        custom_code_namespace = {}

        for node in tree.body:
            wrapper = ast.Module(body=[node])
            try:
                co = compile(wrapper, "<ast>", 'exec')
                exec(co, custom_code_namespace)
            except Exception as e:
                print('error on line %s:\n%s' % (
                    node.lineno,
                    lines[node.lineno]
                  )
                )

    def run(self, **kwargs):
        if not kwargs.get('code'):
            sublime.error_message("You must provide a 'code' option.")
            return

        code = kwargs['code']
        prompts = set(re.findall('({{\w+}})', code))
        if prompts:
            self.prompt_all(
                prompts, [],
                lambda args: self.run_custom_code(code, args),
            )

        self.run_custom_code(code)
