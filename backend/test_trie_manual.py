from trie import Trie


trie = Trie()

trie.insert("iphone", 50)
trie.insert("iphone 15", 100)
trie.insert("iphone case", 80)
trie.insert("ipad", 70)
trie.insert("instagram", 60)

print(trie.autocomplete("iph"))
print(trie.autocomplete("ip"))
print(trie.autocomplete("inst"))
print(trie.autocomplete("x"))