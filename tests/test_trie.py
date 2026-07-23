import sys
import unittest
from importlib import import_module
from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parents[1] / "backend"
sys.path.append(str(BACKEND_DIR))

Trie = import_module("trie").Trie


class TrieTestCase(unittest.TestCase):
    def setUp(self):
        self.trie = Trie()

        self.trie.insert("iphone", 50)
        self.trie.insert("iphone 15", 100)
        self.trie.insert("iphone case", 80)
        self.trie.insert("ipad", 70)
        self.trie.insert("instagram", 60)

    def test_autocomplete_returns_matching_prefixes(self):
        suggestions = self.trie.autocomplete("iph")

        self.assertEqual(suggestions, [
            "iphone 15",
            "iphone case",
            "iphone"
        ])

    def test_autocomplete_ranks_by_frequency(self):
        suggestions = self.trie.autocomplete("ip")

        self.assertEqual(suggestions, [
            "iphone 15",
            "iphone case",
            "ipad",
            "iphone"
        ])

    def test_autocomplete_respects_limit(self):
        suggestions = self.trie.autocomplete("ip", limit=2)

        self.assertEqual(suggestions, [
            "iphone 15",
            "iphone case"
        ])

    def test_autocomplete_returns_empty_list_for_unknown_prefix(self):
        suggestions = self.trie.autocomplete("xyz")

        self.assertEqual(suggestions, [])

    def test_increment_frequency_updates_ranking(self):
        self.trie.increment_frequency("iphone")
        self.trie.increment_frequency("iphone")
        self.trie.increment_frequency("iphone")

        suggestions = self.trie.autocomplete("iph")

        self.assertEqual(suggestions, [
            "iphone 15",
            "iphone case",
            "iphone"
        ])

    def test_increment_frequency_returns_false_for_unknown_term(self):
        was_updated = self.trie.increment_frequency("unknown term")

        self.assertFalse(was_updated)

    def test_debug_mode_returns_terms_with_frequencies(self):
        suggestions = self.trie.autocomplete(
            "iph",
            include_frequencies=True
        )

        self.assertEqual(suggestions, [
            {
                "term": "iphone 15",
                "frequency": 100
            },
            {
                "term": "iphone case",
                "frequency": 80
            },
            {
                "term": "iphone",
                "frequency": 50
            }
        ])


if __name__ == "__main__":
    unittest.main()