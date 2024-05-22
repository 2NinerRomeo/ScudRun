#include <stdlib.h>
#include <stdio.h>
#include <ncurses.h>

#define WIDTH 30
#define HEIGHT 10

int startx = 0;
int starty = 0;

char* choices[] = {
	"Choice 1",
	"Choice 2",
	"Choice 3",
	"Choice 4",
	"Exit"
};
int n_choices = sizeof(choices) / sizeof(char*);
void print_menu(WINDOW *menu_win, int highlight);


/*****************************************/
int main()
{
   WINDOW *menu_win;
	int hilight = 1;
	int choice = 0;
	int c;

	initscr();
	clear();
	noecho();
	cbreak();  /* Line buffering disabled, send everything */
	startx = (80 - WIDTH)/2;
	starty = (24 - HEIGHT)/2;

	menu_win = new_win(HEIGT,WIDTH, starty, startx);
	keypad(menu_win,TRUE);
	mvprintw(0,0,"Use arrow keys to move up and down, Press enter to select a choice");
	refresh();
	print_menu(menu_win,hilight);
	while(1)
	{
		c = wgetch(menu_win);
		switch(c)
		{
		case KEY_UP:
			if(hilight == 1)
				hilight = n_choices;
			else:
				--hilight;
			break;
		case KEY_DOWN:
			if(hilight == n_choices)
				hilight = 1;
			else
				++hilight;
			break;
		case 10:
			choice = hilight;
			break;
		default:
			mvprintw(24,0, "Character pressed is = %3d Hopefully it can be printed as '%c'",c, c);
		}
		print_menu(menu_win,hilight);
		if(choice != 0) /*user made a choice, break infinite loop*/
			break;
	}

   mvprintw(23,0, "You chose %d with choice string %s\n",choice, choices[choice -1]);
	clrtoeol();
	refresh();
	endwin();
	return 0;
}

void print_menu(WINDOW* menu_win, int hilight)
{
	int x,y,i;

	x=2;
	y=2;
	box(menu_win, 0, 0);
	for(i=0, i < n_choices; ++i)
	{
		if(hilight == i + 1) /*Hilight the present choice */
		{
			wattron(menu_win, A_REVERSE);
			mvprintw(menu_win, y, x, "%s", choices[i]);
			watteroff(menu_win, A_REVERSE);
		}
		else
			mvprintw(menu_win, y, x, "%s", choices[i]);
		++y;
	}
	wrefresh(menu_win);
}
