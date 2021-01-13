# Batch-Card-Maker
Make game cards in a batch from CSV! Perfect for rapid game prototyping for print or for Tabletop Simulator.

## Demonstration
[!View the Demo](https://youtu.be/8Xv3JhwMKsI)

## How to use:
You need to have Python 3.0 or higher and pip installed on your computer for this first.
Usually you will automatically install pip when you install Python.

Then you need to install the program's dependencies - you do this by running the INSTALL.bat file.
It will take a little time but once it's done you will be notified on the command prompt.

Next - run MAKEDIRS.bat to create the directories used by the program.
If it will not succeed in creating the folders - make them manually yourself.
Simply create the following new folders: **Cards, Csvs, CardPictures, Configs, Fonts, FinishedCards**
These are case sensitive.

Now you can batch make your cards!

## The program needs at least one .ttf font file inside its Fonts folder, at least one .csv file in its Csvs folder, and at least one .jpg or .png file in its Cards folder.

### How it works:
* The program reads a .png or .jpg image file from inside the Cards folder, that it will use as your card body.
* **Preferred card dimensions: 1400 pixels tall and 1000 pixels wide** but it can be any size you want it.
* The program reads a csv file you have in order to batch create all the cards in the csv file.
* The csv file should have a specific format:
** The first column is dedicated to the card names, the second and third columns are "Card type" columns, the fourth column is the card's text / description - everything else that's written in side it.
** The additional columns can be used to store additional info - such as Stats, if your card has any (such as HP, MP, etc), and the picture to insert into the card (if you have any pictures inside the CardPictures folder).
** If you don't want to use any card types - simply put minus signs (-) inside the second and third column fields on every row.

An example of how a cards spreadsheet should look:
![Spreadsheet Example](spreadsheet_example.png)

### Picture inside cards:
If your cards have pictures in them (for example, if it's a creature card and you want to put a picture of an Orc inside it), that picture must be placed inside the CardPictures folder, and the full name of the picture (for example: org.jpg) needs to be written in the csv in the row of the relevant card.
Refer to the spreadsheet example image above.

Note: The pictures which will be inside the cards have to be smaller than the cards. That is - they need to be contained inside the card. So if the picture is wider or taller than the card, the program will not be able to use it properly and will likely crash.
Just make sure the pictures are smaller than the cards.

### Stats inside cards:
This program by default has some built in stats for cards in it, from my own project that I made it for. However, it accepts custom stats as well. You will be prompted in the command line when you run the program, it will ask you all the necessary questions and instruct you how to answer.

## Running Card Maker
To run Card Maker, simply run the RUN.bat file.
It will start a command line session like this one:
![Spreadsheet Example](command_prompt.png)

And will walk you through the entire process.
You need to pay attention to what is written in the command prompt and what it asks you to input, but the process is very simple.
#### Example:
Command prompt: "You have the following font files available: (0): Arial.ttf, (1): ComicSans.ttf. Which font do you want to use?"
You: Typing in the number "0" and pressing Enter

That's how it goes.

## Configurations:
Once you have gone through the command prompt questions, you will get to the main meat of the program - the visual card configuration.
Here you will have two windows open - the card preview, and the card settings. You can play around with the various trackbars in the card settings window to get to the exact way you want your card to look.

The trackbars have their titles next to them which tell you what they do.
Play around with them to figure it out if they aren't obvious.

Once you're finished setting up your card look, you can press and hold "C" to batch create all the cards from the csv without saving the configurations, or if you want to use the same visual configurations again - press and hold "S" instead to save a config file.
You will need to input the name of the file in the command line that the program is running in, and then press Enter.
It will then save the configurations, and will ask you whether to load them the next time you run the program.

It won't save ALL configurations, only the primary visual ones, and will still ask you about other things like the font to use.
