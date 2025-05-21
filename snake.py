import random
import os
import time
SCORE_FILE = "scores.txt"

# clear map
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# print map
def draw_map(size, snake, apple, score):
    clear()
    for i in range(size):
        row = ''
        for j in range(size):
            if (i, j) == snake[0]:
                row += '🟢'  # head
            elif (i, j) in snake:
                row += '🟩'  # body
            elif (i, j) == apple:
                row += '🍎'
            else:
                row += '⬛'
        print(row)
    print(f"\nScore: {score}")

# Get scores
def load_scores():
    scores = []
    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) == 2:
                    name, score = parts
                    scores.append((name, int(score)))
    return scores

#Save scores
def save_score(name, score):
    with open(SCORE_FILE, 'a') as f:
        f.write(f"{name},{score}\n")
# Show rank
def show_leaderboard():
    scores = load_scores()
    if not scores:
        print("No scores recorded yet.")
        return
    scores.sort(key=lambda x: x[1], reverse=True)
    print("\n🎖 Leaderboard:")
    for i, (name, score) in enumerate(scores[:10], start=1):
        print(f"{i}. {name} - {score}")

# Get direction
def get_direction(current_dir):
    valid = {'w': (-1, 0), 's': (1, 0), 'a': (0, -1), 'd': (0, 1)}
    while True:
        d = input("Move (w/a/s/d or e to exit): ").lower()
        if d == 'e':
            return 'exit'
        if d in valid:
            dx, dy = valid[d]
            # Not allow oposite
            if (dx, dy) != (-current_dir[0], -current_dir[1]):
                return dx, dy
            else:
                print("You can't move directly backwards!")
        else:
            print("Invalid input! Use w/a/s/d or e to exit.")

# Randomly generate apple
def spawn_apple(size, snake):
    empty = [(i, j) for i in range(size) for j in range(size) if (i, j) not in snake]
    return random.choice(empty)

def main():
    while True:
        print("\nWelcome to Snake Game!")
        print("1. Play as guest")
        print("2. Play with username")
        print("3. View leaderboard")
        print("4. Exit")

        choice = input("Choose an option (1/2/3/4): ").strip()

        if choice == '1':
            username = None
            break
        elif choice == '2':
            username = input("Enter your username: ").strip()
            if username:
                break
        elif choice == '3':
            show_leaderboard()
        elif choice == '4':
            print("Goodbye!")
            return
        else:
            print("Invalid choice. Try again.")


    while True:
        try:
            size = int(input("Enter map size (5-15): "))
            if 5 <= size <= 15:
                break
            else:
                print("❌ Invalid size! Please enter a number between 5 and 15.")
        except ValueError:
            print("❌ Invalid input! Please enter an integer.")
    snake = [(size // 2, size // 2)]
    direction = (0, 1)  # Go right at first
    apple = spawn_apple(size, snake)
    score = 0

    while True:
        draw_map(size, snake, apple, score)
        direction = get_direction(direction)

        if direction == 'exit':
            print("\n🚪 You exited the game.")
            break

        # Calculate the position of the snake again
        head_x, head_y = snake[0]
        dx, dy = direction
        new_head = (head_x + dx, head_y + dy)

        # Check knocking the wall
        if not (0 <= new_head[0] < size and 0 <= new_head[1] < size):
            print("\n💥 You hit the wall! Game Over.")
            break

        # Check self-collision
        if new_head in snake:
            print("\n💥 You ran into yourself! Game Over.")
            break

        # Move
        snake.insert(0, new_head)

        # Add apple or move
        if new_head == apple:
            score += 1
            apple = spawn_apple(size, snake)
        else:
            snake.pop()

        # Add latency
        time.sleep(0.05)

    print(f"\nFinal Score: {score}")
    if username:
        save_score(username, score)

    scores = load_scores()
    scores.append((username if username else "Guest", score))
    scores.sort(key=lambda x: x[1], reverse=True)

    rank = [i for i, (n, s) in enumerate(scores, start=1) if n == username and s == score]
    if username:
        if rank:
            print(f"\n🏆 {username}, your rank is #{rank[0]} out of {len(scores)-1} players.")
    else:
        print("\n(Guest scores are not recorded in the leaderboard.)")

if __name__ == "__main__":
    main()
