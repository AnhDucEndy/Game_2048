from random import choice, choices, sample
import numpy as np
from ui import cv2_ui_keyboard as vis
import cv2
import os


class Game2048:

    @staticmethod
    def write_score(username: str, score):
        if not os.path.exists('best_score'):
            os.makedirs('best_score')
        with open(f'best_score/{username}.txt', 'w') as f:
            f.write(str(score))

    @staticmethod
    def read_score(username: str) -> int:
        with open(f'best_score/{username}.txt', 'r') as f:
            score = int(f.read())
        return score

    def __init__(self):

        new_game_value_1 = 2
        new_game_value_2 = choices([4, 2], cum_weights=(1, 3), k=1)[0]

        list_coord = [0, 1, 2, 3]
        
        x_coord_massive = sample(list_coord, 2)
        y_coord_massive = sample(list_coord, 2)
        self.game_field = np.zeros((4, 4), dtype=int)
        self.game_field[x_coord_massive[0]][y_coord_massive[0]] = new_game_value_1
        self.game_field[x_coord_massive[1]][y_coord_massive[1]] = new_game_value_2

        self.previous_game_field = self.game_field.copy()
        self.previous_game_field_for_undo = self.game_field.copy()
        self.accordance = False
        self.none_recursion = True
        self.score = 0
        self.previous_score = 0
        self._previous_matrix()

    def swap_left(self):
        self.previous_game_field = self.game_field.copy()  
        if self.none_recursion:  
            self.previous_game_field_for_undo = self.game_field.copy()
            self.previous_score = self.score
        for k in range(2):
            for j in range(4):
                for i in range(3, -1, -1):

                    if self.game_field[i][j] > 0 and j == 0:
                        continue
                    if self.game_field[i][j] == 0 and j == 3:
                        continue

                    if self.game_field[i][0] > 0 and self.game_field[i][3] > 0 and self.game_field[i][1] == 0:
                        if self.game_field[i][2] == 0:
                            self.game_field[i][1] = self.game_field[i][3]
                            self.game_field[i][3] = 0

                    if self.game_field[i][j] == 0 and j == 0:
                        for p in range(1, 4):
                            if self.game_field[i][p] > 0:
                                self.game_field[i][j] = self.game_field[i][p]
                                self.game_field[i][p] = 0
                                break

                    if self.game_field[i][j] == 0 and self.game_field[i][j + 1] > 0:
                        self.game_field[i][j] = self.game_field[i][j + 1]
                        self.game_field[i][j + 1] = 0
            if k == 0:
                self._sum_elements(direction='left')

        self._previous_matrix()
        if not self.accordance:
            self._add_random_element()
            if self.none_recursion:
                game_over_tag_left = self._game_over_check()
                return game_over_tag_left, self.score 

    def swap_right(self):
        self.previous_game_field = self.game_field.copy()
        if self.none_recursion:
            self.previous_game_field_for_undo = self.game_field.copy()
            self.previous_score = self.score
        for k in range(2):
            for j in range(3, -1, -1):
                for i in range(3, -1, -1):

                    if self.game_field[i][j] > 0 and j == 3:
                        continue
                    if self.game_field[i][j] == 0 and j == 0:
                        continue

                    if self.game_field[i][0] > 0 and self.game_field[i][3] > 0 and self.game_field[i][1] == 0:
                        if self.game_field[i][2] == 0:
                            self.game_field[i][2] = self.game_field[i][0]
                            self.game_field[i][0] = 0

                    if self.game_field[i][j] == 0 and j == 3:
                        for p in range(2, -1, -1):
                            if self.game_field[i][p] > 0:
                                self.game_field[i][j] = self.game_field[i][p]
                                self.game_field[i][p] = 0
                                break

                    if self.game_field[i][j] == 0 and self.game_field[i][j - 1] > 0:
                        self.game_field[i][j] = self.game_field[i][j - 1]
                        self.game_field[i][j - 1] = 0
            if k == 0:
                self._sum_elements(direction='right')

        self._previous_matrix()
        if not self.accordance:
            self._add_random_element()
            if self.none_recursion:
                game_over_tag_right = self._game_over_check()
                return game_over_tag_right, self.score
        return False, self.score

    def swap_down(self):
        self.previous_game_field = self.game_field.copy() 
        if self.none_recursion:  
            self.previous_game_field_for_undo = self.game_field.copy() 
            self.previous_score = self.score 
        for k in range(2):  
            for i in range(3, -1, -1):
                for j in range(3, -1, -1):

                    if self.game_field[i][j] > 0 and i == 3:
                        continue
                    if self.game_field[i][j] == 0 and i == 0:
                        continue
                    if self.game_field[0][j] > 0 and self.game_field[3][j] > 0 and self.game_field[1][j] == 0:
                        if self.game_field[2][j] == 0:
                            self.game_field[2][j] = self.game_field[0][j]
                            self.game_field[0][j] = 0
                    if self.game_field[i][j] == 0 and i == 3:
                        for p in range(2, -1, -1):
                            if self.game_field[p][j] > 0:
                                self.game_field[i][j] = self.game_field[p][j]
                                self.game_field[p][j] = 0
                                break
                    if self.game_field[i][j] == 0 and self.game_field[i - 1][j] > 0:
                        self.game_field[i][j] = self.game_field[i - 1][j]
                        self.game_field[i - 1][j] = 0
            if k == 0:
                self._sum_elements(direction='down')

        self._previous_matrix()
        if not self.accordance:
            self._add_random_element()
            if self.none_recursion:
                game_over_tag_down = self._game_over_check()
                return game_over_tag_down, self.score
        return False, self.score

    def swap_up(self):
        self.previous_game_field = self.game_field.copy()
        if self.none_recursion:
            self.previous_game_field_for_undo = self.game_field.copy()
            self.previous_score = self.score
        for k in range(2):
            for i in range(4):
                for j in range(3, -1, -1):

                    if self.game_field[i][j] > 0 and i == 0:
                        continue
                    if self.game_field[i][j] == 0 and i == 3:
                        continue

                    if self.game_field[0][j] > 0 and self.game_field[3][j] > 0 and self.game_field[1][j] == 0:
                        if self.game_field[2][j] == 0:
                            self.game_field[1][j] = self.game_field[3][j]
                            self.game_field[3][j] = 0

                    if self.game_field[i][j] == 0 and i == 0:
                        for p in range(1, 4):
                            if self.game_field[p][j] > 0:
                                self.game_field[i][j] = self.game_field[p][j]
                                self.game_field[p][j] = 0
                                break

                    if self.game_field[i][j] == 0 and self.game_field[i + 1][j] > 0:
                        self.game_field[i][j] = self.game_field[i + 1][j]
                        self.game_field[i + 1][j] = 0

            if k == 0:
                self._sum_elements(direction='up')

        self._previous_matrix()
        if not self.accordance:
            self._add_random_element()
            if self.none_recursion:
                game_over_tag_up = self._game_over_check()
                return game_over_tag_up, self.score
        return False, self.score

    def _sum_elements(self, direction):

        if direction == 'left':  
            for j in range(4):
                for i in range(3, -1, -1):

                    if self.game_field[i][j] == 0: 
                        continue

                    if self.game_field[i][j] > 0 and j < 3:

                        if self.game_field[i][j] == self.game_field[i][j + 1]:
                            self.game_field[i][j] = self.game_field[i][j] * 2
                            if self.none_recursion:  
                                self.score += self.game_field[i][j]
                            self.game_field[i][j + 1] = 0  

        if direction == 'right':  
            for j in range(3, -1, -1):
                for i in range(3, -1, -1):

                    if self.game_field[i][j] == 0:  
                        continue

                    if self.game_field[i][j] > 0 and j > 0:

                        if self.game_field[i][j] == self.game_field[i][j - 1]:
                            self.game_field[i][j] = self.game_field[i][j] * 2
                            if self.none_recursion:  
                                self.score += self.game_field[i][j]
                            self.game_field[i][j - 1] = 0 

        if direction == 'down':  
            for i in range(3, -1, -1):  
                for j in range(3, -1, -1):

                    if self.game_field[i][j] == 0: 
                        continue
                    if self.game_field[i][j] > 0 and i > 0:
                        if self.game_field[i][j] == self.game_field[i - 1][j]:
                            self.game_field[i][j] = self.game_field[i][j] * 2
                            if self.none_recursion:  
                                self.score += self.game_field[i][j]
                            self.game_field[i - 1][j] = 0 

        if direction == 'up':  
            for i in range(4):
                for j in range(3, -1, -1):

                    if self.game_field[i][j] == 0:
                        continue

                    if self.game_field[i][j] > 0 and i < 3:
                        if self.game_field[i][j] == self.game_field[i + 1][j]:
                            self.game_field[i][j] = self.game_field[i][j] * 2
                            if self.none_recursion:
                                self.score += self.game_field[i][j]
                            self.game_field[i + 1][j] = 0

    def _add_random_element(self):
        index_zeros = [] 

        for i in range(4):
            for j in range(4):
                if self.game_field[i][j] == 0:
                    index_zeros.append([i, j])
        x, y = choice(index_zeros)
        new_value = choices([4, 2], cum_weights=(1, 3), k=1)[0]
        self.game_field[x][y] = new_value  

    def _previous_matrix(self):
        for i in range(4):
            for j in range(4):
                if self.previous_game_field[i][j] == self.game_field[i][j]:
                    self.accordance = True  
                else:
                    self.accordance = False
                    return

    def _game_over_check(self):

        self.none_recursion = False  
        self.previous_game_field = self.game_field.copy() 

        left_game_over_check = False
        right_game_over_check = False  
        down_game_over_check = False  
        up_game_over_check = False  

        for i in range(4):

            if i == 0:
                self.swap_left()  
            elif i == 1:
                self.swap_right()  
            elif i == 2:
                self.swap_down() 
            elif i == 3:
                self.swap_up() 

            self._previous_matrix()

            if self.accordance:
                if i == 0:
                    left_game_over_check = True
                elif i == 1:
                    right_game_over_check = True
                elif i == 2:
                    down_game_over_check = True
                elif i == 3:
                    up_game_over_check = True

            self.game_field = self.previous_game_field.copy() 
        self.none_recursion = True 

        game_over = left_game_over_check and right_game_over_check and down_game_over_check and up_game_over_check
        return game_over

    def undo_step(self):
        self.score = self.previous_score
        self.game_field = self.previous_game_field_for_undo.copy()


if __name__ == '__main__': 

    game = Game2048()

    player = input('Enter the username: ')
    try:
        best_score = Game2048.read_score(player)
    except IOError:
        best_score = 0
        Game2048.write_score(player, best_score)

    game_score = 0
    game_end = False
    game_end_lock = False

    while True:

        key = cv2.waitKey(0)

        if key == 27:
            game = None
            break

        if key == ord('a') or key == 244:
            game_end, game_score = game.swap_left()

        if key == ord('d') or key == 226:
            game_end, game_score = game.swap_right()

        if key == ord('s') or key == 251:
            game_end, game_score = game.swap_down()

        if key == ord('w') or key == 246:
            game_end, game_score = game.swap_up()

        if key == ord('z') or key == 255:
            game.undo_step()

        if key == ord('5') or key == 53:
            del game
            game_end_lock = game_end
            game_end = False
            game_score = 0
            game = Game2048()

        if game_end:
            game_end_lock = game_end

        if game_score > best_score:
            Game2048.write_score(player, game_score)
            best_score = Game2048.read_score(player)
        vis.image_game_field(game.game_field, player, game_score, best_score, game_end_lock)

    cv2.destroyAllWindows()
