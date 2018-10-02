from unittest import TestCase

from mbq.metrics import utils


class TagsAsListTest(TestCase):
    def test_key_and_value_changed_to_strings(self):
        tags = utils.tags_as_list({
            1: 2,
        })
        self.assertEqual(tags, ['1:2'])

    def test_allow_missing_value(self):
        tags = utils.tags_as_list({
            'test': None,
        })
        self.assertEqual(tags, ['test'])

    def test_allow_many_tags(self):
        tags = utils.tags_as_list({
            'test1': None,
            'test2': 'dogs',
        })
        self.assertEqual(tags, ['test1', 'test2:dogs'])

    def test_input_list(self):
        tags = utils.tags_as_list(['tag1:value1', 'tag2:value2'])
        self.assertEqual(tags, ['tag1:value1', 'tag2:value2'])

    def test_input_tuple(self):
        tags = utils.tags_as_list(('tag1:value1', 'tag2:value2'))
        self.assertEqual(tags, ['tag1:value1', 'tag2:value2'])

    def test_input_none(self):
        tags = utils.tags_as_list(None)
        self.assertEqual(tags, [])
