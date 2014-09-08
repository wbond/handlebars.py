# Handlebars.py

A unfished port of Handlebars.js to Python using Grako.

I started this project after porting pybars to Python 3 and maintaining it for
a while. Unfortunately pybars is licensed via the LGPL, and the original
maintainers have no interest in the Python 3 fork. It uses pymeta which also
does not support Python 3.

## Current Status

I have taken a first pass at the grammar for Handlebars 2.0. Using Grako, this
generates a parser which results in an AST that should contain the information
necessary to generate Python code to generate the appropriate HTML.

## Building

```bash
pip install grako
```

Generate the parser from the grammar:

```bash
python -m grako Handlebars.ebnf > handlebars_parser.py
```

Generate the AST for the template:

```bash
python handlebars_parser.py template.handlebars MAIN
```

## Tests

None of the tests currently work since the rendering portion of the project
has not been started yet.

```bash
python -m unittest
```

## License

MIT - see LICENSE for text
