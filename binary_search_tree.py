"""A minimalist Binary Search Tree implementation.

The code draws inspiration from several descriptions of Binary Search Trees:
- https://en.wikipedia.org/wiki/Binary_search_tree
- Chapter 12 of T. H. Cormen, et al., "Introduction to algorithms", MIT press, (2022)
- https://github.com/donsheehy/datastructures

We follow the Cormen et al. convention of allowing duplicate keys.
"""
from typing import Optional


class Node:

    def __init__(self, key, parent=None, left=None, right=None):
        self.key = key
        self.left = left
        self.right = right
        self.parent = parent


class BinarySearchTree:
    
    def __init__(self, root: Optional[Node] = None):
        self.root = root

    def maximum(self, u: Node):
        """Return the node with the largest key in the subtree rooted at the given node

        Args:
            u: the node to search from

        Returns:
            the node with the largest key
        """
        while u.right:
            u = u.right
        return u

    def minimum(self, u: Node):
        """Return the node with the smallest key in the subtree rooted at the given node

        Args:
            u: the node to search from

        Returns:
            the node with the smallest key
        """
        while u.left:
            u = u.left
        return u

    def insert(self, v: Node):
        """Insert the given node into the tree

        Args:
            v: the node to insert
        """
        u = self.root
        par = None
        while u:
            par = u
            u = u.left if v.key < u.key else u.right
        v.parent = par
        if not par:  # handle case when the BST is empty
            self.root = v
        elif v.key < par.key:
            par.left = v
        else:
            par.right = v

    def inorder(self, u: Node, visited: Optional[list] = None):
        """Complete an inorder traversal of the subtree rooted at u, appending
        each visited key to a list.

        Args:
            u: the root of the subtree at which the traversal will be performed
            visited: the list of visited keys.
        """
        if visited is None:
            visited = []
        if u.left:
            self.inorder(u.left, visited)
        visited.append(u.key)
        if u.right:
            self.inorder(u.right, visited)
        return visited

    def preorder(self, u: Node, visited: Optional[list] = None):
        """Complete a preorder traversal of the subtree rooted at u, appending
        each visited key to a list.

        Args:
            u: the root of the subtree at which the traversal will be performed
            visited: the list of visited keys.
        """
        if visited is None:
            visited = []
        visited.append(u.key)
        if u.left:
            self.preorder(u.left, visited)
        if u.right:
            self.preorder(u.right, visited)
        return visited

    def postorder(self, u: Node, visited: Optional[list] = None):
        """Complete a postorder traversal of the subtree rooted at u, appending
        each visited key to a list.

        Args:
            u: the root of the subtree at which the traversal will be performed
            visited: the list of visited keys.
        """
        if visited is None:
            visited = []
        if u.left:
            self.postorder(u.left, visited)
        if u.right:
            self.postorder(u.right, visited)
        visited.append(u.key)
        return visited

    def shift_nodes(self, old, src):
        if not old.parent:
            self.root = src
        elif old == old.parent.left:
            old.parent.left = src
        else:
            old.parent.right = src
        if src:
            src.parent = old.parent
            
    def successor(self, u):
        if u.right:
            succ = self.minimum(u.right)
        else:
            par = u.parent
            while par.left != u:
                u = par
                par = u.parent
            succ = par
        return succ
    
    def delete(self, u):
        if not u.left:
            self.shift_nodes(u, u.right)
        elif not u.right:
            self.shift_nodes(u, u.left)
        else:
            succ = self.minimum(u.right)
            if succ != u.right:
                self.shift_nodes(succ, succ.right)
                succ.right = u.right
                succ.right.parent = succ
            self.shift_nodes(u, succ)
            succ.left = u.left
            succ.left.parent = succ


def main():
    bst = BinarySearchTree()
    insert_keys = [5, 3, 2, 7, 1, 8, 9, 12]
    nodes = [Node(key) for key in insert_keys]
    for u in nodes:
        bst.insert(u)

    # print out traversals
    print(f"Inorder traversal")
    print(bst.inorder(bst.root))
    print(f"Preorder traversal")
    print(bst.preorder(bst.root))
    print(f"Postorder traversal")
    print(bst.postorder(bst.root))

    node_to_delete = nodes[3]
    print(f"Deleting node with key {node_to_delete.key}")
    bst.delete(node_to_delete)
    # print out updated traversal
    print(f"Inorder traversal after deletion")
    print(bst.inorder(bst.root))

    # print out minimum and maximum
    print(f"Minimum key: {bst.minimum(bst.root).key}")
    print(f"Maximum key: {bst.maximum(bst.root).key}")

    """
    Print out:

    Inorder traversal
    1 2 3 5 7 8 9 12
    Preorder traversal
    5 3 2 1 7 8 9 12
    Postorder traversal
    5 3 2 1 7 8 9 12
    Deleting node with key 7
    Inorder traversal after deletion
    1 2 3 5 8 9 12
    Minimum key: 1
    Maximum key: 12
    """


if __name__ == "__main__":
    main()
