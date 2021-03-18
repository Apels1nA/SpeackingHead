import unittest
from resources.instruments import *

class TestInstruments(unittest.TestCase):

    def test_recognize_lang(self):
        self.assertEqual(recognize_lang('ban'), 'eng')
        self.assertEqual(recognize_lang('бан'), 'rus')
        self.assertEqual(recognize_lang(''), False)
        self.assertEqual(recognize_lang('1'), False)
        self.assertEqual(recognize_lang('1d'), False)

    def test_recognize_command(self):
        self.assertEqual(recognize_command(text='!ban [id237350735|@pequil]', peer_id=2000000001, echo=False), [True, 6])
        self.assertEqual(recognize_command(text='! ban [id237350735|@pequil]', peer_id=2000000001, echo=False), [False, 'Not command'])
        self.assertEqual(recognize_command(text='!haha [id237350735|@pequil]', peer_id=2000000001, echo=False), [False, 'Not command'])
        self.assertEqual(recognize_command(text='gg', peer_id=2000000001, echo=False), [False, 'Not command'])
        self.assertEqual(recognize_command(text='', peer_id=2000000001, echo=False), [False, 'Not command'])
        self.assertEqual(recognize_command(text='!!!!!', peer_id=2000000001, echo=False), [False, 'Not command'])

    def test_validate_arg_time(self):
        #Если параметры времени не введены, функция validate_arg_time() не вызывается
        self.assertEqual(validate_arg_time(time='0m'), (True, {'time': {'count': 1, 'unit': 'h'}}))
        self.assertEqual(validate_arg_time(time='0d'), (True, {'time': {'count': 1, 'unit': 'h'}}))
        self.assertEqual(validate_arg_time(time='0h'), (True, {'time': {'count': 1, 'unit': 'h'}}))
        self.assertEqual(validate_arg_time(time='0м'), (True, {'time': {'count': 1, 'unit': 'h'}}))
        self.assertEqual(validate_arg_time(time='0ч'), (True, {'time': {'count': 1, 'unit': 'h'}}))
        self.assertEqual(validate_arg_time(time='0д'), (True, {'time': {'count': 1, 'unit': 'h'}}))

        self.assertEqual(validate_arg_time(time='1m'), (True, {'time': {'count': 1, 'unit': 'm'}}))
        self.assertEqual(validate_arg_time(time='1h'), (True, {'time': {'count': 1, 'unit': 'h'}}))
        self.assertEqual(validate_arg_time(time='1d'), (True, {'time': {'count': 1, 'unit': 'd'}}))
        self.assertEqual(validate_arg_time(time='1м'), (True, {'time': {'count': 1, 'unit': 'м'}}))
        self.assertEqual(validate_arg_time(time='1ч'), (True, {'time': {'count': 1, 'unit': 'ч'}}))
        self.assertEqual(validate_arg_time(time='1д'), (True, {'time': {'count': 1, 'unit': 'д'}}))

        self.assertEqual(validate_arg_time(time='10m'), (True, {'time': {'count': 10, 'unit': 'm'}}))
        self.assertEqual(validate_arg_time(time='10h'), (True, {'time': {'count': 10, 'unit': 'h'}}))
        self.assertEqual(validate_arg_time(time='10d'), (True, {'time': {'count': 10, 'unit': 'd'}}))
        self.assertEqual(validate_arg_time(time='10м'), (True, {'time': {'count': 10, 'unit': 'м'}}))
        self.assertEqual(validate_arg_time(time='10ч'), (True, {'time': {'count': 10, 'unit': 'ч'}}))
        self.assertEqual(validate_arg_time(time='10д'), (True, {'time': {'count': 10, 'unit': 'д'}}))

        self.assertEqual(validate_arg_time(time='100m'), (False, {}))
        self.assertEqual(validate_arg_time(time='-1h'), (False, {}))
        self.assertEqual(validate_arg_time(time='1:d'), (False, {}))
        self.assertEqual(validate_arg_time(time='10r'), (False, {}))
        self.assertEqual(validate_arg_time(time='---'), (False, {}))
        self.assertEqual(validate_arg_time(time='+-d'), (False, {}))

    def test_validate_arg_link(self):
        self.assertEqual(validate_arg_link(raw=[4, 2513, 2629649, 2000000001, 1616069193, '!ban', {'from': '294211206', 'mentions': [267398968], 'marked_users': [[1, [267398968]]]}, {'reply': '{"conversation_message_id":2280}', 'fwd': '0_0'}, 0], link='[]', scenario=1), (True, {'links': {'from_id': '294211206', 'intruder_id': '267398968'}}))

        self.assertEqual(validate_arg_link(raw=[4, 2511, 532497, 2000000001, 1616068945, '!ban [id237350735|@pequil]', {'from': '294211206', 'mentions': [237350735], 'marked_users': [[1, [237350735]]]}, {}, 0], link='[id237350735|@pequil]', scenario=2), (True, {'links': {'from_id': '294211206', 'intruder_id': '237350735'}}))
        self.assertEqual(validate_arg_link(raw=[4, 2516, 532497, 2000000001, 1616069409, '!ban @pequilasdf', {'from': '294211206'}, {}, 0], link='@pequilasdf', scenario=2), (False, {}))
        self.assertEqual(validate_arg_link(raw=[4, 2517, 532497, 2000000001, 1616069507, '!ban https://vk.com/id237350735', {'from': '294211206'}, {}, 0], link='https://vk.com/id237350735', scenario=2), (False, {}))
        self.assertEqual(validate_arg_link(raw=[4, 2519, 532497, 2000000001, 1616069597, '!ban [[id237350735|@pequil]', {'from': '294211206', 'mentions': [237350735], 'marked_users': [[1, [237350735]]]}, {}, 0], link='[[id237350735|@pequil]', scenario=2), (False, {}))

if __name__ == "__main__":
    unittest.main()