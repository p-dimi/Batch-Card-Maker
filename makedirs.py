import os
dirs=['Cards','Csvs','CardPictures','Fonts','FinishedCards', 'Configs']
try:
    for d in dirs:
        os.mkdir(d)
except:
    print('Cannot create directories. Please manually create the following directories / folders:')
    for d in dirs:
        print(d)