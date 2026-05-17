import pygame
from time import sleep
from menu.text import Text
from menu.button import Button
from menu.textbox import TextBox
from menu.popup import PopUp
from material_indicator import MaterialIndicator

class Menu:
    def __init__(self, program):
        self.screen = program.screen
        self.program = program

        self.width = self.screen.get_width()
        self.height = self.screen.get_height()

        self.white_won = False
        self.black_won = False
        self.draw = False

        self.which_screen = 0 # 0 - Menu, 1 - Bot, 2 - PvP, 3 - Entering name p1, 4 - Entering name p2, 5 - "Are you sure?" popup
        self.prev_screen = 0

        self.background_color = (12, 157, 10)
        self.button_color_light = (255, 255, 255)
        self.button_color_dark = (0, 0, 0)

        self.font = pygame.font.SysFont("comicsans", 30)
        self.font2 = pygame.font.SysFont("comicsans", 60)

        # Menu

        self.title = Text(-1, 50, "Chess", self.font2, self.button_color_dark, self.screen)
        self.button_bot = Button(-1, 200, 100, 50, self.button_color_light, self.button_color_dark, "Bot", self.font, (255, 255, 255), self.screen)
        self.button_pvp = Button(-1, 300, 100, 50, self.button_color_light, self.button_color_dark, "PvP", self.font, (255, 255, 255), self.screen)
        self.button_quit = Button(-1, 400, 100, 50, self.button_color_light, self.button_color_dark, "Quit", self.font, (255, 255, 255), self.screen)

        # Board

        self.resign_button_bottom = Button(self.width - 120, self.height - 45, 110, 40, self.button_color_light, self.button_color_dark,
                                           "Resign", self.font, self.button_color_light, self.screen)

        self.resign_button_top = Button(self.width - 120, 5, 110, 40, self.button_color_light, self.button_color_dark,
                                        "Resign", self.font, self.button_color_light, self.screen)

        self.draw_button_top = Button(self.width - 240, 5, 110, 40, self.button_color_light, self.button_color_dark,
                                   "Draw", self.font, self.button_color_light, self.screen)

        self.draw_button_bottom = Button(self.width - 240, self.height - 45, 110, 40, self.button_color_light, self.button_color_dark,
                                   "Draw", self.font, self.button_color_light, self.screen)

        # Entering name 1

        self.player1_tip = Text(-1, 50, "Enter Player1 name", self.font, self.button_color_dark, self.screen)
        self.text_box_p1 = TextBox(-1, 100, 300, 50, self.button_color_light, self.button_color_dark, self.font, self.button_color_dark, self.screen)
        self.confirm_button_p1 = Button(-1, 160, 200, 50, self.button_color_light, self.button_color_dark, "Confirm", self.font, self.button_color_light, self.screen)

        # Entering name 2

        self.player2_tip = Text(-1, 50, "Enter Player2 name", self.font, self.button_color_dark, self.screen)
        self.text_box_p2 = TextBox(-1, 100, 300, 50, self.button_color_light, self.button_color_dark, self.font, self.button_color_dark, self.screen)
        self.confirm_button_p2 = Button(-1, 160, 200, 50, self.button_color_light, self.button_color_dark, "Confirm", self.font, self.button_color_light, self.screen)

        self.player_top_text = Text(0, 0, "", self.font, self.button_color_dark, self.screen)
        self.player_bottom_text = Text(0, self.height - 45, "", self.font, self.button_color_dark, self.screen)

        # Drawing

        self.top_is_drawing = False
        self.bottom_is_drawing = False

        self.back_button = Button(5, 5, 100, 50, self.button_color_light, self.button_color_dark, "Back", self.font, self.button_color_light, self.screen)

        # Victory and draw texts

        self.white_won_text = Text(-1, -1, "White Won", self.font2, self.button_color_dark, self.screen)
        self.black_won_text = Text(-1, -1, "Black Won", self.font2, self.button_color_dark, self.screen)
        self.draw_text = Text(-1, -1, "Draw", self.font2, self.button_color_dark, self.screen)

        # "Are you sure?" popup

        self.ays_popup = PopUp("Are you sure?", self.font, "Yes", "No", self.button_color_light, self.button_color_dark, self.button_color_light,
                               (123,123,123), 250, 200, self.screen)

        self.white_material_indicator = MaterialIndicator(0, (0,0,0), self.font, 100, 5, self.screen)
        self.black_material_indicator = MaterialIndicator(1, (0,0,0), self.font, 100, self.screen.get_width() - 45, self.screen)

    def update_names(self, name_top, name_bottom):
        self.player_top_text.text = name_top
        self.player_bottom_text.text = name_bottom

    def swap_players(self):
        self.player_top_text.text, self.player_bottom_text.text = self.player_bottom_text.text, self.player_top_text.text
        self.top_is_drawing, self.bottom_is_drawing = self.bottom_is_drawing, self.top_is_drawing

    def process_mouse_click(self, mouse_pos):
        # Main menu
        if self.which_screen == 0:
            # Bot button
            if self.button_bot.check_mouse_pos(mouse_pos):
                self.update_names("Bot", "Player")
                self.program.game_running = True
                self.program.game.reset(True)
                self.which_screen = 1
                
            # PvP button
            elif self.button_pvp.check_mouse_pos(mouse_pos):
                self.which_screen = 3
                self.text_box_p1.active = True
            
            # Quit button
            elif self.button_quit.check_mouse_pos(mouse_pos):
                pygame.quit()
        
        # Player versus Bot
        elif self.which_screen == 1:
            # Resign button
            if self.resign_button_bottom.check_mouse_pos(mouse_pos):
                self.which_screen = 5
                self.prev_screen = 1
                self.program.game_running = False
        
        # Player versus Player
        elif self.which_screen == 2:
            # Any of the resign buttons
            if self.resign_button_top.check_mouse_pos(mouse_pos) or self.resign_button_bottom.check_mouse_pos(mouse_pos):
                self.program.game_running = False
                self.which_screen = 5
                self.prev_screen = 2
            
            # Draw button top
            elif self.draw_button_top.check_mouse_pos(mouse_pos):
                self.top_is_drawing = not self.top_is_drawing
            
            # Draw button bottom
            elif self.draw_button_bottom.check_mouse_pos(mouse_pos):
                self.bottom_is_drawing = not self.bottom_is_drawing
            
            # Quitting if both players are offering a draw
            if self.top_is_drawing and self.bottom_is_drawing:
                self.program.game_running = False
                self.top_is_drawing = False
                self.bottom_is_drawing = False
                self.draw_button_top.update_text("Draw")
                self.draw_button_bottom.update_text("Draw")
                self.which_screen = 0
        
        # Entering name 1
        elif self.which_screen == 3:
            # Activating the textbox
            if self.text_box_p1.check_mouse_pos(mouse_pos):
                self.text_box_p1.active = True
            
            # Confirm button
            elif self.confirm_button_p1.check_mouse_pos(mouse_pos):
                self.text_box_p1.active = False
                self.text_box_p2.active = True
                self.which_screen = 4

            # Backing out
            elif self.back_button.check_mouse_pos(mouse_pos):
                self.text_box_p1.active = False
                self.text_box_p1.string = ""
                self.text_box_p2.string = ""
                self.which_screen = 0

            # Deactivating textbox 1
            else:
                self.text_box_p1.active = False

        # Entering name 2
        elif self.which_screen == 4:
            # Activating the textbox
            if self.text_box_p2.check_mouse_pos(mouse_pos):
                self.text_box_p2.active = True

            # Confirm button
            elif self.confirm_button_p2.check_mouse_pos(mouse_pos):
                self.text_box_p2.active = False
                self.update_names(self.text_box_p1.string, self.text_box_p2.string)
                self.text_box_p1.string = ""
                self.text_box_p2.string = ""
                self.program.game_running = True
                self.program.game.reset(False)
                if self.player_top_text.get_width() > self.player_bottom_text.get_width():
                    self.white_material_indicator.x = self.player_top_text.get_width() + 10
                    self.black_material_indicator.x = self.player_top_text.get_width() + 10
                else:
                    self.white_material_indicator.x = self.player_bottom_text.get_width() + 10
                    self.black_material_indicator.x = self.player_bottom_text.get_width() + 10
                self.which_screen = 2

            # Backing out
            elif self.back_button.check_mouse_pos(mouse_pos):
                self.text_box_p2.active = False
                self.text_box_p1.string = ""
                self.text_box_p2.string = ""
                self.which_screen = 0

            # Deactivating textbox 2
            else:
                self.text_box_p2.active = False

        elif self.which_screen == 5:
            # Yes
            if self.ays_popup.button1.check_mouse_pos(mouse_pos):
                self.which_screen = 0
                self.top_is_drawing = False
                self.bottom_is_drawing = False
            # No
            elif self.ays_popup.button2.check_mouse_pos(mouse_pos):
                self.which_screen = self.prev_screen
                self.program.game_running = True

    def process_keyboard_clicks(self, unicode, key):
        if self.which_screen == 3 and self.text_box_p1.active:
            self.text_box_p1.update_text(unicode, key)
        elif self.which_screen == 4 and self.text_box_p2.active:
            self.text_box_p2.update_text(unicode, key)

    def update(self, mouse_pos):
        # Main menu
        if self.which_screen == 0:
            self.title.update()

            self.button_bot.draw(mouse_pos)
            self.button_pvp.draw(mouse_pos)
            self.button_quit.draw(mouse_pos)

        # Player versus Bot
        elif self.which_screen == 1:
            pygame.draw.rect(self.screen, self.button_color_light, [0, 0, self.width, 50])
            pygame.draw.rect(self.screen, self.button_color_light, [0, self.height - 50, self.width, 50])

            self.player_top_text.update()
            self.player_bottom_text.update()

            self.resign_button_bottom.draw(mouse_pos)

        # Player versus Player
        elif self.which_screen == 2:
            pygame.draw.rect(self.screen, self.button_color_light, [0, 0, self.width, 50])
            pygame.draw.rect(self.screen, self.button_color_light, [0, self.height - 50, self.width, 50])

            self.player_top_text.update()
            self.player_bottom_text.update()

            self.resign_button_top.draw(mouse_pos)
            self.resign_button_bottom.draw(mouse_pos)

            self.draw_button_top.draw(mouse_pos)
            self.draw_button_bottom.draw(mouse_pos)

            if self.bottom_is_drawing:
                self.draw_button_bottom.update_text("Undraw")
            else:
                self.draw_button_bottom.update_text("Draw")

            if self.top_is_drawing:
                self.draw_button_top.update_text("Undraw")
            else:
                self.draw_button_top.update_text("Draw")

        # Entering name 1
        elif self.which_screen == 3:
            self.player1_tip.update()

            self.text_box_p1.draw()

            self.confirm_button_p1.draw(mouse_pos)

            self.back_button.draw(mouse_pos)

        # Entering name 2
        elif self.which_screen == 4:
            self.player2_tip.update()

            self.text_box_p2.draw()

            self.confirm_button_p2.draw(mouse_pos)

            self.back_button.draw(mouse_pos)

        # "Are you sure?" popup
        elif self.which_screen == 5:
            self.ays_popup.draw(self.screen, mouse_pos)

        # Drawing the material indicators
        if self.which_screen == 1 or self.which_screen == 2:
            white_captured_pieces = self.program.game.get_white_captured_pieces()
            black_captured_pieces = self.program.game.get_black_captured_pieces()
            white_advantage = self.program.game.get_white_material_advantage()
            if (self.program.game.flip and self.program.game.whose_turn) or (not self.program.game.flip and self.program.game.white_is_player):
                self.white_material_indicator.y, self.white_material_indicator.text.y = self.screen.get_height() - 45, self.screen.get_height() - 45
                self.black_material_indicator.y, self.black_material_indicator.text.y = 5, 5
            else:
                self.white_material_indicator.y, self.white_material_indicator.text.y = 5, 5
                self.black_material_indicator.y, self.black_material_indicator.text.y = self.screen.get_height() - 45, self.screen.get_height() - 45
            self.white_material_indicator.update(black_captured_pieces, white_advantage)
            self.black_material_indicator.update(white_captured_pieces, -white_advantage)


        if self.white_won:
            self.white_won_text.update()
            pygame.display.update()
            sleep(5)
            self.white_won = False
            self.program.game_running = False
            self.which_screen = 0

        elif self.black_won:
            self.black_won_text.update()
            pygame.display.update()
            sleep(5)
            self.black_won = False
            self.program.game_running = False
            self.which_screen = 0

        elif self.draw:
            self.draw_text.update()
            pygame.display.update()
            sleep(5)
            self.draw = False
            self.program.game_running = False
            self.which_screen = 0