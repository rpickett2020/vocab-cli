# main.py

import os
import random
import json
from pathlib import Path

# -------------- Persistence config ---------------
DATA_FILE = Path("vocab.json")

# ------------- In-memory state --------------
vocabulary = []    #empty list to be filled with words                                

session_stats = {
    "asked": 0, "correct": 0, "streak": 0, "best_streak": 0, 
    "per_word": {}   # word -> {"asked": int, "correct": int}
}

########################################################################
# ----------------------- Persistence helpers ---------------------
#######################################################################

def load_words():
    """Load vocabulary list from JSON file. Returns a list."""
    if not DATA_FILE.exists():
        return[]
    try:
        import json
        with DATA_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
        # basic validation: list of dicts with word/meaning
        cleaned = []
        for item in data if isinstance(data, list) else []:
            if isinstance(item, dict) and "word" in item and "meaning" in item:
                w = str(item["word"]).strip()
                m = str(item["meaning"]).strip()
                if w and m:
                    cleaned.append({"word": w, "meaning": m})
        return cleaned
    except Exception as e:
        print(f"⚠️  Could not read {DATA_FILE}: {e}")
        return []

#-----------------------------------------------------------------------

def save_words(words):
    """Save vocabulary list to JSON (pretty-printed)."""
    try:
        with DATA_FILE.open("w", encoding="utf-8") as f:
            json.dump(words, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"⚠️  Could not save to {DATA_FILE}: {e}")


########################################################################
# ------------------ UI Helpers ----------------------------
########################################################################

def clear_screen():       #clears command screen 
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

#---------------------------------------------------------------

def show_menu():          #start up menu
    show_title("Vocabulary App")
    print("1. Add a word")
    print("2. Quiz me")
    print("3. View words")
    print("4. View stats")
    print("5. Exit")
    print("6. Save now")   # optional manual save
    print("=" * 30)

#-------------------------------------------------------------------

def show_title(name):      #displays title for each option
    width = 30
    print("=" * width)
    print(name.center(width))
    print("=" * width)

#######################################################################
#------------------- Stats helpers --------------------------------
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
#------------------------- Features ----------------------------
#####################################################################

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

#-------------------------------------------------------------------------------

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

#----------------------------------------------------------------------------------

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

#----------------------------------------------------------------------

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

#-------------------------------------------------------------------

def debug_storage():            # checks if save file exists, outputs its location if so
    print(f"📁 Using file: {DATA_FILE.resolve()}")
    print(f"   Exists? {DATA_FILE.exists()}")
    if DATA_FILE.exists():
        print(f"   Size: {DATA_FILE.stat().st_size} bytes")
    
    
    with open("vocab.json", "r", encoding="utf-8") as f:
        words = json.load(f)

    print(words)   # shows the list of dicts

###########################################################
###########################################################

"""def choose_word_index():
    #Show numbered list and return a 0-based index, or None to cancel.
    if not vocabulary:         # empty list case
        print("No words yet.")
        return None
    show_title("Vocabulary List")
    for i, e in enumerate(vocabulary, start=1):
        print(f"{i}. {e['word']} - {e['meaning']}")
    raw = input("\nEnter number to select (Press Enter to cancel): ").strip()
    if not raw:
        return None
    if not raw.isdigit():
        print("Please enter a valid number.")
        return None
    idx = int(raw) - 1
    if not (0 <= idx < len(vocabulary)):
        print("Number out of range.")
        return None
    return idx"""



###############################################################
###############################################################

##########################################################################
#------------------------ App Loop ------------------------------------
########################################################################

def main():
    
    global vocabulary
    vocabulary = load_words()
    
    while True:
        clear_screen()
        show_menu()
        choice = input("Choose an option (1-6): ").strip()

        if choice == "0":
            debug_storage()
            input("Debugging")


        elif choice == "1":
            clear_screen()
            show_title("Add a Word")
            add_word()
        elif choice == "2":
            clear_screen()
            show_title("Quiz Time!")
            quiz()
        elif choice == "3":
            clear_screen()
            view_words()
        elif choice == "4":
            clear_screen()
            view_stats()
        elif choice =="5":
            clear_screen()
            show_title("Saving")
            save_words(vocabulary)  # save words on exit
            show_title("Thank You!")
            input("Goodbye!")
            clear_screen()
            break
        elif choice =="6":
            clear_screen()
            save_words(vocabulary)
            input(f"💾 Saved to {DATA_FILE.resolve()}\n")
        else:
            clear_screen()
            show_title("Invalid Choice")
            input("Invalid choice. Please enter value from 1-6.\nPress Enter to return to menu...")
            clear_screen()

if __name__=="__main__":
    
    
    try:
        main()
    except KeyboardInterrupt: 
        input("\nExiting...saving words.")
        save_words(vocabulary)