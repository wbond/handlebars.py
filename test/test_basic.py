import unittest

import handlebars


# Ported from https://github.com/wycats/handlebars.js/blob/master/spec/basic.js
class TestBasic(unittest.TestCase):

    def should_compile_to(self, template, data, output, message=None):
        render = handlebars.compile(template)
        self.assertEqual(render(data), output, message)

    def test_plain_content(self):
        self.should_compile_to('Hello', None, 'Hello')

    def test_most_basic(self):
        self.should_compile_to("{{foo}}", {'foo': "foo"}, "foo")

    def test_escaping(self):
        self.should_compile_to("\\{{foo}}", {'foo': "food"}, "{{foo}}")
        self.should_compile_to("content \\{{foo}}", {'foo': "food"},
            "content {{foo}}")
        self.should_compile_to("\\\\{{foo}}", {'foo': "food"}, "\\food")
        self.should_compile_to("content \\\\{{foo}}", {'foo': "food"},
            "content \\food")
        self.should_compile_to("\\\\ {{foo}}", {'foo': "food"}, "\\\\ food")

    def test_compiling_with_a_basic_context(self):
        self.should_compile_to("Goodbye\n{{cruel}}\n{{world}}!",
            {'cruel': "cruel", 'world': "world"}, "Goodbye\ncruel\nworld!",
            "It works if all the required keys are provided")

    def test_compiling_with_an_undefined_context(self):
        self.should_compile_to("Goodbye\n{{cruel}}\n{{world.bar}}!", None,
            "Goodbye\n\n!")
        self.should_compile_to("{{#unless foo}}Goodbye{{../test}}{{test2}}{{/unless}}",
            None, "Goodbye")

    def test_comments(self):
        self.should_compile_to("{{! Goodbye}}Goodbye\n{{cruel}}\n{{world}}!",
            {'cruel': "cruel", 'world': "world"}, "Goodbye\ncruel\nworld!",
            "comments are ignored")


if __name__ == '__main__':
    unittest.main()
