# poketrainersapi v1.10.1

 ## What is poketrainersapi? 

This python API build over Django and Djangorestframework 
allows the users to manage Pokemon Teams in a simple but useful way. 

 ## How to get started? 

First make sure you have alredy installed PostgreSQL, psycopg2 and djangorestframework libraries installed

Then you will need to create a new database into postgresql server with the name 'poketrainers_db'.
After that, restore this database from the 'db_backup' file which is stored in the project folder

then modify the settings.py file to match your postgresql server configuration ... 

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'poketrainers_db',  
        'USER': 'postgres',           
        'PASSWORD': 'postgres',       
        'HOST': 'localhost',          
        'PORT': '5432',              
    }
}

Once you have done all these steps you can go to manage.py file location in the console and run
the command

python manage.py runserver

which will start the django developments server.. 

if you see the mesage: 'starting development server at http://xxx.x.x.x:xxxx/'
then congratulations! It means you succesfully ran the API!!!

 ## USAGE

To understand how the API works, you should know that there are 3 classes, which are related to 
each other and that the API allows you to manage

    1. Trainers
    2. Teams
    3. Members 

you can add as many instances of these classes as you want, and all of them support 4 basic operations: 
    a. Create
    b. Retrieve
    c. Update
    d. Delete

One Trainer can have many pokemon teams, a team can have up to 6 members and a member can be part of more than one team. 

 - Trainers: 

To register a new trainer, you can send a POST request to this URL: http://xxx.x.x.x:xxxx/api/v1/trainers/
with the body request as follows: 

{
    "name":"Pokemon trainer No.1", 
    "age":"17", 
    "alias":"Poketrainer"
}

to update this register you will have to send a PUT request to http://xxx.x.x.x:xxxx/api/v1/trainers/1
(note that we have added the trainer id at the end of the URL )

overwriting all the fields in the existing register, for example: 

{
    "name":"Pokemon trainer New Name",  
    "age":"18",                         
    "alias":"Poketrainer"               
}

to delete this trainer register you can send a DELETE request to http://xxx.x.x.x:xxxx/api/v1/trainers/1

to retrieve the trainers data you can send a get request to : 

        http://xxx.x.x.x:xxxx/api/v1/trainers/  <--- this will retrieve all trainers data

or

        http://xxx.x.x.x:xxxx/api/v1/trainers/1 <--- will retrieve trainer with id=1 information

the above also can be done filtering by alias, for example: 

        http://xxx.x.x.x:xxxx/api/v1/trainers/Poketrainer <-- alias is case sensitive


This behavior also works on 

    http://xxx.x.x.x:xxxx/api/v1/teams/

and in 

    http://xxx.x.x.x:xxxx/api/v1/members/


to add a new team, for example you can send a POST request to http://xxx.x.x.x:xxxx/api/v1/teams/
with body as follows: 

{
    "name":"team_name", 
    "trainer_id":1
}

same for updating it 

and to add a new member into this team, send a POST request to http://xxx.x.x.x:xxxx/api/v1/members/
with the body as follows: 

{
    "pokemon_id":"25", 
    "team_id":1
}

this will add pikachu as member of the team with team_id = 1, which belongs to trainer with trainer_id = 1

to see all the pokemon and their pokemon_id, you can go to https://pokeapi.co/api/v2/pokemon

have Fun!




