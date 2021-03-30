# CMPUT291-Proj1
This is CMPUT 291 project1

System Overview:
	This program is a python- language- based project implementing on sqlite3 database. The program is developed to serve the needs of typical government registration agents and traffic officer on a PC platform to view and update any individual personal records in the given database.
 Each agent or officer is assigned a unique username along with a password corresponding to the username,  the database can be accessed only when the input username and password matches. Once the user logins in, the user is able to access and modify the given database as the scope of accessing and modification is contingent on users’ type: registration agent or traffic officer. The user is encouraged to choose from multiple functionalities displayed, i.e., register a new birth record, process a bill of payments, etc., and the desired action will be performed by the program. 
The program also allows user to log out after user has finished all desired actions, guaranteeing the level of security of the program.


Design Features:
User Login In:
User is able to log in through the terminal page once they have entered the path of the proper database. The program prompts 2 line: “username: ” and “password: ” encouraging user to enter the username and password associated with the specific username. The password entered is not visible at the terminal page. Both username and password are specified to contain only digits, characters and underlines, to counter sql injection attack. The program checks the format then congruency of username and password. User can try entering up to 3 times, if all 3 trials fail, the system will automatically terminates, else the user is allowed to access the database.

Register a New Birth (user login in as agent):
	User is able to register a newly birthed child in the system. User will be required to enter the first and last name and the gender of the newborn, as well as optional birthday and birthplace. User will also be required to enter the first and last name of newborn’s parents, as well as optional birthday, birthplace, phone, and address (if no personal record exists). The system will automatically assign a unique registration number and a registration place same as user’s address.

Register a New Marriage (user login as agent):
User is able to register a new marriage in the system. User will be required to enter the first and last name of both partners, as well as optional birthday and birthplace, phone, and address (if no personal record exists). The system will automatically assign a unique registration number and a registration place same as user’s address.




Renew a Vehicle Registration (user login as agent):
User is able to renew a vehicle registration given a valid registration number. By renewing the record, the expiry date will be automatically set to the appropriate date, no other changes will be made.

Process a Bill of Sale (user login as agent):
User is able to process a bill of sale given the vin number of sold car, seller’s name, buyer’s name and new plate number. The system automatically set expiry date of the old registration to today and assign a new registration for the buyer.

Process a Payment (user login as agent):
User is able to process a new payment given ticket number being paid and payment amount. The system will check if the payment is a valid integer, as well as whether the total payment amount made to the tickets has exceeded total fine amount, and assign a new payment record if the payment is legal.

Get a Driver’s Abstract (user login as agent):
User is able to retrieve a driver’s abstract given driver’s name, the system will display the total number of tickets, demerit points and demerit notices associated with the specific driver within lifetime and past 2 years. If the user desired to check on abstract of tickets, they can enter y/Y follow the line Enter y/Y to see most 5 recent ticket, otherwise return to the main menu: ". The system also allows users to check more than 5 tickets by prompting a line “Enter y/Y to see more ticket, otherwise return to the main menu: " if the driver has more than 5 ticket records .

Issue a ticket (user login as officer):
	User is able to issue tickets providing registration number. After a registration number is entered, a result include person name, make, model, year, color of the registered car will be shown. Then  a question “proceed or not?” will be shown, and user can type proceed to ticket the car. Next, the user is required to input violation date, violation text and fine amount. If the violation date is none, then the system will set the violation date as today’s date. Finally, the ticket will be recorded in the database and a unique ticket number will be given by the system.

Find a Car Owner (user login as officer):
User is able to find the car owner by input one or more of make, model, year, color, plate number. Then the system will show how many matches found and return all the matches. If no matches found, “No matches found” will be shown. If there are less than 4 matches (one, two or three matches), the system will show results with more details includes make, model, year, color, plate, the latest registration date, the expiry date and the person's name on the latest registration. If there are 4 or more than 4 matches, the system will show every match only with make, model, year, color, plate. Then the system will ask the user to enter a vin number to see detailed record for this car or enter exit to go back to the operation step.


Testing Strategy:
	We have created our own database by modifying test data designed for assignment 2. All tests are done based on the newly created database. Each one of use tested their own codes individually and also help each other to test their codes, we generated a myriad of inputs which helped to define different error cases. 
	

Group Work Strategy:
We divided this project into three parts at first: Jxiang2 wrote login and question 1, 2 and 3. Ruohan2 wrote question 3,4,5 and 6, Thuang2 wrote question 7 and 8. Each one of us completed the first version of the code individually, then we had a meeting at the CSC to merge our code. We then found many errors and we kept working on it. After this meeting, we three continued to fix our codes and post the latest version in an online chat group. We all contributed in debugging and problem solving throughout the entire program. Ruohan2 spent about 1.5 days intermittently, Thuang2 spent about 10 hours, Jxiang2 spent about 12 hours on our codes.
