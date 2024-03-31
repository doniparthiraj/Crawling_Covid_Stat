import os

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def execute_module(module, query, current_module):
    """Executes the specified make query in the given module directory."""
    clear_screen()
    if os.getcwd() != module:
        os.chdir(module)
    os.system(f"make {query}")
    
    input("\nPress Enter to continue...")
    clear_screen()
    os.chdir(current_module)

def main_menu():
    """Displays the main menu."""
    clear_screen()
    print("Welcome to Execute Queries of 3.1 and 3.2 Modules")
    print("1. Execute Module 3.1")
    print("2. Execute Module 3.2")
    print("3. Exit")

def module_31_menu(current_module):
    """Displays the menu for Module 3.1."""
    clear_screen()
    print("Module 3.1(Addressing Queries of Worldometer Covid Statistics")
    print("1. Execute Query 1")
    print("2. Execute Query 2")
    print("3. Back to Main Menu")
    return current_module

def module_32_menu(current_module):
    """Displays the menu for Module 3.2."""
    clear_screen()
    print("Module 3.2(Addressing Queries of Wikipedia Covid News)")
    print("1. Execute Query 3")
    print("2. Execute Query 4")
    print("3. Execute Query 5")
    print("4. Back to Main Menu")
    return current_module

# Main program
current_module = os.getcwd()
while True:
    main_menu()
    choice = input("\nEnter your choice: ")
    
    if choice == '1':
        current_module = module_31_menu(current_module)
        while True:
            module_choice = input("\nEnter your choice: ")
            if module_choice == '1':
                execute_module("Module3.1", "query1", current_module)
            elif module_choice == '2':
                execute_module("Module3.1", "query2", current_module)
            elif module_choice == '3':
                break
            else:
                print("Invalid choice! Please try again.")
        clear_screen()  # Clear the screen after returning from executing queries
    
    elif choice == '2':
        current_module = module_32_menu(current_module)
        while True:
            module_choice = input("\nEnter your choice: ")
            if module_choice == '1':
                execute_module("Module3.2-345", "query3", current_module)
            elif module_choice == '2':
                execute_module("Module3.2-345", "query4", current_module)
            elif module_choice == '3':
                execute_module("Module3.2-345", "query5", current_module)
            elif module_choice == '4':
                break
            else:
                print("Invalid choice! Please try again.")
        clear_screen()  # Clear the screen after returning from executing queries
    
    elif choice == '3':
        print("Exiting the program. Goodbye!")
        break
    
    else:
        print("Invalid choice! Please try again.")
