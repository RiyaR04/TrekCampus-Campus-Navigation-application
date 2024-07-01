class dlist:
    class Node:
        def _init_(self, e):
            self.element = e
            self.prev = None
            self.next = None

    def _init_(self):
        self.head = None
        self.tail = None
        self.size = 0
        self.max = 10

    def insertfirst(self, e):
        newnode = self.Node(e)
        if self.size == self.max:
            print("no availability of cabin")
            return False
        elif self.size == 0:
            self.head = self.tail = newnode
        else:
            newnode.next = self.head
            self.head.prev = newnode
            self.head = newnode
        self.size += 1

        return True

    def insertlast(self, e):
        newnode = self.Node(e)
        if self.size == self.max:
            print("no availability of cabin")
            return False
        elif self.size == 0:
            self.head = self.tail = newnode
        else:
            self.tail.next = newnode
            newnode.prev = self.tail
            self.tail = newnode
        self.size += 1

        return True


    def printlist(self):
        if self.size == 0:
            print("list is empty")
        else:
            c = self.head
            while c:
                print(c.element, end=" ")
                c = c.next
            print()

    def add_faculty(self, name, position,floor_index,room_choice):
        if position == "first":
            t = self.insertfirst(name)
            if t == False:
                return
        elif position == "last":
            t = self.insertlast(name)
            if t == False:
                return
        self.update_faculty_list(floor_index,room_choice)

    def remove_faculty(self, name, floor_index,room_choice):
        current = self.head
        prev = None
        while current:
            if current.element == name:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                self.update_faculty_list(floor_index,room_choice)
                return
            prev = current
            current = current.next

    def print_faculty(self):
        current = self.head
        while current:
            print(current.element, end=" -> ")
            current = current.next
        print("None")
    
    def update_faculty_list(self, floor_index,room_choice):
        with open("edges.py", "r") as file:
            lines = file.readlines()
        room = None

        if floor_index == 0:
            room = "ground"
        elif floor_index == 1:
            room = "first"
        elif floor_index == 2:
            room = "second"
        elif floor_index == 3:
            room = "third"

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