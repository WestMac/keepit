import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
from src.ul_parser import ULParser

class TestULParser(unittest.TestCase):

    def test_single_ul(self):
        html = """
        <ul>
            <li>List item 1</li>
            <li>List item 2</li>
            <li>List item 3</li>
        </ul>
        """
        parser = ULParser()
        parser.feed(html)
        self.assertEqual(parser.result, [["List item 1", "List item 2", "List item 3"]])

    def test_nested_ul(self):
        html = """
        <ul>
            <li>List item 1</li>
            <li>
                <ul>
                    <li>Nested list item 1</li>
                    <li>Nested list item 2</li>
                </ul>
            </li>
            <li>List item 3</li>
        </ul>
        """
        parser = ULParser()
        parser.feed(html)
        self.assertEqual(parser.result, [["List item 1", ["Nested list item 1", "Nested list item 2"], "List item 3"]])

    def test_multiple_uls(self):
        html = """
        <ul>
            <li>List item 1</li>
            <li>List item 2</li>
        </ul>
        <ul>
            <li>List item 1</li>
            <li>List item 2</li>
        </ul>
        """
        parser = ULParser()
        parser.feed(html)
        self.assertEqual(parser.result, [
            ["List item 1", "List item 2"],
            ["List item 1", "List item 2"]
        ])

    def test_multiple_nested_uls(self):
        html = """
        <ul>
            <li>List item 1</li>
            <li>
                List item 2
                <ul>
                    <li>Nested list item 1</li>
                    <li>Nested list item 2</li>
                    <li>Nested list item 3</li>
                    <li>
                        Nested list item 4
                        <ul> 
                            <li>Deep nested list item 1</li>
                            <li>Deep nested list item 2</li>
                        </ul>
                    </li>
                </ul>
            </li>
            <li>List item 3</li>
        </ul>
        """
        parser = ULParser()
        parser.feed(html)
        self.assertEqual(parser.result, [
            ["List item 1", "List item 2",
                ["Nested list item 1", "Nested list item 2", "Nested list item 3", "Nested list item 4", 
                    ["Deep nested list item 1", "Deep nested list item 2"]
                ], 
            "List item 3"]
        ])


    def test_ul_with_text_between(self):
        html = """
        <ul>
            <li>List item 1</li>
            <li>List item 2</li>
        </ul>
        Some text here
        <ul>
            <li>List item 3</li>
            <li>List item 4</li>
        </ul>
        """
        parser = ULParser()
        parser.feed(html)
        self.assertEqual(parser.result, [
            ["List item 1", "List item 2"],
            ["List item 3", "List item 4"]
        ])

    def test_empty_ul(self):
        html = "<ul></ul>"
        parser = ULParser()
        parser.feed(html)
        self.assertEqual(parser.result, [[]])

    def test_ul_with_empty_li(self):
        html = """
        <ul>
            <li>List item 1</li>
            <li></li>
            <li>List item 3</li>
        </ul>
        """
        parser = ULParser()
        parser.feed(html)
        self.assertEqual(parser.result, [["List item 1", "", "List item 3"]])

    def test_ul_with_wrong_childrean_tag(self):
        html = """
        <ul>
            <li>List item 1</li>
            <div>Invalid List Item 1</div>
            <li>List item 3</li>
        </ul>
        """
        parser = ULParser()
        parser.feed(html)
        self.assertEqual(parser.result, [["List item 1", "List item 3"]])

    def test_ul_with_wrong_childrean_tag_with_nested_ul(self):
        html = """
        <ul>
            <li>List item 1</li>
            <div>
                Invalid List Item 1
                <ul>
                    <li>Nested in invalid item 1</li>
                    <li>Nested in invalid item 2</li>
                    <li>Nested in invalid item 3</li>
                    <li>Nested in invalid item 4</li>
                </ul>
            </div>
            <li>List item 3</li>
        </ul>
        """
        parser = ULParser()
        parser.feed(html)
        self.assertEqual(parser.result, [["List item 1", ['Nested in invalid item 1', 'Nested in invalid item 2', 'Nested in invalid item 3', 'Nested in invalid item 4'] ,"List item 3"]])
    
    def test_ul_without_closing_tag(self):
        html = """
        <ul>
            <li>List item 1</li>
            <div>Invalid List Item 1</div>
            <li>List item 3</li>
        """
        parser = ULParser()
        parser.feed(html)
        self.assertEqual(parser.result, [])

    def test_ul_with_tag_inside_li(self):
        html = """
        <ul>
            <li>List item 1</li>
            <li>
                <a href="test">List item 2</a>
                <ul></ul>
            </li>
            <li>List item 3</li>
        </ul>
        """
        parser = ULParser()
        parser.feed(html)
        self.assertEqual(parser.result, [['List item 1', 'List item 2', [], 'List item 3']])

if __name__ == "__main__":
    unittest.main()
