import string
import math

alphUpper = list(string.ascii_uppercase)
alphLower = list(string.ascii_lowercase)
lettCount = [0] * 26
charCount = 0
lettProb = [0] * 26
lettEntr = [0] * 26
totalEntr = 0

with open('sample.txt', 'r') as file:
    while True:
        char = file.read(1)
        if not char:
            break
        if char.isalpha():
            charCount += 1
        for i in range(26):
            if char == alphUpper[i] or char == alphLower[i]:
                lettCount[i] += 1

print("Characters: ", charCount)
for i in range(26):
    if lettCount[i] > 0:
        lettProb[i] = lettCount[i] / charCount
        lettEntr[i] = -lettProb[i] * (math.log(lettProb[i], 2))
        totalEntr += lettEntr[i]

sortedProb = [{'char': alphUpper[i], 'probability': lettProb[i], 'count': lettCount[i]} for i in sorted(range(len(lettProb)), key=lambda k: lettProb[k], reverse=True)]
sortedProb = [item for item in sortedProb if item['probability'] > 0]

for item in sortedProb:
    print(item['char'], ": {:.3f}".format(item['probability']), " - Count:", item['count'])

class Node:
    def __init__(self, data, probability):
        self.left = None
        self.right = None
        self.data = data
        self.probability = probability
        self.code = ""

def build_huffman_tree(nodes):
    while len(nodes) > 1:
        nodes = sorted(nodes, key=lambda x: x.probability)
        left = nodes.pop(0)
        right = nodes.pop(0)
        merged = Node(left.data + right.data, left.probability + right.probability)
        merged.left = left
        merged.right = right
        nodes.append(merged)
    return nodes[0]

huffman_nodes = [Node(item['char'], item['probability']) for item in sortedProb]

huffman_tree = build_huffman_tree(huffman_nodes)

def assign_codes(node, code=""):
    if node is not None:
        node.code = code
        assign_codes(node.left, code + "0")
        assign_codes(node.right, code + "1")

assign_codes(huffman_tree)

L = 0;
print("\nBinary Codes:")
for item in sortedProb:
	node = next((x for x in huffman_nodes if x.data == item['char']), None)
	if node:
		print(item['char'], ":", node.code)
		L += item['probability']*len(node.code)
print("\nTotal Entropy - H(x): {:.3f}".format(totalEntr))
print("Average code length - L(x): {:.3f}".format(L))
CE = totalEntr/L
print("Compression Efficiency(Eff): {:.3f}".format(CE))
