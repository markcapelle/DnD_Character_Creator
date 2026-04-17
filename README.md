GitHub Repository: https://github.com/markcapelle/DnD_Character_Creator 

Render Deployment: https://dnd-character-creator-693k.onrender.com/ 

Dungeons and Dragons (5th Edition) Character Creator

Project Description

The character creator will help newcomers to Dungeons and Dragons quickly and easily build their first character to jump in and play with a group, or even be used by seasoned players to test startup character stats and combinations.
The user will be able to quickly create a level 1 character and be presented a standard, easy to read character sheet along with a curated spellbook for spellcasters and a dice box app to get started.

Features

Character Sheet Generator
Users can explore multiple character race and class options, and based on selections see exactly which abilities their points allocation should focus on, as well as peruse the traits that will be available to them. Instead of having to spend a long time flicking back and forth through a rulebook, everything pertinent will be presented in easily digestible segments, especially for newcomers to the tabletop game.

Dice Box

For prospecting players who just want to try the game out and haven’t invested in their own dice yet, the random number generator using some simple javascript allows users to simulate multi sided dice, from the unusual d4 to the complicated d100 and the bread-and-butter Dungeons and Dragons d20. Additionally, the user will be able to roll multiples of the same dice all at once.

Spellbook

Instead of having to search through the veritable tome for that one spell a user wants to try out, the provided spellbook has some starter spells that are easily accessed through a button click and like all other aspects of the app, can easily be expanded and scaled.

Variable tracker

On their character sheet, the user will have the interactivity to tick off spell slots as they are used, hit dice as they are rolled, and even keep track of death save rolls and managed hit points with just a button click.

Scalability

This iteration is the first working version of the app. Through the use of libraries, the provided race selections, class selections and even the spellbooks and their contents can be expanded easily.

Design

HTML Pages

(‘/’) Abilities.html
Landing page, the player inputs the character name, selects their race and class, which highlights the abilities they’ll get bonuses from because of selected race, and which abilities are key for their chosen class. The player doles out skill points into their abilities from a central pool.
Next button locks in the selections and moves on to the next step.

(‘skills’) Skills.html
The player selects what skills they are proficient in, with the selections capable of being selected based on their chosen class.

(‘background’) Background.html
The player selects their background traits, which will affect skill proficiencies.

(‘index’) Index.html
The completed character page is displayed with some navigation buttons for the rest of the app.
Button for dice.
Button for spellbook and display spellcasting stats if the chosen class is a spellcaster.
Reset button that resets the session and goes back to Abilities.html

(‘dice’) Dice.html
Popup window with a javascript dice roller. Use 2d CSS animations to make animated dice appear. Have a selection for which dice to use (d4, d6, d20, etc) and a selection for how many of the dice are rolled in one go.

(‘spellbook’) Spellbook.html
Popup window revealing the spells for spellcaster class, each spell neatly formatted on its own page.

Colours

The colours used were selected from the classing DnD colour palate seen on most traditional character sheets. It gives a weathered paper, scroll kind of look. Experiments were done with some texture files, but it made some of the text harder to read so a gradient was used to make the background colours less monotonous.

Fonts

A variant of Times New Roman was used. It’s a simple, readable font and gives it a slightly medieval feel in keeping with the general fantasy aesthetic.

Audio

Simple dice rolls in a wooden box were recorded as well as a few page flicks and pen scribbles. The best of each was selected and converted into mp3 files to be used in the app to invoke the classic pen and paper tabletop game feel.

Development

Project Planning

The project must be scalable and expandable. More race options, class options and other features should be easy to add later.
Races and Classes should be libraries that can be expanded; more entries added.
A variable in each class should set ‘spellcaster’ to true or false. On false, the spellcaster part of the character sheet can be hidden. On true, the stats are calculated and displayed.
Each spellcaster has their own Spellbook library that is referred to/attached.

Wireframe

The design is completely derived from a DnD character sheet. The main structure is to box stats into their own areas in a way so that the most important information is easy to see, read and is grouped close together so the user doesn’t have to peruse the entire sheet to find what they’re looking for.
 

Python (app.py)

All of the stats, character variables and major character calculations are stored in app.py. Main character variables, such as health, how may spell slots, death saving throws, etc, are controlled on the front end using javascript, but the values are fed back into python so that the values could be passed off to a database or other sort of save system in future iterations.

Functions

A number of functions simply control the increase and decrease of certain stats as the player makes their choices and commits the values to memory until the character sheet is built properly in build_character_sheet().
Here, all of the stats are calculated and built into a structure that can be recalled using jinja with the ‘sheet’ variable.

Routes

The most important routes save user selections on pages to the session, so that the final step everything can be saved into the user’s character sheet using the build character sheet function.
 
Libraries

Libraries store the core data of the various player options there are.
RACES, CLASSES and SPELLBOOKS are all stored in their own librarys. Races and Classes can be expanded, and spellcaster variables can point to new and specific Spellbooks that can be created, and also expanded.
A library stores all of the skills, along with their associated ability so that the right modifier can be added on the final character sheet.

CSS

Style.css

All the general style data is used across the board in style.css, specifically written to use flex for responsive design and an aesthetic derived from DnD character sheets.

Dice_animations.css

Used exclusively on the dice hub dice.html. It handles the 2d animations that display the dice results.

Javascript

Buttons.js

All the back and forth navigation buttons code is implemented in this js file in order to keep it separate and easier to troubleshoot.

Dice.js

The dice rolling javascript is kept in a separate javascript and just uses a couple of functions to generate random numbers depending on how many sided dice is selected. And the output is arrayed when multiple dice are requested.

Audio.js

This js file exclusively loads the mp3 files and has a function that plays audio from the beginning. Additional functions call the main function, feeding it the required variable for the specific sound required.

Challenges Faced

Most of the challenges came from expansion of features. The whole app requires a sense of modularity so that libraries can be expanded in the future. 
The app started small and grew in iterations. But each iteration had to be added carefully so that the modularity could be maintained. Hard coding everything would have been much easier. But now, because I stuck with it, we can expand the content available within the final app just by adding more basic data to the available libraries – it’s just a lot of typing.
All that, and spelling errors. Referring to library variables later on, miss-spelling them and then wondering why everything has stopped working.

Sources

All of the character creation algorithms, character classes, races, rules, dice designs and equipment are derived from the contents of the Dungeons and Dragons 5th Edition Player’s Handbook by Wizards of the Coast.

Deployed site

This site has been deployed to GitHub Pages at the URL below:
https://markcapelle.github.io/DnD_Character_Creator/ 
