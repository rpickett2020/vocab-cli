# main.py

def show_menu():
    print("\nVocabulary App")
    print("1. Add a word")
    print("2. Quiz me")
    print("3. Exit")

def main():
    while True:
        show_menu()
        choice = input("choose an option (1-3): ")

        if choice == "1":
            print("Add a word feature coming soon...")
        elif choice == "2":
            print("Quiz feature coming soon...")
        elif choice =="3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__=="__main__":
    main()