
# Profil Software Recruitment Task

Hi! This is my solution for the task in the recruitment process for the position of Intern Python Developer at Profil Software.


## Background

I wrote a REPL program that allows user to make a reservation for a tennis court.

## How to run the program

1. Add the main directory to your PYTHONPATH
2. Run `python ./reservation_system/main.py`

## Program description

The program allows the user to perform the following actions. User can provide option as number (1, 2, etc) or text command (e.g. exit)

What do you want to do:
1) MAKE A RESERVATION
2) CANCEL A RESERVATION
3) PRINT SCHEDULE
4) SAVE SCHEDULE TO FILE
5) EXIT
6) LOAD RESERVATIONS FROM FILE

### 1. MAKE A RESERVATION:
User is prompted to give his full name, and date of a reservation
Making reservation will fail if:
* User has more than 2 reservations already this week
* Court is already reserved for the time user specified - in this case, the program will find the nearest free date and propose it to the user 
* The date user gives is less than one hour from now
* User try to make reservation before 08:00 or after 18:00 - Court is open from 08:00 to 18:00

For example:

    $ MAKE A RESERVATION 
    
    What's your Name?
    
    $ Maciej Lewandowski
    
    When would you like to book? DD.MM.YYYY HH:MM
    
    $ 24.03.2023 13:30

    How long would you like to book court?
    1  - 30 minutes
    2  - 60 minutes
    3  - 90 minutes

    Enter your option:
    
    2
    
    The time you chose is unavailable, would you like to make a reservation for 2023-03-24 14:00:00 instead? YES/NO:    
    
    $ YES
    
    Your reservation has been done and added to schedule


### 2. CANCEL A RESERVATION:
User can cancel a reservation by enter a full name and start date, but it fails if:

* There is no reservation for this user on specified date
* The date user gives is less than one hour from now

For example:

    $ CANCEL A RESERVATION 
    
    Please enter your full name:
    
    $ Mieczysław Okniński
    
    Please enter your reservation time DD.MM.YYYY HH:MM :
    
    $ 26.03.2023 13:30

    Your reservation has been deleted.
    

### 3. PRINT SCHEDULE:
The user is prompted to enter a start and end date, then the schedule for the specified period is printed in the following format

    $ PRINT SCHEDULE

    Time range you want to see
    From date DD.MM.YYYY HH:MM :

    $ 10.03.2023 10:00

    To date DD.MM.YYYY HH:MM :

    $ 30.03.2023 10:00

    Friday 17.03.2023:
    * Michał Popek 17.03.2023 14:00 - 17.03.2023 15:00 

    Sunday 19.03.2023:
    * Michał Popek 19.03.2023 14:00 - 19.03.2023 15:00 
    * Dawid Popek 19.03.2023 16:00 - 19.03.2023 17:00 
    
    Yesterday:
    * Michał Najman 20.03.2023 14:00 - 20.03.2023 15:00 
    * Olek Najman 20.03.2023 17:00 - 20.03.2023 19:00 
    
    Today:
    * Tadeusz Stockinger 21.03.2023 11:00 - 21.03.2023 12:30 
    * Marcin Wiśniewski 21.03.2023 17:00 - 21.03.2023 18:00 
    
    Tomorrow:
    * Robert Brzozowski 22.03.2023 12:30 - 22.03.2023 14:00 
    
    Friday 24.03.2023:
    * Norman Dudziuk 24.03.2023 16:30 - 24.03.2023 17:00 
    
    Saturday 25.03.2023:
    * Norman Dudziuk 25.03.2023 14:00 - 25.03.2023 14:30 
    
    Sunday 26.03.2023:
    * Paweł Gulczyński 26.03.2023 12:00 - 26.03.2023 13:30 
    * Mieczysław Okniński 26.03.2023 13:30 - 26.03.2023 14:00 
    
### 4. SAVE SCHEDULE TO FILE:
The user is prompted to enter the start date, end date, file format (csv or json) and file name, and then The schedule should be saved to a file in a format of the user's choice.

    $ SAVE SCHEDULE TO FILE

    From date DD.MM.YYYY HH:MM :

    $ 21.03.2023 10:00

    To date DD.MM.YYYY HH:MM :

    $ 24.03.2023 10:00

    Enter the name of save file:

    $ court_schedule

    Choose a file format: JSON or CSV:

    $ CSV

    The Schedule has been saved to court_schedule.CSV file

### 5. EXIT:
The user can quit the program.

    $ EXIT

    Thank you for your attention! Have a nice day!

### 6. LOAD SCHEDULE FROM FILE:
The user is prompted to enter the file name and file format (csv or json), then the reservations will be loaded. 
Example files (reservations.csv and reservations.json) are provided

    $ LOAD RESERVATIONS FROM FILE

    Enter the name of file:

    $ reservations.csv

    Choose a file format: JSON or CSV:

    $ csv

    Reservations have been loaded from reservations.csv file
