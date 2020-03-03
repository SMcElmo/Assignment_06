#------------------------------------------#
# Title: Assignment06_Starter.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# SMcElmurry, 2020Mar01, Added additional functions, to remove need for code in main body
# TODone TODO - Use this comment to find completed/to be completed tasks with highlights
#------------------------------------------#

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.txt'  # data storage file
objFile = None  # file object


# -- PROCESSING -- #
class DataProcessor:
    # TODone add functions for processing here
    @staticmethod
    def find_Row(idToFind):
        """Function to locate an ID number in lstTbl. Deletes row if user is using delete option.

        Args:
            idToFind (int): Key ID to locate within lstTbl.

        Returns:
            idkFound (Boolean): True if the row exists in lstTbl.
        """
        intRowNr = -1
        idFound = False
        for row in lstTbl:
            intRowNr += 1
            if row['ID'] == idToFind:
                # For deletion
                if strChoice == "d":
                    del lstTbl[intRowNr]
                idFound = True
                break
        return idFound

    @staticmethod
    def check_Duplicate(dupID, dupTitle, dupArtist):
        """Function to check for duplicate entries in lstTbl.

        Args:
            dupID (int): CD ID to be checked.
            dupTitle (string): CD Title to be checked.
            dupArtist (string): CD Artist to be checked.

        Returns:
            idMatch (Boolean): True if the ID exists in lstTbl.
            dupAlbumArtist (Boolean): True if the album/artist pairing exists in lstTbl.
        """
        dupAlbumArtist = False
        idMatch = DataProcessor.find_Row(dupID) # Returns boolean
        for entryRow in lstTbl:
            if entryRow['Title'] == dupTitle and entryRow['Artist'] == dupArtist:
                dupAlbumArtist = True
                break
        return idMatch, dupAlbumArtist


class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        table.clear()  # this clears existing data and allows to load data from file
        objFile = open(file_name, 'r')
        for line in objFile:
            data = line.strip().split(',')
            dicRow = {'ID': int(data[0]), 'Title': data[1], 'Artist': data[2]}
            table.append(dicRow)
        objFile.close()

    @staticmethod
    def write_file(file_name, table):
        """Function to write data from lstTbl to a .txt file.

        Args:
            file_name (string): name of file used to read the data from.
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.
        """
        objFile = open(strFileName, 'w')
        for row in lstTbl:
            lstValues = list(row.values())
            lstValues[0] = str(lstValues[0])
            objFile.write(','.join(lstValues) + '\n')
        objFile.close()


# -- PRESENTATION (Input/Output) -- #
class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """
        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x
        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table

        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.
        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')

    # TODone add I/O functions as needed
    @staticmethod
    def int_check(typedInt):
        """
        Ensures an integer type is being passed by the user.

        Args:
                typedInt (string): User input to be checked and converted.

        Returns:
                (int): Variable initially entered as a string.
        """
        while type(typedInt) != int:
            strID = input("Enter an ID number: ").strip()
            try:
                return int(strID)
            except:
                print("Please enter a valid ID number")

    @staticmethod
    def add_CD(cdID, cdTitle, cdArtist):
        """Function that adds CDs to lstTbl

        Args:
            cdID (int): ID to be added to lstTbl
            cdTitle (string): Album title to be added to lstTbl
            cdArtist (string): Album artist to be added to lstTble

        Returns:
            None
        """
        dicRow = {'ID': cdID, 'Title': cdTitle, 'Artist': cdArtist}
        doubleID, repeatEntry = DataProcessor.check_Duplicate(cdID, cdTitle, cdArtist)
        if repeatEntry:
            print("Album and artist already in library.")
        elif doubleID:
            newID = IO.int_check(input('ID already exists. To add to library, enter a new ID: '))
            IO.add_CD(newID, cdTitle, cdArtist)
        else:
            lstTbl.append(dicRow)

    @staticmethod
    def CD_Entry():
        """
        Asks the user for information to add to their inventory

        Args:
                None

        Returns:
                Length 3 tuple with an integer, string, and string.
        """
        intID = IO.int_check("")
        strTitle = input('What is the CD\'s title? ').strip()
        stArtist = input('What is the Artist\'s name? ').strip()
        return intID, strTitle, stArtist


# 1. When program starts, read in the currently saved Inventory
FileProcessor.read_file(strFileName, lstTbl)

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break

    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            FileProcessor.read_file(strFileName, lstTbl)
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.

    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        # TODone move IO code into function
        intID, strTitle, stArtist = IO.CD_Entry()
        # 3.3.2 Add item to the table
        # TODone move processing code into function (Note: moved portion that adds CD to IO due to new user questions)
        DataProcessor.check_Duplicate(intID, strTitle, stArtist)
        IO.add_CD(intID, strTitle, stArtist)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.

    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.

    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        intIDDel = int(input('Which ID would you like to delete? ').strip())
        # 3.5.2 search thru table and delete CD
        # TODone move processing code into function
        blnCDRemoved = DataProcessor.find_Row(intIDDel)
        if blnCDRemoved:
            print('The CD was removed')
        else:
            print('Could not find this CD!')
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.

    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            # TODone move processing code into function
            FileProcessor.write_file(strFileName, lstTbl)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.

    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')




