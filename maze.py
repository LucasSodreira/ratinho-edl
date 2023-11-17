def solveMaze(maze_list, mouse_x, mouse_y, exit):
    visiteds_path = []
    correct_path = []

    def is_valid(x, y):
        return 0 <= x < len(maze_list[0]) and 0 <= y < len(maze_list)

    while (mouse_x, mouse_y) != (exit[0], exit[1]):
        position = (mouse_x, mouse_y)
        if is_valid(mouse_x + 1, mouse_y) and maze_list[mouse_y][mouse_x + 1] in ["0", "e"] and (mouse_x + 1, mouse_y) not in visiteds_path:
            mouse_x += 1
            visiteds_path.append((mouse_x, mouse_y))
            correct_path.append(position)

        elif is_valid(mouse_x - 1, mouse_y) and maze_list[mouse_y][mouse_x - 1] in ["0", "e"] and (mouse_x - 1, mouse_y) not in visiteds_path:
            mouse_x -= 1
            visiteds_path.append((mouse_x, mouse_y))
            correct_path.append(position)

        elif is_valid(mouse_x, mouse_y + 1) and maze_list[mouse_y + 1][mouse_x] in ["0", "e"] and (mouse_x, mouse_y + 1) not in visiteds_path:
            mouse_y += 1
            visiteds_path.append((mouse_x, mouse_y))
            correct_path.append(position)

        elif is_valid(mouse_x, mouse_y - 1) and maze_list[mouse_y - 1][mouse_x] in ["0", "e"] and (mouse_x, mouse_y - 1) not in visiteds_path:
            mouse_y -= 1
            visiteds_path.append((mouse_x, mouse_y))
            correct_path.append(position)
        else:
            last_position = correct_path.pop()
            mouse_x, mouse_y = last_position

    return correct_path, visiteds_path