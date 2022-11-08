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


def left_rotate(root: Node, x: Node) -> None:
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


def right_rotate(root: Node, x: Node) -> None:
    y = x.left
    x.left = y.right
    if y.right is not None:
        y.right.parent = x
    y.parent = x.parent
    if x.parent is None:
        root = y
    elif x == x.parent.right:
        x.parent.right = y
    else:
        x.parent.left = y
    y.right = x
    x.parent = y


def rb_insert_fixup(root: Node, new_node: Node) -> None:
    while new_node.parent.color == "red":
        if new_node.parent == new_node.parent.parent.left:
            y = new_node.parent.parent.right
            if y.color == "red":
                new_node.parent.color = "gray"
                y.color = "gray"
                new_node.parent.parent.color = "red"
                new_node = new_node.parent.parent
                print("new: ", new_node.key)
            elif new_node == new_node.parent.right:
                new_node = new_node.parent
                left_rotate(root, new_node)
            else:
                new_node.parent.color = "gray"
                new_node.parent.parent.color = "red"
                right_rotate(root, new_node.parent.parent)

        # else:
        #     y = new_node.parent.parent.left
        #     if y.color == "red":
        #         new_node.parent.color = "gray"
        #         y.color = "gray"
        #         new_node.parent.parent.color = "red"
        #         new_node = new_node.parent.parent
        #     elif new_node == new_node.parent.left:
        #         new_node = new_node.parent
        #         right_rotate(root, new_node)
        #     else:
        #         new_node.parent.color = "gray"
        #         new_node.parent.parent.color = "red"
        #         left_rotate(root, new_node.parent.parent)

    root.color = "gray"



def rb_insert(root: Node, new_node: Node) -> None:
    print("new: ", new_node.key)
    # y = None
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
    print("new_parent: ", new_node.parent.color)
    rb_insert_fixup(root, new_node)


def rb_tree(data: list):
    # print(data)
    nil = Node("gray", data[0], None, None, None)
    root = Node("gray", data[0], None, None, nil)
    for i in range(1, len(data)):
        new_node = Node("red", data[i], nil, nil, None)
        print("data: ", data[i])
        rb_insert(root, new_node)
    
    # print(root.right.right.right.key)
    graph = pydot.Dot(graph_type = 'graph', strict=True)
    x = pydot.Node(root.key, style="filled", fillcolor=root.color)
    graph.add_node(x)
    draw_tree(graph, root)



def main():
    # list1 = [1, 2, 4, 5, 7, 8, 11, 14, 15]
    list2 = [7, 2, 14, 5, 1, 8, 11, 4, 15]
    rb_tree(list2)


if __name__ == '__main__':
    main()