import processor, commands
import unittest


class Test(unittest.TestCase):
    
    def setUp(self):
        commands.hotwords = ["hey google", "okey"]
        commands.context_list = {
            'CMD':'test.py'
        }
        commands.numbers = [
            'zero','one','two','three','four',
            'five','six','seven','eight','nine','ten']
            
        commands.command_list = {
            'view the thing ([0-9])':{'func':commands.ctrl_num},
            'press some key':{'press':'{UP}', 'context':'CMD'},
            ('press space', 'space'): {'press':'{SPACE}'}
        }
        
    def test_or_regx_pattern(self):
        """ Returns OR list for a regex pattern """
        entry = ["word1", "word2", "word3", "word4"]
        result = processor.or_regx_pattern(entry)
        expected = '(word1|word2|word3|word4*)'
        self.assertEqual(result, expected)
    
    def test_find_command(self):
       entry = "space"
       result = processor.find_command(entry)
       expected = {'press':'{SPACE}'}
       self.assertEqual(result, expected)
       
    def test_filter_hotword(self):
        entry = "hey google do it!"
        result = processor.filter_hotword(entry)
        self.assertEqual(result, 'do it!')
        
    def test_number(self):
        entry = 'actually are three'
        result = processor.natural_to_int(entry)
        expected = 'actually are 3'
        self.assertEqual(result, expected)
        
    def test_get_int_args(self):
        """ Split text content and number"""
        entry = "view the thing 2"
        result = processor.get_int_args(entry)
        expected = 2
        self.assertEqual(result, expected)
    
    def test_command_with_number(self):
        """ Command with number argument:
            >>> view the thing number two 
            references to 'view the thing' number '2'
        """
        entry = 'view the thing two'
        result = processor.run_command(entry, False)
        self.assertEqual(result, True)
    
    def test_incomplete_command_with_number(self):
        """ Command with number argument:
            >>> view the thing number two 
            references to 'view the thing' number '2'
        """
        entry = 'view the thing'
        result = processor.run_command(entry, False)
        self.assertEqual(result, False)
        
    def test_press_key_command(self):
        """ Command with key to press """
        entry = 'hey google press space'
        result = processor.run_command(entry, True)
        self.assertEqual(result, True)

    def test_press_key_command_context(self):
        """ Command with key to press """
        entry = 'hey google press some key'
        result = processor.run_command(entry, True)
        self.assertEqual(result, True)
    
    
if __name__ == '__main__':
    unittest.main()