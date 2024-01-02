import numpy as np
from .agent import *


class myAgent(Agent):
    def __init__(self, matrix):
        super().__init__(matrix)

    def solve_puzzle(self):
        # priority queue tanimliyoruz
        self.frontier = PriorityQueue()
        self.explored = set()

        print(self.frontier)
        print(self.explored)

        # Baslangic node'u olusturuluyor
        start_node = Node(None, self.empty_tile, self.initial_matrix)
        start_node.g_score = 0
        start_node.h_score = self.calculate_heuristic(start_node.matrix)
        start_node.f_score = start_node.g_score + start_node.h_score

        print(start_node.f_score)

        # baslangic node'u priority queue'ye ekleniyor
        self.frontier.push(start_node, start_node.f_score)

        # A* Algorithm
        while not self.frontier.isEmpty():
            # F skoru en dusuk olan node'u popluyoruz.
            current_node = self.frontier.pop()

            # Hedefe ulasildi mi?
            if self.checkEqual(current_node.matrix, self.desired_matrix):
                return self.get_moves(current_node)

            # İslemekte oldugumuz node'u explored kumesine al.
            self.explored.add(tuple(map(tuple, current_node.matrix)))

            for direction in self.directions:
                new_position = (current_node.position[0] + direction[0], current_node.position[1] + direction[1])
                if 0 <= new_position[0] < self.game_size and 0 <= new_position[1] < self.game_size:
                    # Successor matrixi olusturuluyor.
                    successor_matrix = [row[:] for row in current_node.matrix]
                    successor_matrix[current_node.position[0]][current_node.position[1]], successor_matrix[new_position[0]][new_position[1]] = successor_matrix[new_position[0]][new_position[1]], successor_matrix[current_node.position[0]][current_node.position[1]]

                    # Yeni node olusturuluyor
                    successor_node = Node(current_node, new_position, successor_matrix, current_node.g_score + 1)
                    successor_node.h_score = self.calculate_heuristic(successor_matrix)
                    successor_node.f_score = successor_node.g_score + successor_node.h_score

                    # bulundugumuz state'in explored olup olmadigini ya da daha yuksek bir scorunun olup olmadigini kontrol ediyoruz.
                    if not tuple(map(tuple, successor_matrix)) in self.explored and not self.frontier.contains(successor_matrix):
                        self.frontier.push(successor_node, successor_node.f_score)

        return []  # Cozum bulunamadiysa bos liste dondur.

    def calculate_heuristic(self, matrix):
            """
            Calculate the Manhattan distance for the puzzle.

            Args:
                matrix (array): The current game matrix.

            Returns:
                int: The Manhattan distance of the current state to the goal state.
            """
            h_score = 0
            for i in range(self.game_size):
                for j in range(self.game_size):
                    tile = matrix[i][j]
                    if tile != 0:  #Boş olan kareyi gec
                        # Desired matrix'te karenin istenen pozisyonu
                        target_i, target_j = divmod(tile - 1, self.game_size)
                        # Karenin Manhattan distance'ini ekliyoruz.
                        h_score += abs(target_i - i) + abs(target_j - j)
            return h_score
