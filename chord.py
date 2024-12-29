
import hashlib

class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.data = {}  
        self.successor = None  # Liên kết tới nút kế tiếp

    def store_data(self, key, value):
        """Lưu trữ dữ liệu vào nút hiện tại."""
        self.data[key] = value
        print(f"Node {self.node_id} stored key {key} -> value '{value}'")

    def find_successor(self, key_id):
        """Tìm nút chịu trách nhiệm lưu trữ key dựa vào key_id."""
        if self.node_id < key_id <= self.successor.node_id or (self.node_id > self.successor.node_id and (key_id > self.node_id or key_id <= self.successor.node_id)):
            return self.successor
        else:
            return self.successor.find_successor(key_id)

    def __str__(self):
        return f"Node {self.node_id} -> Successor {self.successor.node_id}"


class Chord:
    def __init__(self):
        self.nodes = []

    def hash_function(self, key, m=4):
        """Hàm băm SHA-1 ánh xạ key vào không gian ID (0–2^m-1)."""
        hash_value = int(hashlib.sha1(key.encode()).hexdigest(), 16)
        return hash_value % (2 ** m)

    def add_node(self, node_id):
        """Thêm một nút vào vòng Chord."""
        new_node = Node(node_id)
        if not self.nodes:
            # Nếu đây là nút đầu tiên
            new_node.successor = new_node
            self.nodes.append(new_node)
        else:
            # Tìm vị trí thêm nút
            self.nodes.append(new_node)
            self.nodes.sort(key=lambda x: x.node_id)

            # Cập nhật liên kết successor
            for i in range(len(self.nodes)):
                self.nodes[i].successor = self.nodes[(i + 1) % len(self.nodes)]

        print(f"Added Node {node_id}")
        self.print_nodes()

    def store_data(self, key, value):
        """Lưu trữ dữ liệu vào hệ thống Chord."""
        key_id = self.hash_function(key)
        print(f"Key '{key}' hashed to ID {key_id}")
        responsible_node = self.find_responsible_node(key_id)
        responsible_node.store_data(key_id, value)

    def find_responsible_node(self, key_id):
        """Tìm nút chịu trách nhiệm lưu trữ dữ liệu."""
        for node in self.nodes:
            if node.node_id >= key_id:
                return node
        return self.nodes[0]  # Nếu vượt qua ID lớn nhất, quay lại nút nhỏ nhất

    def query_data(self, key):
        """Truy xuất dữ liệu từ hệ thống Chord."""
        key_id = self.hash_function(key)
        responsible_node = self.find_responsible_node(key_id)
        if key_id in responsible_node.data:
            print(f"Key '{key}' found in Node {responsible_node.node_id} with value '{responsible_node.data[key_id]}'")
            return responsible_node.data[key_id]
        else:
            print(f"Key '{key}' not found in Node {responsible_node.node_id}")
            return None

    def print_nodes(self):
        """In cấu trúc vòng Chord."""
        print("Chord Ring:")
        for node in self.nodes:
            print(node)
        print("")


# Thực nghiệm
if __name__ == "__main__":
    # Khởi tạo hệ thống Chord
    chord = Chord()

    # Thêm các nút vào vòng
    chord.add_node(1)
    chord.add_node(3)
    chord.add_node(7)
    chord.add_node(10)
    chord.add_node(14)

    # Thêm dữ liệu
    chord.store_data("Key1", "A")
    chord.store_data("Key2", "B")
    chord.store_data("Key3", "C")
    chord.store_data("Key4", "D")

    # Truy vấn dữ liệu
    chord.query_data("Key1")
    chord.query_data("Key3")

    # Thêm một nút mới
    chord.add_node(6)

    # Truy vấn lại sau khi thêm nút
    chord.query_data("Key1")
    chord.query_data("Key2")