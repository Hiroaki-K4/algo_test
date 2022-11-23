from hashlib import new
from typing import Any, Type
import pydot
import random
import copy
from tqdm import tqdm


class Node:
    def __init__(self, color: str, key: int, left: Any, right: Any, parent: Any) -> None:
        self.color = color
        self.key = key
        self.left = left
        self.right = right
        self.parent = parent


def draw_tree(graph, tree: Node):
    if tree.left is None and tree.right is None:
        return
    elif tree.left is not None and tree.right is not None:
        x = pydot.Node(tree.left.key, style="filled", fillcolor=tree.left.color)
        graph.add_node(x)
        x = pydot.Node(tree.right.key, style="filled", fillcolor=tree.right.color)
        graph.add_node(x)
        edge = pydot.Edge(tree.key, tree.left.key)
        graph.add_edge(edge)
        edge = pydot.Edge(tree.key, tree.right.key)
        graph.add_edge(edge)
        draw_tree(graph, tree.left)
        draw_tree(graph, tree.right)
    elif tree.left is not None:
        x = pydot.Node(tree.left.key, style="filled", fillcolor=tree.left.color)
        graph.add_node(x)
        edge = pydot.Edge(tree.key, tree.left.key)
        graph.add_edge(edge)
        draw_tree(graph, tree.left)
    elif tree.right is not None:
        x = pydot.Node(tree.right.key, style="filled", fillcolor=tree.right.color)
        graph.add_node(x)
        edge = pydot.Edge(tree.key, tree.right.key)
        graph.add_edge(edge)
        draw_tree(graph, tree.right)

    graph.write_png("rb_tree.png")


def left_rotate(root: Node, x: Node) -> Node:
    y = x.right
    x.right = y.left
    if y.left is not None:
        y.left.parent = x
    y.parent = x.parent
    if x.parent is None:
        root = y
    elif x == x.parent.left:
        x.parent.left = y
    else:
        x.parent.right = y
    y.left = x
    x.parent = y
    return root


def right_rotate(root: Node, y: Node) -> Node:
    x = y.left
    y.left = x.right
    if x.right is not None:
        x.right.parent = y
    x.parent = y.parent
    if y.parent is None:
        root = x
    elif y == y.parent.right:
        y.parent.right = x
    else:
        y.parent.left = x
    x.right = y
    y.parent = x
    return root


def rb_insert_fixup(root: Node, new_node: Node) -> None:
    while new_node.parent != None and new_node.parent.color == "red":
        if new_node.parent == new_node.parent.parent.left:
            y = new_node.parent.parent.right
            if y != None and y.color == "red":
                new_node.parent.color = "gray"
                y.color = "gray"
                new_node.parent.parent.color = "red"
                new_node = new_node.parent.parent
            elif new_node == new_node.parent.right:
                new_node = new_node.parent
                root = left_rotate(root, new_node)
            else:
                new_node.parent.color = "gray"
                new_node.parent.parent.color = "red"
                root = right_rotate(root, new_node.parent.parent)

        else:
            y = new_node.parent.parent.left
            if y != None and y.color == "red":
                new_node.parent.color = "gray"
                y.color = "gray"
                new_node.parent.parent.color = "red"
                new_node = new_node.parent.parent
            elif new_node == new_node.parent.left:
                new_node = new_node.parent
                root = right_rotate(root, new_node)
            else:
                new_node.parent.color = "gray"
                new_node.parent.parent.color = "red"
                root = left_rotate(root, new_node.parent.parent)

    root.color = "gray"
    return root


def rb_insert(root: Node, new_node: Node) -> Node:
    x = root
    while x != None:
        y = x
        if new_node.key < x.key:
            x = x.left
        else:
            x = x.right

    new_node.parent = y
    if y == None:
        root = new_node
    elif new_node.key < y.key:
        y.left = new_node
    else:
        y.right = new_node
    new_node.left = None
    new_node.right = None
    new_node.color = "red"
    root = rb_insert_fixup(root, new_node)
    return root


def get_black_nodes(node: Node, node_list: list, node_len_list: list) -> Node:
    if node.left is None and node.right is None:
        if node.color == "gray":
            node_list.append(node.key)
        node_len_list.append(len(node_list))
        return
    elif node.left is not None and node.right is not None:
        if node.color == "gray":
            node_list.append(node.key)
        get_black_nodes(node.left, copy.copy(node_list), node_len_list)
        get_black_nodes(node.right, copy.copy(node_list), node_len_list)
    elif node.left is not None:
        if node.color == "gray":
            node_list.append(node.key)
        get_black_nodes(node.left, copy.copy(node_list), node_len_list)
    else:
        if node.color == "gray":
            node_list.append(node.key)
        get_black_nodes(node.right, copy.copy(node_list), node_len_list)


def test_tree(root: Node) -> None:
    node_list = []
    node_len_list = []
    get_black_nodes(root, node_list, node_len_list)
    for i in range(1, len(node_len_list)):
        if node_len_list[i - 1] != node_len_list[i]:
            raise RuntimeError("Error!!!!")


def get_node(curr_node: Node, num: int, remove_node_list: list) -> None:
    if curr_node.key == num:
        remove_node_list.append(curr_node)
        return
    elif curr_node.left is None and curr_node.right is None:
        return
    elif curr_node.left is not None and curr_node.right is not None:
        get_node(curr_node.left, num, remove_node_list)
        get_node(curr_node.right, num, remove_node_list)
    elif curr_node.left is not None:
        get_node(curr_node.left, num, remove_node_list)
    elif curr_node.right is not None:
        get_node(curr_node.right, num, remove_node_list)


def rb_delete(root: Node, new_node: Node) -> Node:
    print("rb_delete: ", new_node.key)
    return root


def rb_tree(data: list) -> None:
    root = Node("gray", data[0], None, None, None)
    for i in range(1, len(data)):
        new_node = Node("red", data[i], None, None, None)
        root = rb_insert(root, new_node)

        # Test rb_tree
        test_tree(root)

    for i in range(len(data)):
        remove_node_list = []
        remove_num = random.choice(data)
        get_node(root, remove_num, remove_node_list)
        rb_delete(root, remove_node_list[0])
        data.remove(remove_num)


    # Draw tree graph
    graph = pydot.Dot(graph_type = 'graph', strict=True)
    x = pydot.Node(root.key, style="filled", fillcolor=root.color)
    graph.add_node(x)
    draw_tree(graph, root)


def main():
    # for i in tqdm(range(10000)):
    #     random_list = random.sample(range(10000), 100)
    #     rb_tree(random_list)
    list2 = [7, 11, 5, 32, 4, 25, 6]
    rb_tree(list2)
    print("TEST OK")


if __name__ == '__main__':
    main()
