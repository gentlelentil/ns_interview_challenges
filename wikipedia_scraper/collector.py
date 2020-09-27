def program_start():
    import sqlite3
    import sys

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    dates = list(range(1, 32, 1))
    months_30_days = ['April', 'June', 'September', 'November']
    section_titles = ['Event', 'Birth', 'Death']

    conn = sqlite3.connect('calendar.db')
    cur = conn.cursor()
    try:
        cur.execute('CREATE TABLE history_calendar (id INT PRIMARY KEY, Month VARCHAR, Date INT, Year INT, Type VARCHAR, Occurrence VARCHAR)')
    except sqlite3.OperationalError:
        print("Table already exists!\n")
        userinput = input("Delete existing table? Y/N ")
        if userinput.lower() == 'y':
            cur.execute('DROP TABLE history_calendar')
            cur.execute('CREATE TABLE history_calendar (id INT PRIMARY KEY, Month VARCHAR, Date INT, Year INT, Type VARCHAR, Occurrence VARCHAR)')
        elif userinput.lower() == 'n':
            print("Keeping existing table, goodbye!")
            sys.exit()
    conn.commit()
    cur.close()
    conn.close()
    wikipedia_dates_to_SQL(months, dates, section_titles, months_30_days)

def insertIntoSQLdb(id, month, date, year, section_type, occurrence):
    import sqlite3
    try:
        conn = sqlite3.connect('calendar.db')
        cursor = conn.cursor()
        insertion = """INSERT INTO history_calendar 
                    (id, month, date, year, type, occurrence)
                    VALUES (?, ?, ?, ?, ?, ?)"""
        
        data = (id, month, date, year, section_type, occurrence)
        cursor.execute(insertion, data)
        conn.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Error occurred ", error)
    finally:
        if (conn):
            conn.close()


#BASE_URL = 'https://en.wikipedia.org/wiki/'


def wikipedia_dates_to_SQL(months, dates, section_titles, months_30_days):
    import re
    import wikipedia
    id = 0
    for M in months:
        if M == 'February':
            dates = list(range(1, 30, 1))
        if M in months_30_days:
            dates = list(range(1, 31, 1))
        for D in dates:
            web_link = str(M) + '_' + str(D)
            print("Parsing current date: ", str(M), " ", str(D))
            count = 0
            page = wikipedia.WikipediaPage(title=web_link)
            entire_page = page.content
            formated = entire_page.split('\n')
            for line in formated:
                events = re.search(r'^\S*\s(Events).*', line)
                births = re.search(r'^\S*\s(Births).*', line)
                deaths = re.search(r'^\S*\s(Deaths).*', line)
                if events:
                    count = 0
                if births:
                    count += 1
                if deaths:
                    count += 1
                match = re.search(r'^\s*(\d*)\s+(.)\s+(.*)', line)
                if match:
                    id += 1
                if not match:
                    continue
                month = M
                date = D
                year = match.group(1)
                occurrence = match.group(3)
                section_type = section_titles[count]
                insertIntoSQLdb(id, month, date, year, section_type, occurrence)

if __name__ == "__main__":
    print("COSI wikipedia calendar parser\n")
    print("As fulfilled by Nathaniel Smith\n")
    program_start()
