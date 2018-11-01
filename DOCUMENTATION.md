**The Best Game Store**



Project documentation
-----------------------

### 1. Team

* Valtteri Lipsanen
* Antero Vaarnamo
* Viljami Virolainen


### 2. Features

#### Minimum functional requirements
* Registration as player and developer
* Able to add games to their inventory and see list of games sales as Developer
* Able to play games, see high scores and record their scores as players

#### Authentication
* Login, logout and register (both as player or developer).
* Email validation
* Used Django auth

#### Basic player functionalities
* Buy games using mockup payment service
* Play games
* Players only able to play games they have purchaced
* Categories for games on the front page and on game detail pages

#### Basic developer functionalities
* Add a game (URL) and set price for that game and manage that game (remove, modify price)
* Basic game inventory and sales statistics (how many of the developers' games have been bought and when)
* Security restrictions, e.g. developers are only allowed to modify/add/etc. their own games, developer can only add games to their own inventory.

#### Game/service interaction
* Recording higscores when player presses the submit score button. Recorded to the players own highscores and global highscores.
* Messages from service to the game Implemented

#### Quality of work
* The quality of work is taken into account when implementing the service
* Purposeful use of framework
* Lot of usability testing

#### Non-functional requirements
* [Project plan](README.md)
* Usage of issues and meaningful commit messages

#### Save/load and resolution feature
* The service supports saving and loading games, and sets the resolution according to received settings from the game.


#### 3rd party login
* The service supports Google login both for player and user login.

#### Own game
* Developed a simple JavaScript game that communicates with the service (save, load, highscore)
* It is a simple math game where the player will win wizards equipment after answering questions right.
* Found in [core/static/own_game.html]()
* To use the game when adding the game the URL should be: https://thebestgamestore.herokuapp.com/static/own_game.html
* OR generally {{domain}}/static/own_game.html


#### Mobile friendly
* The service is responsive to screen sizes and mobile friendly
* Styling made with bootstrap and some customization


#### Social media sharing
* Possible to share individual games to Facebook
* Shows the games mame and image and description


### 3. The successes and problems
#### Successes
The management of the project was easier than at first thought. As most of our communication was done through the Whatsapp group, everything as documented easy to find afterwards. The Whatsapp group made it possible to have all information equally available for everyone, so the status of the project was constantly clear.

The webshop functionalities work really nicely. The shopping cart was not a requirement, but it makes the webshop more familiar to use, as well as makes it possible to buy multiple games at the same time. The Googles login also is a great success as it makes signing up and logging in really easy and smooth. Other aspects of the athentication features were too successful and a really good learning experience.

In total the whole project had an extremely good learning outcome. Our group has learnt more on this course than many other courses combined. Biggest learning outcomes were managing the groupwork, searching for solutions and of cource the expertise in web software development.


#### Problems
The game/service interactions were a problem for a long time when building the service. The jump from Python to JavaScript caused some recollection issues as it was some time since using it. Also the interaction between the JavaScript and the Python codes felt a bit problematic. The game/service interactions were successfully implemented in the end.

The testing part also proved to be very cumbersome. Testing all different scenarios when using the service was hard and the django tests were even harder. What is to be learnt from these experiences, a much more time should be allocated just for testing, and there should be lot of testing for different scenarios too for the complete service.

The final deployment of the application was really problematic as turning the debug setting off seemed to break a lot of things.

### 4. Division of work
The workload divided quite evenly between the group members. Different group members had different amount of time to wor on the project during different stages of the development. The activity of the group members can be seen from the projects commit history. The group only met in person once during the project, but the group had some meetings where two members were present. The first meeting was in the beginning of the project where the first areas of responsibility were discussed and agreed. Everyone was involved equally in the planning of the project and writing the project plan.

#### Antero
Antero's main responsibilities were the authentication features. This included the mandatory features as well as the 3rd party authentication. His other main responsibilities were the testing and the deployment in Heroku. Other work included styling and fixing bugs where ever they were found.

#### Valtteri
Valtteri's main responsibilities were the player and developer functionalities. He also implemented the webshops basic functionalities and the payment services. In the end of the project he also took care of the game/service interactions when Viljami could not finish them. Other work included implementig smaller features where ever they were needed, and testing and fixing bugs.

#### Viljami
Viljami's main responsibility was the game/service interactions. He managed to implement the mandatory functions, but beacuse of time management issues could not finish the whole work. He also took care of some styling issues of the service.


### 5. Instructions
#### Admin
##### [== Link to Heroku ==](https://thebestgamestore.herokuapp.com/)
The webshop needs a superuser to add categories for the games. The adding can be done from the djangos admin page by writing: "host"/admin.

After the categories are set, everything can be done with normal player and developer accounts. To sign up as developer or player follow the instructions on the page. As developer adding games is done from the "Add games" -tab. When adding games the image field needs an image url. The games in the users inventory ( both player and developer ), are found form the "My games" -tab. Logging out happens through dropdown menu under the username on the top right corner.

The categories are needed to be able to add games on the service. Therefore if for some reason there are no categories, you need to add one/some first. Having more than one category can show the functions of the front page better, as it is then possible to browse through the categories.   
