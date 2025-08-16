# main.py

import os
import random

vocabulary = []    #empty list to be filled with words                                

session_stats = {
    "asked": 0, "correct": 0, "streak": 0, "best_streak": 0, 
    "per_word": {}   # word -> {"asked": int, "correct": int}
}

########################################################################

def record_result(word, is_correct):
    # update totals
    session_stats["asked"] += 1
    if is_correct:
        session_stats["correct"] += 1
        session_stats["streak"] += 1
        session_stats["best_streak"] = max(session_stats["best_streak"], session_stats["streak"])
    else:
        session_stats["streak"] = 0

    # update per-word
    stats = session_stats["per_word"].setdefault(word.lower(), {"asked": 0, "correct": 0})
    stats["asked"] += 1
    if is_correct:
        stats["correct"] += 1

#######################################################################

def view_stats():
    show_title("Session Stats")
    a = session_stats["asked"]
    c = session_stats["correct"]
    pct = (c*100 // a) if a else 0
    print(f"Questions answered: {a}")
    print(f"Correct answers:    {c}")
    print(f"Accuracy:           {pct}%")
    print(f"Current streak:     {session_stats['streak']}")
    print(f"Best streak:        {session_stats['best_streak']}\n")

    if not session_stats["per_word"]:
        print("No per-word data yet.")
    else: 
        print("Per word performance:")
        for w, s in sorted(session_stats['per_word'].items()):
            wpct = (s["correct"] * 100 // s["asked"]) if s["asked"] else 0
            print(f"- {w}: {s['correct']}/{s['asked']} ({wpct}%)")
    input("\nPress Enter to return...")
    clear_screen()

########################################################################

def clear_screen():       #clears command screen 
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

#######################################################################

def show_menu():          #start up menu
    show_title("Vocabulary App")
    print("1. Add a word")
    print("2. Quiz me")
    print("3. View words")
    print("4. View stats")
    print("5. Exit")
    print("=" * 30)

##########################################################################

def show_title(name):      #displays title for each option
    width = 30
    print("=" * width)
    print(name.center(width))
    print("=" * width)
    
##########################################################################

def add_word():        #function to add word to vocabulary list
    word = input("Enter the new word: ").strip()
    if not word:
        print("⚠️  Word cannot be empty.\n")
        return
    
    for entry in vocabulary:
        if entry["word"].lower() == word.lower():
            print(f"⚠️  '{word}' is already in your list.\n")
            add_word()
            return
    
    meaning = input(f"Enter the meaning of '{word}': ").strip()
    if not meaning:
        print("⚠️  Meaning cannot be empty.\n")
        return
    vocabulary.append({ "word": word, "meaning": meaning})

    print(f"✅ '{word}' added successfully!\n")
    add_word()
    clear_screen()

#########################################################################

def view_words():
    if not vocabulary:
        input("📭 No words added yet.\nPress Enter to return to menu...")
        clear_screen()
        return
    
    show_title("Vocabulary List")
    for idx, entry in enumerate(vocabulary, start=1):
        print(f"{idx}. {entry['word']} — {entry['meaning']}")
    
    input("---Press Enter to return to menu---") # trailing newline for spacing
    clear_screen()

#####################################################################

def quiz(): # basic quiz to ask for meanings of words
    if not vocabulary:
        input("📭 No words to quiz. Add some first!\n")
        clear_screen()
        return
    
    # work on a shuffled copy so list order doesn't change
    items = vocabulary[:]
    random.shuffle(items)

    score = 0
    total = len(items)

    #show_title("Quiz Time!")
    #print("\n=== Quiz time! ===")
    print("Type the meaning. Press Enter on a blank line to quit early.\n")
    for i, entry in enumerate(items, start=1):
        w = entry["word"]
        correct = entry["meaning"]

        print(f"Q{i}/{total}: What does'{w}' mean")
        ans = input(">").strip()

        if ans == "":  # early exit
            print("\nExiting quiz...")
            total = i-1
            break
        
        is_correct = (ans.lower().strip() == correct.lower().strip())
        record_result(w, is_correct)

        if is_correct:
            print("✓ Correct!\n")
            score += 1
        else:
            print(f"✗ Not quite. Correct answer: {correct}\n")

    if total == 0:
        print("No questions answered.")
    else:
        pct = round(score * 100 / total)
        print(f"Your score: {score}/{total} ({pct}%)")
    input("\nPress Enter to return to menu...")
    clear_screen()


##########################################################################

def main():
    while True:
        clear_screen()
        show_menu()
        choice = input("Choose an option (1-5): ")

        if choice == "1":
            clear_screen()
            show_title("Add a Word")
            add_word()
        elif choice == "2":
            clear_screen()
            show_title("Quiz Time!")
            #input("Starting Quiz...")
            quiz()
        elif choice == "3":
            clear_screen()
            view_words()
        elif choice == "4":
            clear_screen()
            view_stats()
        elif choice =="5":
            clear_screen()
            show_title("Goodbye!")
            input("Press Enter to exit app")
            clear_screen()
            break
        else:
            clear_screen()
            show_title("Invalid Choice")
            input("Invalid choice. Please enter value from 1-5.\nPress Enter to return to menu...")
            clear_screen()

if __name__=="__main__":
    main() 