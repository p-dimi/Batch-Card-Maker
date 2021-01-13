import cv2
import textwrap 
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import csv
import os
from keyboard import is_pressed as key


### init default variables
line_spacing=1
font_size_title=1
title_hor=1
title_ver=1
font_size=1
font_ideal_size=1
text_ver=1
is_creatures_get=0
font_size_stats=1
stats_hor=1
stats_ver=1
stats_per_row=1
row_max_chars=1
row_max_chars_title=1
use_card_picture_trackbar=0
pic_hor=1
pic_ver=1
c_pic_scale=1.0
is_creatures = False
use_card_picture = False
separator_line = None
split_sign = None
stroke = False
content_box_height_constant = 0

print('\n\n~~~ Welcome to Card Maker! ~~~\nPlease follow the instructions below:\n\n')

# Font file
new_config=True
config_folder = 'Configs'
config_files = os.listdir(config_folder)

if len(config_files) > 0:
    print('There are already configuration files present.\nChoose if to use an existing config file or make a new one:')
    print('\n0: Make a new config\n')
    for i in range(len(config_files)):
        print('{}: {}\n'.format(i + 1, config_files[i]))
    conf_idc = int(input("Type an integer\nWhich config file to use?\nType 0 if to make a new one "))
    if conf_idc == 0:
        pass
    else:
        new_config = False
        conf_idc = conf_idc - 1
    if new_config == False:
        # open existing conf
        with open(os.path.join(config_folder,config_files[conf_idc]), 'r') as f:
            open_conf_rows = csv.reader(f, delimiter=',', quotechar='"')
            confs=list(open_conf_rows)
        
        # get the configurations from file (it's inefficient, I know, but it doesn't matter it's not a production code)
        print(confs)
        for i in range(len(confs)):
            c_set = confs[i][0]
            if i == 0:
                line_spacing = int(c_set)
            elif i == 1:
                font_size_title= int(c_set)
            elif i == 2:
                title_hor= int(c_set)
            elif i == 3:
                title_ver= int(c_set)
            elif i == 4:
                font_size= int(c_set)
            elif i == 5:
                font_ideal_size= int(c_set)
            elif i == 6:
                text_ver= int(c_set)
            elif i == 7:
                is_creatures_get= int(c_set)
            elif i == 8:
                font_size_stats= int(c_set)
            elif i == 9:
                stats_hor= int(c_set)
            elif i == 10:
                stats_ver= int(c_set)
            elif i == 11:
                stats_per_row= int(c_set)
            elif i == 12:
                row_max_chars= int(c_set)
            elif i == 13:
                row_max_chars_title= int(c_set)
            elif i == 14:
                use_card_picture_trackbar= int(c_set)
            elif i == 15:
                pic_hor= int(c_set)
            elif i == 16:
                pic_ver= int(c_set)
            elif i == 17:
                c_pic_scale=float(c_set)
            elif i == 18:
                is_creatures = int(c_set)
                if is_creatures == 0:
                    is_creatures = False
                else:
                    is_creatures = True
            elif i == 19:
                use_card_picture = int(c_set)
                if use_card_picture == 0:
                    use_card_picture = False
                else:
                    use_card_picture = True
            elif i == 20:
                separator_line = c_set
            elif i == 21:
                split_sign = c_set
            elif i == 22:
                stroke = int(stroke)
                if stroke == 0:
                    stroke = False
                else:
                    stroke = True
            elif i == 23:
                content_box_height_constant = int(c_set)

print('~~~Select your fonts:~~~\n\n')
font_folder='Fonts'
fonts=os.listdir(font_folder)
print('You have the following font options:\n')
for f in range(len(fonts)):
    print('{}: {}'.format(f, fonts[f]))

font_title_idc = int(input("\nType an integer\nWhich font to use for Card Title? "))
font_idc = int(input("\nType an integer\nWhich font to use for Card Content? "))

font_title_path = os.path.join(font_folder,fonts[font_title_idc])
font_path = os.path.join(font_folder,fonts[font_idc])

if new_config == True:
    # Stroke settings
    print('\n\n~~~Stroke Setting:~~~\n\n')
    stroke=str(input("Text Visibility\nDo you want a white stroke around the text? (Y or N) "))
    if stroke == 'y' or stroke == 'Y':
        stroke = True
    else:
        stroke = False

# Card Face to Use
print('\n\n~~~Select your card image:~~~\n\n')
card_folder='Cards'
cards=os.listdir(card_folder)
print('You have the following card options:\n')
for c in range(len(cards)):
    print('{}: {}\n'.format(c, cards[c]))

card_idc = int(input("Type an integer\nWhich card image to use? "))
card_u = os.path.join(card_folder, cards[card_idc])

# CSV to read
print('\n\n~~~Select your CSV:~~~\n\n')
csv_folder='Csvs'
csvs=os.listdir(csv_folder)
print('You have the following CSV options:\n')
for c in range(len(csvs)):
    print('{}: {}\n'.format(c, csvs[c]))

csv_idc = int(input("Type an integer\nWhich CSV file to use? "))
csv_to_read = os.path.join(csv_folder, csvs[csv_idc])



# Read CSV
rows=None
with open(csv_to_read) as csvfile:
    open_rows = csv.reader(csvfile, delimiter=',', quotechar='"')
    rows=list(open_rows)

# default config window image
config_img_path='config_image.png'

# default stats
hp_idc=4
def_idc=5
spd_idc=6
reach_idc=7
row_idc=8
dmg_idc=9

print('\n\n~~~Stat Columns:~~~\n\n')
stats_default = str(input("\nUse default stat settings?\n(HP, DEF, SPD, Reach, ROW, DMG)\nType Y or N: "))
if stats_default == 'y' or stats_default == 'Y':
    stats_default = True
else:
    stats_default = False

stats_num=0
stats_guide=[]

if stats_default == False:
    stats_num = int(input("\nHow many stats are in your CSV?\nNOTE: You can type 0 if you have no stats in your CSV "))
    if stats_num > 0:
        for c in range(stats_num):
            print('\nColumn {}\n'.format(c+1))
            st=input(str("Name the stat in column {}: ".format(c+1)))
            stats_guide.append(st)
    else:
        print('No stat columns will be used.')
        
print('\n\n~~~Card Pictures:~~~\n\n')
pic_used = str(input('Do the cards in the CSV use pictures? (Y or N) '))
if pic_used == 'y' or pic_used == 'Y':
    c_pic_idc = int(input("\nType an integer higher than 4\nWhich column in the CSV are your picture names?: "))
    c_pic_idc = c_pic_idc - 1
else:
    c_pic_idc=0

if new_config == True:            
    print('\n\n~~~Separator Line:~~~\n\n')
    s_lines=['~'*8, '-'*8, '_'*8, ' '*8, '.'*8, '^'*8]
    print('You have the following Separator Line options:\n')
    for s in range(len(s_lines)):
        print(s, '"{}"\n'.format(s_lines[s]))
    separator_idc = int(input('Type an integer\nChoose your separator line: '))
    separator_line = s_lines[separator_idc]

    print('\n\n~~~Separation Character:~~~\n\n')
    print('Choose a special Separation Character.\nThis character is used internally for some operations. This means that this character can NOT appear anywhere in your CSV.\nGood options are "%", or "$", or "&", or "@", but it can be anything.\n')
    # Split Sign
    split_sign=str(input("Type in a Separation Character: "))

print('\n\nAll set! Press any key to start the maker')
go_on=input()

# Csv Indeces
title_idc=0
type_a_idc=1
type_b_idc=2
effect_idc=3

# for Creatures
is_creatures=False

# Card Output Folder
card_out='FinishedCards'

# Read empty card face
blank_card = cv2.imread(card_u)

card_h = blank_card.shape[0]
card_w = blank_card.shape[1]


def blank(x):
    pass

n_win_name = 'Configurations'
n_win = cv2.namedWindow(n_win_name, cv2.WINDOW_NORMAL)
cv2.resizeWindow(n_win_name, 900,900)
c_win_name = 'Card Preview'
c_win = cv2.namedWindow(c_win_name, cv2.WINDOW_AUTOSIZE)
#n_win='Card Preview'
#c_win = cv2.namedWindow('Card Preview', cv2.WINDOW_AUTOSIZE)


# Trackbars

# misc
previewed_card_trackbar = cv2.createTrackbar('Previewed Card', n_win_name, 0, len(rows), blank)

line_spacing_trackbar = cv2.createTrackbar('Line Spacing', n_win_name , int(card_h*0.007), int(card_h*0.02), blank)
content_box_height_constant_trackbar = cv2.createTrackbar('Context Box Height', n_win_name , int(card_h*0.21), int(card_h*0.42), blank)
max_chars_title_trackbar = cv2.createTrackbar('Max Chars In Row (Title)', n_win_name , 30, 100, blank)
max_chars_trackbar = cv2.createTrackbar('Max Chars In Row (Content)', n_win_name , 34, 100, blank)

# card picture
use_card_pic_trackbar = cv2.createTrackbar('Use Picture', n_win_name , 0, 1, blank)
pic_hor_trackbar = cv2.createTrackbar('Picture Horizontal Adjustment', n_win_name , 0, card_w, blank)
pic_ver_trackbar = cv2.createTrackbar('Picture Vertical Adjustment', n_win_name , 0, card_h, blank)
pic_scale_trackbar = cv2.createTrackbar('Picture Scale', n_win_name, 100, 200, blank)

# title
font_size_title_trackbar = cv2.createTrackbar('Title Font Size', n_win_name , int(card_h*0.035), int(card_h*0.085), blank)
title_hor_trackbar = cv2.createTrackbar('Title Horizontal Adjustment', n_win_name , int(card_w/2), card_w, blank)
title_ver_trackbar = cv2.createTrackbar('Title Vertical Adjustment', n_win_name , int(card_h/2), card_h, blank)

# font
font_size_trackbar = cv2.createTrackbar('Content Font Size', n_win_name , int(card_h*0.014), int(card_h*0.065), blank)
ideal_trackbar = cv2.createTrackbar('S. Content Horizontal Adjustment', n_win_name , int(card_h*0.007), int(card_w/2), blank)
text_vet_trackbar = cv2.createTrackbar('Content Vertical Adjustment', n_win_name , int(card_h/2), card_h, blank)
# stats
is_creature_trackbar = cv2.createTrackbar('Show Stats?', n_win_name , 0, 1, blank)
font_size_stats_trackbar = cv2.createTrackbar('Stats Font Size', n_win_name , int(card_h*0.035), int(card_h*0.085), blank)
stats_hor_trackbar=cv2.createTrackbar('Stats Horizontal Adjustment', n_win_name , int(card_w/2), card_w, blank)
stats_ver_trackbar=cv2.createTrackbar('Stats Vertical Adjustment', n_win_name , int(card_h/2), card_h, blank)

stats_per_row_trackbar=cv2.createTrackbar('Stats Per Row\n(Only when using custom stats)', n_win_name , 3, 10, blank)

# buttons
proceeding=0

# Text Color
text_color = (0,0,0,255)

# Line Drop Generator
def drop_line(iterable, fill, cond):
    iterable = iter(iterable)
    prev = next(iterable)
    yield prev
    for cur in iterable:
        if cond(prev, cur):
            yield fill
        yield cur
        prev = cur

# Separator (between title and description)
separator = "\n"+separator_line

if new_config == True:
    # Config loop
    print('Config Started')
    while True:
        card_num = cv2.getTrackbarPos('Previewed Card', n_win_name)
        row = rows[card_num - 1]

        # get trackbar positions
        # misc adjust
        line_spacing = cv2.getTrackbarPos('Line Spacing', n_win_name)
        content_box_height_constant = cv2.getTrackbarPos('Context Box Height', n_win_name) 
        row_max_chars_title = cv2.getTrackbarPos('Max Chars In Row (Title)', n_win_name) 
        row_max_chars = cv2.getTrackbarPos('Max Chars In Row (Content)', n_win_name)     
        
        # picture adjust
        use_card_picture_trackbar = cv2.getTrackbarPos('Use Picture', n_win_name)
        c_pic_scale = cv2.getTrackbarPos('Picture Scale', n_win_name)
        c_pic_scale = c_pic_scale/100
        
        pic_hor = cv2.getTrackbarPos('Picture Horizontal Adjustment', n_win_name)
        pic_ver = cv2.getTrackbarPos('Picture Vertical Adjustment', n_win_name)
        
        # title adjust
        font_size_title = cv2.getTrackbarPos('Title Font Size', n_win_name)
        title_hor=cv2.getTrackbarPos('Title Horizontal Adjustment', n_win_name)
        title_ver = cv2.getTrackbarPos('Title Vertical Adjustment', n_win_name)
        
        # content adjust
        font_size = cv2.getTrackbarPos('Content Font Size', n_win_name)
        font_ideal_size=cv2.getTrackbarPos('S. Content Horizontal Adjustment', n_win_name)
        text_ver = cv2.getTrackbarPos('Content Vertical Adjustment', n_win_name)
     
        # stats adjust
        # show stats?
        is_creatures_get = cv2.getTrackbarPos('Show Stats?', n_win_name) 
        
        font_size_stats = cv2.getTrackbarPos('Stats Font Size', n_win_name)
        stats_hor=cv2.getTrackbarPos('Stats Horizontal Adjustment', n_win_name)
        stats_ver=cv2.getTrackbarPos('Stats Vertical Adjustment', n_win_name)
        
        stats_per_row=cv2.getTrackbarPos('Stats Per Row\n(Only when using custom stats)', n_win_name)
        
        # confirm there's no negative numbers
        if is_creatures_get < 0:
            is_creatures_get=0
        if line_spacing <= 0:
            line_spacing=1
        if content_box_height_constant <= 0:
            content_box_height_constant=1
        if font_size_title <= 0:
            font_size_title=1
        if font_size <= 0:
            font_size=1
        if font_size_stats <= 0:
            font_size_stats=1
        if title_hor <= 0:
            title_hor=0
        if title_ver <= 0:
            title_ver=0
        if text_ver <= 0:
            text_ver=0
        if stats_per_row <= 0:
            stats_per_row = 1
        if row_max_chars_title <= 0:
            row_max_chars_title=1
        if row_max_chars <= 0:
            row_max_chars=1
        
        if is_creatures_get == 1:
            is_creatures = True
        else:
            is_creatures = False
        
        
        if use_card_picture_trackbar == 1:
            use_card_picture = True
        else:
            use_card_picture = False
        
        
        blank_card_copy = blank_card.copy()
        
        # card picture settings
        if use_card_picture:
            try:
                c_pic=cv2.imread(os.path.join('CardPictures',row[c_pic_idc]))
                
                c_pic = cv2.resize(c_pic,(0,0),fx=c_pic_scale, fy=c_pic_scale)
            except:
                c_pic=np.ones((1,1,3))*255
            
            if pic_hor >= (card_w - c_pic.shape[1]):
                pic_hor = card_w - c_pic.shape[1] - 1
            if pic_ver >= (card_h - c_pic.shape[0]):
                pic_ver = card_h - c_pic.shape[0] - 1
            if pic_hor <= 0:
                pic_hor = 1
            if pic_ver <= 0:
                pic_ver = 1
            if c_pic_scale <= 0:
                c_pic_scale = 0.01
                
            blank_card_copy[pic_ver:pic_ver+c_pic.shape[0],pic_hor:pic_hor+c_pic.shape[1],:] = c_pic
            
            # adjust title and font positions based on picture height
            title_ver = title_ver + pic_ver + c_pic.shape[0]
            text_ver = text_ver + pic_ver + c_pic.shape[0]
            
        
        # Load image into PIL
        img_pil = Image.fromarray(blank_card_copy)

        # card dimensions and positioning
        # Define text box starting positions
        title_box_h = int(card_h * 0.9)
        title_box_w = int(card_w * 0.9)
        text_box_h = title_box_h - content_box_height_constant - (line_spacing*2)
        text_box_w = int(card_w * 0.92)

        title_box_start_h = int((card_h - title_box_h) / 2) + (title_ver - int(card_h/2))
        title_box_start_w = int((card_w - title_box_w) / 2) + (title_hor - int(card_w/2))

        text_box_start_h = int((card_h - text_box_h) / 2) + (text_ver - int(card_h/2))
        text_box_start_w = int((card_w - text_box_w) / 2)

        stats_box_start_h = int(card_h - (card_h*0.19)) + (stats_ver - int(card_h/2))
        stats_box_start_w = int(card_w*0.08) + (stats_hor - int(card_w/2))

        # ideal size is for spacing (for centering), unique multiplier
        font_spacer_multiplier = font_ideal_size / font_size

        # Load font
        title_font = ImageFont.truetype(font_title_path, font_size_title)
        body_font = ImageFont.truetype(font_path, font_size)
        stats_font = ImageFont.truetype(font_path, font_size_stats)

        title = row[title_idc]
        title = title

        type_a = row[type_a_idc]
        type_b = row[type_b_idc]
        
        if type_a == "-":
            type_a = ""
        
        if type_b != "-":
            type_b = ", " + type_b
        else:
            type_b = ""
            
        effect_a = row[effect_idc]

        # Combine text
        type_text = "({}{})".format(type_a, type_b)

        if type_a == "" and type_b == "":
            type_text = ""

        title_text = "{}\n{}\n{}".format(title, type_text, separator)
        
        # If this is a creature card
        if is_creatures:
            # The text structure of creatures
            if stats_default:
                try:
                    stat_line = 'ROW:{}   REACH:{}   SPD:{}\nHP:{}   DEF:{}\nDMG:{}'.format(row[row_idc], row[reach_idc], row[spd_idc], row[hp_idc], row[def_idc], row[dmg_idc])
                except:
                    stat_line = 'ROW:{}   REACH:{}   SPD:{}\nHP:{}   DEF:{}\nDMG:{}'.format("0", "0", "0", "0", "0", "0")
            else:
                try:
                    stat_line=[]
                    for s in range(len(stats_guide)):
                        stat_line.append('{}: {}  '.format(stats_guide[s], row[s+4]))
                        if (s+1) % stats_per_row == 0:
                            stat_line.append('\n')
                    stat_line = ''.join(stat_line)
                except:
                    stat_line=['']
                    if len(stats_guide) > 0:
                        for s in range(len(stats_guide)):
                            stat_line.append('{}: {}  '.format(stats_guide[s], "-"))
                            if (s+1) % stats_per_row == 0:
                                stat_line.append('\n')
                    else:
                        pass
                    stat_line = ''.join(stat_line)

        # Wrap text
        wrapped_title = textwrap.wrap(title_text, width=row_max_chars_title)
        
        ## ~~ ## ~~ ## ~~ ## ~~ ## ~~ ## ~~ ## ~~ ## ~~ ## ~~ ##
        
        # Drop Lines
        # Title
        for l_num in range(len(wrapped_title)):
            line = wrapped_title[l_num]
            
            title_text = "".join(list(drop_line(line, split_sign, lambda x,y: x!="(" and y=="(")))

            title_text = "".join(list(drop_line(title_text, split_sign, lambda x,y: x==" " and y=="~")))

            title_text = title_text.split(split_sign)
            
            wrapped_title[l_num] = title_text
        wrapped_title = [item for sublist in wrapped_title for item in sublist]
        
        to_remove = []
        # Make sure the () section of tags is not split
        for l_num in range(len(wrapped_title)-1):
            line = wrapped_title[l_num]
            next_line = wrapped_title[l_num + 1]
            
            if line[0] == "(" and line[-1] == ",":
                line = line + next_line
                to_remove.append(next_line)
            wrapped_title[l_num] = line

        for l in to_remove:
            if l in wrapped_title:
                wrapped_title.remove(l)
        
        wrapped_text = effect_a.split('\n')
        
        # Calculate per-line spaces for centering
        # Title
        for l_num in range(len(wrapped_title)):
            line = wrapped_title[l_num]
            spaces = " "*int((row_max_chars_title - len(line)) / 2)
            line = spaces + line
            wrapped_title[l_num] = line
        
        # Body
        for l_num in range(len(wrapped_text)):
            line = wrapped_text[l_num]  
            
            wrapped_t = textwrap.wrap(line, width=row_max_chars)
            
            line = '\n'.join(wrapped_t)
            
            # Drop lines in the texts when appropriate
            body_text = "".join(list(drop_line(line, "\n", lambda x,y: x==".")))
            
            spaces = " "*int(( ((row_max_chars * font_spacer_multiplier) - len(line)) / 2 ))
            line = spaces + line
            wrapped_text[l_num] = line

        # Convert wrapped text back into single strings
        fin_title = "\n".join(wrapped_title)
        fin_body = "\n".join(wrapped_text)

        # Draw text
        draw = ImageDraw.Draw(img_pil)
        
        draw.text((title_box_start_w, title_box_start_h), fin_title, font = title_font, fill = text_color, spacing=line_spacing)
        
        draw.text((text_box_start_w, text_box_start_h), fin_body, font = body_font, fill = text_color, spacing=line_spacing)
        
        
        # The card stats (if applicable)
        if is_creatures:
            draw.text((stats_box_start_w, stats_box_start_h), stat_line, font=stats_font, fill = text_color, spacing=line_spacing+15, align='left')
            draw.text((stats_box_start_w + 2, stats_box_start_h), stat_line, font=stats_font, fill = text_color, spacing=line_spacing+15, align='left')
        
        # Convert to cv2 array
        img = np.asarray(img_pil)

        # Show
        cv2.imshow('Configurations', cv2.imread(config_img_path))
        # display preview as 700px tall
        ratio = 700 / card_h
        cv2.imshow(c_win_name, cv2.resize(img.astype(np.uint8), (0,0), fx=ratio, fy=ratio))
        
        # frame delay
        cv2.waitKey(1)
        
        if key('q') or key('Q'):
            print('Quitting')
            break
        elif key('c') or key('C'):
            print('Continuing without saving configurations')
            proceeding = 1
            break
        elif key('s') or key('S'):
            conf_name = str(input("How to call the new config file?: "))
            print('Saving configurations and making cards')
            with open(os.path.join(config_folder, conf_name + ".csv"), "w+", newline='') as csvfile:
                config_writer = csv.writer(csvfile, delimiter=',', quotechar='"') 
                for i in range(24):
                    if i == 0:
                        config_writer.writerow([str(line_spacing)])
                    elif i == 1:
                        config_writer.writerow([str(font_size_title)])
                    elif i == 2:
                        config_writer.writerow([str(title_hor)])
                    elif i == 3:
                        config_writer.writerow([str(title_ver)])
                    elif i == 4:
                        config_writer.writerow([str(font_size)])
                    elif i == 5:
                        config_writer.writerow([str(font_ideal_size)])
                    elif i == 6:
                        config_writer.writerow([str(text_ver)])
                    elif i == 7:
                        config_writer.writerow([str(is_creatures_get)])
                    elif i == 8:
                        config_writer.writerow([str(font_size_stats)])
                    elif i == 9:
                        config_writer.writerow([str(stats_hor)])
                    elif i == 10:
                        config_writer.writerow([str(stats_ver)])
                    elif i == 11:
                        config_writer.writerow([str(stats_per_row)])
                    elif i == 12:
                        config_writer.writerow([str(row_max_chars)])
                    elif i == 13:
                        config_writer.writerow([str(row_max_chars_title)])
                    elif i == 14:
                        config_writer.writerow([str(use_card_picture_trackbar)])
                    elif i == 15:
                        config_writer.writerow([str(pic_hor)])
                    elif i == 16:
                        config_writer.writerow([str(pic_ver)])
                    elif i == 17:
                        config_writer.writerow([str(c_pic_scale)])
                    elif i == 18:
                        if is_creatures == False:
                            config_writer.writerow([str(0)])
                        else:
                            config_writer.writerow([str(1)])
                    elif i == 19:
                        if use_card_picture == False:
                            config_writer.writerow([str(0)])
                        else:
                            config_writer.writerow([str(1)])
                    elif i == 20:
                        config_writer.writerow([str(separator_line)])
                    elif i == 21:
                        config_writer.writerow([str(split_sign)])
                    elif i == 22:
                        if stroke == False:
                            config_writer.writerow([str(0)])
                        else:
                            config_writer.writerow([str(1)])
                    elif i == 23:
                        config_writer.writerow([str(content_box_height_constant)])
            proceeding = 1
            break
            
    cv2.destroyAllWindows()

if proceeding == 1 or new_config == False:
    print('\n\nCreating cards:\n\n')
    # Loop going over Read CSV
    for i in range(len(rows)):
        row = rows[i]
        
        blank_card_copy = blank_card.copy()
        
        # card picture settings
        if use_card_picture:
            try:
                c_pic=cv2.imread(os.path.join('CardPictures',row[c_pic_idc]))
                
                c_pic = cv2.resize(c_pic,(0,0),fx=c_pic_scale, fy=c_pic_scale)
            except:
                c_pic=np.ones((1,1,3))*255
            
            if pic_hor >= (card_w - c_pic.shape[1]):
                pic_hor = card_w - c_pic.shape[1] - 1
            if pic_ver >= (card_h - c_pic.shape[0]):
                pic_ver = card_h - c_pic.shape[0] - 1
            if pic_hor <= 0:
                pic_hor = 1
            if pic_ver <= 0:
                pic_ver = 1
            if c_pic_scale <= 0:
                c_pic_scale = 0.01
                
            blank_card_copy[pic_ver:pic_ver+c_pic.shape[0],pic_hor:pic_hor+c_pic.shape[1],:] = c_pic
            
            """# adjust title and font positions based on picture height
            title_ver = title_ver + pic_ver + c_pic.shape[0]
            text_ver = text_ver + pic_ver + c_pic.shape[0]"""
            
        # Load image into PIL
        img_pil = Image.fromarray(blank_card_copy)
        
        # card dimensions and positioning
        # Define text box starting positions
        title_box_h = int(card_h * 0.9)
        title_box_w = int(card_w * 0.9)
        text_box_h = title_box_h - content_box_height_constant - (line_spacing*2)
        text_box_w = int(card_w * 0.92)

        title_box_start_h = int((card_h - title_box_h) / 2) + (title_ver - int(card_h/2))
        title_box_start_w = int((card_w - title_box_w) / 2) + (title_hor - int(card_w/2))

        text_box_start_h = int((card_h - text_box_h) / 2) + (text_ver - int(card_h/2))
        text_box_start_w = int((card_w - text_box_w) / 2)

        stats_box_start_h = int(card_h - (card_h*0.19)) + (stats_ver - int(card_h/2))
        stats_box_start_w = int(card_w*0.08) + (stats_hor - int(card_w/2))

        # ideal size is for spacing (for centering), unique multiplier
        font_spacer_multiplier = font_ideal_size / font_size

        # Load font
        title_font = ImageFont.truetype(font_title_path, font_size_title)
        body_font = ImageFont.truetype(font_path, font_size)
        stats_font = ImageFont.truetype(font_path, font_size_stats)

        title = row[title_idc]
        title = title

        type_a = row[type_a_idc]
        type_b = row[type_b_idc]
        
        if type_b != "-":
            type_b = ", " + type_b
        else:
            type_b = ""
            
        effect_a = row[effect_idc]

        # Combine text
        type_text = "({}{})".format(type_a, type_b)

        title_text = "{}\n{}\n{}".format(title, type_text, separator)
        
        # If this is a creature card
        if is_creatures:
            # The text structure of creatures
            if stats_default:
                try:
                    stat_line = 'ROW:{}   REACH:{}   SPD:{}\nHP:{}   DEF:{}\nDMG:{}'.format(row[row_idc], row[reach_idc], row[spd_idc], row[hp_idc], row[def_idc], row[dmg_idc])
                except:
                    stat_line = 'ROW:{}   REACH:{}   SPD:{}\nHP:{}   DEF:{}\nDMG:{}'.format("0", "0", "0", "0", "0", "0")
            else:
                try:
                    stat_line=[]
                    for s in range(len(stats_guide)):
                        stat_line.append('{}: {}  '.format(stats_guide[s], row[s+4]))
                        if (s+1) % stats_per_row == 0:
                            stat_line.append('\n')
                    stat_line = ''.join(stat_line)
                except:
                    stat_line=[]
                    for s in range(len(stats_guide)):
                        stat_line.append('{}: {}  '.format(stats_guide[s], "-"))
                        if (s+1) % stats_per_row == 0:
                            stat_line.append('\n')
                    stat_line = ''.join(stat_line)

        # Wrap text
        wrapped_title = textwrap.wrap(title_text, width=row_max_chars_title)
        
        ## ~~ ## ~~ ## ~~ ## ~~ ## ~~ ## ~~ ## ~~ ## ~~ ## ~~ ##
        
        # Drop Lines
        # Title
        for l_num in range(len(wrapped_title)):
            line = wrapped_title[l_num]
            
            title_text = "".join(list(drop_line(line, split_sign, lambda x,y: x!="(" and y=="(")))

            title_text = "".join(list(drop_line(title_text, split_sign, lambda x,y: x==" " and y=="~")))

            title_text = title_text.split(split_sign)
            
            wrapped_title[l_num] = title_text
        wrapped_title = [item for sublist in wrapped_title for item in sublist]
        
        to_remove = []
        # Make sure the () section of tags is not split
        for l_num in range(len(wrapped_title)-1):
            line = wrapped_title[l_num]
            next_line = wrapped_title[l_num + 1]
            
            if line[0] == "(" and line[-1] == ",":
                line = line + next_line
                to_remove.append(next_line)
            wrapped_title[l_num] = line

        for l in to_remove:
            if l in wrapped_title:
                wrapped_title.remove(l)
        
        wrapped_text = effect_a.split('\n')
        
        # Calculate per-line spaces for centering
        # Title
        for l_num in range(len(wrapped_title)):
            line = wrapped_title[l_num]
            spaces = " "*int((row_max_chars_title - len(line)) / 2)
            line = spaces + line
            wrapped_title[l_num] = line
        
        # Body
        for l_num in range(len(wrapped_text)):
            line = wrapped_text[l_num]  
            
            wrapped_t = textwrap.wrap(line, width=row_max_chars)
            
            line = '\n'.join(wrapped_t)
            
            # Drop lines in the texts when appropriate
            body_text = "".join(list(drop_line(line, "\n", lambda x,y: x==".")))
            
            spaces = " "*int(( ((row_max_chars * font_spacer_multiplier) - len(line)) / 2 ))
            line = spaces + line
            wrapped_text[l_num] = line

        # Convert wrapped text back into single strings
        fin_title = "\n".join(wrapped_title)
        fin_body = "\n".join(wrapped_text)

        # Draw text
        draw = ImageDraw.Draw(img_pil)
        
        # Title
        if stroke:
            draw.text((title_box_start_w-4, title_box_start_h), fin_title, font=title_font, fill = (255,255,255), spacing=line_spacing)
            draw.text((title_box_start_w+4, title_box_start_h), fin_title, font=title_font, fill = (255,255,255), spacing=line_spacing)
            draw.text((title_box_start_w, title_box_start_h-4), fin_title, font=title_font, fill = (255,255,255), spacing=line_spacing)
            draw.text((title_box_start_w, title_box_start_h+4), fin_title, font=title_font, fill = (255,255,255), spacing=line_spacing)
        draw.text((title_box_start_w, title_box_start_h), fin_title, font = title_font, fill = text_color, spacing=line_spacing)
        
        # Text
        if stroke:
            draw.text((text_box_start_w-4, text_box_start_h), fin_body, font=body_font, fill = (255,255,255), spacing=line_spacing)
            draw.text((text_box_start_w+4, text_box_start_h), fin_body, font=body_font, fill = (255,255,255), spacing=line_spacing)
            draw.text((text_box_start_w, text_box_start_h-4), fin_body, font=body_font, fill = (255,255,255), spacing=line_spacing)
            draw.text((text_box_start_w, text_box_start_h+4), fin_body, font=body_font, fill = (255,255,255), spacing=line_spacing)
        draw.text((text_box_start_w, text_box_start_h), fin_body, font = body_font, fill = text_color, spacing=line_spacing)
        
        
        # The card stats (if applicable)
        if is_creatures:
            if stroke:
                draw.text((stats_box_start_w-4, stats_box_start_h), stat_line, font=stats_font, fill = (255,255,255), spacing=line_spacing+15, align='left')
                draw.text((stats_box_start_w+6, stats_box_start_h), stat_line, font=stats_font, fill = (255,255,255), spacing=line_spacing+15, align='left')
                draw.text((stats_box_start_w, stats_box_start_h-4), stat_line, font=stats_font, fill = (255,255,255), spacing=line_spacing+15, align='left')
                draw.text((stats_box_start_w, stats_box_start_h+4), stat_line, font=stats_font, fill = (255,255,255), spacing=line_spacing+15, align='left')
            draw.text((stats_box_start_w, stats_box_start_h), stat_line, font=stats_font, fill = text_color, spacing=line_spacing+15, align='left')
            draw.text((stats_box_start_w + 2, stats_box_start_h), stat_line, font=stats_font, fill = text_color, spacing=line_spacing+15, align='left')
        
        # Convert to cv2 array
        img = np.asarray(img_pil)
        # Save card
        # Card name
        card_name = title.replace(" ", "")


        # Save
        cv2.imwrite(os.path.join(card_out,"{}.png".format(card_name)), img)
        print('Saved card {}.png'.format(card_name))
        print('Progress: {}%'.format((i / len(rows)) * 100))
        
    print('Finished {}'.format(csv_to_read))