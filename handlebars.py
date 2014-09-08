from handlebars_parser import HandlebarsParser


def compile(template):
    parser = HandlebarsParser(parseinfo=False)
    ast = parser.parse(
        template,
        'MAIN',
        filename=None,
        trace=False,
        whitespace=None)

    def render(data=None):
        return ast

    return render
