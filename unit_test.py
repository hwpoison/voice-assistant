import command_processor
from settings import Settings, load_settings
import unittest


class Test(unittest.TestCase):

    def setUp(self):
        global lang
        Settings.lang = "en"
        load_settings()
        Settings.hotwords = ["hey google", "okey"]
        Settings.context_list = {
            'CMD': 'test.py'
        }

        Settings.all_commands = {
            'view the thing {n}': {'ctrl_num': '{}'},
            'view that {n} times': {'ctrl_num': '{}'},
            'press total {n}': {'press': '{UP}'},
            'press some key': {'press': '{UP}'},
            'press space': {'press': '{SPACE}', "alternative": ["space"]}
        }
        Settings.literals.update({Settings.numbers[inum]: str(
            inum) for inum in range(0, len(Settings.numbers))})

    def test_list_to_or_regx_pattern(self):
        """ Returns OR list for a regex pattern """
        entry = ["word1", "word2", "word3", "word4"]
        result = command_processor.list_to_or_regx_pattern(entry)
        expected = '(word1|word2|word3|word4*)'
        self.assertEqual(result, expected)

    def test_find_match_command(self):
        entry = "space"
        result = command_processor.find_match_command(entry)
        expected = ({'press': '{SPACE}', 'alternative': [
                    'space'], 'args': False})
        self.assertEqual(result, expected)

    def test_match_and_filter_hotword(self):
        entry = "hey google do it!"
        result = command_processor.match_and_filter_hotword(entry)
        self.assertEqual(result, 'do it!')

    def test_command_with_number(self):
        """ Command with number argument:
            >>> view the thing number two 
            references to 'view the thing' number '2'
        """
        entry = 'view the thing two'
        result = command_processor.intent(entry, False)
        self.assertEqual(result, True)

    def test_command_with_number_and(self):
        """ Command with number argument:
            >>> view the thing number two 
            references to 'view the thing' number '2'
        """
        entry = 'view that two times'
        result = command_processor.intent(entry, False)
        self.assertEqual(result, True)

    def test_command_with_number_without_it(self):
        """ Command with number argument:
            >>> view the thing number two 
            references to 'view the thing' number '2'
        """
        entry = 'press total'  # ignoring the {n} arg will produce a error
        result = command_processor.intent(entry, False)
        self.assertEqual(result, False)

    def test_incomplete_command_with_number(self):
        """ Command with number argument:
            >>> view the thing number two 
            references to 'view the thing' number '2'
        """
        entry = 'view the thing'
        result = command_processor.intent(entry, False)
        self.assertEqual(result, False)

    def test_press_key_command(self):
        """ Command with key to press """
        entry = 'hey google press space'
        result = command_processor.intent(entry, True)
        self.assertEqual(result, True)

    def test_press_key_command_context(self):
        """ Command with key to press """
        entry = 'hey google press some key'
        result = command_processor.intent(entry, True)
        self.assertEqual(result, True)


if __name__ == '__main__':
    unittest.main()
