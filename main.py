class Node:
    def __init__(self, number):
        self.number = number
        self.next = []
        self.previous = 0


left = []
right = []


def read_data():
    data = []
    nodes = []
    nodes_with_neighbours = []
    with open("input.txt") as file:
        for line in file:
            data.append(line)
    data = data[2:len(data) - 1]
    for i in range(len(data)):
        nodes.append(Node(i + 1))
    for i in range(len(data)):
        next_nodes = data[i].split(" ")
        for next_node in next_nodes:
            if int(next_node) != 0:
                nodes[i].next.append(nodes[int(next_node) - 1])
    for node in nodes:
        if len(node.next) != 0:
            nodes_with_neighbours.append(node)
    find_bipartition(nodes_with_neighbours)
    ford_falkerson(nodes_with_neighbours, nodes)


def find_bipartition(nodes):
    while len(left) + len(right) != len(nodes):
        free = nodes[0]
        for node in nodes:
            if node not in left and node not in right:
                free = node
                break
        left.append(free)
        used_nodes = [free]
        while len(used_nodes) != 0:
            current = used_nodes[0]
            used_nodes = used_nodes[1:]
            current_in_left = current in left
            for node in current.next:
                if node not in left and node not in right:
                    used_nodes.append(node)
                    if current_in_left:
                        right.append(node)
                    else:
                        left.append(node)


pairs = []


def ford_falkerson(nodes, all_nodes):
    s = Node(0)
    for node in left:
        s.next.append(node)
    t = Node(len(nodes) + 1)
    for node in right:
        node.next = []
        node.next.append(t)
    find_path = deep_find(s, t.number)
    while find_path:
        find_path = deep_find(s, t.number)
    print_answer(all_nodes)


def deep_find(s, number_t):
    for node in s.next:
        node.previous = s
        if node.number == number_t:
            append_pairs(node)
            return True
        else:
            if deep_find(node, number_t):
                return True
    return False


def append_pairs(t):
    previouses = []
    current = t
    while current.previous != 0:
        previouses.append(current.previous)
        current = current.previous
    s = previouses[-1]
    previouses = previouses[:-1]
    for i in range(len(previouses)):
        if i == 0:
            continue
        if i % 2 == 1:
            pairs.append((previouses[i], previouses[i-1]))
        else:
            pairs.remove((previouses[i-1], previouses[i]))
    for i in range(len(previouses)):
        if i == 0:
            continue
        previouses[i].next.remove(previouses[i-1])
        previouses[i-1].next.append(previouses[i])
    s.next.remove(previouses[len(previouses) - 1])
    previouses[0].next.remove(t)


def print_answer(nodes):
    all_pairs_nodes = []
    for pair in pairs:
        for node in pair:
            all_pairs_nodes.append(node.number)
    with open("output.txt", "w") as file:
        pair_to_write = 0
        for node in nodes:
            if node.number not in all_pairs_nodes:
                file.write("0" + "\n")
            else:
                for pair in pairs:
                    for pair_node in pair:
                        if node.number == pair_node.number:
                            pair_to_write = pair
                for pair_node in pair_to_write:
                    if pair_node.number != node.number:
                        file.write(str(pair_node.number) + "\n")


def main():
    read_data()


if __name__ == '__main__':
    main()
