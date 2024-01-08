# Daiyron Williams
# 21 December 2023
# This code is for a monopoly game

import tkinter as tk
from tkinter import messagebox
import random

class Player:
    def __init__(self, name):
        self.name = name
        self.position = 0
        self.money = 1500
        self.properties = []

    def __str__(self):
        return f"{self.name} - Position: {self.position}, Money: ${self.money}"

class Property:
    def __init__(self, name, cost, rent):
        self.name = name
        self.cost = cost
        self.owner = None
        self.rent = rent

    def __str__(self):
        return f"{self.name} - Cost: ${self.cost}, Rent: ${self.rent}"

class MonopolyApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Monopoly Game")

        self.players = [Player("Player 1"), Player("Player 2")]
        self.current_player = 0

        self.board = [Property("Go", 0, 0), Property("Mediterranean Avenue", 60, 2),
                      Property("Baltic Avenue", 60, 4), Property("Oriental Avenue", 100, 6),
                      Property("Vermont Avenue", 100, 6), Property("Connecticut Avenue", 120, 8)]

        self.create_widgets()

    def create_widgets(self):
        # Create and configure GUI elements
        self.label = tk.Label(self.master, text="Monopoly Game", font=("Helvetica", 16))
        self.label.pack(pady=10)

        self.roll_button = tk.Button(self.master, text="Roll Dice", command=self.play_turn)
        self.roll_button.pack()

        self.text_display = tk.Text(self.master, height=15, width=50)
        self.text_display.pack()

        # Display initial player and board information
        self.display_players()
        self.display_board()

    def display_players(self):
        # Display player information in the text widget
        self.text_display.insert(tk.END, "\n----- Players -----\n")
        for player in self.players:
            self.text_display.insert(tk.END, str(player) + "\n")
        self.text_display.insert(tk.END, "-------------------\n")

    def display_board(self):
        # Display board information in the text widget
        self.text_display.insert(tk.END, "\n----- Monopoly Board -----\n")
        for prop in self.board:
            self.text_display.insert(tk.END, str(prop) + "\n")
        self.text_display.insert(tk.END, "---------------------------\n")

    def roll_dice(self):
        # Simulate rolling a six-sided die
        return random.randint(1, 6)

    def play_turn(self):
        # Handle a player's turn
        dice_roll = self.roll_dice()
        self.text_display.insert(tk.END, f"{self.players[self.current_player].name} rolled a {dice_roll}\n")

        self.players[self.current_player].position = (self.players[self.current_player].position + dice_roll) % len(self.board)
        current_property = self.board[self.players[self.current_player].position]

        self.text_display.insert(tk.END, f"{self.players[self.current_player].name} landed on {current_property.name}\n")

        # Handle property logic in a separate method
        self.handle_property_logic(current_property)

        self.display_players()
        self.display_board()

        # Switch to the next player
        self.current_player = (self.current_player + 1) % len(self.players)

        # Check for game over after each turn
        if all(player.money <= 0 for player in self.players):
            self.text_display.insert(tk.END, "Game Over: All players are out of money!\n")
            self.roll_button.config(state=tk.DISABLED)

    def handle_property_logic(self, current_property):
        # Handle logic related to landing on a property
        if isinstance(current_property, Property):
            if current_property.owner is None:
                response = messagebox.askyesno("Property Purchase", f"{current_property.name} is unowned. Do you want to buy it for ${current_property.cost}?")
                if response and self.players[self.current_player].money >= current_property.cost:
                    self.players[self.current_player].money -= current_property.cost
                    current_property.owner = self.players[self.current_player]
                    self.players[self.current_player].properties.append(current_property)
                    self.text_display.insert(tk.END, f"{self.players[self.current_player].name} bought {current_property.name}!\n")

            elif current_property.owner != self.players[self.current_player]:
                rent_due = current_property.rent
                self.text_display.insert(tk.END, f"{self.players[self.current_player].name} owes ${rent_due} in rent to {current_property.owner.name}.\n")
                self.players[self.current_player].money -= rent_due
                current_property.owner.money += rent_due

if __name__ == "__main__":
    root = tk.Tk()
    app = MonopolyApp(root)
    root.mainloop()

