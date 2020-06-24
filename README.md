# Q_Learning
Asquith Project - Teaching AI to play Snake using Q-Learning
============================================================
I had considered trying my hand at AI for a while, but the Asquith Project brought the motivation I needed (mostly in the form of a deadline) to finally give it a shot.
I spent a few weeks learning from a book: "Hands-On Machine Learning with Scikit-Learn, Keras & TensorFlow" - I know, catchy name right =)
Anyway so after learning about how to predict housing prices in California among other things, I decided the machine-learning approach I needed would be reinforcement learning.
So with that in mind I wrote up a *little* program for the game of Snake, and made it compatible with running at high speed & without visuals or human input.
After neatly packaging it into class systems, I could create game instances on command, and this is what I would use for the main program.


The main idea for this was to use Q-Learning, where the set of possible game states are gradually built up as they are experienced.
For each gamestate there would also be a set of all possible actions to be taken, and they would have WEIGHTS that showed the relative value the action cold bring.
(N.B: One of the prompts for the project was weight so I will settle for that as my slightly tenuous link to the target topic)
To consider each possible gamestate on its own would mean that it would take the AI a while before each state was visited enough times for meaningful values to be obtained, so a slight simplification was needed.
This came in the form of using the relative positions between the head and both fruit and tail end, drastically reducing the set size and making it more suitable for my uses.
To help me make this work I found an article on the topic of Q-Learning in games from Italo Lelis, and it was from there that I got the main equation for iterating my weights. Other sources include Stack Overflow, MIT's course on Artificial Intelligence by Patrick Winston, Code Bullet and others that have escaped my memory.
And I guess thats all I have to say...

After downloading the folder, code to run is Deep_Learn.py, and to see the game run you will need both Python 3.6+ and the pygame library.
If not, python is easy to install:
https://www.python.org/ftp/python/3.8.3/python-3.8.3-amd64.exe
And afterwards by going into your command line (WINDOWS+R, then type "cmd", then ENTER) and typing "pip install pygame" you can add the pygame library as well.

To edit game settings, open the GAME_STATS file, and details are visible inside the file
To run and play the game for yourself, running the GAME file will do the trick
To run the AI, run the Deep_Learn file and if you want to customise the settings of the AI you can either fiddle with the lines in the code for the specific weights and such, or for general aspects use the menu that comes when you run the file.
Bear in mind that the code stores its progress in the Qtable file, and this will only be used when the options asked for by the menu are all on their defaults, but you can feel free to change the GAME_STATS settings and the file will still be used as the qTable is still compatible
