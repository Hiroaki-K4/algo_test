from hashlib import new
from typing import Any, Type
import pydot


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
    print("left: ", x.key)
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
    print("left1: ", x.parent.key)
    return root


def right_rotate(root: Node, y: Node) -> Node:
    x = y.left
    print("y: ", y.key)
    print("x: ", x.key)
    y.left = x.right
    if x.right is not None:
        x.right.parent = y
    x.parent = y.parent
    if y.parent is None:
        print("if1")
        root = x
    elif y == y.parent.right:
        print("if2")
        y.parent.right = x
    else:
        print("if3")
        y.parent.left = x
    x.right = y
    y.parent = x
    print("root: ", root.key)
    print("root.right: ", root.right.key)
    print("root.left: ", root.left.key)
    return root


def rb_insert_fixup(root: Node, new_node: Node) -> None:
    while new_node.parent != None and new_node.parent.color == "red":
        print("new_node: ", new_node.key)
        if new_node.parent == new_node.parent.parent.left:
            y = new_node.parent.parent.right
            if y != None and y.color == "red":
                print("pattern1")
                new_node.parent.color = "gray"
                y.color = "gray"
                new_node.parent.parent.color = "red"
                new_node = new_node.parent.parent
            elif new_node == new_node.parent.right:
                print("pattern2")
                new_node = new_node.parent
                root = left_rotate(root, new_node)
            else:
                print("pattern3")
                new_node.parent.color = "gray"
                new_node.parent.parent.color = "red"
                print("pa: ", new_node.parent.parent.key)
                root = right_rotate(root, new_node.parent.parent)

        else:
            y = new_node.parent.parent.left
            if y != None and y.color == "red":
                print("pattern4")
                new_node.parent.color = "gray"
                y.color = "gray"
                new_node.parent.parent.color = "red"
                new_node = new_node.parent.parent
            elif new_node == new_node.parent.left:
                print("pattern5")
                new_node = new_node.parent
                right_rotate(root, new_node)
            else:
                print("pattern6")
                new_node.parent.color = "gray"
                new_node.parent.parent.color = "red"
                print("new_node_granpa: ", new_node.parent.parent.key)
                left_rotate(root, new_node.parent.parent)

    root.color = "gray"
    return root


def rb_insert(root: Node, new_node: Node, nil: Node) -> Node:
    print("new: ", new_node.key)
    # y = 
    x = root
    while x != None:
        # print("x: ", x.key, root.parent.key)
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
    print("root: ", root.key)
    return root


def rb_tree(data: list):
    # print(data)
    nil = Node("nil", -1, None, None, None)
    root = Node("gray", data[0], None, None, None)
    for i in range(1, len(data)):
        new_node = Node("red", data[i], None, None, None)
        root = rb_insert(root, new_node, nil)
    print("root: ", root.key)
    # print("root.right: ", root.right.key)
    # print("root.left: ", root.left.key)

    # print(root.right.right.right.key)
    graph = pydot.Dot(graph_type = 'graph', strict=True)
    x = pydot.Node(root.key, style="filled", fillcolor=root.color)
    graph.add_node(x)
    draw_tree(graph, root)


def main():
    # list2 = [7, 2, 14, 5, 1, 8, 11, 4, 15, 17, 18, 19, 20, 21, 23, 24, 25, 30, 35]
    # list2 = [7, 2, 14, 25, 12, 13, 11, 20, 15, 30]
    # list2 = [11, 2, 1, 7, 5, 8, 14, 15, 4]
    list2 = [11, 2, 1, 7, 5, 8, 14, 15]
    rb_tree(list2)


if __name__ == '__main__':
    main()
