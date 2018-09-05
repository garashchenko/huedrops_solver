from collections import namedtuple


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
            visited = set()
        if border_elements is None:
            border_elements = set()

        visited.add(hue)

        # adjacent hues are adjacent hues of same color
        adj_hues = [c for c in hue.connections
                    if c.label == hue.label and c not in visited]

        # border elements are adjacent hues of other colors
        border_elements.update([c for c in hue.connections
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

        WalkResults = namedtuple('WalkResults', ['visited', 'border'])

        result = []
        paths = {}
        visited = set()
        borders = set()

        while True:

            summed_up_paths = {}

            # for the very first time we visit all hues of top-left color to get border elements
            # then we will used visited hues from previous steps
            if not visited:
                self.walk_same_color_hues(self.hue_drops_board.board[(0, 0)],
                                          border_elements=borders,
                                          visited=visited)

            # all hues have been visited => they all have got same color => finished
            hues_count = self.hue_drops_board.width * self.hue_drops_board.height
            if len(visited) >= hues_count:
                break

            # now we calculate path lengths for all border hues
            # visited and border elements are saved to a dict to avoid duplicate calculations
            for border_hue in borders:
                border_hue_visited = set()
                border_hue_border = set()
                if border_hue not in paths:
                    self.walk_same_color_hues(border_hue,
                                              visited=border_hue_visited,
                                              border_elements=border_hue_border)
                    paths[border_hue] = WalkResults(visited=border_hue_visited, border=border_hue_border)
                else:
                    border_hue_visited = paths[border_hue].visited
                    border_hue_border = paths[border_hue].border

                # we summarize results for same color
                # (after new color is filled they all will be joined)
                if border_hue.label in summed_up_paths:
                    summed_up_paths[border_hue.label].visited.update(border_hue_visited)
                    summed_up_paths[border_hue.label].border.update(border_hue_border)
                else:
                    summed_up_paths[border_hue.label] = WalkResults(border_hue_visited, border_hue_border)

            best_path_label = max(summed_up_paths, key=lambda x: len(summed_up_paths[x].visited))

            visited.update(summed_up_paths[best_path_label].visited)
            borders.update(summed_up_paths[best_path_label].border)
            borders = borders - visited

            # filling new color
            # hue's visited and border have to be recalculated if it has changed its color
            for v in visited:
                v.label = best_path_label
                paths.pop(v, None)

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

    @classmethod
    def create_from_file(cls, file):
        width, height = map(int, input().split(" "))
        board_input = []
        with open(file, 'r') as board_file:
            for line in board_file:
                board_input.append(line.rstrip().split(" "))
        return HueDropsBoard(width, height, board_input)
