from huedrops import HueDropsBoard, HueDropsSolver

board = HueDropsBoard.create_from_user_input()
solution = HueDropsSolver(board).get_solution(show_steps=True)

print(solution)
