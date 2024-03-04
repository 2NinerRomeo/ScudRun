#include <ncurses.h>

int main (int argc, char *argv[])
{
	initscr();
	start_color();

	init_pair(1, COLOR_CYAN, COLOR_BLACK);
	printw("A Big string which I didn't care to type fully ");
	mvchgat(0,13,5, A_BLINK, 1, NULL);
	//mvchgat params 1,2 : position
	// param 3 number of characters (-1) end of line
	// param 4 attribute
	// param 5 color index (see init_pair)
	// param 6 always null
	refresh();
	getch();
	endwin();
	return 0;
}
