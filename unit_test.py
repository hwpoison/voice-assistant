import unittest
import intents_processor
from settings import Settings, Intents, load_settings


class Test(unittest.TestCase):

    def setUp(self):
        Settings.lang = "en"
        load_settings()
        Intents.hotwords = ["hey google", "okey"]
        Intents.context_list = {
            'CMD': 'test.py'
        }

        Intents.all_commands = {
            'view the thing {n}': {'ctrl_num': '{}'},
            'view that {n} times': {'ctrl_num': '{}'},
            'press total {n}': {'press': '{UP}'},
            'press some key': {'press': '{UP}'},
            'press space': {'press': '{SPACE}', "alternative": ["space"]}
        }
        Intents.literals.update({Intents.numbers[inum]: str(
            inum) for inum in range(0, len(Intents.numbers))})

    def test_list_to_or_regx_pattern(self):
        """ Returns OR list for a regex pattern """
        entry = ["word1", "word2", "word3", "word4"]
        result = intents_processor.list_to_or_regx_pattern(entry)
        expected = '(word1|word2|word3|word4*)'
        self.assertEqual(result, expected)

    def test_find_match_command(self):
        entry = "space"
        result = intents_processor.find_match_command(entry)
        expected = ({'press': '{SPACE}', 'alternative': [
                    'space'], 'args': False})
        self.assertEqual(result, expected)

    def test_match_and_filter_hotword(self):
        entry = "hey google do it!"
        result = intents_processor.match_and_filter_hotword(entry)
        self.assertEqual(result, 'do it!')

    def test_command_with_number(self):
        """ Command with number argument:
            >>> view the thing number two 
            references to 'view the thing' number '2'
        """
        entry = 'view the thing two'
        result = intents_processor.intent(entry, False)
        self.assertEqual(result, True)

    def test_command_with_number_and(self):
        """ Command with number argument:
            >>> view the thing number two 
            references to 'view the thing' number '2'
        """
        entry = 'view that two times'
        result = intents_processor.intent(entry, False)
        self.assertEqual(result, True)

    def test_command_with_number_without_it(self):
        """ Command with number argument:
            >>> view the thing number two 
            references to 'view the thing' number '2'
        """
        entry = 'press total'  # ignoring the {n} arg will produce a error
        result = intents_processor.intent(entry, False)
        self.assertEqual(result, False)

    def test_incomplete_command_with_number(self):
        """ Command with number argument:
            >>> view the thing number two 
            references to 'view the thing' number '2'
        """
        entry = 'view the thing'
        result = intents_processor.intent(entry, False)
        self.assertEqual(result, False)

    def test_press_key_command(self):
        """ Command with key to press """
        entry = 'hey google press space'
        result = intents_processor.intent(entry, True)
        self.assertEqual(result, True)

    def test_press_key_command_context(self):
        """ Command with key to press """
        entry = 'hey google press some key'
        result = intents_processor.intent(entry, True)
        self.assertEqual(result, True)


if __name__ == '__main__':
    unittest.main()
