# ------------------------------------------#
# Title: Assignment08.py
# Desc: Assignnment 08 - Working with classes
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, created file
# DBiesinger, 2030-Jan-01, added pseudocode to complete assignment 08
# PMoy, 2022-Aug-28, implemented assignment code
# ------------------------------------------#

"""A CD Inventory management system.

This module implements a CD inventory management system using a CD class.
"""

import pickle  # used to save/load binary files
import os.path  # used to check if file exists

# -- DATA -- #
strFileName = 'cdInventory.dat'
lstOfCDObjects = []


class CD:
    """Stores data about a CD.

    Properties
    ----------
        cd_id: (int) with CD ID
        cd_title: (str) with the title of the CD
        cd_artist: (str) with the artist of the CD

    Methods
    -------
        add_cd_to_table(newCD): -> None
        reset_cd_table(): -> None
        del_cd_from_table(idToDel): -> None
    """

    # -- Fields -- #
    __unique_ids = set()
    """set: Set of IDs of existing CDs"""

    # -- Constructor -- #
    def __init__(self, id, title, artist):
        """Construct a CD class instance.

        Parameters
        ----------
        id : int
            ID of the CD
        title : str
            Title of the CD
        artist : str
            Artist of the CD
        """
        self.__cd_id = id
        self.__cd_title = title
        self.__cd_artist = artist

    # -- Properties -- #
    @property
    def cd_id(self):
        """Return the ID of the CD.

        Returns
        -------
            int: ID of the CD
        """
        return self.__cd_id

    @property
    def cd_title(self):
        """Return the title of the CD.

        Returns
        -------
            str: CD title as a str
        """
        return self.__cd_title

    @property
    def cd_artist(self):
        """Return the artist of the CD.

        Returns
        -------
            str: Arist name as a str
        """
        return self.__cd_artist

    # -- Methods -- #
    def __str__(self):
        """Return the CD information as a str.

        Returns
        -------
            str: CD information as a str
        """
        return "{}\t{} (by: {})".format(
            self.cd_id, self.cd_title, self.cd_artist
        )

    @staticmethod
    def add_cd_to_table(newCD):
        """Add the CD object to the table after confirming unique ID.

        Args
        ----
            CD: instance of CD class

        Returns
        -------
            None
        """
        if newCD.cd_id in CD.__unique_ids:
            print("Found duplicate CD ID. Skipping CD: {}".format(newCD))
        else:
            lstOfCDObjects.append(newCD)
            CD.__unique_ids.add(newCD.cd_id)

    @staticmethod
    def reset_cd_table():
        """Clear the table of CD inventory.

        Args
        ----
            None

        Returns
        -------
            None
        """
        CD.__unique_ids.clear()
        lstOfCDObjects.clear()

    @staticmethod
    def checkID(strID):
        """Check an ID argument for validity.

        Args
        ----
            str: ID argument

        Returns
        -------
            boolean: True if ID is valid, and false otherwise
        """
        try:
            intID = int(strID)
            if intID < 1:
                print("ID must be greater than 0.")
                return False
            elif intID in CD.__unique_ids:
                print("This is a duplicate ID.")
                return False
            return True
        except ValueError:
            print("Invalid number {} entered.".format(strID))
            return False


# -- PROCESSING -- #


class FileIO:
    """Processes data to and from file.

    Properties:

    Methods
    -------
        save_inventory(file_name, lst_Inventory): -> None
        load_inventory(file_name): -> (a list of CD objects)

    """

    @staticmethod
    def load_inventory(file_name):
        """Load CD inventory from file to a list of dictionaries.

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table; one line in the file represents one dictionary
        row in table.

        Args
        ----
            file_name (string): name of file used to read the data from

        Returns
        -------
            None
        """
        if not os.path.isfile(file_name):
            open(file_name, 'a').close()  # create file if it does not exist
        else:
            with open(file_name, 'rb') as fileObj:
                fileContents = None
                try:
                    fileContents = pickle.load(fileObj)
                except Exception:
                    print('Error loading file!')
                    print('\nProgram started, but nothing was loaded...\n')
                if fileContents is not None:
                    CD.reset_cd_table()
                    for nextCD in fileContents:
                        CD.add_cd_to_table(nextCD)

    @staticmethod
    def save_inventory(file_name, table):
        """Write table data to file.

        Writes data from list of CD objects to file identified by file_name.

        Args
        ----
            file_name (string): name of file to write data to
            table (list of CD): List that holds the data during runtime

        Returns
        -------
            None
        """
        with open(file_name, 'wb') as fileObj:
            pickle.dump(table, fileObj)

# -- PRESENTATION (Input/Output) -- #


class IO:
    """Handle input and output for user choices.

    Methods
    -------
       save_inventory(file_name, lst_Inventory): -> None
       load_inventory(file_name): -> (a list of CD objects)
    """

    @staticmethod
    def print_menu():
        """Display a menu of choices to the user.

        Args
        ----
            None

        Returns
        -------
            None
        """
        print('Menu\n\n[l] Load Inventory from file\n[a] Add CD\n'
              '[i] Display Current Inventory\n[s] Save Inventory to file\n'
              '[x] Exit\n')

    @staticmethod
    def menu_choice():
        """Get user input for menu selection.

        Args
        ----
            None

        Returns
        -------
            choice (string): a lower case string of the users input out of the
            choices l, a, i, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 's', 'c', 'x']:
            choice = input(
                'Which operation would you like to perform? [l, a, i, s, c,'
                ' or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Display current inventory table.

        Args
        ----
            table (list of CD): List data structure (list of CD objects) that
            holds the data during runtime.

        Returns
        -------
            None

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for cdEntry in table:
            print(cdEntry)
        print('======================================')

    @staticmethod
    def get_new_CD():
        """Get user input for new CD.

        Args
        ----
            None

        Returns
        -------
            tuple: Tuple of strings representing ID, title, and artist

        """
        while True:
            strID = input('Enter ID: ').strip()
            if CD.checkID(strID) is True:
                break
        try:
            # This should be impossible to trigger since we checked with
            # checkID already, but include in case
            intID = int(strID)
        except ValueError:
            print("Could not convert {} to integer!".format(strID))
        strTitle = input('What is the CD\'s title? ').strip()
        strArtist = input('What is the Artist\'s name? ').strip()
        return intID, strTitle, strArtist

# -- Main Body of Script -- #


# Load data from file into a list of CD objects on script start
FileIO.load_inventory(strFileName)

# Display menu to user
while True:
    IO.print_menu()
    strChoice = IO.menu_choice()

    # Show user current inventory
    if strChoice == 'i':
        IO.show_inventory(lstOfCDObjects)
        continue

    # Let user add data to the inventory
    elif strChoice == 'a':
        CD.add_cd_to_table(CD(*IO.get_new_CD()))
        continue

    # Let user save inventory to file
    elif strChoice == 's':
        FileIO.save_inventory(strFileName, lstOfCDObjects)
        continue

    # Let user load inventory from file
    elif strChoice == 'l':
        FileIO.load_inventory(strFileName)
        continue

    # Let user exit program
    elif strChoice == 'x':
        break
