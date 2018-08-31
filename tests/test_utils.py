from unittest import TestCase

from mbq.metrics import utils


class TagDictToListTest(TestCase):
    def test_key_and_value_changed_to_strings(self):
        tags = utils.tag_dict_to_list({
            1: 2,
        })
        self.assertEqual(tags, ['1:2'])

    def test_allow_missing_value(self):
        tags = utils.tag_dict_to_list({
            'test': None,
        })
        self.assertEqual(tags, ['test'])

    def test_allow_many_tags(self):
        tags = utils.tag_dict_to_list({
            'test1': None,
            'test2': 'dogs',
        })
        self.assertEqual(set(tags), {'test1', 'test2:dogs'})
