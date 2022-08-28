#Author : Barasa Michael Murunga
#Date : 30/07/2022 1701h

import json
import requests
import time
import pandas as pd

api = 'https://hnapi.hydronet.com/api/'

api_token = 'eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJZX2pEcG9IWUY3b3lxOWxsVVFoRTlqUTVwb0NfdkZ6MVQ0V19pTW00encwIn0.eyJleHAiOjE2NjY0MTYwMDgsImlhdCI6MTYzNDg4MDAwOCwianRpIjoiMWJlZmFkNzEtNWNlMy00NzZiLWJkNzEtOWI5ZGMxMjVjYWMxIiwiaXNzIjoiaHR0cHM6Ly9sb2dpbi5oeWRyb25ldC5jb20vYXV0aC9yZWFsbXMvaHlkcm9uZXQiLCJhdWQiOlsicG9ydGFsLmJhY2tlbmQuYXBpIiwiYWNjb3VudCJdLCJzdWIiOiI3Njg2ZmZiMy02NzRjLTRiMzEtYTdkZi0zYjNmZTJhYzQ4MTkiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJhcGktaHlkcm9uZXQtdHdpZ2EiLCJhY3IiOiIxIiwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwidW1hX2F1dGhvcml6YXRpb24iXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6ImVtYWlsIHByb2ZpbGUiLCJjbGllbnRJZCI6ImFwaS1oeWRyb25ldC10d2lnYSIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiY2xpZW50SG9zdCI6IjE5Mi4xNjguMTIuMTEyOjYwMTcyIiwicHJlZmVycmVkX3VzZXJuYW1lIjoic2VydmljZS1hY2NvdW50LWFwaS1oeWRyb25ldC10d2lnYSIsImNsaWVudEFkZHJlc3MiOiIxOTIuMTY4LjEyLjExMjo2MDE3MiJ9.p13NIP-_zpr7NOJ1i2r9JeIhBi-Sj_c1p12OWL7eENYWsSwOPohgjTrKsFLgtoJKqmmzUcFWnJ7xjs8VIq5iMYgCur0VPA0dTp3ngBCGUc_9hXjbhvPScMmJJ_cZQE-FCJYtuQubA2BFKwaaFYIj-7sp8Hr74ikfMRReRBUFt8C3LdowoJz5WJTpzbQvK_rFnGkscG8NxGziEghU5AchNliJhdqqUVVOcudN43i4rxK1kX2WPfYF_JlYQdYVs4DmqF8xoA4Lzay7QH3-0hEGvsspxRPMCGWcEkWKIrmXUwuzGhsVS1g-wO6pvA6-2XFEo3erHqtdeyN7DaMWPu4mtw'

api_header = {'content-type': 'application/json', 'Authorization': 'bearer ' + api_token}

def welcome():
    """welcomes the user to the program"""

    statement = """
     ====================================================================================
     
                            WELCOME TO GREENER AGRIC API
     
     ====================================================================================

     This program aims at making it easier for users to work on data rather than striving
     to retrieve the data.
     The program enables you to:
        1. Select a data source from available ones
        2. Select a location from available ones
        3. Select a variable from the available ones
        4. Write acquired data to a csv file
    The data is acquired from the hydronet server via the api

    NOTE : We have discovered that most of the errors related to json encoding that are 
        raised at runtime are caused by the response returned by request module being 
        with a status code other than 200.
    """
    print(statement)


def exit_program():
    """Allows for a smooth termination of the program"""

    choice = input("Are you sure you want to exit? (Y/N) : ")
    if choice == 'Y' or choice == 'y' or choice == 'yes' or choice == 'YES':
        print("Exiting program...")
        time.sleep(5)
        exit()
    else:
        main_menu()

def filters_config(selected_datasource_code = None, save = False):
    filters_dict = {} #holds the filters to be applied in the program

    def input_dates():
        start_date = input("Enter start date (format is strictly yyyymmdd): ")
        end_date = input("Enter stop date (format is strictly yyyymmdd): ")
        
        if len(start_date) != 8 and len(end_date) != 8:
            input_dates()
        else:
            return start_date, end_date

    start_date, end_date = input_dates()
    filters_dict.update({'StartDate' : start_date, 'EndDate' : end_date})

    variables_dict = {}
    variables = view_variables_measured(selected_datasource_code, True)

    print("===============================================================")
    for key, value in enumerate(variables):
        variables_dict.update({key : value})
        print("{:>4} {:<30}".format(key, value))

    try:
        choice = int(input("Select variable from available ones : (integers only) "))
        if choice in variables_dict.keys():
            filters_dict.update({"VariableCodes" : variables_dict.get(choice)})
        else:
            raise ValueError
    except:
        print("Invalid choice. Please try again (integers only) : ")
        time.sleep(0.8)
        filters(selected_datasource_code)

    if save:
        formats = {'html' : '.html', 'csv' : '.csv', 'excel' : '.xlsx'}
        print("Supported file formats include : ")
        formats_dict = {}
        for key, value in enumerate(formats.keys()):
            formats_dict.update({key : value})
            print("     {:<5} {:<10}".format(key, value))

        try:
            choice = int(input("Select desired file format (integers only) : "))
            if choice in formats_dict.keys():
                pass
            else:
                raise KeyError
        except:
            choice = 0 #default is the file format at index 0
        filters_dict.update({'FileFormat' : formats_dict.get(choice)})

    return filters_dict


def view_data(profile = None, selected_datasource_code = None, save = False):
    """
    Allows user to to access records for a particular location based on a selected 
    variable and display the data in table format; option to save the file available
        profile is the data related to the selected location
        selected_datasource_code is the source of the particular record
    """
    if profile and selected_datasource_code:
        filters = filters_config(selected_datasource_code, save)

        request_tahmo_data = {
            "Readers" : [{
                "DataSourceCode" : selected_datasource_code,
                "Settings" : {
                    "LocationCodes" : [profile.get('Code')],
                    "VariableCodes" : [filters.get("VariableCodes")],
                    "StartDate" : filters.get("StartDate") + "000000",
                    "EndDate" : filters.get("EndDate") + "000000",
                    "StructureType" : "TimeSeries",
                }
            }]
        }
        data_response = requests.post(api + 'data/get', headers = api_header, 
                data = json.dumps(request_tahmo_data))
        tahmo_data = json.loads(data_response.content.decode('utf-8-sig'))

        tahmo_data_df = pd.DataFrame(tahmo_data['Data'][0]['Data'])
        tahmo_data_df['DateTime'] = pd.to_datetime(tahmo_data_df['DateTime'])

        #modify the data frame
        del tahmo_data_df['Availability']
        del tahmo_data_df['Quality']
        tahmo_data_df = tahmo_data_df.rename(
                columns = {'Value' : filters.get('VariableCodes')})

        #add data to data frame
        tahmo_data_df['Code'] = profile.get('Code')
        tahmo_data_df['X'] = profile.get('X')
        tahmo_data_df['Y'] = profile.get('Y')
        tahmo_data_df['Location'] = profile.get('Name')

        #retrieve data yearly
        first_year = int(filters.get("StartDate")[:4])
        last_year = int(filters.get("EndDate")[:4])

        dataframes = []
        for year in range(first_year, last_year):
            #filter based on year
            df = tahmo_data_df[tahmo_data_df['DateTime'].dt.year == year]

            #perform calculations (monthly mean)
            df = df.groupby(df['DateTime'].dt.strftime("%-m"))[
                    filters.get("VariableCodes")].sum().reset_index()

            #add a new column called Year with current year as value
            df.insert(loc = 0, column = 'Year', value = year)
            #df = df.pivot(index = 'Year', columns = 'DateTime')

            dataframes.append(df)
            print(df)

        print(dataframes)
        tahmo_data_df = dataframes[0]
        for index in range(1, len(dataframes)):
            tahmo_data_df = pd.concat([tahmo_data_df, dataframes[index]], axis = 0)

        #add data to data frame
        print("columns")
        tahmo_data_df['Code'] = profile.get('Code')
        tahmo_data_df['X'] = profile.get('X')
        tahmo_data_df['Y'] = profile.get('Y')
        tahmo_data_df['Location'] = profile.get('Name')
        tahmo_data_df['Country'] = 'Kenya'

        print(tahmo_data_df)

        if save:
            if filters.get("FileFormat") == 'csv':
                tahmo_data_df.to_csv(profile.get('Name') + '.csv', index = False)
                print(f"Saving of data in {profile.get('Name')}.csv successful")

            elif filters.get("FileFormat") == 'html':
                tahmo_data_df.to_html(profile.get('Name') + '.html', index = False)
                print(f"Saving of data in {profile.get('Name')}.html successful")

            elif filters.get("FileFormat") == 'excel':
                tahmo_data_df.to_excel(profile.get('Name') + '.xlsx', index = False)
                print(f"Saving of data in {profile.get('Name')}.xlsx successful")

    print("\nYou will be redirected to the select location menu in 10 seconds...")
    time.sleep(10)
    select_location(selected_datasource_code)

def location_profile(location = None, selected_datasource_code = None):
    
    if location and selected_datasource_code:
        request_locations_tahmo = {"DataSourceCodes" : [selected_datasource_code]}
        locations_tahmo_response = requests.post(api + 'entity/locations/get',
            headers = api_header, data = json.dumps(request_locations_tahmo))
        locations_tahmo = locations_tahmo_response.json()

        profile = locations_tahmo.get("Locations").get(location)
        title = """
        =================================================================================
                                    LOCATION PROFILE
        =================================================================================
        """
        print(title)
        try:
            for key, value in profile.items():
                print("         {:<16}   {:<50}".format(key, value))
        except:
            pass

        menu = """
        =================================================================================
                                LOCATION LEVEL ACTION MENU
        =================================================================================
        Various actions can be carried out at the location level. You may decide to 
        display the data in table format, or write the data to a csv file for further 
        custom analysis. The following are some of the supported actions :

            1. VIEW DATA
            2. SAVE DATA TO FILE
            3. GO TO MAIN MENU
            4. EXIT PROGRAM
        """
        print(menu)
        try:
            choice = int(input("Select an item from the menu (integers only) : "))
            if choice == 1:
                view_data(profile, selected_datasource_code)

            elif choice == 2:
                view_data(profile, selected_datasource_code, True)

            elif choice == 3:
                main_menu()

            elif choice == 0:
                exit_program()
        except ValueError:
            print("Invalid choice. Please try again...")
            time.sleep(0.8)
            location_profile(location, selected_datasource_code)


def view_available_locations(selected_datasource_code = None, required = False):
    """Retrieves all available locations for the selected_datasource_code"""

    if selected_datasource_code:
        request_locations_tahmo = {"DataSourceCodes" : [selected_datasource_code]}
        locations_tahmo_response = requests.post(api + 'entity/locations/get',
            headers = api_header, data = json.dumps(request_locations_tahmo))
        locations_tahmo = locations_tahmo_response.json()
        
        if required:
            return locations_tahmo.get("Locations").keys()

        title= """
        =================================================================================
                                    AVAILABLE LOCATIONS
        =================================================================================
        """
        total_locations = len(locations_tahmo.get("Locations"))
        print(title, f"There are {total_locations} locations. These are : ")

        for location in locations_tahmo.get("Locations").keys():
            print("             ", location)


def select_location(selected_datasource_code = None):
    if selected_datasource_code:
        locations_dict = {} #holds the locations with an index
        choices = view_available_locations(selected_datasource_code, True)

        for key, value in enumerate(choices):
            locations_dict.update({key : value})
            print("     ", key, "   ", value)

        try:
            choice = int(input("Select a location from the menu (integers only) : "))
            if choice in locations_dict.keys():
                location_profile(locations_dict.get(choice), selected_datasource_code)
            else:
                raise ValueError

        except:
            print("Invalid choice. Please enter a valid choice...")
            time.sleep(0.8)
            select_location(selected_datasource_code)
            

def view_variables_measured(selected_datasource_code = None, required = False):
    if selected_datasource_code:
        request_variables_tahmo = {"DataSourceCodes" : [selected_datasource_code]}
        variables_tahmo_response = requests.post(api + 'entity/variables/get',
            headers = api_header, data = json.dumps(request_variables_tahmo))
        variables_tahmo = variables_tahmo_response.json()
        
        if required:
            return variables_tahmo.get("Variables").keys()

        title= """
        =================================================================================
                                    AVAILABLE VARIABLES
        =================================================================================
        """
        total_variables = len(variables_tahmo.get("Variables"))
        print(title, f"There are {total_variables} variables. These are : ")

        for variable in variables_tahmo.get("Variables").keys():
            print("             ", variable)
def bulk_data(selected_datasource_code = None, save = None):
    """Retrieves data for multiple variables from a selected data source and permits 
    saving into a file format of choice."""
    filters = bulk_filters(save)
    if save:
        filename = selected_datasource_code
        if filters.get("FileFormat") == 'html':
            data_df.to_html(filename  + ".html", index = False)
            print(f"Data saved successfully in file {filename}.html")
            time.sleep(0.8)

        elif filters.get("FileFormat") == 'excel':
            data_df.to_excel(filename  + ".xlsx", index = False)
            print(f"Data saved successfully in file {filename}.xlsx")
            time.sleep(0.8)

        
        elif filters.get("FileFormat") == 'csv':
            data_df.to_csv(filename  + ".csv", index = False)
            print(f"Data saved successfully in file {filename}.csv")
            time.sleep(0.8)



def data_source_profile(selected = None):
    if selected:
        menu = """
        =================================================================================
        """
        print(menu, f"      DATA SOURCE : {selected}", menu)

        menu = """
            1. VIEW LOCATIONS COVERED e.g., Ole Tipis Girls' Secondary School
            2. VIEW VARIABLES MEASURED e.g., rainfall, temperature
            3. SELECT A LOCATION
            4. GO TO MAIN MENU
            5. BULK OBTAIN DATA
            0. EXIT PROGRAM
        """
        print(menu)
        try:
            choice = int(input("Select a choice from the menu (only integers allowed) :"))
            if choice == 1:
                view_available_locations(selected)
            elif choice == 2:
                view_variables_measured(selected)
            elif choice == 3:
                select_location(selected)
            elif choice == 4:
                main_menu()

            elif choice == 5:
                bulk_data()

            elif choice == 0:
                exit_program()
        except ValueError:
            print("Invalid choice...please try again (integers only) :")
            time.sleep(0.8)
            data_source_profile(selected)

def select_data_source():
    data = """
    =====================================================================================
                                  SELECT DATA SOURCE
    =====================================================================================
    """
    print(data)

    #create an empty dictionary to hold the data sources
    data_sources = {}
    choices = view_data_sources(required = True)

    #print the data sources and add key, value dict to data_sources
    for value, data in enumerate(choices):
        print("     ", value, " ", data)
        data_sources.update({value : data})

    #select data source from available ones
    try:
        choice = int(input("Select data source from available ones (integers only) : "))
        if choice in data_sources.keys():
            data_source_profile(data_sources.get(choice))
        else:
            raise ValueError

    except:
        print("Ensure you select a valid choice from the menu...")
        time.sleep(1)
        select_data_source()


def view_data_sources(required = False):
    datasource_metadata = {}
    datasource_response = requests.post(api + 'entity/datasources/get', 
            headers=api_header,data=json.dumps(datasource_metadata))
    datasource_metadata = datasource_response.json()

    if required:
        return datasource_metadata.get("DataSources").keys()

    total_sources = len(datasource_metadata.get("DataSources"))
    print(f"There are a total of {total_sources} data sources currently available. These are : ")
    time.sleep(0.2)

    for item in datasource_metadata.get("DataSources").keys():
        #slow down display to allow user to see the number of stations available
        time.sleep(0.1)
        print(item)

    time.sleep(0.8)
    main_menu()

def main_menu():
    """Displays the main menu and allows user to select an option from it"""

    menu = """
    =====================================================================================
                                    MAIN MENU
    =====================================================================================

    The TWIGA api holds a lot of data. There are different data sources available, each 
    containing relevant data for TWIGA. Using the API one can request data of any of the 
    TWIGA data sources.

    1. VIEW AVAILABLE DATA SOURCES
    2. SELECT DATA SOURCE
    0. EXIT

    """
    print(menu)
    try:
        choice = int(input("Select an option from the menu (only integers allowed) : "))
        if choice == 1:
            view_data_sources()
        elif choice == 2:
            select_data_source()
        elif choice == 0:
            exit_program()
        else:
            main_menu()
    except ValueError:
        print("Only integer options are allowed...please try again")
        main_menu()


def main():
    welcome()
    main_menu()

if __name__ == '__main__':
    main()
