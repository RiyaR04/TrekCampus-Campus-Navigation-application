from edges import edges_main, edges_Ab3,faculty_room1_ground,faculty_room2_ground,faculty_room1_first,faculty_room2_first,faculty_room2_second,faculty_room1_second,faculty_room2_third,faculty_room1_third
import os
import time

class dlist:
    class Node:
        def __init__(self, e):
            self.element = e
            self.prev = None
            self.next = None

    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def insertfirst(self, e):
        newnode = self.Node(e)
        if self.size == 0:
            self.head = self.tail = newnode
        else:
            newnode.next = self.head
            self.head.prev = newnode
            self.head = newnode
        self.size += 1

    def insertlast(self, e):
        newnode = self.Node(e)
        if self.size == 0:
            self.head = self.tail = newnode
        else:
            self.tail.next = newnode
            newnode.prev = self.tail
            self.tail = newnode
        self.size += 1

    def deletefirst(self):
        if self.size == 0:
            print("list is empty")
        elif self.size == 1:
            self.head = self.tail = None
            self.size -= 1
        else:
            self.head = self.head.next
            self.size -= 1

    def deletelast(self):
        if self.size == 0:
            print("list is empty")
        elif self.size == 1:
            self.head = self.tail = None
            self.size -= 1
        else:
            self.tail = self.tail.prev
            self.tail.next = None
            self.size -= 1

    def deleteposition(self, pos):
        if pos < 0 or pos >= self.size:
            print("invalid position")
        elif pos == 0:
            self.deletefirst()
        elif pos == self.size - 1:
            self.deletelast()
        else:
            c = self.head
            i = 0
            while i < pos - 1:
                c = c.next
                i += 1

            c.next = c.next.next
            c.next.prev = c
            self.size -= 1

    def insertposition(self, pos, key):
        if pos < 0 or pos > self.size:
            print("invalid position")
        elif pos == 0:
            self.insertfirst(key)
        elif pos == self.size:
            self.insertlast(key)
        else:
            newnode = self.Node(key)
            c = self.head
            i = 0
            while i < pos - 1:
                c = c.next
                i += 1

            newnode.prev = c
            newnode.next = c.next
            c.next.prev = newnode
            c.next = newnode
            self.size += 1

    def printlist(self):
        if self.size == 0:
            print("list is empty")
        else:
            c = self.head
            while c:
                print(c.element, end=" ")
                c = c.next
            print()

    def add_faculty(self, name, position="last", room="",room_choice=""):
        if position == "first":
            self.insertfirst(name)
        elif position == "last":
            self.insertlast(name)


        self.update_faculty_list(room,room_choice)

    def remove_faculty(self, name, room="",room_choice=""):
        current = self.head
        prev = None
        while current:
            if current.element == name:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                self.update_faculty_list(room,room_choice)
                return
            prev = current
            current = current.next

    def print_faculty(self):
        current = self.head
        while current:
            print(current.element, end=" -> ")
            current = current.next
        print("None")
    
    def update_faculty_list(self, room,room_choice):
        with open("edges.py", "r") as file:
            lines = file.readlines()
        if room_choice == "fr1":
            faculty_room_str = "faculty_room1_" + room
        elif room_choice == "fr2":
            faculty_room_str = "faculty_room2_" + room

        with open("edges.py", "w") as file:
            for line in lines:
                if faculty_room_str in line:
                    file.write(f"{faculty_room_str} = [")
                    current = self.head
                    while current:
                        file.write(f'"{current.element}"')
                        current = current.next
                        if current:
                            file.write(", ")
                    file.write("]\n")
                else:
                    file.write(line)



class Node:
    def __init__(self, value):
        self.fr1 = None
        self.fr2 = None
        self.value = value
        self.neighbors = []

class Graph:
    def __init__(self, vertices):
        self.vertices = vertices
        self.nodes = {str(i): Node(str(i)) for i in range(vertices)}
        self.edges = None

    def add_edges_from_list(self):
        for source, destination, weight in edges_main:
            self.add_edge(source, destination, weight)

    def remove_node(self, vertex):
        if vertex in self.nodes:
            for neighbor, weight in self.nodes[vertex].neighbors:
                self.nodes[neighbor].neighbors = [(v, w) for v, w in self.nodes[neighbor].neighbors if v != vertex]
                self.edges = [edge for edge in self.edges if edge[0] != vertex and edge[1] != vertex]
            del self.nodes[vertex]

    def add_edge(self, u, v, weight=1):
        if u not in self.nodes:
            self.nodes[u] = Node(u)
        if v not in self.nodes:
            self.nodes[v] = Node(v)

        self.nodes[u].neighbors.append((v, weight))
        self.nodes[v].neighbors.append((u, weight))
        self.edges.append((u, v, weight))

    def remove_edge(self, u, v):
        if u in self.nodes and v in self.nodes:
            self.nodes[u].neighbors = [(node, weight) for node, weight in self.nodes[u].neighbors if node != v]
            self.nodes[v].neighbors = [(node, weight) for node, weight in self.nodes[v].neighbors if node != u]
            self.edges = [edge for edge in self.edges if not (edge[0] == u and edge[1] == v) and not (edge[0] == v and edge[1] == u)]

            with open("edges.py", "w") as file:
                file.write("edges_main = [\n")
                for edge in self.edges:
                    file.write(f"    {str(edge)},\n")
                file.write("]\n\n")

                file.write("edges_Ab3 = [\n")
                for edge in edges_Ab3:
                    file.write(f"    {str(edge)},\n")
                file.write("]")

            print("Edge removed successfully!")
            self.print_graph()
        else:
            print(f"One or both of the vertices ({u}, {v}) do not exist in the graph.")

    def print_graph(self):
        print('------------------------------------------------------------------------------------------')
        print("Current graph with all locations:")
        for vertex in self.nodes:
            neighbors = self.nodes[vertex].neighbors
            if neighbors:
                print(f"{vertex}:{neighbors}")
        print('------------------------------------------------------------------------------------------')

    def dijkstra(self, start_vertex):
        import heapq

        distances = {v: float('inf') for v in self.nodes}
        distances[start_vertex] = 0
        priority_queue = [(0, start_vertex)]
        predecessors = {v: None for v in self.nodes}
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
                path_info.append((self.get_vertex_name(path[i]), self.get_vertex_name(path[i + 1]), self.get_weight(path[i], path[i + 1])))
            return path, distances[end_vertex], path_info

    def get_vertex_index(self, name):
        for index, node in self.nodes.items():
            if node.value == name:
                return index
        return None

    def get_vertex_name(self, index):
        return self.nodes[index].value if index in self.nodes else None

    def find_path(self, start_vertex, end_vertex):
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
    
    def find_faculty(self, faculty_name):
        for vertex in self.nodes:
            if self.nodes[vertex].value == faculty_name:
                return vertex
        return None




    
def find_shortest_path(graph):
    graph.print_graph()
    start_vertex = input("Enter the location where you are: ")
    end_vertex = input("Enter the location you want to go: ")
    if start_vertex not in graph.nodes or end_vertex not in graph.nodes:
        print(f"One or both of the vertices ({start_vertex}, {end_vertex}) do not exist in the graph.")
    else:
        result = graph.shortest_path(start_vertex, end_vertex)
        if isinstance(result, str):  # Incorrect, should check the content of the path instead
            print(result)
        else:
            path, distance, path_info = result
            if distance == float('inf'):  # Check if the distance is infinite
                print(f"No path from {start_vertex} to {end_vertex}")
            else:
                print(f"Shortest path from {start_vertex} to {end_vertex} is: {path}")
                print(f"Distance: {distance}")
                print("Path Details:")
                for (src, dest, weight) in path_info:
                    print(f"From {src} to {dest} with weight {weight}")


def find_faculty_member_all_floors(graphs, faculty_name):
    floors = ['Ground Floor', 'First Floor', 'Second Floor', 'Third Floor']
    entrances = ['entrance1', 'entrance1', 'entrance1', 'entrance1']
    
    for i, graph in enumerate(graphs):
        fr1 = graph.fr1
        fr2 = graph.fr2
        
        # Check if the faculty is in the faculty room 1 list of this floor
        current = fr1.head
        while current:
            if current.element == faculty_name:
                # Assuming find_shortest_path takes graph, start node, and end node
                path = print_shortest_path(graph, entrances[i], 'FR1')
                print(f"The faculty member '{faculty_name}' is located in: {floors[i]} in faculty room 1")
                #print(f"Shortest path from the entrance: {' -> '.join(path)}")
                return
            current = current.next
        
        # Check if the faculty is in the faculty room 2 list of this floor
        current = fr2.head
        while current:
            if current.element == faculty_name:
                # Assuming find_shortest_path takes graph, start node, and end node
                path = print_shortest_path(graph, entrances[i], 'FR2')
                print(f"The faculty member '{faculty_name}' is located in: {floors[i]} in faculty room 2")
                #print(f"Shortest path from the entrance: {' -> '.join(path)}")
                return
            current = current.next
    
    print(f"The faculty member '{faculty_name}' was not found on any floor.")
    input("Press Enter to continue...")

def print_shortest_path(graph, start_vertex, end_vertex):
    if start_vertex not in graph.nodes or end_vertex not in graph.nodes:
        print(f"One or both of the vertices ({start_vertex}, {end_vertex}) do not exist in the graph.")
    else:
        result = graph.shortest_path(start_vertex, end_vertex)
        if isinstance(result, str):  # Incorrect, should check the content of the path instead
            print(result)
        else:
            path, distance, path_info = result
            if distance == float('inf'):  # Check if the distance is infinite
                print(f"No path from {start_vertex} to {end_vertex}")
            else:
                print(f"Shortest path from {start_vertex} to {end_vertex} is: {path}")
                print(f"Distance: {distance}")
                print("Path Details:")
                for (src, dest, weight) in path_info:
                    print(f"From {src} to {dest} with weight {weight}")

def add_edge(graph, a, p=0):
    u = input("Enter the source vertex: ")
    v = input("Enter the destination vertex: ")
    try:
        w = int(input("Enter the weight: "))
    except ValueError:
        print("Weight must be an integer.")
        return
    
    new_edge = (u, v, w)
    if a == "campus":
        edges_main.append(new_edge)
    elif a == "building":
        if 0 < p <= len(edges_Ab3):
            edges_Ab3[p-1].append(new_edge)  # Store the edge in the correct sublist of edges_Ab3
        else:
            print("Invalid building index.")
            return
    else:
        print("Invalid edge type.")
        return

    with open("edges.py", "r") as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if line.startswith("edges_main = ["):
            index = i
            for j in range(i + 1, len(lines)):
                if lines[j].startswith("]"):
                    lines.insert(j, f"    {str(new_edge)},\n")
                    break
            break
        elif line.startswith("edges_Ab3 = ["):
            index = i
            for j in range(i + 1, len(lines)):
                if lines[j].startswith("]"):
                    lines.insert(j, f"        {str(new_edge)},\n")
                    break
            break

    with open("edges.py", "w") as file:
        file.writelines(lines)

    print("Edge added successfully!")
    graph.add_edge(u, v, w)
    graph.print_graph()


def print_graph_all(graph):
    graph.print_graph()
    

def delete_edge(graph):
    print('------------------------------------------------------------------------------------------')
    u = input("Enter the source vertex: ")
    v = input("Enter the destination vertex: ")
    print('------------------------------------------------------------------------------------------')
    graph.remove_edge(u, v)

import time
import time

def main():
    graph = None
    while True:
        print("""

████████╗██████╗░███████╗██╗░░██╗░█████╗░░█████╗░███╗░░░███╗██████╗░██╗░░░██╗░██████╗
╚══██╔══╝██╔══██╗██╔════╝██║░██╔╝██╔══██╗██╔══██╗████╗░████║██╔══██╗██║░░░██║██╔════╝
░░░██║░░░██████╔╝█████╗░░█████═╝░██║░░╚═╝███████║██╔████╔██║██████╔╝██║░░░██║╚█████╗░
░░░██║░░░██╔══██╗██╔══╝░░██╔═██╗░██║░░██╗██╔══██║██║╚██╔╝██║██╔═══╝░██║░░░██║░╚═══██╗
░░░██║░░░██║░░██║███████╗██║░╚██╗╚█████╔╝██║░░██║██║░╚═╝░██║██║░░░░░╚██████╔╝██████╔╝
░░░╚═╝░░░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝╚═╝░░░░░╚═╝╚═╝░░░░░░╚═════╝░╚═════╝░
              """)
        print('------------------------------------------------------------------------------------------')
        print("\nWelcome to TrekCampus!\n")
        print('------------------------------------------------------------------------------------------')

        user_or_admin = input("Enter 'user', 'admin', or 'exit': ")

        if user_or_admin.lower() == "user":
            while True:
                print("User menu:")
                print('----------------------------------------')
                print("1. Campus navigation")
                print("2. Building navigation")
                print("3. Exit")
                choice = input("Enter your choice (1-3): ")
                print('----------------------------------------')
                if choice == "1":
                    vertices = 54
                    graph = Graph(vertices)
                    graph.edges = edges_main.copy()
                    graph.add_edges_from_list()
                    while True:
                        print("user campus navigation")
                        print('----------------------------------------')
                        print("1. Find shortest path")
                        print("2. print graph")
                        print("3. Exit")
                        print('----------------------------------------')
                        ch = input("Enter your choice (1-3): ")
                    
                        if ch == "1":
                            find_shortest_path(graph)

                        elif ch == "2":
                            print_graph_all(graph)

                        elif ch == "3":
                            break

                        else:
                            print("Invalid choice. Please try again.")

                elif choice == "2":
                        vertices = 56  # Assuming the number of vertices is the same for all floors
                        graphs = []

                        # Create Graph instances for each floor
                        for floor_edges in edges_Ab3:
                            graph = Graph(vertices)
                            graph.edges = floor_edges.copy()
                            for u, v, w in floor_edges:
                                graph.add_edge(u, v, w)
                            graphs.append(graph)

                        # Insert faculty lists into respective graphs
                        for i, graph in enumerate(graphs):
                            if i == 0:  # Ground Floor
                                f1 = faculty_room1_ground
                                f2 = faculty_room2_ground
                            elif i == 1:  # First Floor
                                f1 = faculty_room1_first
                                f2 = faculty_room2_first
                            elif i == 2:  # Second Floor
                                f1 = faculty_room1_second
                                f2 = faculty_room2_second
                            elif i == 3:  # Third Floor
                                f1 = faculty_room1_third
                                f2 = faculty_room2_third

                            graph.fr1 = dlist()
                            graph.fr2 = dlist()

                            for faculty in f1:
                                graph.fr1.insertlast(faculty)
                            for faculty in f2:
                                graph.fr2.insertlast(faculty)

                        while True:
                            print("user building navigation")
                            print('----------------------------------------')
                            print("1. Ground Floor")
                            print("2. First Floor")
                            print("3. Second Floor")
                            print("4. Third Floor")
                            print("5. Find Faculty Member")
                            print("6. Exit")

                            choice = input("Enter your choice (1-6):")

                            if choice == '6':
                                break

                            elif choice == '5':
                                faculty_name = input("Enter the name of the faculty member: ")
                                find_faculty_member_all_floors(graphs, faculty_name)

                            elif choice in ['1', '2', '3', '4']:
                                floor_index = int(choice) - 1
                                graph = graphs[floor_index]

                                while True:
                                    print('----------------------------------------')
                                    print(f"{['Ground Floor', 'First Floor', 'Second Floor', 'Third Floor'][floor_index]}")
                                    print("1. Find shortest path")
                                    print("2. Print graph")
                                    print("3. Enter the faculty list")
                                    print("4. Exit")
                                    ch = input("Enter your choice (1-4): ")

                                    if ch == "1":
                                        find_shortest_path(graph)

                                    elif ch == "2":
                                        print_graph_all(graph)

                                    elif ch == "3":
                                        print("Faculty room 1 teacher's list")
                                        graph.fr1.printlist()
                                        print("Faculty room 2 teacher's list")
                                        graph.fr2.printlist()

                                    elif ch == "4":
                                        break

                                    else:
                                        print("Invalid choice. Please try again.")

                            else:
                                print("Invalid floor choice. Please try again.")

                elif choice == "3":
                    break

                else:
                    print("Invalid choice. Please try again.")
                    print('----------------------------------------')

        elif user_or_admin.lower() == "admin":
            admin_password = input("Enter the admin password: ")
            while True:
                print('--------------------------------------------')
                
                if admin_password == "admin123":

                    print("Admin menu:")
                    print('----------------------------------------')
                    print("1. Campus navigation")
                    print("2. Building navigation")
                    print("3. Exit")

                    choice = input("Enter your choice (1-3): ")
                    print('--------------------------------------------')
                    if choice == "1":
                        vertices = 56
                        graph = Graph(vertices)
                        graph.edges = edges_main.copy()
                        graph.add_edges_from_list()
                        while True:
                            print("Admin campus navigation")
                            print('----------------------------------------')
                            print("1. add edges")
                            print("2. remove edges")
                            print("3. print graph")
                            print("4. Exit")

                            ch = input("Enter your choice (1-4): ")
                            print('----------------------------------------')

                            if ch == "1":
                                add_edge(graph,"campus")

                            elif ch == "2":
                                delete_edge(graph)

                            elif ch == "3":
                                print_graph_all(graph)

                            elif ch == "4":
                                break

                            else:
                                print("Invalid choice. Please try again.")

                    elif choice == "2":
                        while True:
                            print("Admin building navigation")
                            print('----------------------------------------')

                            print("1. Ground Floor")
                            print("2. First Floor")
                            print("3. Second Floor")
                            print("4. Third Floor")
                            print("5. Exit")

                            floor_choice = input("Enter the floor number (1/2/3/4):")

                            if floor_choice == '5':
                                break

                            elif floor_choice in ['1','2','3','4']:
                                floor_index = int(floor_choice) - 1
                                floor_edges = edges_Ab3[floor_index]
                                vertices = 56
                                graph = Graph(vertices)
                                graph.edges = floor_edges.copy()
                                for u,v,w in floor_edges:
                                    graph.add_edge(u,v,w)

                                f1 = None
                                f2 = None
                                graph.fr1 = dlist()
                                graph.fr2 = dlist()
                                if floor_choice == '1':
                                    room="ground"
                                    f1 = faculty_room1_ground
                                    f2 = faculty_room2_ground

                                elif floor_choice == '2':
                                    room="first"
                                    f1 = faculty_room1_first
                                    f2 = faculty_room2_first

                                for i in f1:
                                    graph.fr1.insertlast(i)
                                for i in f2:
                                    graph.fr2.insertlast(i)

                                while True:
                                    print('----------------------------------------')
                                    print("1. add edges")
                                    print("2. remove edges")
                                    print("3. print graph")
                                    print("4.Add Faculty")
                                    print("5.Remove Faculty")
                                    print("6.Faculty list for a floor")
                                    print("7. Exit")

                                    ch = input("Enter your choice (1-7): ")
                                    print('----------------------------------------')

                                    if ch == "1":
                                        add_edge(graph,"building",int(floor_choice))

                                    elif ch == "2":
                                        delete_edge(graph)

                                    elif ch == "3":
                                        print_graph_all(graph)

                                    elif ch == "4":
                                        room_choice = input("Enter the room (fr1 or fr2): ")
                                        name = input("Enter the faculty name: ")
                                        #room=input("Enter whether its ground/first: ")
                                        position = input("Enter the position (first/last): ")

                                        if room_choice == "fr1":
                                            graph.fr1.add_faculty(name, position,room,room_choice)
                                        elif room_choice == "fr2":
                                            graph.fr2.add_faculty(name, position,room,room_choice)
                                        else:
                                            print("Invalid room choice.")

                                    elif ch == "5":
                                        room_choice=input("Enter the room (fr1 or fr2): ")
                                        name = input("Enter the faculty name: ")
                                        room=input("Enter whether its ground/first: ")
                                        position = input("Enter the position (first/last): ")

                                        if room_choice == "fr1":
                                            graph.fr1.remove_faculty(name,room,room_choice)
                                        elif room_choice == "fr2":
                                            graph.fr2.remove_faculty(name,room,room_choice)
                                        else:
                                            print("Invalid room choice.")

                                    elif ch == "6":
                                        print("Faculty room 1 teacher's list")
                                        graph.fr1.printlist()
                                        print("Faculty room 2 teacher's list")
                                        graph.fr2.printlist()

                                    elif ch == "7":
                                        break

                                    else:
                                        print("Invalid choice. Please try again.")
                            else:
                                print("Invalid floor choice. Please try again.")

                    elif choice == "3":
                        print("\nReturning to user/admin selection\n", end="")
                        for _ in range(3):
                            time.sleep(1)
                            print(".", end="", flush=True)
                        print("\n")
                        break
                    else:
                        print("\nInvalid choice. Please try again.\n")
                else:
                    print("Invalid password. Please try again.")
        elif user_or_admin.lower() == "exit":
            print("\nThank you for using TrekCampus! We hope you enjoyed it.\n")
            break
        else:
            print("\nInvalid input. Please enter 'user', 'admin', or 'exit'.\n")

if __name__ == "__main__":
    main()