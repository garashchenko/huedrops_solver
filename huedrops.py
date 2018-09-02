class Hue:
    def __init__(self, x, y, label, connections=None):
        self.label = label
        self.x = x
        self.y = y
        self.connections = connections if connections is not None else []


class HueDropsSolver:
    def __init__(self, hue_drops_board=None):
        self.hue_drops_board = hue_drops_board

    def walk_same_color_hues(self, hue, path_len=1,
                             visited=None,
                             border_elements=None):
        if visited is None:
            visited = []
        if border_elements is None:
            border_elements = []

        visited.append(hue)

        # adjacent hues are adjacent hues of same color
        adj_hues = [c for c in hue.connections
                    if c.label == hue.label and c not in visited]

        # border elements are adjacent hues of other colors
        border_elements.extend([c for c in hue.connections
                                if c.label != hue.label
                                and c not in border_elements])

        if len(adj_hues) == 0:
            return path_len
        for ad in adj_hues:
            path_len = self.walk_same_color_hues(ad, path_len + 1,
                                                 visited=visited,
                                                 border_elements=border_elements)
        return path_len

    def get_solution(self, show_steps=False):
        result = []
        while True:
            visited = []
            borders = []

            # first we visit all hues of top-left color to get border elements
            self.walk_same_color_hues(self.hue_drops_board.board[(0, 0)],
                                      border_elements=borders,
                                      visited=visited)

            # all hues have been visited => they all have got same color => finished
            hues_count = self.hue_drops_board.width * self.hue_drops_board.height
            if len(set(visited)) >= hues_count:
                break

            # now we calculate path lengths for all border hues
            paths = {}
            for border_hue in borders:
                border_visited = []
                self.walk_same_color_hues(border_hue,
                                          visited=border_visited)

                # we summarize results for same color
                # (after new color is filled they all will be joined)
                if border_hue.label in paths:
                    paths[border_hue.label].update(border_visited)
                else:
                    paths[border_hue.label] = set(border_visited)

            best_path_label = max(paths, key=lambda x: len(paths[x]))

            # filling new color
            for v in visited:
                v.label = best_path_label

            result.append(self.hue_drops_board.board[(0, 0)].label)

            if show_steps:
                self.hue_drops_board.output()

        return ' '.join(result)


class HueDropsBoard:

    board = {}

    def __init__(self, width, height, board_input=None):
        self.width = width
        self.height = height
        board_input = board_input if board_input is not None else []
        for y in range(height):
            for x in range(width):
                hue = Hue(x, y, board_input[y][x])
                self.board[(x, y)] = hue
        for hue in self.board.values():
            connections = []

            if hue.y > 0:           # up possible?
                connections.append(self.board[(hue.x, hue.y - 1)])
            if hue.y < height - 1:  # down possible?
                connections.append(self.board[(hue.x, hue.y + 1)])
            if hue.x > 0:           # left possible?
                connections.append(self.board[(hue.x - 1, hue.y)])
            if hue.x < width - 1:   # right possible?
                connections.append(self.board[(hue.x + 1, hue.y)])

            hue.connections = connections.copy()

    def output(self):
        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(self.board[(x, y)].label)
            print(row)
        print(' ')

    @classmethod
    def create_from_user_input(cls):
        width, height = map(int, input().split(" "))
        board_input = []
        for i in range(height):
            row = input().split(" ")
            if len(row) != width:
                raise ValueError('Wrong length of input row')
            board_input.append(row)
        return HueDropsBoard(width, height, board_input)
