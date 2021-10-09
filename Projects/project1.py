import sqlite3
import csv
import sys


def main( filename, create_flag ):
    conn = sqlite3.connect(filename)
    curr = conn.cursor()
    print("Connection opened succesfully.\n")

    if create_flag:
            create_db( curr ) # create tables for the database
            insert_db( curr ) # insert data into the tables from csv files
    query_db( curr ) # Querying the database

    # commit the changes in database
    conn.commit()

    print("Records created successfully\n")

    # close the connection to database
    curr.close()
    conn.close()



def create_db( cursor ):
    print("Creating Table PLAYER... ")
    cursor.execute("""
    CREATE TABLE PLAYER(
    	Name		VARCHAR(20)		NOT NULL,
    	Position	VARCHAR(20)		NOT NULL,
    	Skill_level	INTEGER,
    	Salary		INTEGER,
    	Team_id		INTEGER,
    	Id		INTEGER,
    	City		VARCHAR(20),
    	PRIMARY KEY (Id),
    	FOREIGN KEY (Team_id)	REFERENCES TEAM (Id)
    	);
    """)
    print("Created table successfully.")

    print("Creating Table TEAM... ")
    cursor.execute("""
    CREATE TABLE TEAM(
    	Name		VARCHAR(20)		NOT NULL,
    	City		VARCHAR(20)		NOT NULL,
    	Coach		VARCHAR(20),
    	Id		INTEGER,
    	Captain		VARCHAR(20),
    	PRIMARY KEY (Name)
    	);
    """)
    print("Created table successfully.")

    print("Creating Table GAME... ")
    cursor.execute("""
    CREATE TABLE GAME(
    	Id		INTEGER			NOT NULL,
    	Host_team	INTEGER			NOT NULL,
    	Guest_team	INTEGER			NOT NULL,
    	H_T_Score	INTEGER			NOT NULL,
    	G_T_Score	INTEGER			NOT NULL,
    	Game_date	DATE,
    	PRIMARY KEY (Id),
    	FOREIGN KEY (Host_team) REFERENCES TEAM(Id),
    	FOREIGN KEY (Guest_team) REFERENCES TEAM(Id),
    	CHECK (Host_team <> Guest_team)
    	);
    """)
    print("Created table successfully.")

    print("Creating Table INJURY_RECORDS... ")
    cursor.execute("""
    CREATE TABLE INJURY_RECORDS(
    	Id		INTEGER			NOT NULL,
    	Inci_desc	VARCHAR(20)		NOT NULL,
    	Inj_desc	VARCHAR(20),
    	Player_id	INTEGER			NOT NULL,
    	FOREIGN KEY (Player_id)		REFERENCES PLAYER(Id)
    		ON DELETE SET DEFAULT	ON UPDATE CASCADE
    	);
    """)
    print("Created table successfully.")
    return cursor

def insert_db( cursor ):
    print("Inserting data into table...")
    # open the csv files
    team_data = open("../sql_practice/NHLTables/Team.csv")
    player_data = open("../sql_practice/NHLTables/Player.csv")
    game_data = open("../sql_practice/NHLTables/Game.csv")
    inj_data = open("../sql_practice/NHLTables/InjuryRecord.csv")

    # read the csv
    team_rows = csv.reader(team_data)
    player_rows = csv.reader(player_data)
    game_rows = csv.reader(game_data)
    inj_rows = csv.reader(inj_data)

    # skip the first row
    next(team_rows)
    next(player_rows)
    next(game_rows)
    next(inj_rows)

    #insert query for each table
    it_query = """INSERT INTO TEAM (Id, Name, City, Coach, Captain) VALUES (?,?,?,?,?);"""
    ip_query = """INSERT INTO PLAYER (Id, Team_id, Name, Position, Skill_level, Salary) VALUES (?,?,?,?,?,?);"""
    ig_query = """INSERT INTO GAME (Id, Host_team, Guest_team, H_T_Score, G_T_Score, Game_date) VALUES (?,?,?,?,?,?);"""
    iir_query = """INSERT INTO INJURY_RECORDS (Id, Player_id, Inci_desc, Inj_desc) VALUES (?,?,?,?);"""

    # insert data in bulk using iterator

    cursor.executemany(it_query, team_rows)
    cursor.executemany(ip_query, player_rows)
    cursor.executemany(ig_query, game_rows)
    cursor.executemany(iir_query, inj_rows)

    print("Insertion successful")

def query_db( cursor ):
    print("Querying from the database...")

    print("\n\nEnter a team name and retrieve all the names and salaries of all team members who play on that team.")
    cursor.execute( """
    SELECT PLAYER.Name, PLAYER.Salary
    FROM PLAYER, TEAM
    WHERE PLAYER.Team_id = TEAM.Id AND TEAM.Name = '''Chicago Blackhawks''';
    """)
    print_queries(["Name", "Salary"], cursor.fetchall() )

    print("\n\n4.Enter a player’s last name and first name and retrieve a list of their injuries.")
    cursor.execute( """
        SELECT INJURY_RECORDS.Id, INJURY_RECORDS.Inci_desc, INJURY_RECORDS.Inj_desc
        FROM INJURY_RECORDS, PLAYER
        WHERE PLAYER.Name = '''Dylan Coghlan''' AND PLAYER.Id = INJURY_RECORDS.Player_id;
    """)
    print_queries(["Id", "Inci_desc", "Inj_desc"], cursor.fetchall() )

    print("\n\n5.List all captains and the team they play for. ")
    cursor.execute( """
        SELECT TEAM.Captain, TEAM.Name as 'Team Name' FROM TEAM;
    """)
    print_queries(["Id", "Inci_desc", "Inj_desc"], cursor.fetchall() )

    print("\n\n6.For each team, retrieve the name and the number (count) of players on that team.Order the result by number of players in descending order.")
    cursor.execute( """
        SELECT Team.Name, COUNT(PLAYER.Name) AS 'Number_of_players'
        FROM PLAYER, TEAM
        WHERE TEAM.Id = PLAYER.Team_id
        GROUP BY TEAM.Name
        ORDER BY COUNT(PLAYER.Name) DESC;
    """)
    print_queries(["Name", "Number of Players"], cursor.fetchall() )

    print("\n\n7.For each host_team list the team’s name and the number of wins and losses of that team.")
    cursor.execute( """
        SELECT TEAM.Name,
          COUNT(
            CASE
              WHEN GAME.H_T_Score > GAME.G_T_Score THEN 1 END
              ) AS 'Number of wins',
          COUNT(
            CASE
            WHEN GAME.H_T_Score < GAME.G_T_Score THEN 1 END
              ) AS 'Number of losses'
        FROM TEAM, GAME
        WHERE TEAM.Id = GAME.Host_team
        GROUP BY TEAM.Name;
    """)
    print_queries(["Name", "Number of wins", "Number of losses"], cursor.fetchall() )

    print("\nAll queries successful.")

def print_queries( col_names, query_list ):
    for row in query_list:
        for i in range(len(row)):
            print("%s:%s" % (col_names[i], row[i]))
        print("")



if __name__ == "__main__":
    main( sys.argv[1], int(sys.argv[2]) )
