#include <ncurses/ncurses.h>

int main(int argc, char ** argv)
{
    int ch;
    // init screen and sets up screen
    initscr();
    raw(); //disable line buffering
    keypad(stdscr, TRUE);  //function keys
    noecho();
    // print to screen
    printw("Type any character to see it in bold\n");
    //since we're using raw() no CR is required
    ch = getch();
    // refreshes the screen
    if(ch == KEY_F(1))
       printw("F1 key pressed");
    else
	 {
		 printw("The pressed key is ");
		 attron(A_BOLD);
		 printw("%c", ch);
		 attroff(A_BOLD);
	 }

    refresh();
    // pause the screen output
    getch();
    // deallocates memory and ends ncurses
    endwin();
    return 0;
}
