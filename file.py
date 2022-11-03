import re


def parse_line(line):
    search_result = re.fullmatch(r'(\d+) (\d+)\n', line)
    if search_result is None:
        print("Not valid line:", line)
        exit(1)
    groups = search_result.groups()
    node = groups[0]
    neighbor = groups[1]
    if node == neighbor:
        print("Node and neighbor can not be the same:", node, neighbor)
        exit(1)
    return node, neighbor


def parse_input_file(filepath):
    with open(filepath, "r") as f:
        lines = f.readlines()
        nodes_neighbors = {}
        for line in lines:
            node, neighbor = parse_line(line)
            if node in nodes_neighbors:
                nodes_neighbors[node].add(neighbor)
            else:
                nodes_neighbors[node] = {neighbor}
            if neighbor in nodes_neighbors:
                nodes_neighbors[neighbor].add(node)
            else:
                nodes_neighbors[neighbor] = {node}
        return nodes_neighbors


def color_nodes_sequentially(nodes_to_color, possible_colors, nodes_neighbors):
    node_to_color = {}
    color_to_nodes = {}
    for node in nodes_to_color:
        for color in possible_colors:
            already_colored_nodes = color_to_nodes[color] if color in color_to_nodes else set()
            neighbor_nodes = nodes_neighbors[node]
            if len(already_colored_nodes & neighbor_nodes) == 0:
                node_to_color[node] = color
                if color in color_to_nodes:
                    color_to_nodes[color].add(node)
                else:
                    color_to_nodes[color] = {node}
                break
    return node_to_color


def write_output_file(filepath, colored_nodes):
    with open(filepath, "w") as f:
        for node, color in colored_nodes.items():
            f.write("%s %s\n" % (node, color))


def main():
    nodes_neighbors = parse_input_file('input.txt')
    nodes_to_color = sorted(nodes_neighbors.keys())
    possible_colors = range(1, len(nodes_to_color) + 1)
    print("Nodes neighbors:", nodes_neighbors)
    print("Nodes to color:", *nodes_to_color)
    print("Possible colors:", *possible_colors)
    colored_nodes = color_nodes_sequentially(nodes_to_color, possible_colors, nodes_neighbors)
    print("Colored nodes:", colored_nodes)
    used_colors = sorted(set(colored_nodes.values()))
    print("Used colors: ", used_colors)
    write_output_file("output.txt", colored_nodes)


if __name__ == "__main__":
    main()
