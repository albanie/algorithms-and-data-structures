"""A minimalist Binary Search Tree implementation.

The code draws inspiration from several descriptions of Binary Search Trees:
- https://en.wikipedia.org/wiki/Binary_search_tree
- Chapter 12 of T. H. Cormen, et al., "Introduction to algorithms", MIT press, (2022)
- https://github.com/donsheehy/datastructures

We follow the Cormen et al. convention of allowing duplicate keys.

If you would like a fully object-oriented Binary Search Tree implementation, I recommend:
- https://github.com/donsheehy/datastructures
"""


class BinarySearchTree:

    def __init__(self, root=None):
        self.root = root


class Node:

    def __init__(self, key, parent=None, left=None, right=None):
        self.key = key
        self.parent = parent
        self.left = left
        self.right = right

    def __str__(self):
        summary = f"Node({self.key})"
        if self.parent:
            summary += f" parent={self.parent.key}"
        if self.left:
            summary += f" left={self.left.key}"
        if self.right:
            summary += f" right={self.right.key}"
        return summary


def insert(bst: BinarySearchTree, new_node: Node):
    """Insert a new node into the tree.

    Args:
        bst: the tree to insert into.
        new_node: the node to insert.
    """
    node = bst.root
    parent = None
    while node:
        parent = node
        node = node.left if new_node.key < node.key else node.right
    new_node.parent = parent
    if not parent:  # handle the case when the tree is empty
        bst.root = new_node
    elif new_node.key < parent.key:
        parent.left = new_node
    else:
        parent.right = new_node


def search(key: int, node: Node):
    """Search for a node with a given key in the subtree of the given node.

    Args:
        key: the key to search for.
        node: the node whose subtree we wish to search
    """
    while node and node.key != key:
        if key < node.key:
            node = node.left
        else:
            node = node.right
    return node


def delete(bst: BinarySearchTree, node: Node):
    """Delete a node from the tree.

    Args:
        bst: the tree to delete from.
        node: the node to delete.
    """
    if not node.right:  # node to be deleted has no right child
        shift_nodes(bst, node, node.right)  # node to be deleted has no left child
    elif not node.left:
        shift_nodes(bst, node, node.right)
    else:  # node to be deleted has both a left and right child
        successor = minimum(node.right)
        if successor != node.right:
            shift_nodes(bst, successor, successor.right)
            successor.right = node.right
            successor.right.parent = successor
        shift_nodes(bst, node, successor)
        successor.left = node.left
        successor.left.parent = successor


def shift_nodes(bst: BinarySearchTree, old_node: Node, new_node: Node):
    """Shift the nodes from the subtree at new_node to the position of old_node.

    Args:
        bst: the tree to shift the nodes in.
        old_node: the node to be replaced.
        new_node: the node (and subtree) that is shifted.
    """
    if not old_node.parent:
        bst.root = new_node
    elif old_node == old_node.parent.left:
        old_node.parent.left = new_node
    else:
        old_node.parent.right = new_node
    if new_node:
        new_node.parent = old_node.parent


def minimum(node: Node):
    """Find the minimum node in the subtree rooted at node.

    Args:
        node: Node - the root of the tree to search.
    """
    while node.left:
        node = node.left
    return node


def maximum(node: Node):
    """Find the maximum node in the subtree rooted at node.

    Args:
        node: Node - the root of the tree to search.
    """
    while node.right:
        node = node.right
    return node


def inorder(node):
    """Perform an inorder traversal of the tree rooted at node.

    Args:
        node: Node - the root of the tree to traverse.
    """
    if node is not None:
        inorder(node.left)
        print(node.key, end=" ")
        inorder(node.right)


def preorder(node):
    """Perform a preorder traversal of the tree rooted at node.

    Args:
        node: Node - the root of the tree to traverse.
    """
    if node is not None:
        print(node.key, end=" ")
        preorder(node.left)
        preorder(node.right)


def postorder(node):
    """Perform a postorder traversal of the tree rooted at node.

    Args:
        node: Node - the root of the tree to traverse.
    """
    if node is not None:
        postorder(node.left)
        postorder(node.right)
        print(node.key, end=" ")


def main():
    bst = BinarySearchTree()
    insert_keys = [5, 3, 2, 7, 1, 8, 9, 12]
    node_list = [Node(key) for key in insert_keys]
    for node in node_list:
        insert(bst, node)

    # print out traversals
    print(f"Inorder traversal")
    inorder(bst.root)
    print("")
    print(f"Preorder traversal")
    preorder(bst.root)
    print("")
    print(f"Postorder traversal")
    preorder(bst.root)
    print("")

    node_to_delete = node_list[3]
    print(f"Deleting node {node_to_delete}")
    delete(bst, node_to_delete)

    # print out traversal
    print(f"Inorder traversal after deletion")
    inorder(bst.root)
    print("")

    # print out minimum and maximum
    print(f"Minimum key: {minimum(bst.root).key}")
    print(f"Maximum key: {maximum(bst.root).key}")

    """
    Print out:

    Inorder traversal
    1 2 3 5 7 8 9 12
    Preorder traversal
    5 3 2 1 7 8 9 12
    Postorder traversal
    5 3 2 1 7 8 9 12
    Deleting node Node(7) parent=5 right=8
    Inorder traversal after deletion
    1 2 3 5 8 9 12
    Minimum key: 1
    Maximum key: 12
    """


if __name__ == "__main__":
    main()
