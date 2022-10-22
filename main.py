import curses
import time
import random
from curses import wrapper


text = '''
                                                                                       @@@@@@@@@@@@@@@
                                                                                  @@@@@*******&@@     @@
                                                                               %@@*/*/******@@* ,     . @@@
                                                                          #&&&&@@@&&********@@,       &&,,,&&
                                                                        &%**.*,,*,,,&&&*****@@,       @@   @@
                                                                        @@,         ,,,&%/**//%%%     ,,   @@
                                                                        @@/,,       ,,,@@*****/((%%%%%&%&&%@@&&%
                                                                        ..#@@*******@@@//*****%@@%%%%%%%%%%%%%%%&&,
                                                                             @@@@@@@////////@@%##@@@@@@@@@@@@@@@
                                                                             @@#//////////////&@@############@@@
                                                                             . &@@@@//////////(//@@@@@@@@@@@@, .
                                                                                .,,,,&&&&&&&&&&&&&,,,,,,,,,,,,
                                                                                    **.*.*,,*,,,*

'''


def main(stdscr):
    """ A simple flappy game on terminal

    The game is built on curses library which does some cool functions in the terminal i.e. makes it more functional.
    So, I decided to make a simple Flappy bird game based on this library. Not sure why but enjoyed every moment while
    making it.
    """

    # Initializing color pairs
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_GREEN)

    # Game variables, changes to it will make big differences
    game_variables = {
        'game_time': 0,
        'initial_velocity': 20,
        'height': 0,
        'last_click': 0,
        'last_height': 0,
        'fps': 15,
        'game_ended': False,
        'open_debug': True,
        'obstacles': {150: random.randint(3, 7), 185: random.randint(3, 7)},
        'key': ' ',
        'point': 0,
        'Highest': 0
    }

    def points():
        """Point system of the game

        Calculated based on time. First point is achieved if the player survives for about 3.1 seconds. Then
        increases incrementally by x seconds

        Returns:
            int: The points obtained in a given time
        """
        game_variables['point'] = (game_variables['game_time'] - 4) // (35 / game_variables['fps']) + 1
        if game_variables['point'] < 0:
            game_variables['point'] = 0

    def flappy_bird(stdscr, color=curses.color_pair(1)):
        """ Displays the bird in the terminal

        Args:
            stdscr: Curses window
            color: Color pair to use in the bird
        """
        stdscr.addstr(game_variables['y'] - 1, 91, '   ', color)
        stdscr.addstr(game_variables['y'], 90, '     ', color)
        stdscr.addstr(game_variables['y'] + 1, 91, '   ', color)

    def check_input(stdscr):
        """ Checks user input

        When used, it checks for user input without delay. If no input given ' ' is considered as input. If the
        desired key is pressed, the function will return ' ' for next .5 second.

        Args:
            stdscr: Curses window

        Returns:
            str: ' ' or the key pressed
        """
        if game_variables['last_click'] > 0.5:
            try:
                game_variables['key'] = stdscr.getkey()
                if game_variables['key'] == 'KEY_UP':
                    game_variables['last_click'] = 0
                if game_variables['key'] == 'd':
                    game_variables['open_debug'] = not game_variables['open_debug']
            except:
                game_variables['key'] = ' '
                game_variables['last_click'] += 1 / game_variables['fps']
        else:
            game_variables['key'] = ' '

    def debug(key=' '):
        """ Puts a debug screen on top-left

        A debug screen is showed if game_variables['open_debug'] is True.

        Args:
            key (str) : Input provided by user. ' ' if not value provided
        """
        if game_variables['open_debug']:
            pad = curses.newpad(10, 30)
            # pad.clear()
            pad.addstr(0, 0, 'Key Pressed      : ' + key)
            pad.addstr(1, 0, 'Horizontal Pixels: ' + str(curses.COLS))
            pad.addstr(2, 0, 'Vertical Pixels  : ' + str(curses.LINES))
            pad.addstr(3, 0, 'FPS              : ' + str(game_variables['fps']))
            pad.addstr(4, 0, 'Initial velocity : ' + str(round(game_variables['initial_velocity'], 3)))
            pad.addstr(5, 0, 'Height           : ' + str(round(game_variables['height'], 3)))
            pad.addstr(6, 0, 'Ordinate         : ' + str(round(game_variables['y'], 3)))
            pad.addstr(7, 0, 'Real Time        : ' + str(round(game_variables['game_time'], 3)))
            pad.addstr(8, 0, 'Last Click Delta : ' + str(round(game_variables['last_click'], 3)))
            pad.addstr(9, 0, 'Points           : ' + str(int(game_variables['point'])))
            pad.refresh(0, 0, 0, 0, 10, 30)

    def height(t, u=30, g=15):
        """ Determines height on a time

        Uses the formula of determining height when an object is thrown upwards.

        Args:
            t (float) : Time from start
            u (float) : Initial velocity. Default 30
            g (flaot) : Gravitational acceleration. Default 20

        Returns:
            float: height from ground. Can be both positive and negative
        """
        return (u * t) - (.5 * g * (t ** 2))

    def ordinate(key):
        """ Determines the height from ground and ordinate on screen

        By determining height from ground by using height function, ordinate(y) is determined for the bird. Note that
        the mid-point of the screen is considered as the ground. Going upward is positive and vice versa.
        """
        if key == 'KEY_UP':
            game_variables['last_height'] = game_variables['height']
            game_variables['last_click'] = 0

        game_variables['height'] = game_variables['last_height'] + height(game_variables['last_click'], game_variables['initial_velocity'])
        game_variables['y'] = 24 - round(game_variables['height'])

    def game():
        """ All the above functions put together to run the game.

        At first the screen is cleared. Then user input is taken. Depending on input, new ordinate is
        determined. The obstacles are placed in the screen. Blah blah blah
        """
        stdscr.addstr(15, 75, text, curses.A_BOLD | curses.A_BLINK)
        stdscr.addstr(30, 77, 'Press any key to start game')
        stdscr.refresh()
        stdscr.getch()

        # No delay while inputting setting
        stdscr.nodelay(True)

        while True:
            # Clear screen
            stdscr.clear()
            # Check for input
            check_input(stdscr)
            # Determine y
            ordinate(game_variables['key'])
            # Some shortcuts
            if game_variables['y'] > 49:
                game_variables['y'] = 49
            # Display bird
            flappy_bird(stdscr)
            # Display and function of obstacles
            obstacles(stdscr)
            # Refresh screen
            stdscr.refresh()
            # Display debug (toggle)
            debug(game_variables['key'])
            # Determine points
            points()
            # Ends game when y is less than 1 and greater than 47
            if not 1 < game_variables['y'] < 48:
                game_variables['game_ended'] = True

            if game_variables['game_ended']:
                break
            # Add time to variables
            game_variables['game_time'] += 1 / game_variables['fps']
            game_variables['last_click'] += 1 / game_variables['fps']
            # Sleep to make it 15 fps
            time.sleep(1 / game_variables['fps'])

        stdscr.nodelay(False)
        stdscr.addstr(15, 60, " ______ _______ _______ _______       _____  _    _ _______  ______", curses.A_BOLD)
        stdscr.addstr(16, 60, "|  ____ |_____| |  |  | |______      |     |  \  /  |______ |_____/", curses.A_BOLD)
        stdscr.addstr(17, 60, "|_____| |     | |  |  | |______      |_____|   \/   |______ |    \_", curses.A_BOLD)
        stdscr.addstr(19, 89, f"Points: {int(game_variables['point'])}", curses.A_BOLD | curses.A_STANDOUT)
        stdscr.refresh()
        time.sleep(3)
        stdscr.getch()

    def obstacles(stdscr):
        """ Displays obstacles and implement of obstacles

        The obstacles are distanced equally and randomized. By checking the obstacle values a barrier is placed.

        Args:
             stdscr: Curses window
        """
        items = list(game_variables['obstacles'].items())
        if items[-1][0] == 150:
            items.append((185, random.randint(3, 7)))
        if items[0][0] == 1:
            items.pop(0)
        game_variables['obstacles'] = {k - 1: v for k, v in items}

        for k, v in game_variables['obstacles'].items():
            stdscr.attron(curses.color_pair(1))

            stdscr.vline(0, k, '|', v * 5 - 8, curses.color_pair(1))
            stdscr.vline(0, k + 1, '|', v * 5 - 8, curses.color_pair(1))
            stdscr.vline(0, k + 2, '|', v * 5 - 8, curses.color_pair(1))

            stdscr.vline(v * 5 + 8, k, '|', 50, curses.color_pair(1))
            stdscr.vline(v * 5 + 8, k + 1, '|', 50, curses.color_pair(1))
            stdscr.vline(v * 5 + 8, k + 2, '|', 50, curses.color_pair(1))
            stdscr.attroff(curses.color_pair(1))

        for x_value in [90, 91, 92, 93, 94, 95]:
            if game_variables['obstacles'].get(x_value):
                check = game_variables['obstacles'].get(x_value)

                if not (check * 5 + 6 > game_variables['y'] > check * 5 - 7):
                    game_variables['game_ended'] = True

    return game()


wrapper(main)