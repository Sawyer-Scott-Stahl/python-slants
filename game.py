"""
This is a recreation of the game "Slants" in an Android puzzle game collection I have. This will be split into
4 main parts, which will be in different .py files for ease of maintenance.

1. The game itself (this script), which has input for the game board that can be either entered manually or generated.
2. An AI that solves the games, first through pre-coded rules and then through brute force if necessary.
3. A gameboard generator that will (hopefully) generate boards that only have one solution and are solvable
    either without brute force or without too much brute force.
4. A menu system

A few things:
    - width and height refers to the CELLS of the board
    - the matrix is referring to the LINES of the board
    - the cells of the board are numbered starting with 1, starting from left and top
    - the lines of the board are numbered starting with 0, starting from left and top
    - therefore a cell defines the number of the line to the RIGHT of it and BELOW it
    - the topmost line isn't below any cell, so it is 0
    - the leftmost line isn't right of any cell, so it is 0
    - slants: 0 = no slant, 1 = slant top left to bottom right, 2 = slant top right to bottom left
    - solved: 0 = neutral, 1 = solved, 2 = wrong

The Game to-do list:
    - Read the board.txt and put all the info the appropriate places DONE
    - Size the board properly based on board.txt DONE
    - Build in click handling (placing slants) DONE
    - Check if numbers are neutral, solved, or wrong DONE
    - Draw basic board DONE
    - Draw number solve state DONE
    - Draw slants DONE
    - Fill in set cells DONE
    - Highlight moused over cells DONE
    - Make bottom bar menu visuals / function binding: DONE
        - undo / redo DONE
        - help DONE
        - menu DONE
    - Help DONE
    - Menu DONE
    - Restart DONE
    - New game DONE
    - Undo / Redo DONE
    - Loop recognition DONE
    - Change slant color for loops DONE
    - Check for solve:
        - check if all cells filled in DONE
        - check for solved numbers DONE
        - check for loops DONE

    - New game okay
    - Solve with AI
    - Main Menu
    - Win screen

    - bug test undo/redo : some issue there?

"""

import pygame
import sys
import random
import os
pygame.init()


# Holds general variables, including functional variables
class General:
    def __init__(self):
        self.g_fps = 30
        self.g_undolimit = 999999
        self.g_boardSize_max = 40
        self.g_boardSize_min = 4

        self.g_width = 800
        self.g_height = 900
        self.g_fillColor = [0, 0, 0]
        self.g_transColor = [0, 0, 0]
        self.g_transAlpha = 150
        self.g_colorkey = [255, 0, 255]

        # Testing
        self.g_testing_fps = 1
        self.g_testing_undoredo = 0
        self.g_testing_loops = 0
        self.g_testing_winscreen = 1

        # Don't change these
        self.g_cellMouseover = "none"
        self.g_moveList = [[""]]
        self.g_currentMove = 0
        self.g_widthInput = ""
        self.g_heightInput = ""
        self.g_widthActive = 0
        self.g_heightActive = 0
        self.g_solvedMatrix = []
        self.g_slantDict = {}

        self.g_loopDict = {}
        self.g_connectDict = {}
        self.g_pathDict = {}

        self.g_alreadywon = 0


general = General()


# Holds Game Screen visual variables
class Gamescreen:
    def __init__(self):
        # Board general
        self.gs_board_bufferx = 50
        self.gs_sizeScale = 60

        # Lines
        self.gs_lineWidth = 3
        self.gs_lineColor = [255, 255, 255]

        # Cells
        self.gs_cell_hoverColor = [255, 100, 100]
        self.gs_cell_solvedColor = [100, 100, 100]

        # Circles
        self.gs_circleRadius_def = 20
        self.gs_circleWidth = 2
        self.gs_circleOutlineColor_neutral = [255, 255, 255]
        self.gs_circleFillColor_neutral = [0, 0, 0]
        self.gs_circleOutlineColor_solved = [50, 50, 50]
        self.gs_circleFillColor_solved = [100, 100, 100]
        self.gs_circleOutlineColor_wrong = [200, 0, 0]
        self.gs_circleFillColor_wrong = [0, 0, 0]

        # Numbers
        self.gs_numColor_neutral = [255, 255, 255]
        self.gs_numColor_solved = [50, 50, 50]
        self.gs_numColor_wrong = [200, 0, 0]
        self.gs_numSize_def = 20
        self.gs_numFont = "opensans.ttf"

        self.gs_0nudgex_def = 2
        self.gs_1nudgex_def = 0
        self.gs_2nudgex_def = 2
        self.gs_3nudgex_def = 2
        self.gs_4nudgex_def = 0

        # Slants
        self.gs_slantWidth = 5
        self.gs_slantColor = [255, 255, 255]
        self.gs_slantColor_loop = [255, 0, 0]


gamescreen = Gamescreen()


# Holds BotBar visual variables
class BotBar:
    def __init__(self):
        # General
        self.bb_height = 100
        self.bb_fillColor = [100, 100, 100]

        # Button General
        self.bb_button_borderSize = 5
        self.bb_button_borderColor = [0, 0, 0]
        self.bb_button_fillColor = [245, 245, 50]
        self.bb_button_hoverColor = [200, 200, 50]
        self.bb_button_graphicColor = [0, 0, 0]

        # Button Positioning
        self.bb_button_bufferc = 10
        self.bb_button_buffery = 10
        self.bb_button_bufferx = 50

        # Help Button
        self.bb_help_textColor = [0, 0, 0]
        self.bb_help_textSize = 70
        self.bb_help_textFont = "opensans.ttf"
        self.bb_help_textStr = "?"

        self.bb_help_text_nudgex = 2
        self.bb_help_text_nudgey = -2

        # Menu Button
        self.bb_menu_graphic_color = [0, 0, 0]
        self.bb_menu_graphic_width = 8

        self.bb_menu_graphic_bufferx = 10
        self.bb_menu_graphic_buffery = 10
        self.bb_menu_graphic_nudgex = 0
        self.bb_menu_graphic_nudgey = 3

        # Undo Button
        self.bb_undo_graphic_file = pygame.image.load("assets/undo.png")
        self.bb_redo_graphic_file = pygame.image.load("assets/redo.png")

        self.bb_undo_graphic_nudgex = -5
        self.bb_undo_graphic_nudgey = -4
        self.bb_redo_graphic_nudgex = -5
        self.bb_redo_graphic_nudgey = -5

        # =====Dependent Variables=====
        button_size = int(self.bb_height - (self.bb_button_buffery * 2))

        # Bottom Bar
        self.bb_rect = [0,
                        general.g_height - self.bb_height,
                        general.g_width,
                        self.bb_height]

        # Help Button
        self.bb_help_borderRect = [self.bb_button_bufferx,
                                   general.g_height - self.bb_height + self.bb_button_buffery,
                                   button_size,
                                   button_size]

        self.bb_help_rect = [self.bb_help_borderRect[0] + self.bb_button_borderSize,
                             self.bb_help_borderRect[1] + self.bb_button_borderSize,
                             self.bb_help_borderRect[2] - (self.bb_button_borderSize * 2),
                             self.bb_help_borderRect[3] - (self.bb_button_borderSize * 2)]

        self.bb_helpFont = pygame.font.Font(self.bb_help_textFont, self.bb_help_textSize)
        self.bb_helpText = self.bb_helpFont.render(self.bb_help_textStr, 1, self.bb_help_textColor)
        helptextw = self.bb_helpText.get_rect().width
        helptexth = self.bb_helpText.get_rect().height
        self.bb_helpText_x = (self.bb_help_borderRect[0] + (self.bb_help_borderRect[2] / 2) -
                              (helptextw / 2) + self.bb_help_text_nudgex)
        self.bb_helpText_y = (self.bb_help_borderRect[1] + (self.bb_help_borderRect[3] / 2) -
                              (helptexth / 2) + self.bb_help_text_nudgey)

        # Menu Button
        self.bb_menu_borderRect = [general.g_width - self.bb_button_bufferx - button_size,
                                   general.g_height - self.bb_height + self.bb_button_buffery,
                                   button_size,
                                   button_size]

        self.bb_menu_rect = [self.bb_menu_borderRect[0] + self.bb_button_borderSize,
                             self.bb_menu_borderRect[1] + self.bb_button_borderSize,
                             self.bb_menu_borderRect[2] - (self.bb_button_borderSize * 2),
                             self.bb_menu_borderRect[3] - (self.bb_button_borderSize * 2)]

        menu_graphic_spacing = int(
            ((button_size - (self.bb_button_borderSize * 2) - (self.bb_menu_graphic_buffery * 2) -
              self.bb_menu_graphic_width) / 2) - self.bb_menu_graphic_width)

        self.bb_menu_graphic1_a = [self.bb_menu_rect[0] + self.bb_menu_graphic_bufferx + self.bb_menu_graphic_nudgex,
                                   self.bb_menu_rect[1] + self.bb_menu_graphic_buffery + self.bb_menu_graphic_nudgey]

        self.bb_menu_graphic1_b = [self.bb_menu_rect[0] + button_size - (self.bb_button_borderSize * 2) -
                                   self.bb_menu_graphic_bufferx + self.bb_menu_graphic_nudgex,
                                   self.bb_menu_rect[1] + self.bb_menu_graphic_buffery + self.bb_menu_graphic_nudgey]

        self.bb_menu_graphic2_a = [self.bb_menu_rect[0] + self.bb_menu_graphic_bufferx + self.bb_menu_graphic_nudgex,
                                   self.bb_menu_rect[1] + self.bb_menu_graphic_buffery + self.bb_menu_graphic_width +
                                   menu_graphic_spacing + self.bb_menu_graphic_nudgey]

        self.bb_menu_graphic2_b = [self.bb_menu_rect[0] + button_size - (self.bb_button_borderSize * 2) -
                                   self.bb_menu_graphic_bufferx + self.bb_menu_graphic_nudgex,
                                   self.bb_menu_rect[1] + self.bb_menu_graphic_buffery + self.bb_menu_graphic_width +
                                   menu_graphic_spacing + self.bb_menu_graphic_nudgey]

        self.bb_menu_graphic3_a = [self.bb_menu_rect[0] + self.bb_menu_graphic_bufferx + self.bb_menu_graphic_nudgex,
                                   self.bb_menu_rect[1] + self.bb_menu_graphic_buffery +
                                   ((self.bb_menu_graphic_width + menu_graphic_spacing) * 2) +
                                   self.bb_menu_graphic_nudgey]

        self.bb_menu_graphic3_b = [self.bb_menu_rect[0] + button_size - (self.bb_button_borderSize * 2) -
                                   self.bb_menu_graphic_bufferx + self.bb_menu_graphic_nudgex,
                                   self.bb_menu_rect[1] + self.bb_menu_graphic_buffery +
                                   ((self.bb_menu_graphic_width + menu_graphic_spacing) * 2) +
                                   self.bb_menu_graphic_nudgey]

        # Undo Button
        self.bb_undo_borderRect = [(general.g_width / 2) - self.bb_button_bufferc - button_size,
                                   general.g_height - self.bb_height + self.bb_button_buffery,
                                   button_size,
                                   button_size]

        self.bb_undo_rect = [self.bb_undo_borderRect[0] + self.bb_button_borderSize,
                             self.bb_undo_borderRect[1] + self.bb_button_borderSize,
                             self.bb_undo_borderRect[2] - (self.bb_button_borderSize * 2),
                             self.bb_undo_borderRect[3] - (self.bb_button_borderSize * 2)]

        self.bb_undo_graphic_x = self.bb_undo_rect[0] + self.bb_undo_graphic_nudgex
        self.bb_undo_graphic_y = self.bb_undo_rect[1] + self.bb_undo_graphic_nudgey

        # Redo Button
        self.bb_redo_borderRect = [(general.g_width / 2) + self.bb_button_bufferc,
                                   general.g_height - self.bb_height + self.bb_button_buffery,
                                   button_size,
                                   button_size]

        self.bb_redo_rect = [self.bb_redo_borderRect[0] + self.bb_button_borderSize,
                             self.bb_redo_borderRect[1] + self.bb_button_borderSize,
                             self.bb_redo_borderRect[2] - (self.bb_button_borderSize * 2),
                             self.bb_redo_borderRect[3] - (self.bb_button_borderSize * 2)]

        self.bb_redo_graphic_x = self.bb_redo_rect[0] + self.bb_redo_graphic_nudgex
        self.bb_redo_graphic_y = self.bb_redo_rect[1] + self.bb_redo_graphic_nudgey


botbar = BotBar()


# Holds Game Menu visual variables
class GameMenu:
    def __init__(self):
        # General:
        self.gm_width = 400
        self.gm_height = 460
        self.gm_borderSize = 10
        self.gm_borderColor = [50, 50, 50]
        self.gm_fillColor = [125, 125, 125]

        # Title:
        self.gm_title_textColor = [0, 0, 0]
        self.gm_title_textSize = 80
        self.gm_title_textFont = "Chunkfive.otf"
        self.gm_title_textStr = "Menu"

        self.gm_title_buffery = 30

        # Button General
        self.gm_button_width = 150
        self.gm_button_height = 50
        self.gm_button_borderSize = 5
        self.gm_button_borderColor = [0, 0, 0]
        self.gm_button_fillColor = [245, 245, 50]
        self.gm_button_hoverColor = [200, 200, 50]

        self.gm_button_textColor = [0, 0, 0]
        self.gm_button_text_font = "opensans.ttf"

        self.gm_button_spacing = 10

        # Main Menu Button
        self.gm_mainmenu_textSize = 22
        self.gm_mainmenu_textStr = "Main Menu"

        self.gm_mainmenu_buffery = 300
        self.gm_mainmenu_text_nudgex = 0
        self.gm_mainmenu_text_nudgey = 0

        # New Game Button
        self.gm_newgame_textSize = 22
        self.gm_newgame_textStr = "New Game"

        self.gm_newgame_text_nudgex = 0
        self.gm_newgame_text_nudgey = 0

        # Restart Button
        self.gm_restart_textSize = 22
        self.gm_restart_textStr = "Restart"
        self.gm_restart_text_nudgex = 0
        self.gm_restart_text_nudgey = 0

        # AI Button
        self.gm_ai_textSize = 18
        self.gm_ai_textStr = "Solve with AI"

        self.gm_ai_text_nudgex = 0
        self.gm_ai_text_nudgey = 0

        # Back Button
        self.gm_back_textSize = 22
        self.gm_back_textStr = "Back"

        self.gm_back_text_nudgex = 0
        self.gm_back_text_nudgey = 0

        # =====Dependent Variables=====
        # Game Menu
        self.gm_borderRect = [(general.g_width / 2) - (self.gm_width / 2),
                              ((general.g_height - botbar.bb_height) / 2) - (self.gm_height / 2),
                              self.gm_width,
                              self.gm_height]

        self.gm_rect = [self.gm_borderRect[0] + self.gm_borderSize,
                        self.gm_borderRect[1] + self.gm_borderSize,
                        self.gm_borderRect[2] - (self.gm_borderSize * 2),
                        self.gm_borderRect[3] - (self.gm_borderSize * 2)]

        # Title
        titlefont = pygame.font.Font(self.gm_title_textFont, self.gm_title_textSize)
        self.gm_titleText = titlefont.render("Menu", 1, self.gm_title_textColor)
        titletext_w = self.gm_titleText.get_rect().width
        self.gm_titleText_x = self.gm_rect[0] + (self.gm_rect[2] / 2) - (titletext_w / 2)
        self.gm_titleText_y = self.gm_rect[1] + self.gm_title_buffery

        # Buttons X/Y
        button_x = (general.g_width / 2) - (self.gm_button_width / 2)
        newgame_y = self.gm_mainmenu_buffery + self.gm_button_height + self.gm_button_spacing
        restart_y = newgame_y + self.gm_button_height + self.gm_button_spacing
        ai_y = restart_y + self.gm_button_height + self.gm_button_spacing
        back_y = ai_y + self.gm_button_height + self.gm_button_spacing

        # Main Menu Button
        self.gm_mainmenu_borderRect = [button_x,
                                       self.gm_mainmenu_buffery,
                                       self.gm_button_width,
                                       self.gm_button_height]

        self.gm_mainmenu_rect = [self.gm_mainmenu_borderRect[0] + self.gm_button_borderSize,
                                 self.gm_mainmenu_borderRect[1] + self.gm_button_borderSize,
                                 self.gm_mainmenu_borderRect[2] - (self.gm_button_borderSize * 2),
                                 self.gm_mainmenu_borderRect[3] - (self.gm_button_borderSize * 2)]

        mainmenufont = pygame.font.Font(self.gm_button_text_font, self.gm_mainmenu_textSize)
        self.gm_mainmenuText = mainmenufont.render(self.gm_mainmenu_textStr, 1, self.gm_button_textColor)
        mainmenutxt_w = self.gm_mainmenuText.get_rect().width
        mainmenutxt_h = self.gm_mainmenuText.get_rect().height
        self.gm_mainmenuText_x = (general.g_width / 2) - (mainmenutxt_w / 2) + self.gm_mainmenu_text_nudgex
        self.gm_mainmenuText_y = (self.gm_mainmenu_rect[1] + (self.gm_mainmenu_rect[3] / 2) - (mainmenutxt_h / 2) +
                                  self.gm_mainmenu_text_nudgey)

        # New Game Button
        self.gm_newgame_borderRect = [button_x,
                                      newgame_y,
                                      self.gm_button_width,
                                      self.gm_button_height]

        self.gm_newgame_rect = [self.gm_newgame_borderRect[0] + self.gm_button_borderSize,
                                self.gm_newgame_borderRect[1] + self.gm_button_borderSize,
                                self.gm_newgame_borderRect[2] - (self.gm_button_borderSize * 2),
                                self.gm_newgame_borderRect[3] - (self.gm_button_borderSize * 2)]

        newgamefont = pygame.font.Font(self.gm_button_text_font, self.gm_newgame_textSize)
        self.gm_newgameText = newgamefont.render(self.gm_newgame_textStr, 1, self.gm_button_textColor)
        newgametext_w = self.gm_newgameText.get_rect().width
        newgametext_h = self.gm_newgameText.get_rect().height
        self.gm_newgameText_x = (general.g_width / 2) - (newgametext_w / 2) + self.gm_newgame_text_nudgex
        self.gm_newgameText_y = (self.gm_newgame_rect[1] + (self.gm_newgame_rect[3] / 2) - (newgametext_h / 2) +
                                 self.gm_newgame_text_nudgey)

        # Restart Button
        self.gm_restart_borderRect = [button_x,
                                      restart_y,
                                      self.gm_button_width,
                                      self.gm_button_height]

        self.gm_restart_rect = [self.gm_restart_borderRect[0] + self.gm_button_borderSize,
                                self.gm_restart_borderRect[1] + self.gm_button_borderSize,
                                self.gm_restart_borderRect[2] - (self.gm_button_borderSize * 2),
                                self.gm_restart_borderRect[3] - (self.gm_button_borderSize * 2)]

        restartfont = pygame.font.Font(self.gm_button_text_font, self.gm_restart_textSize)
        self.gm_restartText = restartfont.render(self.gm_restart_textStr, 1, self.gm_button_textColor)
        restarttext_w = self.gm_restartText.get_rect().width
        restarttext_h = self.gm_restartText.get_rect().height
        self.gm_restartText_x = (general.g_width / 2) - (restarttext_w / 2) + self.gm_restart_text_nudgex
        self.gm_restartText_y = (self.gm_restart_rect[1] + (self.gm_restart_rect[3] / 2) - (restarttext_h / 2) +
                                 self.gm_restart_text_nudgey)

        # AI Button
        self.gm_ai_borderRect = [button_x,
                                 ai_y,
                                 self.gm_button_width,
                                 self.gm_button_height]

        self.gm_ai_rect = [self.gm_ai_borderRect[0] + self.gm_button_borderSize,
                           self.gm_ai_borderRect[1] + self.gm_button_borderSize,
                           self.gm_ai_borderRect[2] - (self.gm_button_borderSize * 2),
                           self.gm_ai_borderRect[3] - (self.gm_button_borderSize * 2)]

        aifont = pygame.font.Font(self.gm_button_text_font, self.gm_ai_textSize)
        self.gm_aiText = aifont.render(self.gm_ai_textStr, 1, self.gm_button_textColor)
        aitext_w = self.gm_aiText.get_rect().width
        aitext_h = self.gm_aiText.get_rect().height
        self.gm_aiText_x = (general.g_width / 2) - (aitext_w / 2) + self.gm_ai_text_nudgex
        self.gm_aiText_y = (self.gm_ai_rect[1] + (self.gm_ai_rect[3] / 2) - (aitext_h / 2) +
                            self.gm_ai_text_nudgey)

        # Back Button
        self.gm_back_borderRect = [button_x,
                                   back_y,
                                   self.gm_button_width,
                                   self.gm_button_height]

        self.gm_back_rect = [self.gm_back_borderRect[0] + self.gm_button_borderSize,
                             self.gm_back_borderRect[1] + self.gm_button_borderSize,
                             self.gm_back_borderRect[2] - (self.gm_button_borderSize * 2),
                             self.gm_back_borderRect[3] - (self.gm_button_borderSize * 2)]

        backfont = pygame.font.Font(self.gm_button_text_font, self.gm_back_textSize)
        self.gm_backText = backfont.render(self.gm_back_textStr, 1, self.gm_button_textColor)
        backtext_w = self.gm_backText.get_rect().width
        backtext_h = self.gm_backText.get_rect().height
        self.gm_backText_x = (general.g_width / 2) - (backtext_w / 2) + self.gm_back_text_nudgex
        self.gm_backText_y = (self.gm_back_rect[1] + (self.gm_back_rect[3] / 2) - (backtext_h / 2) +
                              self.gm_back_text_nudgey)


gamemenu = GameMenu()


# Holds Help Menu visual variables
class HelpMenu:
    def __init__(self):
        # General
        self.hm_width = 400
        self.hm_height = 460
        self.hm_borderSize = 10
        self.hm_borderColor = [50, 50, 50]
        self.hm_fillColor = [125, 125, 125]

        # Title
        self.hm_title_textColor = [0, 0, 0]
        self.hm_title_textSize = 80
        self.hm_title_textFont = "Chunkfive.otf"
        self.hm_title_textStr = "Help"

        self.hm_title_buffery = 50
        self.hm_title_nudgex = 0

        # X Button
        self.hm_x_size = 30
        self.hm_x_borderSize = 5
        self.hm_x_borderColor = [0, 0, 0]
        self.hm_x_fillColor = [255, 0, 0]
        self.hm_x_hoverColor = [175, 0, 0]

        self.hm_x_bufferx = 10

        self.hm_x_textColor = [0, 0, 0]
        self.hm_x_textSize = 26
        self.hm_x_textFont = "opensans.ttf"
        self.hm_x_textStr = "x"

        self.hm_x_text_nudgex = 0
        self.hm_x_text_nudgey = -2

        # Info Text
        self.hm_info_textColor = [0, 0, 0]
        self.hm_info_textSize = 23
        self.hm_info_textFont = "opensans.ttf"
        self.hm_info_textStr1 = "Fill every cell with a slant,"
        self.hm_info_textStr2 = "such that each number has"
        self.hm_info_textStr3 = "that many lines touching it,"
        self.hm_info_textStr4 = "with no closed loops."
        self.hm_info_textStr5 = "Use left and right click to"
        self.hm_info_textStr6 = "cycle through slants."

        self.hm_info_buffery1 = 160
        self.hm_info_nudgey2 = 0
        self.hm_info_nudgey3 = 0
        self.hm_info_nudgey4 = 0
        self.hm_info_nudgey5 = 0
        self.hm_info_nudgey6 = 0

        self.hm_info_spacing = 0

        # =====Dependent Variables=====
        # Help Menu
        self.hm_borderRect = [(general.g_width / 2) - (self.hm_width / 2),
                              ((general.g_height - botbar.bb_height) / 2) - (self.hm_height / 2),
                              self.hm_width,
                              self.hm_height]

        self.hm_rect = [self.hm_borderRect[0] + self.hm_borderSize,
                        self.hm_borderRect[1] + self.hm_borderSize,
                        self.hm_borderRect[2] - (self.hm_borderSize * 2),
                        self.hm_borderRect[3] - (self.hm_borderSize * 2)]

        # X Button
        self.hm_x_borderRect = [self.hm_borderRect[0] + self.hm_width - self.hm_borderSize -
                                self.hm_x_bufferx - self.hm_x_size,
                                self.hm_borderRect[1] + self.hm_borderSize + self.hm_x_bufferx,
                                self.hm_x_size,
                                self.hm_x_size]

        self.hm_x_rect = [self.hm_x_borderRect[0] + self.hm_x_borderSize,
                          self.hm_x_borderRect[1] + self.hm_x_borderSize,
                          self.hm_x_borderRect[2] - (self.hm_x_borderSize * 2),
                          self.hm_x_borderRect[3] - (self.hm_x_borderSize * 2)]

        xfont = pygame.font.Font(self.hm_x_textFont, self.hm_x_textSize)
        self.hm_xText = xfont.render("x", 1, self.hm_x_textColor)
        xtext_w = self.hm_xText.get_rect().width
        xtext_h = self.hm_xText.get_rect().height
        self.hm_xText_x = (self.hm_x_rect[0] + (self.hm_x_rect[2] / 2) -
                           (xtext_w / 2) + self.hm_x_text_nudgex)
        self.hm_xText_y = (self.hm_x_rect[1] + (self.hm_x_rect[3] / 2) -
                           (xtext_h / 2) + self.hm_x_text_nudgey)

        # Title Text
        titlefont = pygame.font.Font(self.hm_title_textFont, self.hm_title_textSize)
        self.hm_titleText = titlefont.render("Help", 1, self.hm_title_textColor)
        titletext_w = self.hm_titleText.get_rect().width
        self.hm_titleText_x = self.hm_rect[0] + (self.hm_rect[2] / 2) - (titletext_w / 2) + self.hm_title_nudgex
        self.hm_titleText_y = self.hm_rect[1] + self.hm_title_buffery

        # Info Text
        infotextfont = pygame.font.Font(self.hm_info_textFont, self.hm_info_textSize)
        self.hm_infoText1 = infotextfont.render(self.hm_info_textStr1, 1, self.hm_info_textColor)
        self.hm_infoText2 = infotextfont.render(self.hm_info_textStr2, 1, self.hm_info_textColor)
        self.hm_infoText3 = infotextfont.render(self.hm_info_textStr3, 1, self.hm_info_textColor)
        self.hm_infoText4 = infotextfont.render(self.hm_info_textStr4, 1, self.hm_info_textColor)
        self.hm_infoText5 = infotextfont.render(self.hm_info_textStr5, 1, self.hm_info_textColor)
        self.hm_infoText6 = infotextfont.render(self.hm_info_textStr6, 1, self.hm_info_textColor)

        infotext1_w = self.hm_infoText1.get_rect().width
        infotext1_h = self.hm_infoText1.get_rect().height
        infotext2_w = self.hm_infoText2.get_rect().width
        infotext2_h = self.hm_infoText2.get_rect().height
        infotext3_w = self.hm_infoText3.get_rect().width
        infotext3_h = self.hm_infoText3.get_rect().height
        infotext4_w = self.hm_infoText4.get_rect().width
        infotext4_h = self.hm_infoText4.get_rect().height
        infotext5_w = self.hm_infoText5.get_rect().width
        infotext5_h = self.hm_infoText5.get_rect().height
        infotext6_w = self.hm_infoText6.get_rect().width

        self.hm_infoText1_x = self.hm_rect[0] + (self.hm_rect[2] / 2) - (infotext1_w / 2)
        self.hm_infoText2_x = self.hm_rect[0] + (self.hm_rect[2] / 2) - (infotext2_w / 2)
        self.hm_infoText3_x = self.hm_rect[0] + (self.hm_rect[2] / 2) - (infotext3_w / 2)
        self.hm_infoText4_x = self.hm_rect[0] + (self.hm_rect[2] / 2) - (infotext4_w / 2)
        self.hm_infoText5_x = self.hm_rect[0] + (self.hm_rect[2] / 2) - (infotext5_w / 2)
        self.hm_infoText6_x = self.hm_rect[0] + (self.hm_rect[2] / 2) - (infotext6_w / 2)

        self.hm_infoText1_y = self.hm_rect[1] + self.hm_info_buffery1
        self.hm_infoText2_y = (self.hm_infoText1_y + infotext1_h + self.hm_info_spacing +
                               self.hm_info_nudgey3)
        self.hm_infoText3_y = (self.hm_infoText2_y + infotext2_h + self.hm_info_spacing +
                               self.hm_info_nudgey4)
        self.hm_infoText4_y = (self.hm_infoText3_y + infotext3_h + self.hm_info_spacing +
                               self.hm_info_nudgey5)
        self.hm_infoText5_y = (self.hm_infoText4_y + (infotext4_h * 2) + (self.hm_info_spacing * 2) +
                               self.hm_info_nudgey5)
        self.hm_infoText6_y = (self.hm_infoText5_y + infotext5_h + self.hm_info_spacing +
                               self.hm_info_nudgey6)


helpmenu = HelpMenu()


# Holds New Game Menu visual variables
class NewGameMenu:
    def __init__(self):
        # General
        self.ng_width = 500
        self.ng_height = 300
        self.ng_borderSize = 10
        self.ng_borderColor = [50, 50, 50]
        self.ng_fillColor = [125, 125, 125]

        # Title
        self.ng_title_textColor = [0, 0, 0]
        self.ng_title_textSize = 60
        self.ng_title_textFont = "Chunkfive.otf"
        self.ng_title_textStr = "New Game"

        self.ng_title_buffery = 20

        # Input Labels
        self.ng_inputLabel_textColor = [0, 0, 0]
        self.ng_inputLabel_textSize = 30
        self.ng_inputLabel_textFont = "opensans.ttf"
        self.ng_inputLabel_width_textStr = "Width:"
        self.ng_inputLabel_height_textStr = "Height:"

        self.ng_inputLabel_buffery = 137
        self.ng_inputLabel_bufferx = 30
        self.ng_inputLabel_spacing = 5
        self.ng_inputLabel_width_text_nudgex = 0
        self.ng_inputLabel_width_text_nudgey = 0
        self.ng_inputLabel_height_text_nudgex = 0
        self.ng_inputLabel_height_text_nudgey = 0

        # Input Boxes
        self.ng_inputBox_width = 80
        self.ng_inputBox_height = 50
        self.ng_inputBox_borderSize = 5
        self.ng_inputBox_borderColor = [0, 0, 0]
        self.ng_inputBox_fillColor = [75, 75, 75]
        self.ng_inputBox_hoverColor = [255, 255, 255]

        self.ng_inputBox_width_nudgex = 0
        self.ng_inputBox_width_nudgey = -3
        self.ng_inputBox_height_nudgex = 0
        self.ng_inputBox_height_nudgey = -3

        # Numbers
        self.ng_number_textColor = [0, 0, 0]
        self.ng_number_textSize = 30
        self.ng_number_textFont = "opensans.ttf"

        self.ng_number_width_nudgex = 0
        self.ng_number_width_nudgey = 0
        self.ng_number_height_nudgex = 0
        self.ng_number_height_nudgey = 0

        # Button General
        self.ng_button_width = 150
        self.ng_button_height = 60
        self.ng_button_borderSize = 5
        self.ng_button_borderColor = [0, 0, 0]
        self.ng_button_fillColor = [245, 245, 50]
        self.ng_button_hoverColor = [200, 200, 50]
        self.ng_button_noclickColor = [50, 50, 50]

        self.ng_button_textColor = [0, 0, 0]
        self.ng_button_textSize = 30
        self.ng_button_textFont = "opensans.ttf"

        self.ng_button_buffery = 200
        self.ng_button_bufferx = 75

        # Okay Button
        self.ng_okay_textStr = "Okay"

        self.ng_okay_nudgex = 0
        self.ng_okay_nudgey = 0
        self.ng_okay_text_nudgex = 0
        self.ng_okay_text_nudgey = 0

        # Back Button
        self.ng_back_textStr = "Back"

        self.ng_back_nudgex = 0
        self.ng_back_nudgey = 0
        self.ng_back_text_nudgex = 0
        self.ng_back_text_nudgey = 0

        # Info Text
        self.ng_info_textColor = [0, 0, 0]
        self.ng_info_textSize = 16
        self.ng_info_textFont = "opensans.ttf"
        self.ng_info_textStr1 = "Click in a box to edit. Type digits with the keyboard."
        self.ng_info_textStr2 = "Press Enter to confirm. Click outside the box to cancel."

        self.ng_info_buffery = 77
        self.ng_info_spacing = -2

        # =====Dependent Variables
        # New Game Menu
        self.ng_x = (general.g_width / 2) - (self.ng_width / 2)
        self.ng_y = ((general.g_height - botbar.bb_height) / 2) - (self.ng_height / 2)

        self.ng_borderRect = [self.ng_x,
                              self.ng_y,
                              self.ng_width,
                              self.ng_height]

        self.ng_rect = [self.ng_borderRect[0] + self.ng_borderSize,
                        self.ng_borderRect[1] + self.ng_borderSize,
                        self.ng_borderRect[2] - (self.ng_borderSize * 2),
                        self.ng_borderRect[3] - (self.ng_borderSize * 2)]

        # Title
        titlefont = pygame.font.Font(self.ng_title_textFont, self.ng_title_textSize)
        self.ng_titleText = titlefont.render(self.ng_title_textStr, 1, self.ng_title_textColor)
        title_w = self.ng_titleText.get_rect().width
        self.ng_title_x = (general.g_width / 2) - (title_w / 2)
        self.ng_title_y = self.ng_rect[1] + self.ng_title_buffery

        # Labels
        labelfont = pygame.font.Font(self.ng_inputLabel_textFont, self.ng_inputLabel_textSize)
        self.ng_label_widthText = labelfont.render(self.ng_inputLabel_width_textStr, 1,
                                                   self.ng_inputLabel_textColor)
        self.ng_label_heightText = labelfont.render(self.ng_inputLabel_height_textStr, 1,
                                                    self.ng_inputLabel_textColor)
        label_widthtext_w = self.ng_label_widthText.get_rect().width
        label_heighttext_w = self.ng_label_heightText.get_rect().width
        self.ng_label_widthText_x = (self.ng_rect[0] + self.ng_inputLabel_bufferx +
                                     self.ng_inputLabel_width_text_nudgex)
        self.ng_label_widthText_y = (self.ng_rect[1] + self.ng_inputLabel_buffery +
                                     self.ng_inputLabel_width_text_nudgey)
        self.ng_label_heightText_x = (self.ng_rect[0] + self.ng_rect[2] - self.ng_inputLabel_bufferx -
                                      self.ng_inputBox_width - self.ng_inputLabel_spacing - label_heighttext_w +
                                      self.ng_inputLabel_height_text_nudgex)
        self.ng_label_heightText_y = (self.ng_rect[1] + self.ng_inputLabel_buffery +
                                      self.ng_inputLabel_height_text_nudgey)

        # Boxes
        self.ng_width_borderRect = [(self.ng_label_widthText_x + label_widthtext_w + self.ng_inputLabel_spacing +
                                     self.ng_inputBox_width_nudgex),
                                    (self.ng_rect[1] + self.ng_inputLabel_buffery +
                                     self.ng_inputBox_width_nudgey),
                                    self.ng_inputBox_width,
                                    self.ng_inputBox_height]

        self.ng_width_rect = [self.ng_width_borderRect[0] + self.ng_inputBox_borderSize,
                              self.ng_width_borderRect[1] + self.ng_inputBox_borderSize,
                              self.ng_width_borderRect[2] - (self.ng_inputBox_borderSize * 2),
                              self.ng_width_borderRect[3] - (self.ng_inputBox_borderSize * 2)]

        self.ng_height_borderRect = [(self.ng_rect[0] + self.ng_rect[2] - self.ng_inputLabel_bufferx -
                                      self.ng_inputBox_width + self.ng_inputBox_height_nudgex),
                                     (self.ng_rect[1] + self.ng_inputLabel_buffery +
                                      self.ng_inputBox_height_nudgey),
                                     self.ng_inputBox_width,
                                     self.ng_inputBox_height]

        self.ng_height_rect = [self.ng_height_borderRect[0] + self.ng_inputBox_borderSize,
                               self.ng_height_borderRect[1] + self.ng_inputBox_borderSize,
                               self.ng_height_borderRect[2] - (self.ng_inputBox_borderSize * 2),
                               self.ng_height_borderRect[3] - (self.ng_inputBox_borderSize * 2)]

        # Buttons
        self.ng_okay_borderRect = [self.ng_rect[0] + self.ng_button_bufferx,
                                   self.ng_rect[1] + self.ng_button_buffery,
                                   self.ng_button_width,
                                   self.ng_button_height]

        self.ng_okay_rect = [self.ng_okay_borderRect[0] + self.ng_button_borderSize,
                             self.ng_okay_borderRect[1] + self.ng_button_borderSize,
                             self.ng_okay_borderRect[2] - (self.ng_button_borderSize * 2),
                             self.ng_okay_borderRect[3] - (self.ng_button_borderSize * 2)]

        self.ng_back_borderRect = [(self.ng_rect[0] + self.ng_rect[2] -
                                    self.ng_button_bufferx - self.ng_button_width),
                                   self.ng_rect[1] + self.ng_button_buffery,
                                   self.ng_button_width, self.ng_button_height]

        self.ng_back_rect = [self.ng_back_borderRect[0] + self.ng_button_borderSize,
                             self.ng_back_borderRect[1] + self.ng_button_borderSize,
                             self.ng_back_borderRect[2] - (self.ng_button_borderSize * 2),
                             self.ng_back_borderRect[3] - (self.ng_button_borderSize * 2)]

        buttonfont = pygame.font.Font(self.ng_button_textFont, self.ng_button_textSize)

        self.ng_okayText = buttonfont.render(self.ng_okay_textStr, 1, self.ng_button_textColor)
        okaytext_w = self.ng_okayText.get_rect().width
        okaytext_h = self.ng_okayText.get_rect().height
        self.ng_okayText_x = (self.ng_okay_rect[0] + (self.ng_okay_rect[2] / 2) -
                              (okaytext_w / 2) + self.ng_okay_text_nudgex)
        self.ng_okayText_y = (self.ng_okay_rect[1] + (self.ng_okay_rect[3] / 2) -
                              (okaytext_h / 2) + self.ng_okay_text_nudgey)

        self.ng_backText = buttonfont.render(self.ng_back_textStr, 1, self.ng_button_textColor)
        backtext_w = self.ng_backText.get_rect().width
        backtext_h = self.ng_backText.get_rect().height
        self.ng_backText_x = (self.ng_back_rect[0] + (self.ng_back_rect[2] / 2) -
                              (backtext_w / 2) + self.ng_back_text_nudgex)
        self.ng_backText_y = (self.ng_back_rect[1] + (self.ng_back_rect[3] / 2) -
                              (backtext_h / 2) + self.ng_back_text_nudgey)

        # Numbers
        self.ng_numberFont = pygame.font.Font(self.ng_number_textFont, self.ng_number_textSize)

        # Info Text
        infotextfont = pygame.font.Font(self.ng_info_textFont, self.ng_info_textSize)
        self.ng_infoText1 = infotextfont.render(self.ng_info_textStr1, 1, self.ng_info_textColor)
        self.ng_infoText2 = infotextfont.render(self.ng_info_textStr2, 1, self.ng_info_textColor)
        infotext1_w = self.ng_infoText1.get_rect().width
        infotext1_h = self.ng_infoText1.get_rect().height
        infotext2_w = self.ng_infoText2.get_rect().width
        self.ng_infoText1_x = (general.g_width / 2) - (infotext1_w / 2)
        self.ng_infoText1_y = self.ng_rect[1] + self.ng_info_buffery
        self.ng_infoText2_x = (general.g_width / 2) - (infotext2_w / 2)
        self.ng_infoText2_y = self.ng_infoText1_y + infotext1_h + self.ng_info_spacing


newgame = NewGameMenu()


# Object that holds details for drawing the winscreen
class WinScreen:
    def __init__(self):
        # General
        self.ws_width = 400
        self.ws_height = 360
        self.ws_borderSize = 10
        self.ws_borderColor = [50, 50, 50]
        self.ws_fillColor = [125, 125, 125]

        # Title:
        self.ws_title_textColor = [0, 0, 0]
        self.ws_title_textSize = 70
        self.ws_title_textFont = "Chunkfive.otf"
        self.ws_title_textStr = "You Win!"

        self.ws_title_buffery = 30

        # Button General
        self.ws_button_width = 150
        self.ws_button_height = 50
        self.ws_button_borderSize = 5
        self.ws_button_borderColor = [0, 0, 0]
        self.ws_button_fillColor = [245, 245, 50]
        self.ws_button_hoverColor = [200, 200, 50]

        self.ws_button_textColor = [0, 0, 0]
        self.ws_button_textFont = "opensans.ttf"

        self.ws_button_spacing = 15
        self.ws_button_buffery = 120

        # New Game Button
        self.ws_newgame_textSize = 22
        self.ws_newgame_textStr = "New Game"

        self.ws_newgame_text_nudgex = 0
        self.ws_newgame_text_nudgey = -5

        # Main Menu Button
        self.ws_mainmenu_textSize = 22
        self.ws_mainmenu_textStr = "Main Menu"

        self.ws_mainmenu_text_nudgex = 0
        self.ws_mainmenu_text_nudgey = -5

        # Back Button
        self.ws_back_textSize = 22
        self.ws_back_textStr = "Back"

        self.ws_back_text_nudgex = 0
        self.ws_back_text_nudgey = -5

        # =====Dependent Variables=====
        # General
        self.ws_borderRect = [(general.g_width / 2) - (self.ws_width / 2),
                              ((general.g_height - botbar.bb_height) / 2) - (self.ws_height / 2),
                              self.ws_width,
                              self.ws_height]

        self.ws_rect = [self.ws_borderRect[0] + self.ws_borderSize,
                        self.ws_borderRect[1] + self.ws_borderSize,
                        self.ws_borderRect[2] - (self.ws_borderSize * 2),
                        self.ws_borderRect[3] - (self.ws_borderSize * 2)]

        # Title
        titlefont = pygame.font.Font(self.ws_title_textFont, self.ws_title_textSize)
        self.ws_titleText = titlefont.render(self.ws_title_textStr, 1, self.ws_title_textColor)
        titletext_w = self.ws_titleText.get_rect().width
        self.ws_titleText_x = (general.g_width / 2) - (titletext_w / 2)
        self.ws_titleText_y = self.ws_rect[1] + self.ws_title_buffery

        # Button General
        buttonx = (general.g_width / 2) - (self.ws_button_width / 2)

        # New Game Button
        self.ws_newgame_borderRect = [buttonx,
                                      self.ws_rect[1] + self.ws_button_buffery,
                                      self.ws_button_width,
                                      self.ws_button_height]

        self.ws_newgame_rect = [self.ws_newgame_borderRect[0] + self.ws_button_borderSize,
                                self.ws_newgame_borderRect[1] + self.ws_button_borderSize,
                                self.ws_newgame_borderRect[2] - (self.ws_button_borderSize * 2),
                                self.ws_newgame_borderRect[3] - (self.ws_button_borderSize * 2)]

        newgamefont = pygame.font.Font(self.ws_button_textFont, self.ws_newgame_textSize)
        self.ws_newgameText = newgamefont.render(self.ws_newgame_textStr, 1, self.ws_button_textColor)
        newgametext_w = self.ws_newgameText.get_rect().width
        newgametext_h = self.ws_newgameText.get_rect().height
        self.ws_newgameText_x = (general.g_width / 2) - (newgametext_w / 2) + self.ws_newgame_text_nudgex
        self.ws_newgameText_y = (self.ws_newgame_rect[1] + (self.ws_button_height / 2) - (newgametext_h / 2) +
                                 self.ws_newgame_text_nudgey)

        # Main Menu Button
        self.ws_mainmenu_borderRect = [buttonx,
                                       (self.ws_newgame_borderRect[1] + self.ws_newgame_borderRect[3] +
                                        self.ws_button_spacing),
                                       self.ws_button_width,
                                       self.ws_button_height]

        self.ws_mainmenu_rect = [self.ws_mainmenu_borderRect[0] + self.ws_button_borderSize,
                                 self.ws_mainmenu_borderRect[1] + self.ws_button_borderSize,
                                 self.ws_mainmenu_borderRect[2] - (self.ws_button_borderSize * 2),
                                 self.ws_mainmenu_borderRect[3] - (self.ws_button_borderSize * 2)]

        mainmenufont = pygame.font.Font(self.ws_button_textFont, self.ws_mainmenu_textSize)
        self.ws_mainmenuText = mainmenufont.render(self.ws_mainmenu_textStr, 1, self.ws_button_textColor)
        mainmenutext_w = self.ws_mainmenuText.get_rect().width
        mainmenutext_h = self.ws_mainmenuText.get_rect().height
        self.ws_mainmenuText_x = (general.g_width / 2) - (mainmenutext_w / 2) + self.ws_mainmenu_text_nudgex
        self.ws_mainmenuText_y = (self.ws_mainmenu_rect[1] + (self.ws_button_height / 2) - (mainmenutext_h / 2) +
                                  self.ws_mainmenu_text_nudgey)

        # Back Button
        self.ws_back_borderRect = [buttonx,
                                   (self.ws_mainmenu_borderRect[1] + self.ws_mainmenu_borderRect[3] +
                                    self.ws_button_spacing),
                                   self.ws_button_width,
                                   self.ws_button_height]

        self.ws_back_rect = [self.ws_back_borderRect[0] + self.ws_button_borderSize,
                             self.ws_back_borderRect[1] + self.ws_button_borderSize,
                             self.ws_back_borderRect[2] - (self.ws_button_borderSize * 2),
                             self.ws_back_borderRect[3] - (self.ws_button_borderSize * 2)]

        backfont = pygame.font.Font(self.ws_button_textFont, self.ws_back_textSize)
        self.ws_backText = backfont.render(self.ws_back_textStr, 1, self.ws_button_textColor)
        backtext_w = self.ws_backText.get_rect().width
        backtext_h = self.ws_backText.get_rect().height
        self.ws_backText_x = (general.g_width / 2) - (backtext_w / 2) + self.ws_back_text_nudgex
        self.ws_backText_y = (self.ws_back_rect[1] + (self.ws_button_height / 2) - (backtext_h / 2) +
                              self.ws_back_text_nudgey)


winscreen = WinScreen()


# Object that holds details for drawing the board.
# These are all placeholder values that get changed by boardbuilder().
class Board:
    def __init__(self):
        self.b_width = 1
        self.b_height = 1
        self.b_numMatrix = []
        self.b_cellDict = {}
        self.b_cell_width = 1
        self.b_cell_height = 1
        self.b_lineList = []
        self.b_lineDict_x = {}
        self.b_lineDict_y = {}
        self.b_bufferx = gamescreen.gs_board_bufferx
        self.b_buffery = gamescreen.gs_board_bufferx
        self.b_num_textSize = gamescreen.gs_numSize_def
        self.b_circleRadius = gamescreen.gs_circleRadius_def
        self.b_adjust0 = gamescreen.gs_0nudgex_def
        self.b_adjust1 = gamescreen.gs_1nudgex_def
        self.b_adjust2 = gamescreen.gs_2nudgex_def
        self.b_adjust3 = gamescreen.gs_3nudgex_def
        self.b_adjust4 = gamescreen.gs_4nudgex_def


board = Board()


# Pygame Initialization
win = pygame.display.set_mode([general.g_width, general.g_height])
pygame.display.set_caption("Slants")
win.fill(general.g_fillColor)
clock = pygame.time.Clock()


# Read board.txt and adjust all visual variables in the board object accordingly.
# Build initial starting logic variables in general
def boardbuilder():
    # Read the file and puts every line in a list
    boardtxt = open("board.txt", "r")
    lines = boardtxt.readlines()
    boardtxt.close()

    # Remove the identifier characters and put width and height into variables in board object
    width_str = lines[0]
    width_str = width_str.replace('w', '')
    width_str = width_str.replace('=', '')
    board.b_width = int(width_str)
    height_str = lines[1]
    height_str = height_str.replace('h', '')
    height_str = height_str.replace('=', '')
    board.b_height = int(height_str)

    # Until the ending signifier (!) is reached, strip each line of identifier characters and newlines
    # and put them into the matrix variable in the board object
    # Also, build the initial solved number check matrix
    line = 1
    while 1:
        line += 1
        line_str = lines[line]
        if line_str == "!":
            break
        else:
            line_str = line_str.rstrip()
            line_str = line_str[3:]
            board.b_numMatrix.append(line_str)  # Add to matrix
            solve_str = ""
            for char in line_str:
                if char == "x":
                    solve_str += char
                else:
                    solve_str += "0"
            general.g_solvedMatrix.append(solve_str)  # Add to solved matrix

    # Decide Cell Width and Cell Height
    if board.b_width > board.b_height:
        bigger = board.b_width
    else:
        bigger = board.b_height

    if bigger < 8:  # This exists so the cell sizes don't get too absurd
        board.b_cell_width = 87
        board.b_cell_height = 87
    else:
        if board.b_width >= board.b_height:
            board.b_cell_width = int((general.g_width - (gamescreen.gs_board_bufferx * 2) -
                                      gamescreen.gs_lineWidth) / board.b_width)
            board.b_cell_height = int(board.b_cell_width)
        else:
            board.b_cell_height = int((general.g_width - botbar.bb_height - (gamescreen.gs_board_bufferx * 2) -
                                       gamescreen.gs_lineWidth) / board.b_height)
            board.b_cell_width = int(board.b_cell_height)

    # Decide horizontal buffer between edge and board and vertical buffer between edge and board
    play_w = int((board.b_cell_width * board.b_width) + gamescreen.gs_lineWidth)
    play_h = int((board.b_cell_height * board.b_height) + gamescreen.gs_lineWidth)
    board.b_bufferx = int((general.g_width - play_w) / 2)
    board.b_buffery = int((general.g_height - botbar.bb_height - play_h) / 2)

    # Build a dictionary of x/y cell positions (top left corner of cell)
    xtrack = board.b_bufferx + gamescreen.gs_lineWidth - 1
    ytrack = board.b_buffery + gamescreen.gs_lineWidth - 1
    for x in range(1, board.b_width + 1):
        if x != 1:
            xtrack += board.b_cell_width
            xtrack = int(xtrack)
            ytrack = board.b_buffery + gamescreen.gs_lineWidth - 1
            ytrack = int(ytrack)
        for y in range(1, board.b_height + 1):
            key = str(x) + "," + str(y)
            pos = [xtrack, ytrack]
            board.b_cellDict[key] = list(pos)
            ytrack += board.b_cell_height
            ytrack = int(ytrack)

            # Build dictionary of slants
            general.g_slantDict[key] = 0

            # Build dictionary of loops
            general.g_loopDict[key] = 0

            # Build dictionary of connections
            general.g_connectDict[key] = {"top": [], "bottom": []}

            # Build dictionary of paths
            general.g_pathDict[key] = []

    # Build list of x1/y1/x2/y2 positions for each line
    # Vertical Lines:
    xtrack = board.b_bufferx
    for x in range(0, board.b_width + 1):
        x1 = xtrack
        y1 = board.b_buffery
        x2 = xtrack
        y2 = board.b_buffery + play_h - gamescreen.gs_lineWidth
        board.b_lineList.append([x1, y1, x2, y2])
        board.b_lineDict_x[str(x)] = [x1, y1, x2, y2]
        xtrack += board.b_cell_width

    # Horizontal Lines:
    ytrack = board.b_buffery
    for y in range(0, board.b_height + 1):
        x1 = board.b_bufferx
        y1 = ytrack
        x2 = board.b_bufferx + play_w - gamescreen.gs_lineWidth
        y2 = ytrack
        board.b_lineList.append([x1, y1, x2, y2])
        board.b_lineDict_y[str(y)] = [x1, y1, x2, y2]
        ytrack += board.b_cell_height

    # Decide number font size:
    board.b_num_textSize = int((board.b_cell_width * gamescreen.gs_numSize_def) / gamescreen.gs_sizeScale)

    # Decide circle size:
    board.circlesize = int((gamescreen.gs_circleRadius_def * board.b_cell_width) / gamescreen.gs_sizeScale)

    # Decide number adjustments:
    board.b_adjust0 = int((board.b_cell_width * gamescreen.gs_0nudgex_def) / gamescreen.gs_sizeScale)
    board.b_adjust1 = int((board.b_cell_width * gamescreen.gs_1nudgex_def) / gamescreen.gs_sizeScale)
    board.b_adjust2 = int((board.b_cell_width * gamescreen.gs_2nudgex_def) / gamescreen.gs_sizeScale)
    board.b_adjust3 = int((board.b_cell_width * gamescreen.gs_3nudgex_def) / gamescreen.gs_sizeScale)
    board.b_adjust4 = int((board.b_cell_width * gamescreen.gs_4nudgex_def) / gamescreen.gs_sizeScale)


# Determine if the number is neutral, solved, or wrong
# 0 = neutral, 1 = solved, 2 = wrong
# Only check the numbers around the cell that was just clicked
def solvednumbertest(cell):
    cellx = ""
    celly = ""
    celladd = "x"
    for char in cell:
        if char == ",":
            celladd = "y"
        else:
            if celladd == "x":
                cellx += char
            else:
                celly += char
    cellx = int(cellx)
    celly = int(celly)
    numstocheck = [[cellx - 1, celly - 1], [cellx - 1, celly], [cellx, celly - 1], [cellx, celly]]
    for number in numstocheck:
        x = number[0]
        y = number[1]
        if general.g_solvedMatrix[y][x] != "x":
            # First make sure you're only checking cells that exist
            doul = 1
            dour = 1
            dodl = 1
            dodr = 1
            if x <= 0:
                doul = 0
                dodl = 0
            if x >= board.b_width:
                dour = 0
                dodr = 0
            if y <= 0:
                doul = 0
                dour = 0
            if y >= board.b_height:
                dodl = 0
                dodr = 0

            # Then check the cells that exist and set them to "0" if they're not set,
            # "1" if they're set and not touching the number,
            # "2" if they're set and touching the number.
            # Increment touching if they're touching, nottouching if they're not touching
            ul = "none"
            ur = "none"
            dl = "none"
            dr = "none"
            touching = 0
            nottouching = 0
            if doul == 1:
                cellkeystr = str(x) + "," + str(y)
                cell = general.g_slantDict[cellkeystr]
                if cell == 0:
                    ul = 0
                elif cell == 1:
                    ul = 2
                    touching += 1
                else:
                    ul = 1
                    nottouching += 1
            if dour == 1:
                cellkeystr = str(x + 1) + "," + str(y)
                cell = general.g_slantDict[cellkeystr]
                if cell == 0:
                    ur = 0
                elif cell == 1:
                    ur = 1
                    nottouching += 1
                else:
                    ur = 2
                    touching += 1
            if dodl == 1:
                cellkeystr = str(x) + "," + str(y + 1)
                cell = general.g_slantDict[cellkeystr]
                if cell == 0:
                    dl = 0
                elif cell == 1:
                    dl = 1
                    nottouching += 1
                else:
                    dl = 2
                    touching += 1
            if dodr == 1:
                cellkeystr = str(x + 1) + "," + str(y + 1)
                cell = general.g_slantDict[cellkeystr]
                if cell == 0:
                    dr = 0
                elif cell == 1:
                    dr = 2
                    touching += 1
                else:
                    dr = 1
                    nottouching += 1

            # Determine if the number is neutral, solved, or wrong
            # If any cells are 0:
            #   if the number of touching cells is less than the number, neutral
            #   if the number of touching cells is equal to the number, neutral
            #   if the number of touching cells is greater than the number, wrong
            #   if the number of not touching cells is less than 4 - the number, no change
            #   if the number of not touching cells is equal to 4 - the number, no change
            #   if the number of not touching cells is greater than 4 - the number, wrong
            # If no cells are 0:
            #   if the number of touching cells is less than the number, wrong
            #   if the number of touching cells is equal to the number, solved
            #   if the number of touching cells is greater than the number, wrong
            num = int(board.b_numMatrix[y][x])
            if ul == 0 or ur == 0 or dl == 0 or dr == 0:
                if touching <= num:
                    state = "0"
                else:
                    state = "2"
                if nottouching > 4 - num:
                    state = "2"
            else:
                if touching < num:
                    state = "2"
                elif touching == num:
                    state = "1"
                else:
                    state = "2"

            # Finally, update the matrix
            line = general.g_solvedMatrix[y]
            linelist = list(line)
            linelist[x] = state
            line = ""
            for i in linelist:
                line += i
            general.g_solvedMatrix[y] = line


def loopcheckmain():
    # Reset the loop dict, connection dict, and path dict
    for cell in general.g_loopDict:
        general.g_loopDict[cell] = 0
        general.g_connectDict[cell] = {"top": [], "bottom": []}
        general.g_pathDict[cell] = []

    # Build the connection dict for each cell
    for cell in general.g_loopDict:
        if general.g_slantDict[cell] != 0:
            loopconnectdict(cell)

    # Build the path dict for each cell
    for cell in general.g_loopDict:
        if general.g_slantDict[cell] != 0:
            looppathdict(cell, cell, "top", ["top", cell])
            looppathdict(cell, cell, "bottom", ["bottom", cell])

    # Build the loop dict for each cell
    for cell in general.g_loopDict:
        if general.g_slantDict[cell] != 0:
            pathlist = general.g_pathDict[cell]

            for path in pathlist:
                if path[1] == path[-2] and path[0] == path[-1]:
                    general.g_loopDict[cell] = 1


# Determine which cells are connected to the given cell and put them in that cell's connect dict
# Cells in the connect dict are formatted as [cell2, relation to cell]
def loopconnectdict(cell):
    # Separate the x and y of the cell
    cellx = ""
    celly = ""
    celladd = "x"
    for c in cell:
        if c == ",":
            celladd = "y"
        elif celladd == "x":
            cellx += c
        elif celladd == "y":
            celly += c
    cellx = int(cellx)
    celly = int(celly)

    # If the slant is 1
    if general.g_slantDict[cell] == 1:
        # up: (x, y - 1)
        if celly != 1:
            cell2 = [str(cellx) + "," + str(celly - 1), "up"]
            if general.g_slantDict[cell2[0]] == 2:
                general.g_connectDict[cell]["top"].append(cell2)
        # left: (x - 1, y)
        if cellx != 1:
            cell2 = [str(cellx - 1) + "," + str(celly), "left"]
            if general.g_slantDict[cell2[0]] == 2:
                general.g_connectDict[cell]["top"].append(cell2)
        # right: (x + 1, y)
        if cellx != board.b_width:
            cell2 = [str(cellx + 1) + "," + str(celly), "right"]
            if general.g_slantDict[cell2[0]] == 2:
                general.g_connectDict[cell]["bottom"].append(cell2)
        # down: (x, y + 1)
        if celly != board.b_height:
            cell2 = [str(cellx) + "," + str(celly + 1), "down"]
            if general.g_slantDict[cell2[0]] == 2:
                general.g_connectDict[cell]["bottom"].append(cell2)
        # upleft: (x - 1, y - 1)
        if cellx != 1 and celly != 1:
            cell2 = [str(cellx - 1) + "," + str(celly - 1), "upleft"]
            if general.g_slantDict[cell2[0]] == 1:
                general.g_connectDict[cell]["top"].append(cell2)
        # downright: (x + 1, y + 1)
        if cellx != board.b_width and celly != board.b_height:
            cell2 = [str(cellx + 1) + "," + str(celly + 1), "downright"]
            if general.g_slantDict[cell2[0]] == 1:
                general.g_connectDict[cell]["bottom"].append(cell2)

    # If the slant is 2
    if general.g_slantDict[cell] == 2:
        # up: (x, y - 1)
        if celly != 1:
            cell2 = [str(cellx) + "," + str(celly - 1), "up"]
            if general.g_slantDict[cell2[0]] == 1:
                general.g_connectDict[cell]["top"].append(cell2)
        # left: (x - 1, y)
        if cellx != 1:
            cell2 = [str(cellx - 1) + "," + str(celly), "left"]
            if general.g_slantDict[cell2[0]] == 1:
                general.g_connectDict[cell]["bottom"].append(cell2)
        # right: (x + 1, y)
        if cellx != board.b_width:
            cell2 = [str(cellx + 1) + "," + str(celly), "right"]
            if general.g_slantDict[cell2[0]] == 1:
                general.g_connectDict[cell]["top"].append(cell2)
        # down: (x, y + 1)
        if celly != board.b_height:
            cell2 = [str(cellx) + "," + str(celly + 1), "down"]
            if general.g_slantDict[cell2[0]] == 1:
                general.g_connectDict[cell]["bottom"].append(cell2)
        # downleft: (x - 1, y + 1)
        if cellx != 1 and celly != board.b_height:
            cell2 = [str(cellx - 1) + "," + str(celly + 1), "downleft"]
            if general.g_slantDict[cell2[0]] == 2:
                general.g_connectDict[cell]["bottom"].append(cell2)
        # upright: (x + 1, y - 1)
        if cellx != board.b_width and celly != 1:
            cell2 = [str(cellx + 1) + "," + str(celly - 1), "upright"]
            if general.g_slantDict[cell2[0]] == 2:
                general.g_connectDict[cell]["top"].append(cell2)


# Determines which paths come from the cell and adds them to that cell's path list
def looppathdict(pathstart, cell, endpoint, path):
    cellconnections = list(general.g_connectDict[cell][endpoint])
    for cell2 in cellconnections:
        # Gets endpoints of cell2 for appending later
        if general.g_slantDict[cell] == 1:
            if cell2[1] == "up" or cell2[1] == "right" or cell2[1] == "upleft":
                ep = "top"
            else:
                ep = "bottom"
        else:
            if cell2[1] == "up" or cell2[1] == "left" or cell2[1] == "upright":
                ep = "top"
            else:
                ep = "bottom"
        # Gets list of connections for cell2 for check later
        cellconnections2 = list(general.g_connectDict[cell2[0]][ep])
        newpath = list(path)
        newpath.append(cell2[0])

        # Reaches an endpoint with no connections
        if len(cellconnections2) == 0:
            newpath.append(ep)
            general.g_pathDict[pathstart].append(newpath)

        # Reaches a cell already in the path
        elif cell2[0] in path:
            newpath.append(ep)
            general.g_pathDict[pathstart].append(newpath)

        # Continues the path
        else:
            looppathdict(pathstart, cell2[0], ep, newpath)


# Check if the board is solved
def wincheck():
    # Only checks for winscreen if this isn't the first time they've beaten this board
    if general.g_alreadywon == 0:
        winner = 1

        # Check if the board is filled in
        for cell in general.g_slantDict:
            slant = general.g_slantDict[cell]
            if slant == 0:
                winner = 0
                break

        # Check if all the numbers are solved
        if winner:
            for row in general.g_solvedMatrix:
                for num in row:
                    if num != "x":
                        if num != "1":
                            winner = 0
                            break

        # TO-DO check if there are no loops
        if winner:
            for cell in general.g_loopDict:
                if general.g_loopDict[cell] == 1:
                    winner = 0
                    break

        # Go to winscreen if winner
        if winner:
            general.g_alreadywon = 1
            winscreenmenu()


# Win Screen
def winscreenmenu():
    while 1:
        clock.tick(general.g_fps)
        framelength = clock.get_time()
        realfps = str(int(1000 / framelength))
        mouse = pygame.mouse.get_pos()
        drawgame(realfps, "win")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    # New Game
                    if ((winscreen.ws_newgame_borderRect[0] <= mouse[0] <=
                            winscreen.ws_newgame_borderRect[0] + winscreen.ws_newgame_borderRect[2]) and
                            (winscreen.ws_newgame_borderRect[1] <= mouse[1] <=
                             winscreen.ws_newgame_borderRect[1] + winscreen.ws_newgame_borderRect[3])):
                        newgamebutton("winscreen")

                    # Main Menu
                    if ((winscreen.ws_mainmenu_borderRect[0] <= mouse[0] <=
                         winscreen.ws_mainmenu_borderRect[0] + winscreen.ws_mainmenu_borderRect[2]) and
                            (winscreen.ws_mainmenu_borderRect[1] <= mouse[1] <=
                             winscreen.ws_mainmenu_borderRect[1] + winscreen.ws_mainmenu_borderRect[3])):
                        menubutton()

                    # Back
                    if ((winscreen.ws_back_borderRect[0] <= mouse[0] <=
                         winscreen.ws_back_borderRect[0] + winscreen.ws_back_borderRect[2]) and
                            (winscreen.ws_back_borderRect[1] <= mouse[1] <=
                             winscreen.ws_back_borderRect[1] + winscreen.ws_back_borderRect[3])):
                        gameloop()


# Game Menu
def menuscreen():
    while 1:
        clock.tick(general.g_fps)
        framelength = clock.get_time()
        realfps = str(int(1000 / framelength))
        mouse = pygame.mouse.get_pos()
        drawgame(realfps, "menu")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    # Main Menu
                    if ((gamemenu.gm_mainmenu_borderRect[0] <= mouse[0] <=
                            gamemenu.gm_mainmenu_borderRect[0] + gamemenu.gm_mainmenu_borderRect[2]) and
                            (gamemenu.gm_mainmenu_borderRect[1] <= mouse[1] <=
                             gamemenu.gm_mainmenu_borderRect[1] + gamemenu.gm_mainmenu_borderRect[3])):
                        menubutton()

                    # New Game
                    if ((gamemenu.gm_newgame_borderRect[0] <= mouse[0] <=
                            gamemenu.gm_newgame_borderRect[0] + gamemenu.gm_newgame_borderRect[2]) and
                            (gamemenu.gm_newgame_borderRect[1] <= mouse[1] <=
                             gamemenu.gm_newgame_borderRect[1] + gamemenu.gm_newgame_borderRect[3])):
                        newgamebutton("gamemenu")

                    # Restart
                    if ((gamemenu.gm_restart_borderRect[0] <= mouse[0] <=
                            gamemenu.gm_restart_borderRect[0] + gamemenu.gm_restart_borderRect[2]) and
                            (gamemenu.gm_restart_borderRect[1] <= mouse[1] <=
                             gamemenu.gm_restart_borderRect[1] + gamemenu.gm_restart_borderRect[3])):
                        restart()

                    # Solve With AI
                    if ((gamemenu.gm_ai_borderRect[0] <= mouse[0] <=
                         gamemenu.gm_ai_borderRect[0] + gamemenu.gm_ai_borderRect[2]) and
                            (gamemenu.gm_ai_borderRect[1] <= mouse[1] <=
                             gamemenu.gm_ai_borderRect[1] + gamemenu.gm_ai_borderRect[3])):
                        solvewithai()

                    # Back
                    if ((gamemenu.gm_back_borderRect[0] <= mouse[0] <=
                         gamemenu.gm_back_borderRect[0] + gamemenu.gm_back_borderRect[2]) and
                            (gamemenu.gm_back_borderRect[1] <= mouse[1] <=
                             gamemenu.gm_back_borderRect[1] + gamemenu.gm_back_borderRect[3])):
                        gameloop()


# Game Menu -> Main Menu
def menubutton():
    print("MAIN MENU")


# Game Menu - > New Game
def newgamebutton(backto):
    general.g_widthInput = str(board.b_width)
    general.g_heightInput = str(board.b_height)
    general.g_widthActive = 0
    general.g_heightActive = 0

    while 1:
        clock.tick(general.g_fps)
        framelength = clock.get_time()
        realfps = str(int(1000 / framelength))
        mouse = pygame.mouse.get_pos()
        drawgame(realfps, "new")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # If a text input box is not active
                    if general.g_widthActive == 0 and general.g_heightActive == 0:
                        # User clicks "Okay"
                        if ((newgame.ng_okay_borderRect[0] <= mouse[0] <=
                             newgame.ng_okay_borderRect[0] + newgame.ng_okay_borderRect[2]) and
                                (newgame.ng_okay_borderRect[1] <= mouse[1] <=
                                 newgame.ng_okay_borderRect[1] + newgame.ng_okay_borderRect[3])):
                            newgameokay()
                        # User clicks "Back"
                        elif ((newgame.ng_back_borderRect[0] <= mouse[0] <=
                                newgame.ng_back_borderRect[0] + newgame.ng_back_borderRect[2]) and
                                (newgame.ng_back_borderRect[1] <= mouse[1] <=
                                 newgame.ng_back_borderRect[1] + newgame.ng_back_borderRect[3])):
                            if backto == "gamemenu":
                                menuscreen()
                            elif backto == "winscreen":
                                winscreenmenu()
                        # User clicks width box
                        elif ((newgame.ng_width_borderRect[0] <= mouse[0] <=
                                newgame.ng_width_borderRect[0] + newgame.ng_width_borderRect[2]) and
                                (newgame.ng_width_borderRect[1] <= mouse[1] <=
                                 newgame.ng_width_borderRect[1] + newgame.ng_width_borderRect[3])):
                            general.g_widthActive = 1
                            general.g_widthInput = ""

                        # User clicks height box
                        elif ((newgame.ng_height_borderRect[0] <= mouse[0] <=
                                newgame.ng_height_borderRect[0] + newgame.ng_height_borderRect[2]) and
                                (newgame.ng_height_borderRect[1] <= mouse[1] <=
                                 newgame.ng_height_borderRect[1] + newgame.ng_height_borderRect[3])):
                            general.g_heightActive = 1
                            general.g_heightInput = ""

                    # If width input box is active
                    elif general.g_widthActive == 1:
                        # User clicks height box
                        if ((newgame.ng_height_borderRect[0] <= mouse[0] <=
                             newgame.ng_height_borderRect[0] + newgame.ng_height_borderRect[2]) and
                                (newgame.ng_height_borderRect[1] <= mouse[1] <=
                                 newgame.ng_height_borderRect[1] + newgame.ng_height_borderRect[3])):
                            general.g_heightActive = 1
                            general.g_widthActive = 0
                            general.g_heightInput = ""
                            general.g_widthInput = str(board.b_width)
                        # User clicks "Back"
                        elif ((newgame.ng_back_borderRect[0] <= mouse[0] <=
                                newgame.ng_back_borderRect[0] + newgame.ng_back_borderRect[2]) and
                                (newgame.ng_back_borderRect[1] <= mouse[1] <=
                                 newgame.ng_back_borderRect[1] + newgame.ng_back_borderRect[3])):
                            if backto == "gamemenu":
                                menuscreen()
                            elif backto == "winscreen":
                                winscreenmenu()
                        # User clicks anywhere but either box
                        else:
                            general.g_widthActive = 0
                            general.g_widthInput = str(board.b_width)
                            general.g_heightActive = 0

                    # If h input box is active
                    elif general.g_heightActive == 1:
                        # User clicks width box
                        if ((newgame.ng_width_borderRect[0] <= mouse[0] <=
                             newgame.ng_width_borderRect[0] + newgame.ng_width_borderRect[2]) and
                            (newgame.ng_width_borderRect[1] <= mouse[1] <=
                             newgame.ng_width_borderRect[1] + newgame.ng_width_borderRect[3])):
                            general.g_widthActive = 1
                            general.g_heightActive = 0
                            general.g_widthInput = ""
                            general.g_heightInput = str(board.b_height)
                        # User clicks "Back"
                        elif ((newgame.ng_back_borderRect[0] <= mouse[0] <=
                               newgame.ng_back_borderRect[0] + newgame.ng_back_borderRect[2]) and
                              (newgame.ng_back_borderRect[1] <= mouse[1] <=
                               newgame.ng_back_borderRect[1] + newgame.ng_back_borderRect[3])):
                            if backto == "gamemenu":
                                menuscreen()
                            elif backto == "winscreen":
                                winscreenmenu()
                        # User clicks anywhere but either box
                        else:
                            general.g_heightActive = 0
                            general.g_widthActive = 0
                            general.g_heightInput = str(board.b_width)

            # Text input handling

            # For width editing
            if general.g_widthActive == 1:

                # Basic addition of characters
                if len(general.g_widthInput) < 2:
                    charadd = ""
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_0 or event.key == pygame.K_KP0:
                            charadd = "0"
                        elif event.key == pygame.K_1 or event.key == pygame.K_KP1:
                            charadd = "1"
                        elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                            charadd = "2"
                        elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                            charadd = "3"
                        elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
                            charadd = "4"
                        elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
                            charadd = "5"
                        elif event.key == pygame.K_6 or event.key == pygame.K_KP6:
                            charadd = "6"
                        elif event.key == pygame.K_7 or event.key == pygame.K_KP7:
                            charadd = "7"
                        elif event.key == pygame.K_8 or event.key == pygame.K_KP8:
                            charadd = "8"
                        elif event.key == pygame.K_9 or event.key == pygame.K_KP9:
                            charadd = "9"
                    if len(general.g_widthInput) == 0 and charadd == "0":
                        # Doesn't allow leading 0s
                        pass
                    else:
                        general.g_widthInput += charadd

                if len(general.g_widthInput) > 0:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE:
                            # Handles backspacing
                            newstr = ""
                            for i in range(0, len(general.g_widthInput) - 1):
                                newstr += general.g_widthInput[i]
                            general.g_widthInput = str(newstr)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        if len(general.g_widthInput) == 0:
                            # Same as canceling
                            general.g_heightActive = 0
                            general.g_heightInput = str(board.b_height)
                            general.g_widthActive = 0
                            general.g_widthInput = str(board.b_width)
                        else:
                            # Input confirmed
                            general.g_heightActive = 0
                            general.g_widthActive = 0

                            # Doesn't allow numbers higher or lower than the set range
                            if int(general.g_widthInput) > general.g_boardSize_max:
                                general.g_widthInput = str(general.g_boardSize_max)
                            if int(general.g_widthInput) < general.g_boardSize_min:
                                general.g_widthInput = str(general.g_boardSize_min)
                            if int(general.g_heightInput) > general.g_boardSize_max:
                                general.g_heightInput = str(general.g_boardSize_max)
                            if int(general.g_heightInput) < general.g_boardSize_min:
                                general.g_heightInput = str(general.g_boardSize_min)

            # For h editing
            elif general.g_heightActive == 1:

                # Basic addition of characters
                if len(general.g_heightInput) < 2:
                    charadd = ""
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_0 or event.key == pygame.K_KP0:
                            charadd = "0"
                        elif event.key == pygame.K_1 or event.key == pygame.K_KP1:
                            charadd = "1"
                        elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                            charadd = "2"
                        elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                            charadd = "3"
                        elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
                            charadd = "4"
                        elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
                            charadd = "5"
                        elif event.key == pygame.K_6 or event.key == pygame.K_KP6:
                            charadd = "6"
                        elif event.key == pygame.K_7 or event.key == pygame.K_KP7:
                            charadd = "7"
                        elif event.key == pygame.K_8 or event.key == pygame.K_KP8:
                            charadd = "8"
                        elif event.key == pygame.K_9 or event.key == pygame.K_KP9:
                            charadd = "9"
                    if len(general.g_heightInput) == 0 and charadd == "0":

                        # Doesn't allow leading 0s
                        pass
                    else:
                        general.g_heightInput += charadd

                if len(general.g_heightInput) > 0:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE:
                            # Handles backspacing
                            newstr = ""
                            for i in range(0, len(general.g_heightInput) - 1):
                                newstr += general.g_heightInput[i]
                            general.g_heightInput = str(newstr)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        if len(general.g_heightInput) == 0:
                            # Same as canceling
                            general.g_heightActive = 0
                            general.g_heightInput = str(board.b_height)
                            general.g_widthActive = 0
                            general.g_widthInput = str(board.b_width)
                        else:
                            # Input confirmed
                            general.g_heightActive = 0
                            general.g_widthActive = 0

                            # Doesn't allow numbers higher or lower than the set range
                            if int(general.g_widthInput) > general.g_boardSize_max:
                                general.g_widthInput = str(general.g_boardSize_max)
                            if int(general.g_widthInput) < general.g_boardSize_min:
                                general.g_widthInput = str(general.g_boardSize_min)
                            if int(general.g_heightInput) > general.g_boardSize_max:
                                general.g_heightInput = str(general.g_boardSize_max)
                            if int(general.g_heightInput) < general.g_boardSize_min:
                                general.g_heightInput = str(general.g_boardSize_min)


# Game Menu -> New Game -> Okay
def newgameokay():
    print("New Game Okay")
    print(general.g_widthInput)
    print(general.g_heightInput)


# Game Menu -> Help
def helpbutton():
    while 1:
        clock.tick(general.g_fps)
        framelength = clock.get_time()
        realfps = str(int(1000 / framelength))
        mouse = pygame.mouse.get_pos()
        drawgame(realfps, "help")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if ((helpmenu.hm_x_borderRect[0] <= mouse[0] <=
                         (helpmenu.hm_x_borderRect[0] + helpmenu.hm_x_borderRect[2])) and
                            (helpmenu.hm_x_borderRect[1] <= mouse[1] <=
                                (helpmenu.hm_x_borderRect[1] + helpmenu.hm_x_borderRect[3]))):
                        gameloop()


# Solve with AI button
def solvewithai():
    print("SOLVE WITH AI")


# Undo / Redo
# The current move should match the index of the undoList
# The undoList always has at least one item in it: no moves means the only item is [""]
# Note that cellstate is the state AFTER the click
def undoredo(option, cell, cellstate, click):
    # If the player moved
    if option == "move":
        # Update list to only be current move plus previous moves
        newmovelist = []
        for i in range(0, len(general.g_moveList)):
            if i <= general.g_currentMove:
                newmovelist.append(general.g_moveList[i])
        general.g_moveList = list(newmovelist)

        # Current move gets incremented 1
        general.g_currentMove += 1

        # The newest move gets added to the move list
        general.g_moveList.append([cell, cellstate, click])

    # If the player clicked undo
    elif option == "undo":
        # If the current move is the starting position (blank board),
        # do nothing
        # Otherwise:
        if general.g_currentMove != 0:
            # cell, cellstate, and click all equal what the current move's attributes are
            cell = general.g_moveList[general.g_currentMove][0]
            cellstate = general.g_moveList[general.g_currentMove][1]
            click = general.g_moveList[general.g_currentMove][2]

            # the current move gets undone on the board (in slantDict)
            if click == "left":
                if cellstate == 0:
                    general.g_slantDict[cell] = 2
                else:
                    general.g_slantDict[cell] -= 1
            elif click == "right":
                if cellstate == 2:
                    general.g_slantDict[cell] = 0
                else:
                    general.g_slantDict[cell] += 1
            else:  # This should never be reached
                print("ERROR: undoredo() -> option == undo -> if currentMove != 0 -> else")
                sys.exit()

            # Re-checks solved numbers and loops
            solvednumbertest(cell)
            loopcheckmain()

            # Subtracts 1 from current move
            general.g_currentMove -= 1

    # If the player clicked redo
    elif option == "redo":
        # This should never be reached
        if general.g_currentMove > len(general.g_moveList) - 1:
            print("ERROR: undoredo() -> option == redo -> if currentMove > len(moveList) - 1")
            sys.exit()

        # If the current move is the most recent move,
        # do nothing
        # Otherwise:
        elif general.g_currentMove != len(general.g_moveList) - 1:
            # cell, cellstate, and click all equal what the next move's attributes are
            cell = general.g_moveList[general.g_currentMove + 1][0]
            cellstate = general.g_moveList[general.g_currentMove + 1][1]
            click = general.g_moveList[general.g_currentMove + 1][2]

            # the next move gets redone on the board (in slantDict)
            if click == "left":
                if cellstate == 2:
                    general.g_slantDict[cell] = 0
                else:
                    general.g_slantDict[cell] += 1
            elif click == "right":
                if cellstate == 0:
                    general.g_slantDict[cell] = 2
                else:
                    general.g_slantDict[cell] -= 1
            else:  # This should never be reached
                print("ERROR: undoredo() -> option == redo -> if currentMove != len(moveList) -> else")
                sys.exit()

            # Re-checks solved numbers and loops
            solvednumbertest(cell)
            loopcheckmain()

            # Adds 1 to current move
            general.g_currentMove += 1

    # Testing undo/redo function
    if general.g_testing_undoredo == 1:
        print("Undo/Redo Testing")
        print("Option: " + str(option))
        print("Cell: " + str(cell) + " CellState: " + str(cellstate) + " Click: " + str(click))
        for move in general.g_moveList:
            print(move)
        print(
            "Current Move: " + str(general.g_currentMove) + " | " + str(general.g_moveList[general.g_currentMove]))
        print("")


# Draw the screen once per frame
def drawgame(rfps, menu):
    win.fill(general.g_fillColor)
    mouse = pygame.mouse.get_pos()

    # Fill solved cells
    for xy in general.g_slantDict:
        slant = general.g_slantDict[xy]
        cell = board.b_cellDict[xy]
        if slant != 0:
            pygame.draw.rect(win, gamescreen.gs_cell_solvedColor,
                             [cell[0],
                              cell[1],
                              board.b_cell_width,
                              board.b_cell_height])

    # Light up cells on mouse over
    general.g_cellMouseover = "none"
    if menu == "none":
        for c in board.b_cellDict:
            cell = board.b_cellDict[c]
            if ((cell[0] <= mouse[0] <= cell[0] + board.b_cell_width - gamescreen.gs_lineWidth) and
                    cell[1] <= mouse[1] <= cell[1] + board.b_cell_height - gamescreen.gs_lineWidth):
                pygame.draw.rect(win, gamescreen.gs_cell_hoverColor,
                                 [cell[0],
                                  cell[1],
                                  board.b_cell_width,
                                  board.b_cell_height])
                general.g_cellMouseover = str(c)
                break

    # Draw lines
    for ln in board.b_lineList:
        pygame.draw.line(win, gamescreen.gs_lineColor, [ln[0], ln[1]], [ln[2], ln[3]], gamescreen.gs_lineWidth)

    # Draw Slants
    # Note that it draws looped slants and normal slants to separate surfaces then blits the two so that
    # looped slants are on top
    loopslants = pygame.Surface([general.g_width, general.g_height])
    loopslants.fill(general.g_colorkey)
    loopslants.set_colorkey(general.g_colorkey)
    normslants = pygame.Surface([general.g_width, general.g_height])
    normslants.fill(general.g_colorkey)
    normslants.set_colorkey(general.g_colorkey)
    for xy in general.g_slantDict:
        slant = general.g_slantDict[xy]
        cellx = ""
        celly = ""
        celladd = "x"
        for c in xy:
            if c == ",":
                celladd = "y"
            elif celladd == "x":
                cellx += c
            elif celladd == "y":
                celly += c

        line_left = board.b_lineDict_x[str(int(cellx) - 1)]
        line_right = board.b_lineDict_x[cellx]
        line_up = board.b_lineDict_y[str(int(celly) - 1)]
        line_down = board.b_lineDict_y[celly]

        if general.g_loopDict[xy] == 1:
            slantcolor = gamescreen.gs_slantColor_loop
            if slant == 0:
                pass
            elif slant == 1:
                pygame.draw.line(loopslants, slantcolor,
                                 [line_left[0],
                                  line_up[1]],
                                 [line_right[0],
                                  line_down[1]],
                                 gamescreen.gs_slantWidth)
            else:
                pygame.draw.line(loopslants, slantcolor,
                                 [line_left[0],
                                  line_down[1]],
                                 [line_right[0],
                                  line_up[1]],
                                 gamescreen.gs_slantWidth)
        else:
            slantcolor = gamescreen.gs_slantColor
            if slant == 0:
                pass
            elif slant == 1:
                pygame.draw.line(normslants, slantcolor,
                                 [line_left[0],
                                  line_up[1]],
                                 [line_right[0],
                                  line_down[1]],
                                 gamescreen.gs_slantWidth)
            else:
                pygame.draw.line(normslants, slantcolor,
                                 [line_left[0],
                                  line_down[1]],
                                 [line_right[0],
                                  line_up[1]],
                                 gamescreen.gs_slantWidth)
    win.blit(normslants, [0, 0])
    win.blit(loopslants, [0, 0])

    # Draw numbers
    for y in range(0, board.b_height + 1):
        for x in range(0, board.b_width + 1):
            try:
                num = board.b_numMatrix[y][x]
            except IndexError:
                pass
            else:
                if num != "x":
                    if num == "0":
                        adjust = board.b_adjust0
                    elif num == "1":
                        adjust = board.b_adjust1
                    elif num == "2":
                        adjust = board.b_adjust2
                    elif num == "3":
                        adjust = board.b_adjust3
                    else:
                        adjust = board.b_adjust4

                    # Check if the number is solved or not
                    state = general.g_solvedMatrix[y][x]
                    if state == "0":
                        circlecolor = gamescreen.gs_circleOutlineColor_neutral
                        circlefill = general.g_fillColor
                        numcolor = gamescreen.gs_numColor_neutral
                    elif state == "1":
                        circlecolor = gamescreen.gs_circleOutlineColor_solved
                        circlefill = gamescreen.gs_circleFillColor_solved
                        numcolor = gamescreen.gs_numColor_solved
                    else:
                        circlecolor = gamescreen.gs_circleOutlineColor_wrong
                        circlefill = gamescreen.gs_circleFillColor_wrong
                        numcolor = gamescreen.gs_numColor_wrong

                    numx = int(board.b_bufferx + (x * board.b_cell_width))
                    numy = int(board.b_buffery + (y * board.b_cell_height))
                    pygame.draw.circle(win, circlefill, [numx, numy], board.b_circleRadius)
                    pygame.draw.circle(win, circlecolor, [numx, numy],
                                       board.b_circleRadius, gamescreen.gs_circleWidth)
                    numfont = pygame.font.Font(gamescreen.gs_numFont, board.b_num_textSize)
                    numtext = numfont.render(num, 1, numcolor)
                    numw = numtext.get_rect().width
                    numh = numtext.get_rect().height
                    win.blit(numtext, [numx - (numw / 2) + adjust, numy - (numh / 2)])

    # Draw bottom bar
    pygame.draw.rect(win, botbar.bb_fillColor, botbar.bb_rect)

    # Draw bottom bar Help Button
    pygame.draw.rect(win, botbar.bb_button_borderColor, botbar.bb_help_borderRect)
    pygame.draw.rect(win, botbar.bb_button_fillColor, botbar.bb_help_rect)
    if menu == "none":
        if ((botbar.bb_help_borderRect[0] <= mouse[0] <=
             botbar.bb_help_borderRect[0] + botbar.bb_help_borderRect[2]) and
                (botbar.bb_help_borderRect[1] <= mouse[1] <=
                 botbar.bb_help_borderRect[1] + botbar.bb_help_borderRect[3])):
            pygame.draw.rect(win, botbar.bb_button_hoverColor, botbar.bb_help_rect)

    win.blit(botbar.bb_helpText, [botbar.bb_helpText_x, botbar.bb_helpText_y])

    # Draw bottom bar Menu Button
    pygame.draw.rect(win, botbar.bb_button_borderColor, botbar.bb_menu_borderRect)
    pygame.draw.rect(win, botbar.bb_button_fillColor, botbar.bb_menu_rect)
    if menu == "none":
        if ((botbar.bb_menu_borderRect[0] <= mouse[0] <=
             botbar.bb_menu_borderRect[0] + botbar.bb_menu_borderRect[2]) and
                (botbar.bb_menu_borderRect[1] <= mouse[1] <=
                 botbar.bb_menu_borderRect[1] + botbar.bb_menu_borderRect[3])):
            pygame.draw.rect(win, botbar.bb_button_hoverColor, botbar.bb_menu_rect)

    pygame.draw.line(win, botbar.bb_menu_graphic_color,
                     botbar.bb_menu_graphic1_a, botbar.bb_menu_graphic1_b, botbar.bb_menu_graphic_width)
    pygame.draw.line(win, botbar.bb_menu_graphic_color,
                     botbar.bb_menu_graphic2_a, botbar.bb_menu_graphic2_b, botbar.bb_menu_graphic_width)
    pygame.draw.line(win, botbar.bb_menu_graphic_color,
                     botbar.bb_menu_graphic3_a, botbar.bb_menu_graphic3_b, botbar.bb_menu_graphic_width)

    # Draw bottom bar Undo Button
    pygame.draw.rect(win, botbar.bb_button_borderColor, botbar.bb_undo_borderRect)
    pygame.draw.rect(win, botbar.bb_button_fillColor, botbar.bb_undo_rect)
    if menu == "none":
        if ((botbar.bb_undo_borderRect[0] <= mouse[0] <=
             botbar.bb_undo_borderRect[0] + botbar.bb_undo_borderRect[2]) and
                (botbar.bb_undo_borderRect[1] <= mouse[1] <=
                 botbar.bb_undo_borderRect[1] + botbar.bb_undo_borderRect[3])):
            pygame.draw.rect(win, botbar.bb_button_hoverColor, botbar.bb_undo_rect)

    win.blit(botbar.bb_undo_graphic_file, [botbar.bb_undo_graphic_x, botbar.bb_undo_graphic_y])

    # Draw bottom bar Redo Button
    pygame.draw.rect(win, botbar.bb_button_borderColor, botbar.bb_redo_borderRect)
    pygame.draw.rect(win, botbar.bb_button_fillColor, botbar.bb_redo_rect)
    if menu == "none":
        if ((botbar.bb_redo_borderRect[0] <= mouse[0] <=
             botbar.bb_redo_borderRect[0] + botbar.bb_redo_borderRect[2]) and
                (botbar.bb_redo_borderRect[1] <= mouse[1] <=
                 botbar.bb_redo_borderRect[1] + botbar.bb_redo_borderRect[3])):
            pygame.draw.rect(win, botbar.bb_button_hoverColor, botbar.bb_redo_rect)

    win.blit(botbar.bb_redo_graphic_file, [botbar.bb_redo_graphic_x, botbar.bb_redo_graphic_y])

    # Draw Help Menu
    if menu == "help":
        # Grey out the screen behind
        translayer = pygame.Surface([general.g_width, general.g_height])
        translayer.set_alpha(general.g_transAlpha)
        translayer.fill(general.g_transColor)
        win.blit(translayer, [0, 0])

        # Menu block
        pygame.draw.rect(win, helpmenu.hm_borderColor, helpmenu.hm_borderRect)
        pygame.draw.rect(win, helpmenu.hm_fillColor, helpmenu.hm_rect)

        # X Button
        pygame.draw.rect(win, helpmenu.hm_x_borderColor, helpmenu.hm_x_borderRect)
        pygame.draw.rect(win, helpmenu.hm_x_fillColor, helpmenu.hm_x_rect)
        if ((helpmenu.hm_x_borderRect[0] <= mouse[0] <=
             helpmenu.hm_x_borderRect[0] + helpmenu.hm_x_borderRect[2]) and
                (helpmenu.hm_x_borderRect[1] <= mouse[1] <=
                 helpmenu.hm_x_borderRect[1] + helpmenu.hm_x_borderRect[3])):
            pygame.draw.rect(win, helpmenu.hm_x_hoverColor, helpmenu.hm_x_rect)
        win.blit(helpmenu.hm_xText, [helpmenu.hm_xText_x, helpmenu.hm_xText_y])

        # Title
        win.blit(helpmenu.hm_titleText, [helpmenu.hm_titleText_x, helpmenu.hm_titleText_y])

        # Info Text
        win.blit(helpmenu.hm_infoText1, [helpmenu.hm_infoText1_x, helpmenu.hm_infoText1_y])
        win.blit(helpmenu.hm_infoText2, [helpmenu.hm_infoText2_x, helpmenu.hm_infoText2_y])
        win.blit(helpmenu.hm_infoText3, [helpmenu.hm_infoText3_x, helpmenu.hm_infoText3_y])
        win.blit(helpmenu.hm_infoText4, [helpmenu.hm_infoText4_x, helpmenu.hm_infoText4_y])
        win.blit(helpmenu.hm_infoText5, [helpmenu.hm_infoText5_x, helpmenu.hm_infoText5_y])
        win.blit(helpmenu.hm_infoText6, [helpmenu.hm_infoText6_x, helpmenu.hm_infoText6_y])

    # Draw Game Menu
    if menu == "menu":
        # Grey out the screen behind
        translayer = pygame.Surface([general.g_width, general.g_height])
        translayer.set_alpha(general.g_transAlpha)
        translayer.fill(general.g_transColor)
        win.blit(translayer, [0, 0])

        # Menu block
        pygame.draw.rect(win, gamemenu.gm_borderColor, gamemenu.gm_borderRect)
        pygame.draw.rect(win, gamemenu.gm_fillColor, gamemenu.gm_rect)

        # Title
        win.blit(gamemenu.gm_titleText, [gamemenu.gm_titleText_x, gamemenu.gm_titleText_y])

        # Buttons
        # Main Menu
        pygame.draw.rect(win, gamemenu.gm_button_borderColor, gamemenu.gm_mainmenu_borderRect)
        pygame.draw.rect(win, gamemenu.gm_button_fillColor, gamemenu.gm_mainmenu_rect)
        if ((gamemenu.gm_mainmenu_borderRect[0] <= mouse[0] <=
             gamemenu.gm_mainmenu_borderRect[0] + gamemenu.gm_mainmenu_borderRect[2]) and
                (gamemenu.gm_mainmenu_borderRect[1] <= mouse[1] <=
                 gamemenu.gm_mainmenu_borderRect[1] + gamemenu.gm_mainmenu_borderRect[3])):
            pygame.draw.rect(win, gamemenu.gm_button_hoverColor, gamemenu.gm_mainmenu_rect)

        # New Game
        pygame.draw.rect(win, gamemenu.gm_button_borderColor, gamemenu.gm_newgame_borderRect)
        pygame.draw.rect(win, gamemenu.gm_button_fillColor, gamemenu.gm_newgame_rect)
        if ((gamemenu.gm_newgame_borderRect[0] <= mouse[0] <=
             gamemenu.gm_newgame_borderRect[0] + gamemenu.gm_newgame_borderRect[2]) and
                (gamemenu.gm_newgame_borderRect[1] <= mouse[1] <=
                 gamemenu.gm_newgame_borderRect[1] + gamemenu.gm_newgame_borderRect[3])):
            pygame.draw.rect(win, gamemenu.gm_button_hoverColor, gamemenu.gm_newgame_rect)

        # Restart
        pygame.draw.rect(win, gamemenu.gm_button_borderColor, gamemenu.gm_restart_borderRect)
        pygame.draw.rect(win, gamemenu.gm_button_fillColor, gamemenu.gm_restart_rect)
        if ((gamemenu.gm_restart_borderRect[0] <= mouse[0] <=
             gamemenu.gm_restart_borderRect[0] + gamemenu.gm_restart_borderRect[2]) and
                (gamemenu.gm_restart_borderRect[1] <= mouse[1] <=
                 gamemenu.gm_restart_borderRect[1] + gamemenu.gm_restart_borderRect[3])):
            pygame.draw.rect(win, gamemenu.gm_button_hoverColor, gamemenu.gm_restart_rect)

        # Solve with AI
        pygame.draw.rect(win, gamemenu.gm_button_borderColor, gamemenu.gm_ai_borderRect)
        pygame.draw.rect(win, gamemenu.gm_button_fillColor, gamemenu.gm_ai_rect)
        if ((gamemenu.gm_ai_borderRect[0] <= mouse[0] <=
             gamemenu.gm_ai_borderRect[0] + gamemenu.gm_ai_borderRect[2]) and
                (gamemenu.gm_ai_borderRect[1] <= mouse[1] <=
                 gamemenu.gm_ai_borderRect[1] + gamemenu.gm_ai_borderRect[3])):
            pygame.draw.rect(win, gamemenu.gm_button_hoverColor, gamemenu.gm_ai_rect)

        # Back
        pygame.draw.rect(win, gamemenu.gm_button_borderColor, gamemenu.gm_back_borderRect)
        pygame.draw.rect(win, gamemenu.gm_button_fillColor, gamemenu.gm_back_rect)
        if ((gamemenu.gm_back_borderRect[0] <= mouse[0] <=
             gamemenu.gm_back_borderRect[0] + gamemenu.gm_back_borderRect[2]) and
                (gamemenu.gm_back_borderRect[1] <= mouse[1] <=
                 gamemenu.gm_back_borderRect[1] + gamemenu.gm_back_borderRect[3])):
            pygame.draw.rect(win, gamemenu.gm_button_hoverColor, gamemenu.gm_back_rect)

        # Button Text
        win.blit(gamemenu.gm_mainmenuText, [gamemenu.gm_mainmenuText_x, gamemenu.gm_mainmenuText_y])
        win.blit(gamemenu.gm_newgameText, [gamemenu.gm_newgameText_x, gamemenu.gm_newgameText_y])
        win.blit(gamemenu.gm_restartText, [gamemenu.gm_restartText_x, gamemenu.gm_restartText_y])
        win.blit(gamemenu.gm_aiText, [gamemenu.gm_aiText_x, gamemenu.gm_aiText_y])
        win.blit(gamemenu.gm_backText, [gamemenu.gm_backText_x, gamemenu.gm_backText_y])

    # New Game menu
    if menu == "new":
        # Grey out the screen behind
        translayer = pygame.Surface([general.g_width, general.g_height])
        translayer.set_alpha(general.g_transAlpha)
        translayer.fill(general.g_transColor)
        win.blit(translayer, [0, 0])

        # Menu block
        pygame.draw.rect(win, newgame.ng_borderColor, newgame.ng_borderRect)
        pygame.draw.rect(win, newgame.ng_fillColor, newgame.ng_rect)

        # Title
        win.blit(newgame.ng_titleText, [newgame.ng_title_x, newgame.ng_title_y])

        # Labels
        win.blit(newgame.ng_label_widthText, [newgame.ng_label_widthText_x, newgame.ng_label_widthText_y])
        win.blit(newgame.ng_label_heightText, [newgame.ng_label_heightText_x, newgame.ng_label_heightText_y])

        # Width Input Box
        pygame.draw.rect(win, newgame.ng_inputBox_borderColor, newgame.ng_width_borderRect)
        if general.g_widthActive == 0:
            pygame.draw.rect(win, newgame.ng_inputBox_fillColor, newgame.ng_width_rect)
            if ((newgame.ng_width_borderRect[0] <= mouse[0] <=
                 newgame.ng_width_borderRect[0] + newgame.ng_width_borderRect[2]) and
                    (newgame.ng_width_borderRect[1] <= mouse[1] <=
                     newgame.ng_width_borderRect[1] + newgame.ng_width_borderRect[3])):
                pygame.draw.rect(win, newgame.ng_inputBox_hoverColor, newgame.ng_width_rect)
        else:
            pygame.draw.rect(win, newgame.ng_inputBox_hoverColor, newgame.ng_width_rect)
        widthnumtext = newgame.ng_numberFont.render(general.g_widthInput, 1, newgame.ng_number_textColor)
        widthnumtext_w = widthnumtext.get_rect().width
        widthnumtext_x = (newgame.ng_width_rect[0] + newgame.ng_width_rect[2] - widthnumtext_w -
                          newgame.ng_inputBox_borderSize + newgame.ng_number_width_nudgex)
        widthnumtext_y = newgame.ng_label_widthText_y + newgame.ng_number_width_nudgey
        win.blit(widthnumtext, [widthnumtext_x, widthnumtext_y])

        # Height Input Box
        pygame.draw.rect(win, newgame.ng_inputBox_borderColor, newgame.ng_height_borderRect)
        if general.g_heightActive == 0:
            pygame.draw.rect(win, newgame.ng_inputBox_fillColor, newgame.ng_height_rect)
            if ((newgame.ng_height_borderRect[0] <= mouse[0] <=
                 newgame.ng_height_borderRect[0] + newgame.ng_height_borderRect[2]) and
                    (newgame.ng_height_borderRect[1] <= mouse[1] <=
                     newgame.ng_height_borderRect[1] + newgame.ng_height_borderRect[3])):
                pygame.draw.rect(win, newgame.ng_inputBox_hoverColor, newgame.ng_height_rect)
        else:
            pygame.draw.rect(win, newgame.ng_inputBox_hoverColor, newgame.ng_height_rect)
        heightnumtext = newgame.ng_numberFont.render(general.g_heightInput, 1, newgame.ng_number_textColor)
        heightnumtext_w = heightnumtext.get_rect().width
        heightnumtext_x = (newgame.ng_height_rect[0] + newgame.ng_height_rect[2] - heightnumtext_w -
                           newgame.ng_inputBox_borderSize + newgame.ng_number_height_nudgex)
        heightnumtext_y = newgame.ng_label_heightText_y + newgame.ng_number_height_nudgey
        win.blit(heightnumtext, [heightnumtext_x, heightnumtext_y])

        # Okay Button
        pygame.draw.rect(win, newgame.ng_button_borderColor, newgame.ng_okay_borderRect)
        if general.g_widthActive == 0 and general.g_heightActive == 0:
            pygame.draw.rect(win, newgame.ng_button_fillColor, newgame.ng_okay_rect)
            if ((newgame.ng_okay_borderRect[0] <= mouse[0] <=
                 newgame.ng_okay_borderRect[0] + newgame.ng_okay_borderRect[2]) and
                    (newgame.ng_okay_borderRect[1] <= mouse[1] <=
                     newgame.ng_okay_borderRect[1] + newgame.ng_okay_borderRect[3])):
                pygame.draw.rect(win, newgame.ng_button_hoverColor, newgame.ng_okay_rect)
        else:
            pygame.draw.rect(win, newgame.ng_button_noclickColor, newgame.ng_okay_rect)
        win.blit(newgame.ng_okayText, [newgame.ng_okayText_x, newgame.ng_okayText_y])

        # Back Button
        pygame.draw.rect(win, newgame.ng_button_borderColor, newgame.ng_back_borderRect)
        pygame.draw.rect(win, newgame.ng_button_fillColor, newgame.ng_back_rect)
        if ((newgame.ng_back_borderRect[0] <= mouse[0] <=
             newgame.ng_back_borderRect[0] + newgame.ng_back_borderRect[2]) and
                (newgame.ng_back_borderRect[1] <= mouse[1] <=
                 newgame.ng_back_borderRect[1] + newgame.ng_back_borderRect[3])):
            pygame.draw.rect(win, newgame.ng_button_hoverColor, newgame.ng_back_rect)
        win.blit(newgame.ng_backText, [newgame.ng_backText_x, newgame.ng_backText_y])

        # Info Text
        win.blit(newgame.ng_infoText1, [newgame.ng_infoText1_x, newgame.ng_infoText1_y])
        win.blit(newgame.ng_infoText2, [newgame.ng_infoText2_x, newgame.ng_infoText2_y])

    # Win Screen
    if menu == "win":
        # Grey out the screen behind
        translayer = pygame.Surface([general.g_width, general.g_height])
        translayer.set_alpha(general.g_transAlpha)
        translayer.fill(general.g_transColor)
        win.blit(translayer, [0, 0])

        # Menu block
        pygame.draw.rect(win, winscreen.ws_borderColor, winscreen.ws_borderRect)
        pygame.draw.rect(win, winscreen.ws_fillColor, winscreen.ws_rect)

        # Title
        win.blit(winscreen.ws_titleText, [winscreen.ws_titleText_x, winscreen.ws_titleText_y])

        # New Game
        pygame.draw.rect(win, winscreen.ws_button_borderColor, winscreen.ws_newgame_borderRect)
        pygame.draw.rect(win, winscreen.ws_button_fillColor, winscreen.ws_newgame_rect)
        if ((winscreen.ws_newgame_borderRect[0] <= mouse[0] <=
             winscreen.ws_newgame_borderRect[0] + winscreen.ws_newgame_borderRect[2]) and
                (winscreen.ws_newgame_borderRect[1] <= mouse[1] <=
                 winscreen.ws_newgame_borderRect[1] + winscreen.ws_newgame_borderRect[3])):
            pygame.draw.rect(win, winscreen.ws_button_hoverColor, winscreen.ws_newgame_rect)
        win.blit(winscreen.ws_newgameText, [winscreen.ws_newgameText_x, winscreen.ws_newgameText_y])

        # Main Menu
        pygame.draw.rect(win, winscreen.ws_button_borderColor, winscreen.ws_mainmenu_borderRect)
        pygame.draw.rect(win, winscreen.ws_button_fillColor, winscreen.ws_mainmenu_rect)
        if ((winscreen.ws_mainmenu_borderRect[0] <= mouse[0] <=
             winscreen.ws_mainmenu_borderRect[0] + winscreen.ws_mainmenu_borderRect[2]) and
                (winscreen.ws_mainmenu_borderRect[1] <= mouse[1] <=
                 winscreen.ws_mainmenu_borderRect[1] + winscreen.ws_mainmenu_borderRect[3])):
            pygame.draw.rect(win, winscreen.ws_button_hoverColor, winscreen.ws_mainmenu_rect)
        win.blit(winscreen.ws_mainmenuText, [winscreen.ws_mainmenuText_x, winscreen.ws_mainmenuText_y])

        # Back
        pygame.draw.rect(win, winscreen.ws_button_borderColor, winscreen.ws_back_borderRect)
        pygame.draw.rect(win, winscreen.ws_button_fillColor, winscreen.ws_back_rect)
        if ((winscreen.ws_back_borderRect[0] <= mouse[0] <=
             winscreen.ws_back_borderRect[0] + winscreen.ws_back_borderRect[2]) and
                (winscreen.ws_back_borderRect[1] <= mouse[1] <=
                 winscreen.ws_back_borderRect[1] + winscreen.ws_back_borderRect[3])):
            pygame.draw.rect(win, winscreen.ws_button_hoverColor, winscreen.ws_back_rect)
        win.blit(winscreen.ws_backText, [winscreen.ws_backText_x, winscreen.ws_backText_y])

    # Draw FPS (for testing)
    if general.g_testing_fps == 1:
        fnt = pygame.font.SysFont("default", 20)
        fpstxt = fnt.render(rfps, 1, [0, 255, 0])
        win.blit(fpstxt, [10, 10])

    # Display Update
    pygame.display.update()


# Main gameloop
def gameloop():
    while 1:
        clock.tick(general.g_fps)
        framelength = clock.get_time()
        realfps = str(int(1000 / framelength))
        mouse = pygame.mouse.get_pos()
        drawgame(realfps, "none")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # Click Handling
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Left Click slant change
                    if general.g_cellMouseover != "none":
                        if general.g_slantDict[general.g_cellMouseover] == 2:
                            general.g_slantDict[general.g_cellMouseover] = 0
                        else:
                            general.g_slantDict[general.g_cellMouseover] += 1
                        solvednumbertest(general.g_cellMouseover)
                        loopcheckmain()
                        undoredo("move", general.g_cellMouseover,
                                 general.g_slantDict[general.g_cellMouseover], "left")

                    # Help Button click
                    if ((botbar.bb_help_borderRect[0] <= mouse[0] <=
                         botbar.bb_help_borderRect[0] + botbar.bb_help_borderRect[2]) and
                            (botbar.bb_help_borderRect[1] <= mouse[1] <=
                             botbar.bb_help_borderRect[1] + botbar.bb_help_borderRect[3])):
                        helpbutton()

                    # Menu Button click
                    if ((botbar.bb_menu_borderRect[0] <= mouse[0] <=
                         botbar.bb_menu_borderRect[0] + botbar.bb_menu_borderRect[2]) and
                            (botbar.bb_menu_borderRect[1] <= mouse[1] <=
                             botbar.bb_menu_borderRect[1] + botbar.bb_menu_borderRect[3])):
                        menuscreen()

                    # Undo Button click
                    if ((botbar.bb_undo_borderRect[0] <= mouse[0] <=
                         botbar.bb_undo_borderRect[0] + botbar.bb_undo_borderRect[2]) and
                            (botbar.bb_undo_borderRect[1] <= mouse[1] <=
                             botbar.bb_undo_borderRect[1] + botbar.bb_undo_borderRect[3])):
                        undoredo("undo", "", 0, "")

                    # Redo Button click
                    if ((botbar.bb_redo_borderRect[0] <= mouse[0] <=
                         botbar.bb_redo_borderRect[0] + botbar.bb_redo_borderRect[2]) and
                            (botbar.bb_redo_borderRect[1] <= mouse[1] <=
                             botbar.bb_redo_borderRect[1] + botbar.bb_redo_borderRect[3])):
                        undoredo("redo", "", 0, "")

                if event.button == 3:
                    # Right Click slant change
                    if general.g_cellMouseover != "none":
                        if general.g_slantDict[general.g_cellMouseover] == 0:
                            general.g_slantDict[general.g_cellMouseover] = 2
                        else:
                            general.g_slantDict[general.g_cellMouseover] -= 1
                        solvednumbertest(general.g_cellMouseover)
                        loopcheckmain()
                        undoredo("move", general.g_cellMouseover,
                                 general.g_slantDict[general.g_cellMouseover], "right")

                # Testing Loops
                if event.button == 2:
                    if general.g_testing_loops == 1:
                        if general.g_cellMouseover != "none":
                            print(general.g_pathDict[general.g_cellMouseover])
                            print(general.g_connectDict[general.g_cellMouseover])
                            print("")

                # Testing Winscreen
                if event.button == 7:
                    if general.g_testing_winscreen == 1:
                        winscreenmenu()

                # Slant change Win Check
                if general.g_cellMouseover != "none":
                    if general.g_slantDict[general.g_cellMouseover] != 0:
                        wincheck()


# Starts / Restarts the game
def restart():
    global board
    global general
    general = General()
    board = Board()
    boardbuilder()
    gameloop()


restart()
