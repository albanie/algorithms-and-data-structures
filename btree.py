"""A (relatively) lightweight B-tree implementation.

The code draws inspiration from several descriptions of Binary Search Trees:
- Chapter 18 of T. H. Cormen, et al., "Introduction to algorithms", MIT press (2022)
- Chapter 7 of Elementary Algorithms by Liu Xinyu https://github.com/liuxinyu95/AlgoXY

Note: the behaviour is not defined for duplicate keys.
"""

import argparse
from pathlib import Path


class Node:

    def __init__(self, keys=None, children=None, is_leaf=True):
        self.keys = keys if keys else []
        self.children = children if children else []
        self.is_leaf = is_leaf

    def is_full(self, t):
        """Check if the node is full (i.e. has 2t-1 keys).

        Args:
            t: the minimum degree of the B-tree.

        Returns:
            True if the node is full, False otherwise.
        """
        return len(self.keys) == 2 * t - 1

    def __str__(self):
        summary = f"Node({self.keys})"
        if self.children:
            summary += f" with {len(self.children)} children"
        return summary


class Btree:

    def __init__(self, t, root=None, verbose=False):
        """Create a B-tree with minimum degree t.
        """
        self.t = t
        self.root = root
        self.verbose = verbose

    def search(self, u, key):
        """Find the node containing key in the subtree rooted at u

        Args:
            u: the root of the subtree to search.
            key: the key to search for.

        Returns:
            The node containing key, together with the position of the key
            or None if key is not in the tree.
        """
        # linear scan to find index of key
        i = 0
        while i < len(u.keys) and key > u.keys[i]:
            i += 1
        if i < len(u.keys) and key == u.key[i]:
            return (u, i)
        if u.is_leaf:
            return None
        self.read_block(u.children[i])
        return self.search(u.children[i], key)

    def read_block(self, node: Node):
        if self.verbose:
            print(f"Performed I/O operation to read block containing {node} from disk")

    def write_block(self, node: Node):
        if self.verbose:
            print(f"Performed I/O operation to write block containing {node} to disk")

    def insert(self, key):
        """Insert key into the B-tree.

        Args:
            key: the key to insert.
        """
        root = self.root
        if root.is_full(t=self.t):  # root has 2t - 1 keys
            root = self.split_root()
        self.insert_not_full(root, key)

    def split_root(self):
        """
        Split the root of the B-tree.

        Returns:
            The new root of the B-tree.
        """
        new_root = Node()
        new_root.is_leaf = False
        new_root.children = [self.root]
        self.root = new_root
        self.split_child(new_root, 0)
        return new_root

    def insert_not_full(self, u: Node, key):
        """Insert key into the subtree rooted at u, which is assumed
        to be not full.

        Args:
            u: the root of the subtree to insert into.
            key: the key to insert.
        """
        i = 0
        while i < len(u.keys) and key > u.keys[i]:
            i += 1
        if u.is_leaf:
            u.keys.insert(i, key)
            self.write_block(u)
        else:
            self.read_block(u.children[i])
            if u.children[i].is_full(t=self.t):
                self.split_child(u, i)
                i = i if key <= u.keys[i] else i+ 1
            self.insert_not_full(u.children[i], key)

    def split_child(self, u: Node, i: int):
        """Split the child of u at index i.

        Args:
            u: the parent node.
            i: the index of the child to split.
        """
        t = self.t
        full_node = u.children[i]
        new_node = Node()
        new_node.is_leaf = full_node.is_leaf
        new_node.keys = full_node.keys[t:]
        if not full_node.is_leaf:
            new_node.children = full_node.children[t:]
        u.children.insert(i + 1, new_node)
        u.keys.insert(i, full_node.keys[t - 1])  # median
        full_node.keys = full_node.keys[:t - 1]
        full_node.children = full_node.children[:t]
        self.write_block(full_node)
        self.write_block(new_node)
        self.write_block(u)

    def delete(self, u: Node, key):
        assert len(u.keys) >= self.t  or u == self.root, (
            "The node u must have at least t keys or be the root"
        )
        i = 0
        while i < len(u.keys) and key > u.keys[i]:
            i += 1

        # handle cases
        if u.is_leaf:  # case 1
            if i < len(u.keys) and key == u.keys[i]:
                u.keys.pop(i)
                self.write_block(u)
            else:
                raise KeyError(f"Key {key} not found in the tree")
            return
        # u is not a leaf
        if i < len(u.keys) and key == u.keys[i]:  # case 2
            if len(u.children[i].keys) >= self.t:  # case 2a
                # pred_key = self.predecessor(key, u.children[i])
                pred_key = self.maximum(u.children[i])
                self.delete(u.children[i], pred_key)
                u.keys[i] = pred_key
            elif len(u.children[i+1].keys) >= self.t: # case 2b
                # succ_key = self.successor(key, u.children[i+1])
                # succ_key = self.minimum(key, u.children[i+1])
                succ_key = self.minimum(u.children[i+1])
                self.delete(u.children[i+1], succ_key)
                u.keys[i] = succ_key
            else:  # case 2c, both children have t-1 keys
                self.merge_children(u, i)
                if u == self.root and not u.keys:
                    # height of the tree 
                    self.root = u.children[0]
                self.delete(u.children[i], key)
        else: # case 3 (key not in u)
            if len(u.children[i].keys) >= self.t:  
                self.delete(u.children[i], key)  # recurse
            elif self.has_sibling_with_at_least_t_keys(u, i): # case 3a
                j = self.index_of_sibling_with_at_least_t_keys(u, i)
                if j == i + 1:  # right sibling has at least t keys
                    u.children[i].keys.append(u.keys[i])
                    u.keys[i] = u.children[j].keys.pop(0)
                    if not u.children[j].is_leaf:
                        u.children[i].children.append(u.children[j].children.pop(0))
                else:  # left sibling has at least t keys
                    u.children[i].keys.insert(0, u.keys[j])
                    u.keys[j] = u.children[j].keys.pop()
                    if not u.children[j].is_leaf:
                        u.children[i].children.insert(0, u.children[j].children.pop())
                self.delete(u.children[i], key)
            else: # u is not a leaf and both siblings have t-1 keys
                if i > 0:  # we merge with left sibling
                    self.merge_children(u, i - 1)
                    i -= 1 # we now have one less child, so we shift over
                else:  # we merge with right sibling
                    self.merge_children(u, i)
                if u == self.root and not u.keys:
                    # reduce height of the tree
                    self.root = u.children[0]
                self.delete(u.children[i], key)

    def has_sibling_with_at_least_t_keys(self, u: Node, i: int):
        """Check if child i of u has a sibling with at least t keys.

        Args:
            u: the parent node.
            i: the index of the child to check.

        Returns:
            True if child i of u has a sibling with at least t keys.
        """
        left_sibling_has_at_least_t_keys = i > 0 and len(u.children[i - 1].keys) >= self.t
        right_sibling_has_at_least_t_keys = (i < len(u.children) - 1 and
                                             len(u.children[i+1].keys) >= self.t)
        return left_sibling_has_at_least_t_keys or right_sibling_has_at_least_t_keys

    def index_of_sibling_with_at_least_t_keys(self, u: Node, i: int):
        """Compute the index of the sibling of u with at least t keys.

        Args:
            u: the parent node.
            i: the index of the child of u.

        Returns:
            The index of the sibling of u with at least t keys.
        """
        if i > 0 and len(u.children[i-1].keys) >= self.t:
            return i - 1
        if i < len(u.children) - 1 and len(u.children[i+1].keys) >= self.t:
            return i + 1
        raise ValueError("No sibling of u has at least t keys")

    def merge_children(self, u: Node, i: int):
        """Merge the children of u at index i and i+1.

        Args:
            u: the parent node.
            i: the index of the first child to merge.
        """
        median_key = u.keys.pop(i)
        u.children[i].keys.append(median_key)
        u.children[i].keys.extend(u.children[i+1].keys)
        if not u.children[i].is_leaf:
            u.children[i].children.extend(u.children[i+1].children)
        u.children.pop(i+1)

    def inorder(self, node: Node):
        """Perform an inorder traversal of the B-tree.

        Args:
            node: Node - the root of the tree to traverse.
        """
        for i in range(len(node.keys)):
            if not node.is_leaf:
                self.inorder(node.children[i])
            print(node.keys[i], end=" ")

        # don't forget the last child (there are more children than keys)
        if not node.is_leaf:
            self.inorder(node.children[-1])

    def preorder(self, node: Node):
        """Perform a preorder traversal of the B-tree.

        Args:
            node: Node - the root of the tree to traverse.
        """
        for key in node.keys:
            print(key, end=" ")
        if not node.is_leaf:
            for child in node.children:
                self.preorder(child)

    def postorder(self, node: Node):
        """Perform a postorder traversal of the B-tree.

        Args:
            node: Node - the root of the tree to traverse.
        """
        if not node.is_leaf:
            for child in node.children:
                self.postorder(child)
        for key in node.keys:
            print(key, end=" ")

    def minimum(self, node: Node) -> Node:
        """Find the minimum key in the subtree rooted at node.

        Args:
            node: the root of the subtree to search.

        Returns:
            The minimum key in the tree rooted at node.
        """
        while not node.is_leaf:
            node = node.children[0]
        return node.keys[0]

    def maximum(self, node: Node) -> Node:
        """Find the maximum key in the subtree rooted at node.

        Args:
            node: the root of the subtree to search.

        Returns:
            The maximum key in the subtree.
        """
        while not node.is_leaf:
            node = node.children[-1]
        return node.keys[-1]

    def viz_btree(self, dest_path: Path, refresh: bool = False):
        # We only perform the import here to prevent people from having to install
        # graphviz if they don't want to visualise the tree.
        import pygraphviz as pgv

        if dest_path.exists() and not refresh:
            print(f"Visualisation already exists at {dest_path}, skipping")
            return

        def key_str(keys):
            return " , ".join([str(key) for key in keys])

        def render_preorder(node, parent, pgv_graph):
            pgv_graph.add_node(key_str(node.keys), shape="rectangle", style="filled",
                               fillcolor="#fcf0cf")
            if parent is not None:
                pgv_graph.add_edge(key_str(parent.keys), key_str(node.keys))
            for child in node.children:
                render_preorder(node=child, parent=node, pgv_graph=pgv_graph)

        # Create a new Graph object
        pgv_graph = pgv.AGraph(directed=False)
        render_preorder(node=self.root, parent=None, pgv_graph=pgv_graph)
        print(f"Saving visualisation to {dest_path}")
        pgv_graph.draw(dest_path, prog="dot")


def main():
    # pylint: disable=line-too-long
    # flake8: noqa: E501
    parser = argparse.ArgumentParser()
    parser.add_argument("--viz", action="store_true", help="visualise the tree with pygraphviz")
    args = parser.parse_args()

    btree = Btree(t=2, root=Node(is_leaf=True))
    insert_keys = [5, 3, 2, 7, 1, 8, 9, 12, 13, 4, 0, 6, -1, 19, 24, 25, -2, -3, -4, -5]
    print("Keys to be inserted:")
    print(insert_keys)
    for key in insert_keys:
        btree.insert(key)

    # print out traversals
    print(f"Inorder traversal")
    btree.inorder(btree.root)
    print("")
    print(f"Preorder traversal")
    btree.preorder(btree.root)
    print("")
    print(f"Postorder traversal")
    btree.postorder(btree.root)
    print("")

    if args.viz:
        dest_path = Path("figs/btree.png")
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        btree.viz_btree(dest_path=dest_path, refresh=True)

    keys_to_delete = [2, 5, 6, 7, 0, 1, 3, 4, 8, 9, 12, 13, 19, 24, 25]
    print("Keys to be deleted:")
    print(keys_to_delete)
    for key in keys_to_delete:
        btree.delete(btree.root, key)

    if args.viz:
        dest_path = Path("figs/btree-after-deletions.png")
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        btree.viz_btree(dest_path=dest_path, refresh=True)

    print(f"Print out minimum and maximum values")
    print(f"Minimum key: {btree.minimum(btree.root)}")
    print(f"Maximum key: {btree.maximum(btree.root)}")

    """
    Print out:

    Keys to be inserted:
    [5, 3, 2, 7, 1, 8, 9, 12, 13, 4, 0, 6, -1, 19, 24, 25, -2, -3, -4, -5]
    Inorder traversal
    -5 -4 -3 -2 -1 0 1 2 3 4 5 6 7 8 9 12 13 19 24 25 
    Preorder traversal
    1 7 -3 -1 -5 -4 -2 0 3 2 4 5 6 9 13 8 12 19 24 25 
    Postorder traversal
    -5 -4 -2 0 -3 -1 2 4 5 6 3 8 12 19 24 25 9 13 1 7 
    Saving visualisation to figs/btree.png
    Keys to be deleted:
    [2, 5, 6, 7, 0, 1, 3, 4, 8, 9, 12, 13, 19, 24, 25]
    Saving visualisation to figs/btree-after-deletions.png
    Print out minimum and maximum values
    Minimum key: -5
    Maximum key: -1
    """

if __name__ == "__main__":
    main()
