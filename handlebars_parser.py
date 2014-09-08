#!/usr/bin/env python
# -*- coding: utf-8 -*-

# CAVEAT UTILITOR
#
# This file was automatically generated by Grako.
#
#    https://pypi.python.org/pypi/grako/
#
# Any changes you make to it will be overwritten the next time
# the file is generated.


from __future__ import print_function, division, absolute_import, unicode_literals
from grako.parsing import graken, Parser


__version__ = (2014, 9, 8, 0, 26, 45, 0)

__all__ = [
    'HandlebarsParser',
    'HandlebarsSemantics',
    'main'
]


class HandlebarsParser(Parser):
    def __init__(self, whitespace=None, nameguard=True, **kwargs):
        super(HandlebarsParser, self).__init__(
            whitespace=whitespace,
            nameguard=nameguard,
            **kwargs
        )

    @graken()
    def _CONTENT_(self):

        def block0():
            with self._choice():
                with self._option():
                    self._pattern(r'[^{\\]+')
                with self._option():
                    self._ESCAPE_()
                with self._option():
                    self._NON_OPEN_()
                self._error('expecting one of: [^{\\\\]+')
        self._positive_closure(block0)

    @graken()
    def _NEWLINE_(self):
        self._pattern(r'\n')

    @graken()
    def _ESCAPE_(self):
        self._token('\\')
        self._pattern(r'.')
        self.ast['@'] = self.last_node

    @graken()
    def _NON_OPEN_(self):
        self._token('{')
        with self._ifnot():
            self._token('{')

    @graken()
    def _WS_CONTROL_(self):
        with self._optional():
            self._token('~')

    @graken()
    def _DATA_(self):
        self._token('@')

    @graken()
    def _PATH_THIS_(self):
        self._token('./')

    @graken()
    def _PATH_PARENT_(self):
        self._token('../')

    @graken()
    def _REF_(self):
        with self._group():
            with self._optional():
                self._DATA_()
            self.ast['data'] = self.last_node

            def block2():
                with self._choice():
                    with self._option():
                        self._PATH_PARENT_()
                    with self._option():
                        self._PATH_THIS_()
                    with self._option():
                        with self._group():
                            with self._choice():
                                with self._option():
                                    self._IDENTIFIER_()
                                with self._option():
                                    self._QUOTED_IDENTIFIER_()
                                self._error('no available options')
                        self._SEPARATOR_()
                    self._error('no available options')
            self._closure(block2)
            self.ast['traversal'] = self.last_node
            with self._group():
                with self._choice():
                    with self._option():
                        self._IDENTIFIER_()
                    with self._option():
                        self._QUOTED_IDENTIFIER_()
                    self._error('no available options')
            self.ast['name'] = self.last_node

        self.ast._define(
            ['data', 'traversal', 'name'],
            []
        )

    @graken()
    def _IDENTIFIER_(self):
        self._pattern(r'[^ \t\n!"#%&\'()*+,./;<=>@[\\\]^`{|}~]+')

    @graken()
    def _QUOTED_IDENTIFIER_(self):
        self._pattern(r'\[[^\]]+\]')

    @graken()
    def _SEPARATOR_(self):
        with self._choice():
            with self._option():
                self._token('.')
            with self._option():
                self._token('/')
            self._error('expecting one of: . /')

    @graken()
    def _WS_(self):
        self._pattern(r'[ \n]*')

    @graken()
    def _STRING_LITERAL_(self):
        self._pattern(r'"([^\"]+|\\")*"')

    @graken()
    def _BASIC_ARG_(self):
        with self._group():
            with self._choice():
                with self._option():
                    self._STRING_LITERAL_()
                with self._option():
                    self._REF_()
                with self._option():
                    self._IDENTIFIER_()
                    self.ast['name'] = self.last_node
                    self._token('=')
                    with self._group():
                        with self._choice():
                            with self._option():
                                self._STRING_LITERAL_()
                            with self._option():
                                self._REF_()
                            self._error('no available options')
                    self.ast['value'] = self.last_node
                self._error('no available options')

        self.ast._define(
            ['name', 'value'],
            []
        )

    @graken()
    def _SUBEXPRESSION_OPEN_(self):
        self._token('(')

    @graken()
    def _SUBEXPRESSION_CLOSE_(self):
        self._token(')')

    @graken()
    def _SUBEXPRESSION_(self):
        self._SUBEXPRESSION_OPEN_()
        self._IDENTIFIER_()
        self._ARGS_()
        self._SUBEXPRESSION_CLOSE_()

    @graken()
    def _ARG_(self):
        with self._choice():
            with self._option():
                self._BASIC_ARG_()
            with self._option():
                self._SUBEXPRESSION_()
            self._error('no available options')

    @graken()
    def _ARGS_(self):

        def block0():
            self._pattern(r'[ \n]+')
            self._ARG_()
            self.ast['@'] = self.last_node
        self._closure(block0)

    @graken()
    def _COMMENT_LONG_OPEN_(self):
        self._token('{{!--')

    @graken()
    def _COMMENT_LONG_CONTENT_(self):

        def block0():
            with self._choice():
                with self._option():
                    self._pattern(r'[^-]+')
                with self._option():
                    self._pattern(r'-')
                    with self._ifnot():
                        self._token('-}}')
                self._error('expecting one of: - [^-]+')
        self._closure(block0)

    @graken()
    def _COMMENT_LONG_CLOSE_(self):
        self._token('--}}')

    @graken()
    def _COMMENT_LONG_TAG_(self):
        with self._group():
            self._COMMENT_LONG_OPEN_()
            self._COMMENT_LONG_CONTENT_()
            self.ast['content'] = self.last_node
            self._COMMENT_LONG_CLOSE_()

        self.ast._define(
            ['content'],
            []
        )

    @graken()
    def _COMMENT_OPEN_(self):
        self._token('{{!')

    @graken()
    def _COMMENT_CONTENT_(self):

        def block0():
            with self._choice():
                with self._option():
                    self._pattern(r'[^}]+')
                with self._option():
                    self._token('}')
                    with self._ifnot():
                        self._token('}')
                self._error('expecting one of: [^}]+ }')
        self._closure(block0)

    @graken()
    def _COMMENT_TAG_(self):
        with self._group():
            self._COMMENT_OPEN_()
            self._COMMENT_CONTENT_()
            self.ast['content'] = self.last_node
            self._TAG_CLOSE_()

        self.ast._define(
            ['content'],
            []
        )

    @graken()
    def _BLOCK_OPEN_(self):
        with self._group():
            self._token('{{')
            self._WS_CONTROL_()
            self.ast['tb'] = self.last_node
            self._token('#')
            self._REF_()
            self.ast['ref'] = self.last_node
            self._ARGS_()
            self.ast['args'] = self.last_node
            self._WS_()
            self._WS_CONTROL_()
            self.ast['tf'] = self.last_node
            self._TAG_CLOSE_()

        self.ast._define(
            ['tb', 'ref', 'args', 'tf'],
            []
        )

    @graken()
    def _BLOCK_INVERTED_OPEN_(self):
        with self._group():
            self._token('{{')
            self._WS_CONTROL_()
            self.ast['tb'] = self.last_node
            self._token('^')
            self._REF_()
            self.ast['ref'] = self.last_node
            self._ARGS_()
            self.ast['args'] = self.last_node
            self._WS_()
            self._WS_CONTROL_()
            self.ast['tf'] = self.last_node
            self._TAG_CLOSE_()

        self.ast._define(
            ['tb', 'ref', 'args', 'tf'],
            []
        )

    @graken()
    def _BLOCK_ELSE_(self):
        with self._group():
            with self._choice():
                with self._option():
                    self._token('{{')
                    self._WS_CONTROL_()
                    self.ast['tb'] = self.last_node
                    self._token('^')
                    self._WS_CONTROL_()
                    self.ast['tf'] = self.last_node
                    self._token('}}')
                with self._option():
                    self._token('{{')
                    self._WS_CONTROL_()
                    self.ast['tb'] = self.last_node
                    self._token('else')
                    self._WS_CONTROL_()
                    self.ast['tf'] = self.last_node
                    self._token('}}')
                self._error('no available options')

        self.ast._define(
            ['tb', 'tf'],
            []
        )

    @graken()
    def _BLOCK_CLOSE_(self):
        with self._group():
            self._token('{{')
            self._WS_CONTROL_()
            self.ast['tb'] = self.last_node
            self._token('/')
            self._REF_()
            self.ast['ref'] = self.last_node
            self._WS_()
            self._WS_CONTROL_()
            self.ast['tf'] = self.last_node
            self._TAG_CLOSE_()

        self.ast._define(
            ['tb', 'ref', 'tf'],
            []
        )

    @graken()
    def _RAW_TAG_OPEN_(self):
        self._token('{{{')

    @graken()
    def _RAW_TAG_CLOSE_(self):
        self._token('}}}')

    @graken()
    def _RAW_TAG_(self):
        with self._group():
            self._RAW_TAG_OPEN_()
            self._WS_CONTROL_()
            self.ast['tb'] = self.last_node
            self._REF_()
            self.ast['ref'] = self.last_node
            self._ARGS_()
            self.ast['args'] = self.last_node
            self._WS_()
            self._WS_CONTROL_()
            self.ast['tf'] = self.last_node
            self._RAW_TAG_CLOSE_()

        self.ast._define(
            ['tb', 'ref', 'args', 'tf'],
            []
        )

    @graken()
    def _PARTIAL_TAG_(self):
        with self._group():
            self._token('{{')
            self._WS_CONTROL_()
            self.ast['tb'] = self.last_node
            self._token('>')
            self._WS_()
            self._REF_()
            self.ast['ref'] = self.last_node
            self._ARGS_()
            self.ast['args'] = self.last_node
            self._WS_()
            self._WS_CONTROL_()
            self.ast['tf'] = self.last_node
            self._TAG_CLOSE_()

        self.ast._define(
            ['tb', 'ref', 'args', 'tf'],
            []
        )

    @graken()
    def _TAG_OPEN_(self):
        self._token('{{')

    @graken()
    def _TAG_CLOSE_(self):
        self._token('}}')

    @graken()
    def _TAG_(self):
        with self._group():
            self._TAG_OPEN_()
            self._WS_CONTROL_()
            self.ast['tb'] = self.last_node
            self._REF_()
            self.ast['ref'] = self.last_node
            self._ARGS_()
            self.ast['args'] = self.last_node
            self._WS_()
            self._WS_CONTROL_()
            self.ast['tf'] = self.last_node
            self._TAG_CLOSE_()

        self.ast._define(
            ['tb', 'ref', 'args', 'tf'],
            []
        )

    @graken()
    def _MAIN_(self):

        def block0():
            with self._choice():
                with self._option():
                    self._CONTENT_()
                with self._option():
                    self._RAW_TAG_()
                with self._option():
                    self._PARTIAL_TAG_()
                with self._option():
                    self._COMMENT_LONG_TAG_()
                with self._option():
                    self._COMMENT_TAG_()
                with self._option():
                    self._BLOCK_OPEN_()
                with self._option():
                    self._BLOCK_CLOSE_()
                with self._option():
                    self._TAG_()
                self._error('no available options')
        self._closure(block0)


class HandlebarsSemantics(object):
    def CONTENT(self, ast):
        return ast

    def NEWLINE(self, ast):
        return ast

    def ESCAPE(self, ast):
        return ast

    def NON_OPEN(self, ast):
        return ast

    def WS_CONTROL(self, ast):
        return ast

    def DATA(self, ast):
        return ast

    def PATH_THIS(self, ast):
        return ast

    def PATH_PARENT(self, ast):
        return ast

    def REF(self, ast):
        return ast

    def IDENTIFIER(self, ast):
        return ast

    def QUOTED_IDENTIFIER(self, ast):
        return ast

    def SEPARATOR(self, ast):
        return ast

    def WS(self, ast):
        return ast

    def STRING_LITERAL(self, ast):
        return ast

    def BASIC_ARG(self, ast):
        return ast

    def SUBEXPRESSION_OPEN(self, ast):
        return ast

    def SUBEXPRESSION_CLOSE(self, ast):
        return ast

    def SUBEXPRESSION(self, ast):
        return ast

    def ARG(self, ast):
        return ast

    def ARGS(self, ast):
        return ast

    def COMMENT_LONG_OPEN(self, ast):
        return ast

    def COMMENT_LONG_CONTENT(self, ast):
        return ast

    def COMMENT_LONG_CLOSE(self, ast):
        return ast

    def COMMENT_LONG_TAG(self, ast):
        return ast

    def COMMENT_OPEN(self, ast):
        return ast

    def COMMENT_CONTENT(self, ast):
        return ast

    def COMMENT_TAG(self, ast):
        return ast

    def BLOCK_OPEN(self, ast):
        return ast

    def BLOCK_INVERTED_OPEN(self, ast):
        return ast

    def BLOCK_ELSE(self, ast):
        return ast

    def BLOCK_CLOSE(self, ast):
        return ast

    def RAW_TAG_OPEN(self, ast):
        return ast

    def RAW_TAG_CLOSE(self, ast):
        return ast

    def RAW_TAG(self, ast):
        return ast

    def PARTIAL_TAG(self, ast):
        return ast

    def TAG_OPEN(self, ast):
        return ast

    def TAG_CLOSE(self, ast):
        return ast

    def TAG(self, ast):
        return ast

    def MAIN(self, ast):
        return ast


def main(filename, startrule, trace=False, whitespace=None):
    import json
    with open(filename) as f:
        text = f.read()
    parser = HandlebarsParser(parseinfo=False)
    ast = parser.parse(
        text,
        startrule,
        filename=filename,
        trace=trace,
        whitespace=whitespace)
    print('AST:')
    print(ast)
    print()
    print('JSON:')
    print(json.dumps(ast, indent=2))
    print()

if __name__ == '__main__':
    import argparse
    import string
    import sys

    class ListRules(argparse.Action):
        def __call__(self, parser, namespace, values, option_string):
            print('Rules:')
            for r in HandlebarsParser.rule_list():
                print(r)
            print()
            sys.exit(0)

    parser = argparse.ArgumentParser(description="Simple parser for Handlebars.")
    parser.add_argument('-l', '--list', action=ListRules, nargs=0,
                        help="list all rules and exit")
    parser.add_argument('-t', '--trace', action='store_true',
                        help="output trace information")
    parser.add_argument('-w', '--whitespace', type=str, default=string.whitespace,
                        help="whitespace specification")
    parser.add_argument('file', metavar="FILE", help="the input file to parse")
    parser.add_argument('startrule', metavar="STARTRULE",
                        help="the start rule for parsing")
    args = parser.parse_args()

    main(
        args.file,
        args.startrule,
        trace=args.trace,
        whitespace=args.whitespace
    )
