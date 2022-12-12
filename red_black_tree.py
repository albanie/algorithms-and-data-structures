"""A minimalist Red-Black Tree implementation.

The code draws inspiration from several descriptions/code snippets for Red-Black Trees:
- https://en.wikipedia.org/wiki/Red%E2%80%93black_tree
- https://blog.boot.dev/python/red-black-tree-python/
- Chapter 13 of T. H. Cormen, et al., "Introduction to algorithms", MIT press, (2022)

We follow the Cormen et al. convention of allowing duplicate keys.

The code was implemented with assistance from GitHub Copilot.
"""


class Node:

    def __init__(self, key, parent=None, left=None, right=None, color=None):
        self.key = key
        self.parent = parent
        self.left = left
        self.right = right
        self.color = color

    def __repr__(self):
        summary = f"Node({self.key}, color={self.color})"
        if self.parent:
            summary += f" parent={self.parent.key}"
        if self.left:
            summary += f" left={self.left.key}"
        if self.right:
            summary += f" right={self.right.key}"
        return summary


class Nil(Node):
    """Nil node (used to represent the leaves of the tree)."""

    def __init__(self):
        super().__init__(key="Nil", parent=None, left=None, right=None, color="black")


class RedBlackTree:

    def __init__(self):
        # Use a single Nil node as a "sentinel" for all leaves
        self.nil = Nil()
        self.root = self.nil

    def __repr__(self):
        return f"RedBlackTree({self.root})"

    def search(self, key: int) -> Node:
        """Search for a node with a given key in the subtree of the given node.

        Args:
            key: the key to search for
        """
        node = self.root
        while node and node.key != key:
            if key < node.key:
                node = node.left
            else:
                node = node.right
        return node

    def minimum(self, node: Node) -> Node:
        """Find the minimum node in the subtree rooted at node.

        Args:
            node: the root of the subtree to search.

        Returns:
            The minimum node in the tree rooted at node.
        """
        while node.left is not self.nil:
            node = node.left
        return node

    def maximum(self, node: Node) -> Node:
        """Find the maximum node in the subtree rooted at node.

        Args:
            node: the root of the subtree to search.

        Returns:
            The maximum node in the tree.
        """
        while node.right is not self.nil:
            node = node.right
        return node

    def inorder(self, node: Node):
        """Perform an inorder traversal of the tree.

        Args:
            node: Node - the root of the tree to traverse.
        """
        if node != self.nil:
            self.inorder(node.left)
            print(node.key, end=" ")
            self.inorder(node.right)

    def preorder(self, node: Node):
        """Perform a preorder traversal of the tree rooted at node.

        Args:
            node: Node - the root of the tree to traverse.
        """
        if node != self.nil:
            print(node.key, end=" ")
            self.preorder(node.left)
            self.preorder(node.right)

    def postorder(self, node: Node):
        """Perform a postorder traversal of the tree rooted at node.

        Args:
            node: Node - the root of the tree to traverse.
        """
        if node is not None:
            self.postorder(node.left)
            self.postorder(node.right)
            print(node.key, end=" ")

    def rotate_left(self, u: Node):
        """Rotate the subtree rooted at u to the left."""
        v = u.right
        u.right = v.left
        if v.left != self.nil:
            v.left.parent = u
        v.parent = u.parent
        if not u.parent:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.left, u.parent = u, v

    def rotate_right(self, v: Node):
        """Rotate the subtree rooted at v to the right."""
        u = v.left
        v.left = u.right
        if u.right != self.nil:
            u.right.parent = v
        u.parent = v.parent
        if not v.parent:
            self.root = u
        elif v == v.parent.right:
            v.parent.right = u
        else:
            v.parent.left = u
        u.right, v.parent = v, u

    def insert(self, new_node: Node):
        """Insert a new node into the tree.

        Args:
            new_node: the node to insert.
        """

        # Typical Binary Search Tree insertion method
        node = self.root
        parent = None
        while not isinstance(node, Nil):
            parent = node
            node = node.left if new_node.key < node.key else node.right

        new_node.parent = parent

        if not parent:  # handle the case when the tree is empty
            self.root = new_node
        elif new_node.key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        # set Red-Black Tree node attributes
        new_node.left = self.nil
        new_node.right = self.nil
        new_node.color = "red"

        self.fix_insert_violations(new_node)

    def fix_insert_violations(self, node: Node):
        """Fix any Red-Black Tree insert violations.

        Args:
            node: the node that was inserted.
        """
        while node != self.root and node.parent.color == "red":
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                if uncle.color == "red":
                    node.parent.color = "black"
                    uncle.color = "black"
                    node.parent.parent.color = "red"
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self.rotate_left(node)
                    node.parent.color = "black"
                    node.parent.parent.color = "red"
                    self.rotate_right(node.parent.parent)
            else:
                uncle = node.parent.parent.left
                if uncle.color == "red":
                    node.parent.color = "black"
                    uncle.color = "black"
                    node.parent.parent.color = "red"
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self.rotate_right(node)
                    node.parent.color = "black"
                    node.parent.parent.color = "red"
                    self.rotate_left(node.parent.parent)
        self.root.color = "black"

    def shift_nodes(self, old_node: Node, new_node: Node):
        """Replace the subtree rooted at old_node with the subtree rooted at new_node.

        Args:
            old_node: the root of the subtree to replace.
            new_node: the root of the subtree to replace with.
        """
        if not old_node.parent:
            self.root = new_node
        elif old_node == old_node.parent.left:
            old_node.parent.left = new_node
        else:
            old_node.parent.right = new_node
        new_node.parent = old_node.parent

    def delete(self, node: Node):
        """Delete a node from the Red-Black Tree.

        Args:
            node: the node to delete.
        """
        original_color = node.color
        if node.left == self.nil:
            x = node.right
            self.shift_nodes(node, x)
        elif node.right == self.nil:
            x = node.left
            self.shift_nodes(node, x)
        else:
            v = self.minimum(node.right)
            original_color = v.color
            x = v.right
            if v.parent == node:
                x.parent = v
            else:
                self.shift_nodes(v, v.right)
                v.right = node.right
                v.right.parent = v
            self.shift_nodes(node, v)
            v.left = node.left
            v.left.parent = v
            v.color = node.color
        if original_color == "black":
            self.fix_delete_violations(x)

    def fix_delete_violations(self, node: Node):
        """Fix any Red-Black Tree delete violations.

        Args:
            node: the node that was deleted.
        """
        while node != self.root and node.color == "black":
            if node == node.parent.left:
                s = node.parent.right
                if s.color == "red":
                    s.color = "black"
                    node.parent.color = "red"
                    self.rotate_left(node.parent)
                    s = node.parent.right
                if s.left.color == "black" and s.right.color == "black":
                    s.color = "red"
                    node = node.parent
                else:
                    if s.right.color == "black":
                        s.left.color = "black"
                        s.color = "red"
                        self.rotate_right(s)
                        s = node.parent.right
                    s.color = node.parent.color
                    node.parent.color = "black"
                    s.right.color = "black"
                    self.rotate_left(node.parent)
                    node = self.root
            else:
                s = node.parent.left
                if s.color == "red":
                    s.color = "black"
                    node.parent.color = "red"
                    self.rotate_right(node.parent)
                    s = node.parent.left
                if s.right.color == "black" and s.left.color == "black":
                    s.color = "red"
                    node = node.parent
                else:
                    if s.left.color == "black":
                        s.right.color = "black"
                        s.color = "red"
                        self.rotate_left(s)
                        s = node.parent.left
                    s.color = node.parent.color
                    node.parent.color = "black"
                    s.left.color = "black"
                    self.rotate_right(node.parent)
                    node = self.root
        node.color = "black"


def main():
    rbt = RedBlackTree()
    insert_keys = [5, 3, 2, 7, 1, 8, 9, 12]
    node_list = [Node(key) for key in insert_keys]
    for node in node_list:
        rbt.insert(node)

    # print out traversals
    print(f"Inorder traversal")
    rbt.inorder(rbt.root)
    print("")
    print(f"Preorder traversal")
    rbt.preorder(rbt.root)
    print("")
    print(f"Postorder traversal")
    rbt.preorder(rbt.root)
    print("")

    node_to_delete = node_list[3]
    print(f"Deleting node {node_to_delete}")
    rbt.delete(node_to_delete)

    # print out traversal
    print(f"Inorder traversal after deletion")
    rbt.inorder(rbt.root)
    print("")

    # print out minimum and maximum
    print(f"Minimum key: {rbt.minimum(rbt.root).key}")
    print(f"Maximum key: {rbt.maximum(rbt.root).key}")

    """
    Print out:

    Inorder traversal
    1 2 3 5 7 8 9 12
    Preorder traversal
    3 2 1 7 5 9 8 12
    Postorder traversal
    3 2 1 7 5 9 8 12
    Deleting node Node(7, color=red) parent=3 left=5 right=9
    Inorder traversal after deletion
    1 2 3 5 8 9 12
    Minimum key: 1
    Maximum key: 12
    """


if __name__ == "__main__":
    main()
