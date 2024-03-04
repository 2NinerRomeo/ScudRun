#include <ncurses.h>
#include <cstdlib>
#include <iostream>
#include <string>
#include <format>

void swap_to_window(void);

void swap_to_console(void);

void print_in_middle(WINDOW* win,
							int starty,
							int startx,
							int width,
							std::string str);
void console_message(void);

int loopcount = 0;

typedef  enum IfaceState{
   IFACE_CONSOLE,
	IFACE_WINDOW
}IfaceState;

int main(int argc, char* argv[])
{
	IfaceState state = IFACE_CONSOLE;
	bool quit = false;
	//Todo:
	// - find a keypress, to replace console input with cin
	// - Find a way to capture console output while in window mode
	// -- https://www.linuxquestions.org/questions/linux-newbie-8/can-a-process-redirect-stdout-and-still-use-ncurses-in-a-terminal-4175411385/
	// - Fix the fact that window mode is not printing anything.
	// +++Fixed by defining color pair after start_color()
	// - Fix that we lose the stty output in console and on returning out of the program
	// - Back to console, clear screen and start at the beginning
	// +++Needed a system call - unsatisfying
	// - Failing to echo or show console:
	// -- Ideas. Quit at points in the program, test console

   std::cout << "Starting in console mode\r\n";
	console_message();
	
	while(!quit)
	{
		switch(state)
		{
		case IFACE_CONSOLE:
		{
			std::string cmd;
			std::cin >> cmd;
			if(cmd == std::string("win"))
			{
				swap_to_window();
				state = IFACE_WINDOW;
			}
			else if (cmd == std::string("quit"))
			{
				std::cout << "Quitting from Console...\r\n";
				quit = true;
			}
		}
		case IFACE_WINDOW:
		{
			print_in_middle(stdscr,
		                   LINES/2,0,0,
                         std::format(("Window active. Loop: {}", loopCount).c_str());

			std::cout << "Printing while in window\r\n";
			int ch = getch();
			
			if(ch == KEY_RIGHT)
			{
				std::cout << "Print more...\r\n";
			}
			else if(ch == KEY_LEFT)
			{
				std::cout << "Trying for console...\r\n";
				swap_to_console;
				state = IFACE_CONSOLE;
			}
			if(ch == KEY_DOWN)
			{
				std::cout << "Quitting from Window...\r\n";
				endwin();
				quit = true;
			}
		}
		default:
			continue;
		}
		loopcount++;
	}
   return 0;
}

void swap_to_window(void)
{
	initscr();
	keypad(stdscr, TRUE);

	if(has_colors() == FALSE)
	{
		print_in_middle(stdscr,
							 LINES/2,0,0,
							 "Window view, No color option");
	}
	else
	{
		start_color();
		init_pair(1, COLOR_RED, COLOR_BLACK);
		attron(COLOR_PAIR(1));
 		print_in_middle(stdscr,
		                LINES/2,0,0,
                      std::format(("Window active. Loop: {}", loopCount).c_str());
		attroff(COLOR_PAIR(1));
	}
}

void swap_to_console(void)
{
	endwin();
	system("clear"); //works in msys
	std::cout << "Exited to console...\r\n";
	console_message();
}


void print_in_middle(WINDOW* win,
							int starty,
							int startx,
							int width,
							std::string str)
{
	int length, x,y;
	float temp;

	if(win == NULL)
		win = stdscr;
	getyx(win, y, x);
	if(startx != 0)
		x = startx;
	if(starty != 0)
		y = starty;
	if(width == 0)
		width = 80;

	length = str.length();
	temp = (width - length)/2;
	x = startx + (int)temp;
	mvwprintw(win, y, x, "%s", str.c_str());
	refresh();
}

void console_message(void)
{
	std::cout << "\"win\"  - swap to ncurses window\r\n";
	std::cout << "\"quit\" - exit\r\n";
}
