import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd


def create_graph():
    """Создание графа с заданными весами"""
    edges = [
        ('s', 'x1', 5),
        ('s', 'x4', 1),
        ('s', 'x5', 3),
        ('x1', 'x2', 1),
        ('x5', 'x6', 2),
        ('x4', 'x2', 8),
        ('x4', 'x6', 4),
        ('x2', 'x3', 2),
        ('x6', 'x3', 1),
        ('x6', 't', 6),
        ('x3', 't', 3)
    ]

    G = nx.DiGraph()
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)

    return G


def find_shortest_paths(G, source):
    """Нахождение кратчайших путей из истока"""
    paths = nx.single_source_dijkstra_path(G, source)
    lengths = nx.single_source_dijkstra_path_length(G, source)

    result = {}
    for node in paths:
        result[node] = (paths[node], lengths[node])

    return result


def create_table_data(shortest_paths, source):
    """Создание данных для таблицы"""
    data = []
    for vertex, (path, length) in sorted(shortest_paths.items()):
        if vertex == source:
            continue
        path_str = " → ".join(path)
        data.append({
            'Вершина': vertex,
            'Длина пути': f"{length}",
            'Путь': path_str
        })

    return pd.DataFrame(data)


def draw_graph(G, source, sink, shortest_paths, ax):
    """Рисование графа с поиском layout без пересечений"""

    def count_edge_crossings(G, pos):
        edges = list(G.edges())
        crossings = 0

        for i in range(len(edges)):
            for j in range(i + 1, len(edges)):
                u1, v1 = edges[i]
                u2, v2 = edges[j]

                # Проверяем, являются ли рёбра разными
                if len({u1, v1, u2, v2}) == 4:  # Все 4 вершины разные
                    x1, y1 = pos[u1]
                    x2, y2 = pos[v1]
                    x3, y3 = pos[u2]
                    x4, y4 = pos[v2]

                    # Простая проверка пересечения отрезков
                    def ccw(A, B, C):
                        return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

                    A, B, C, D = (x1, y1), (x2, y2), (x3, y3), (x4, y4)
                    if ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D):
                        crossings += 1

        return crossings

    best_pos = None
    min_crossings = float('inf')
    best_seed = 42

    for seed in range(500, 600):
        for k in [1.5, 2.0, 2.5, 3.0]:
            pos = nx.spring_layout(G, seed=seed, k=k, scale=2, iterations=100)
            crossings = count_edge_crossings(G, pos)

            if crossings < min_crossings:
                min_crossings = crossings
                best_pos = pos
                best_seed = seed
                best_k = k

    pos = best_pos

    node_colors = []
    for node in G.nodes():
        if node == source:
            node_colors.append('limegreen')
        elif node == sink:
            node_colors.append('orange')
        elif sink in shortest_paths and node in shortest_paths[sink][0]:
            node_colors.append('red')
        else:
            node_colors.append('lightblue')

    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors,
                           node_size=1000, edgecolors='black', linewidths=2)

    nx.draw_networkx_edges(G, pos, ax=ax, edge_color='gray',
                           arrows=True, arrowsize=20, width=2)

    if sink in shortest_paths:
        path = shortest_paths[sink][0]
        path_edges = list(zip(path[:-1], path[1:]))
        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=path_edges,
                               edge_color='red', width=4, arrows=True, arrowsize=25)

    nx.draw_networkx_labels(G, pos, ax=ax, font_size=14, font_weight='bold')

    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, ax=ax, edge_labels=edge_labels,
                                 font_size=12,
                                 bbox=dict(boxstyle='round,pad=0.3',
                                           facecolor='white',
                                           edgecolor='gray',
                                           alpha=0.9))

    ax.set_title(f"Орграф с кратчайшим путем от '{source}' к '{sink}'",
                 fontsize=14, fontweight='bold', pad=15)
    ax.axis('off')


def draw_table(df, sink, ax):
    ax.axis('off')
    table = ax.table(cellText=df.values,
                     colLabels=df.columns,
                     cellLoc='center',
                     loc='center',
                     colWidths=[0.15, 0.15, 0.7])

    table.set_fontsize(14)

    for i in range(len(df.columns)):
        table[(0, i)].set_facecolor('#4a6fa5')
        table[(0, i)].set_text_props(weight='bold', color='white', fontsize=16)
        table[(0, i)].set_height(0.15)

    for i in range(len(df)):
        color = 'red' if df.iloc[i]['Вершина'] == sink else 'black'
        weight = 'bold' if df.iloc[i]['Вершина'] == sink else 'normal'

        for j in range(len(df.columns)):
            cell = table[(i + 1, j)]
            cell.set_text_props(color=color, weight=weight, fontsize=14)
            cell.set_facecolor('#f8f9fa' if i % 2 == 0 else '#e9ecef')
            cell.set_height(0.12)

    table.scale(1, 1.8)


def main():
    G = create_graph()

    source = 's'
    sink = 't'

    shortest_paths = find_shortest_paths(G, source)

    df = create_table_data(shortest_paths, source)

    fig = plt.figure(figsize=(14, 10))

    ax1 = plt.subplot(2, 1, 1)
    draw_graph(G, source, sink, shortest_paths, ax1)

    ax2 = plt.subplot(2, 1, 2)
    draw_table(df, sink, ax2)

    # Сохраняем
    plt.tight_layout()
    plt.savefig('graph_and_table.pdf', bbox_inches='tight', dpi=300)
    plt.show()


if __name__ == "__main__":
    main()
