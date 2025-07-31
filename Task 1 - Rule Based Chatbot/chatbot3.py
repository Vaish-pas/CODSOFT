import tkinter as tk
from tkinter import scrolledtext
import re
import random
from datetime import datetime

# --- Chatbot Logic ---
responses = {
    r"(hello|hi|hey)": ["Hi there!", "Hello! 👋", "Hey! How can I help you?"],
    r"(thank you|thanks|thx|thank u)": ["You're welcome! 😊", "Glad I could help!", "No problem at all!", "Always here if you need me! 🤖"],
    r"(what.*you.*doing|doing)": ["Just chatting with you! 😊", "Thinking about the universe... and snacks 😋"],
    r"(how are you)": ["I'm doing great, thank you!", "All good! What about you?"],
    r"(your name|who are you)": ["I am Teddy 🤖", "You can call me Teddy!"],
    r"(i am.*sad|feeling.*down)": ["Oh no! I'm here for you ❤️", "Sending virtual hugs 🤗"],
    r"(what.*time|current time|time now)": [f"The time is {datetime.now().strftime('%H:%M:%S')} ⏰"],
    r"(help|support)": ["I can help with small talk and some answers! Just ask me something 💬"],
    r"(nice|good|great)": ["Thanks, Want to know something else?"],
    r"(ok|okay|fine|got it|alright|k)": ["Great! Let me know if you need anything else 😄", "Cool! ✅", "Alrighty!", "Sounds good! 👍"],
    r"(bye|exit|goodbye)": ["Goodbye! Take care! 👋", "See you soon!", "Exiting the chat now."]
}

default_responses = [
    "I'm not sure how to respond to that 🤔",
    "Can you rephrase it?",
    "I'm still learning. Please try something else."
]

def get_response(user_input):
    user_input = user_input.lower()
    for pattern, replies in responses.items():
        if re.search(pattern, user_input):
            return random.choice(replies)
    return random.choice(default_responses)

root = tk.Tk()
root.title("Parul's Teddy 🤖")
root.geometry("420x550")
root.config(bg="#E8F0FE")  # Soft background color

# Chat area
chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled', bg="#ffffff", font=("Calibri", 12), fg="#333333")
chat_area.pack(padx=12, pady=12, fill=tk.BOTH, expand=True)

# Entry field
entry_field = tk.Entry(root, font=("Calibri", 13), bg="#ffffff", fg="#000000")
entry_field.pack(padx=12, pady=(0, 8), fill=tk.X)
entry_field.insert(0, "Type your message here...")
entry_field.bind("<FocusIn>", lambda args: entry_field.delete('0', 'end'))

# Send message logic
def send_message():
    user_input = entry_field.get()
    if not user_input.strip():
        return

    chat_area.config(state='normal')
    chat_area.insert(tk.END, "👩 You: " + user_input + "\n")
    response = get_response(user_input)
    chat_area.insert(tk.END, "🤖 Teddy: " + response + "\n\n")
    chat_area.config(state='disabled')
    chat_area.yview(tk.END)

    entry_field.delete(0, tk.END)

    if re.search(r"(bye|exit|goodbye)", user_input.lower()):
        root.after(2000, root.destroy)

# Send button
send_button = tk.Button(root, text="Send", command=send_message,
                        font=("Calibri", 12), bg="#4CAF50", fg="white", relief=tk.RAISED, bd=2)
send_button.pack(padx=12, pady=(0, 15))

# Run the chatbot GUI
root.mainloop()