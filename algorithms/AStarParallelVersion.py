import heapq
import random
from matplotlib import pyplot as plt
import threading


def generate_large_matrix(size, obstacle_chance=0.3):
    matrix = [[0 if random.random() > obstacle_chance else 1 for _ in range(size)] for _ in range(size)]
    return matrix


def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def reconstruct_path(came_from, start, end):
    path = []
    current = end
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path


def neighbors(matrix, node):
    x, y = node
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    result = []
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(matrix) and 0 <= ny < len(matrix[0]) and matrix[nx][ny] != 1:
            result.append((nx, ny))
    return result


def a_star(matrix, start, end):
    # print('Successfully achieved solution from {} to {}'.format(start, end))

    queue = [(manhattan_distance(start, end), 0, start)]
    came_from = {start: None}
    cost_so_far = {start: 0}

    while queue:
        _, cost, current = heapq.heappop(queue)

        if current == end:
            return reconstruct_path(came_from, start, end)

        for neighbor in neighbors(matrix, current):
            new_cost = cost + 1
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + manhattan_distance(neighbor, end)
                heapq.heappush(queue, (priority, new_cost, neighbor))
                came_from[neighbor] = current

    return []


def visualize_matrix_and_path(matrix, paths=None):
    plt.figure(figsize=(10, 10))
    plt.imshow(matrix, cmap='hot', interpolation='nearest')
    # print(isinstance(paths[0], tuple))
    if isinstance(paths[0], tuple):
        x_coords, y_coords = zip(*paths)
        plt.plot(y_coords, x_coords, marker='o', color='blue')
    else:
        for path in paths:
            if path:
                x_coords, y_coords = zip(*path)
                plt.plot(y_coords, x_coords, marker='o', color='blue')
    plt.show()


def threaded_a_star(matrix, start, goal, results, index):
    path = a_star(matrix, start, goal)
    results[index] = path


def parallel_a_star(matrix, start, end, num_threads):
    results = [None] * num_threads
    threads = []
    endpoints = []

    for i in range(1, num_threads):
        num = i * len(matrix) // num_threads
        temp = (num, num)

        if matrix[temp[0]][temp[1]] == 0:
            endpoints.append(temp)
        else:
            is_valid = False
            j = 1

            while not is_valid:
                temp = (num, num - j)
                j += 1
                if matrix[temp[0]][temp[1]] == 0:
                    is_valid = True
                    endpoints.append(temp)

    endpoints.append(end)

    for i in range(num_threads):
        if i == 0:
            sub_start = start
        else:
            sub_start = endpoints[i - 1]
        sub_goal = endpoints[i]

        t = threading.Thread(target=threaded_a_star, args=(matrix, sub_start, sub_goal, results, i))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # print('Successfully parallel solution from {} to {}'.format(start, end))
    return results
