#!/usr/bin/python
from os import system
from time import sleep
from collections import defaultdict

def parse_tools():
    '''
    Get the black arch security tool list.
    If the file is not available, use pacman to
    generate a new one.
    '''
    try:
        blackarch_file = open("./blackarchtools")
    except FileNotFoundError:
        print("Black Arch tool list not found!")
        answer = input("Generate the tool list? (Y/N): ")
        if answer.lower() == 'y':
            system("sudo pacman -Sgg | grep blackarch > blackarchtools")
            blackarch_file = open("./blackarchtools")
        else:
            exit(0)
    ba_tools = sorted(blackarch_file.readlines())
    blackarch_file.close()
    ba_tools_dict = defaultdict(list)
    for tool in ba_tools:
        tool_category = tool.split(' ')[0].split('-')[-1]
        tool = tool.split(' ')[-1].strip()
        ba_tools_dict[tool_category].append(tool)
    i = 1
    tool_ids = {}
    for tool_cat in sorted(ba_tools_dict):
        tool_ids[i] = tool_cat
        i += 1
    return tool_ids, ba_tools_dict

def display_menu(tool_ids, ba_tools_dict):
    '''
    Use the tool_ids and ba_tools_dict to display the 
    menu and get a selection.
    '''
    while True:
        system("clear")
        print("Black Arch Browser")
        for tool_id in tool_ids:
            tool_cat = tool_ids[tool_id]
            if len(tool_cat) < 4:
                tool_cat = tool_cat.upper()
            else:
                tool_cat = tool_cat.capitalize()
            print("%d. %s" % (tool_id, tool_cat))
        print("0. Exit")
        choice = get_input(tool_ids, "Choose a category: ")
        if choice == False:
            return
        elif choice in tool_ids:
            display_sub_menu(tool_ids[choice], \
                             ba_tools_dict)

def display_sub_menu(category, ba_tools_dict):
    '''
    List all of the programs available for that category
    '''
    while True:
        system("clear")
        print("> %s" % category.capitalize())
        i = 0
        programs = []
        for program in sorted(ba_tools_dict[category]):
            print("%d. %s" % (i + 1, program))
            i += 1
            programs.append(program)
        print ("0. Go Back")
        choice = get_input(ba_tools_dict[category], \
                           "Choose a program: ")
        if choice == False:
            return
        elif choice in range(1, \
                             len(ba_tools_dict[category]) + 1): 
            execute_program(programs[choice - 1])

def get_input(option_list, message):
    '''
    Validate user input against the list of options.
    '''
    try:
        choice = int(input(message))
        options = range(1, len(option_list) + 1)
        if choice == 0:
            return False
        elif choice not in options or str(choice).isalpha():
            raise ValueError
        return choice
    except ValueError:
        print("Invalid Option")
        sleep(2)
        choice = ""

def execute_program(program):
    '''
    Get arguments for the selected program, if any, and append it to the
    program's name.
    '''
    print("Executing %s!" % program)
    program = program + ' ' + ' '.join(input("Arguments []: ").split(' '))
    system(program)
    exit(0)

if __name__=="__main__":
    tool_ids, ba_tools_dict = parse_tools()
    display_menu(tool_ids, ba_tools_dict)
