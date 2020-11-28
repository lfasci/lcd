#!/usr/bin/python
import datetime
import lcddriver
import time
import sys
import getopt


# Load the driver and set it to "display"
display = lcddriver.lcd()

def show_message_blink(display, text , row_num , max_cols):
    display.lcd_display_string(text,row_num)
    time.sleep(0.4)
    padding = ' ' * max_cols
    display.lcd_display_string(padding,row_num)
    time.sleep(0.4)
    
def show_usage():
    print ("Usage: " + sys.argv[0] + ' -f <first row message> -s <second row message>  -b <blink first row> -B <blink second row> -c <center first row> -C <center second row> -d <duration in seconds>')
    display.lcd_clear()
    display.lcd_backlight(0) 
    sys.exit()

def show_message_one_row(display, text, row_num , max_cols, center, blink):
    if(len(text) > max_cols):
        time.sleep(1)
        #To allow show two special functions as blink and scoll at the same time this must be converted to multi thread execution
        blink = 0;
        padding = ' ' * max_cols
        txt2show = padding + text + padding
        for i in range(len(txt2show) - max_cols + 1):
            text_to_print = txt2show[i:i+max_cols]
            display.lcd_display_string(text_to_print,row_num)
            time.sleep(0.2)
        time.sleep(0.7)
    else:
        txt2show = text
        if ((center == 1) and (len(text) < max_cols)):
            padding = ' ' * int(round((max_cols - len(text))/2))
            txt2show = padding + text + padding
        if (blink == 1):    
            show_message_blink(display, txt2show , row_num , max_cols)
        else :   
            display.lcd_display_string(txt2show,row_num)
        
def show_message_two_row(display, text1 = '',text2 = '', max_cols = 15 ):
    display.lcd_display_string(text1[:max_cols],1)
    display.lcd_display_string(text2[:max_cols],2)
    time.sleep(1)
    scroll = max(len(text1), len(text2))
    for i in range( scroll - max_cols + 1):
        text_to_print1 = text1[i:i+max_cols].ljust(scroll)
        text_to_print2 = text2[i:i+max_cols].ljust(scroll)
        display.lcd_display_string(text_to_print1,1)
        display.lcd_display_string(text_to_print2,2)
        time.sleep(0.2)
    time.sleep(1)

def main(argv):
    row1_msg = ''
    row2_msg = ''
    duration = 10
    blink1 = 0
    center1 = 0
    blink2 = 0
    center2 = 0
    display_cols = 15
    row_num = 1
    text = ""

    try:
      opts, args = getopt.getopt(argv,"hf:s:d:b:B:c:C:",["msg1=","msg2=","duration=","blink1=","blink2=","center1=","center2="])
    except getopt.GetoptError:
      show_usage()
    for opt, arg in opts:
      if opt == '-h':
         show_usage()
      elif opt in ("-f", "--msg1"):
         row1_msg = arg
      elif opt in ("-s", "--msg2"):
         row2_msg = arg       
      elif opt in ("-d", "--duration"):
         duration = int(arg)      
      elif opt in ("-b", "--blink1"):
         blink1 = int(arg)            
      elif opt in ("-B", "--blink2"):
         blink2 = int(arg)      
      elif opt in ("-c", "--center1"):
         center1 = int(arg)      
      elif opt in ("-C", "--center2"):
         center2 = int(arg)

    try:
        # Make sure backlight is on / turn on
        display.lcd_backlight(1)                                         
        t_end = time.time() + duration * 1
        if ((len(row1_msg) > display_cols) and (len(row2_msg) > display_cols)):
            while time.time() < t_end:
                show_message_two_row(display, row1_msg, row2_msg)     
        else:
            while time.time() < t_end:
                #To allow show two special functions as blink and scoll at the same time this must be converted to multi thread execution
                if (((len(row1_msg) > display_cols) or (len(row2_msg) > display_cols)) and ((blink1 == 1) or (blink2 == 1))):
                    print ("Scolling and blinking at the same time is non supported in the current version")
                    blink1 = 0
                    blink2 = 0
                show_message_one_row(display, row1_msg, 1, display_cols, center1, blink1)     
                show_message_one_row(display, row2_msg, 2, display_cols, center2, blink2)     
        # Clear and Turn backlight off
        display.lcd_clear()
        display.lcd_backlight(0)                          
    except KeyboardInterrupt: # If there is a KeyboardInterrupt (when you press CTRL + C), exit the program and cleanup
            display.lcd_clear()
            display.lcd_backlight(0)

if __name__ == "__main__":
   main(sys.argv[1:])            



