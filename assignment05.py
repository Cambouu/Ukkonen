# Suffixarrays und Suffixbaeume
###########################################################################
import argparse

###########################################################################
# SUFFIXTREE
# Your implementation
class Node():

    def __init__(self, suffixStart=0, suffixEnd=-1, suffixLink=None, isRoot=False):
        self.suffixStart = suffixStart
        self.suffixEnd = suffixEnd
        self.suffixLink = suffixLink
        self.isRoot = isRoot
        self.children = {}

    def getText(self, T, end):
        if self.suffixEnd == -1:
            return T[self.suffixStart:end]
        else:
            return T[self.suffixStart:self.suffixEnd]

    def splitNode(self, currentEdge, newEdge, activeLength, end):
        self.addChild(currentEdge, activeLength + self.suffixStart)
        self.addChild(newEdge, end)
        self.suffixEnd = activeLength + self.suffixStart

    def addChild(self, edge, suffixStart, suffixEnd=-1, suffixLink=None):
        self.children[edge] = Node(suffixStart=suffixStart, suffixEnd=suffixEnd, suffixLink=self)

##################################################################

def build_suffixtree(T):
    """
    INPUT: Text T
    OUTPUT:
    - Your suffix tree ST
    - leaves: list of number of leaves after each step
    - inner_nodes: list of number of inner nodes after each step
    """
    ST = Node(isRoot=True) # this should be your suffix tree
    # leaves = []
    # inner_nodes = []

    remaining = 0
    activeNode = ST
    activeEdge = ''
    activeLength = 0

    for end, c in enumerate(T):
        remaining += 1
        lastNodeSplitted = None # Temporal to address SuffixLinks

        while remaining > 0:
            if activeLength == 0:
                if c in activeNode.children:
                    activeEdge = c
                    activeLength += 1
                    break
                else:
                    activeNode.addChild(c, suffixStart=end)
                    remaining -= 1

            else:
                childNode = activeNode.children[activeEdge]
                edge_text = childNode.getText(T, end)
                if activeLength > len(edge_text):
                    activeNode = childNode
                    activeEdge = T[activeNode.suffixStart]
                    activeLength = 0

                elif c == edge_text[activeLength]:
                    activeLength += 1

                else:
                    childNode.splitNode(T[activeLength + childNode.suffixStart], c, activeLength, end) #FIXME
                    remaining -= 1
                    
                    if lastNodeSplitted is not None:
                        lastNodeSplitted.suffixLink = childNode
                    lastNodeSplitted = childNode

                    if activeNode.isRoot:
                        activeEdge = edge_text[1]
                        activeLength -= 1
                    else:
                        activeNode = activeNode.suffixLink
                    

        # leaves_count, inners_count = count_leaves_and_inners(ST)
        # leaves.append(leaves_count)
        # inner_nodes.append(inners_count)

    return ST, leaves, inner_nodes


def count_leaves_and_inners(node):
    leaves = 0
    inners = 0

    if len(node.children) == 0:
        leaves += 1

    else:
        if not node.isRoot:
            inners += 1

        for child in node.children.values():
            leaf, inner = count_leaves_and_inners(child)
            leaves += leaf
            inners += inner

    return leaves, inners


def print_tree(T, ST, i=0):
    i += 1
    if ST.isRoot:
        print('root')
    for child in ST.children.values():
        print('{0} {1}'.format('--' * i, child.getText(T, -1)))
        print_tree(T, child, i)

def get_text(args):
    if args.text is not None:
        return args.text
    with open(args.textfile, "r") as ftext:
        text = ftext.read()
    return text

def get_argument_parser():
    p = argparse.ArgumentParser(description="Ukonnen")
    txt = p.add_mutually_exclusive_group(required=True)
    txt.add_argument("-T", "--text",
        help="text to build suffix tree")
    txt.add_argument("-t", "--textfile",
        help="name of file containing text (will be read in one piece)")
    return p

def main(args):

    T = get_text(args)
    ST = test_suffixtree(T)

if __name__=="__main__":
    build_suffixtree('abac$')
    # main(get_argument_parser().parse_args())
