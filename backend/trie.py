class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_term = False
        self.term = None
        self.frequency = 0


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, term, frequency):
        current_node = self.root

        for character in term:
            if character not in current_node.children:
                current_node.children[character] = TrieNode()

            current_node = current_node.children[character]

        current_node.is_end_of_term = True
        current_node.term = term
        current_node.frequency = frequency

    def autocomplete(self, prefix, limit=5, include_frequencies=False):
        prefix_node = self._find_prefix_node(prefix)

        if prefix_node is None:
            return []

        results = []
        self._collect_terms(prefix_node, results)

        results.sort(key=lambda item: item["frequency"], reverse=True)

        top_results = results[:limit]

        if include_frequencies:
            return top_results

        return [item["term"] for item in top_results]

    def _find_prefix_node(self, prefix):
        current_node = self.root

        for character in prefix:
            if character not in current_node.children:
                return None

            current_node = current_node.children[character]

        return current_node

    def _collect_terms(self, node, results):
        if node.is_end_of_term:
            results.append({
                "term": node.term,
                "frequency": node.frequency
            })

        for child_node in node.children.values():
            self._collect_terms(child_node, results)

    def increment_frequency(self, term):
        current_node = self.root

        for character in term:
            if character not in current_node.children:
                return False

            current_node = current_node.children[character]

        if not current_node.is_end_of_term:
            return False

        current_node.frequency += 1
        return True