import pygame.font
from pygame.sprite import Group

from ship import Ship


class Scoreboard:

    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.min_pos = 4
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # preparing initiol score image
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):

        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(
            score_str, True, self.text_color, self.settings.bg_color)

        # display score at topright
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def prep_high_score(self):
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(
            high_score_str, True, self.text_color, self.settings.bg_color)

        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def check_high_scores(self):
        if len(self.stats.high_scores_list) == 5:

            if not self.stats.high_score_flag and self.stats.score > min(self.stats.high_scores_list):
                self.min_pos = self.stats.high_scores_list.index(
                    min(self.stats.high_scores_list))
                self.stats.high_scores_list[self.min_pos] = self.stats.score
                self.stats.high_score = max(self.stats.high_scores_list)
                self.stats.high_scores_dict[self.stats.username] = self.stats.high_scores_list
                self.stats.save_highscores()
                self.prep_high_score()
                self.stats.high_score_flag = True

            if self.stats.high_score_flag and self.stats.score > self.stats.high_scores_list[self.min_pos]:
                self.stats.high_scores_list[self.min_pos] = self.stats.score
                self.stats.high_score = max(self.stats.high_scores_list)
                self.stats.high_scores_dict[self.stats.username] = self.stats.high_scores_list
                self.stats.save_highscores()
                self.prep_high_score()

        else:
            if self.stats.high_score_flag and self.stats.score > self.stats.high_scores_list[len(self.stats.high_scores_list) - 1]:
                self.stats.high_scores_list[len(
                    self.stats.high_scores_list) - 1] = self.stats.score
                self.stats.high_score = max(self.stats.high_scores_list)
                self.stats.high_scores_dict[self.stats.username] = self.stats.high_scores_list
                self.stats.save_highscores()
                self.prep_high_score()

            if not self.stats.high_score_flag:
                self.stats.high_scores_list.append(self.stats.score)
                self.stats.high_score = max(self.stats.high_scores_list)
                self.stats.high_scores_dict[self.stats.username] = self.stats.high_scores_list
                self.stats.save_highscores()
                self.prep_high_score()
                self.stats.high_score_flag = True

    def prep_level(self):
        level_str = str(self.stats.level)
        self.level_image = self.font.render(
            level_str, True, self.text_color, self.settings.bg_color)

        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)
