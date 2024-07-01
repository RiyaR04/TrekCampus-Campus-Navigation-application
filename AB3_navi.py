from edges import edges_Ab3

class room:
    def __init__(self, value):
        self.value = value
        self.neighbors = []

class AB3:
    def __init__(self, vertices):
        self.vertices = vertices
        self.nodes = {str(i): room(str(i)) for i in range(vertices)} 
        self.edges = []

    def remove_node(self, vertex):
        if vertex in self.nodes:
            # Remove all edges associated with this vertex
            for neighbor, weight in self.nodes[vertex].neighbors:
                self.nodes[neighbor].neighbors = [(v, w) for v, w in self.nodes[neighbor].neighbors if v != vertex]
                self.edges = [edge for edge in self.edges if edge[0] != vertex and edge[1] != vertex]
            del self.nodes[vertex]

    def add_edge(self, u, v, weight=1):
        if u not in self.nodes:
            self.nodes[u] = room(u)
        if v not in self.nodes:
            self.nodes[v] = room(v)

        self.nodes[u].neighbors.append((v, weight))
        self.nodes[v].neighbors.append((u, weight))
        self.edges.append((u, v, weight))


    def remove_edge(self, u, v):
        self.nodes[u].neighbors = [(node, weight) for node, weight in self.nodes[u].neighbors if node != v]
        self.nodes[v].neighbors = [(node, weight) for node, weight in self.nodes[v].neighbors if node != u]
        self.edges = [edge for edge in self.edges if not (edge[0] == u and edge[1] == v) and not (edge[0] == v and edge[1] == u)]

    def dijkstra(self, start_vertex):
        import heapq

        distances = {v: float('inf') for v in self.nodes}  # Use vertices as keys directly
        distances[start_vertex] = 0
        priority_queue = [(0, start_vertex)]
        predecessors = {v: None for v in self.nodes}  # Use vertices as keys directly
        visited = set()
        
        while priority_queue:
            current_distance, current_vertex = heapq.heappop(priority_queue)
            if current_vertex in visited:
                continue
            visited.add(current_vertex)

            for neighbor, weight in self.nodes[current_vertex].neighbors:
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    predecessors[neighbor] = current_vertex
                    heapq.heappush(priority_queue, (distance, neighbor))

        return distances, predecessors

    def shortest_path(self, start_vertex, end_vertex):
        start_vertex = start_vertex if isinstance(start_vertex, int) else self.get_vertex_index(start_vertex)
        end_vertex = end_vertex if isinstance(end_vertex, int) else self.get_vertex_index(end_vertex)
        
        distances, predecessors = self.dijkstra(start_vertex)
        path = []
        current_vertex = end_vertex
        
        while current_vertex is not None:
            path.insert(0, current_vertex)
            current_vertex = predecessors[current_vertex]
        
        if distances[end_vertex] == float('inf'):
            return f"No path from {start_vertex} to {end_vertex}"
        else:
            path_info = []
            for i in range(len(path) - 1):
                path_info.append((self.get_vertex_name(path[i]), self.get_vertex_name(path[i+1]), self.get_weight(path[i], path[i+1])))
            return path, distances[end_vertex], path_info

    def get_vertex_index(self, name):
        for index, node in self.nodes.items():
            if node.value == name:
                return index
        return None

    def get_vertex_name(self, index):
        return self.nodes[index].value if index in self.nodes else None

    def find_path(self, start_vertex, end_vertex):
        start_vertex = start_vertex if isinstance(start_vertex, int) else self.get_vertex_index(start_vertex)
        end_vertex = end_vertex if isinstance(end_vertex, int) else self.get_vertex_index(end_vertex)
        visited = set()
        all_paths = []

        def dfs_util(curr_vertex, end_vertex, path):
            visited.add(curr_vertex)
            if curr_vertex == end_vertex:
                all_paths.append(path[:])
            else:
                for neighbor, _ in self.nodes[curr_vertex].neighbors:
                    if neighbor not in visited:
                        path.append(neighbor)
                        dfs_util(neighbor, end_vertex, path)
                        path.pop()
            visited.remove(curr_vertex)

        dfs_util(start_vertex, end_vertex, [start_vertex])
        return all_paths

    def get_weight(self, u, v):
        for edge in self.edges:
            if (edge[0] == u and edge[1] == v) or (edge[0] == v and edge[1] == u):
                return edge[2]
        return None

    def graph_size(self):
        return self.vertices

    def get_neighbors(self, vertex):
        return self.nodes[vertex].neighbors if vertex in self.nodes else []

    def print_graph(self):
        print("-----------------------------------------------------------")
        print("Choose the start location and destination from the below : ")
        for vertex in self.nodes:
            neighbors = self.nodes[vertex].neighbors
            if neighbors:  # Check if the list of neighbors is not empty
                print(f"{vertex}")

    

def find_shortest_path(graph):
    start_vertex, end_vertex = input("Enter start vertex and end vertex separated by a space: ").split()
    paths = graph.find_path(start_vertex, end_vertex)
    shortest_path, shortest_distance, path_info = graph.shortest_path(start_vertex, end_vertex)

    print(f"Shortest path from {start_vertex} to {end_vertex}: {shortest_path}")
    print(f"Shortest distance: {shortest_distance} meters")


    walking_speed = 1.4  
    estimated_time = shortest_distance / walking_speed
    estimated_time_rounded = int(estimated_time + 0.5)  # Round up to the next integer
    print(f"Estimated time to walk the shortest path: {estimated_time_rounded+1} seconds")

    print(f"All possible paths from {start_vertex} to {end_vertex}:")
    for path in paths:
        print(" -> ".join(path))

def testGraph():
    vertices = 20
    graph = AB3(vertices)

    for u, v, w in edges_Ab3:
        graph.add_edge(u, v, w)

    graph.print_graph()
    find_shortest_path(graph)

def main():
    testGraph()

if __name__ == "__main__":
    main()