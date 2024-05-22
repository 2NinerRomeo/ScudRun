#include <ncurses.h>
#include <cstdlib>
#include <cstring>
#include <iostream>
#include <string>

void swap_to_window(void);

void swap_to_console(void);

void print_in_middle(WINDOW* win,
							int starty,
							int startx,
							int width,
							char* string);

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
	// ---Fixed by defining color pair after start_color()
	// - Fix that we lose the stty output in console and on returning out of the program

   std::cout << "Starting in console mode" << std::endl;
	
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
				quit = true;
			break;
		}
		case IFACE_WINDOW:
		{
			int ch = 0;
			ch = getch();
			
			printf("Printing while in window\n");
			if(ch == KEY_RIGHT)
			{
				std::cout << "Print more..." << std::endl;
				break;
			}
			else if(ch == KEY_LEFT)
			{
				swap_to_console;
				std::cout << "Exit to console..." << std::endl;
				state = IFACE_CONSOLE;
			}
			if(ch == KEY_DOWN)
			{
				endwin();
				quit = true;
			}
		}
		default:
			break;
		}
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
                      "Window active ...");
		attroff(COLOR_PAIR(1));
	}
}

void swap_to_console(void)
{
	endwin();
	printf("Back to console\n");
}


void print_in_middle(WINDOW* win,
							int starty,
							int startx,
							int width,
							char* string)
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

	length = strlen(string);
	temp = (width - length)/2;
	x = startx + (int)temp;
	mvwprintw(win, y, x, "%s", string);
	refresh();
}
