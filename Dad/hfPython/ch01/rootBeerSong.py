word = "bottles"
for rb_num in range (99, 0, -1):
    print( rb_num, word, "of root beer on the wall.")
    print( rb_num, word, "of root beer!")
    print( "Take one down.")
    print( "Pass it around.")
    if rb_num == 1:
        print( "We're out of Root Beer....  :(")
    else:
        new_num = rb_num - 1
        if new_num == 1:
            word = "bottle"
        print( new_num, word, "of root beer on the wall.")
    print()
