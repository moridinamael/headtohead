# -*- coding: utf-8 -*-
"""
Created on Sun May 21 21:47:08 2023

@author: Matt
"""
import math
import random
import logging

logging.basicConfig(level=logging.DEBUG)

class Book:
    def __init__(self, title):
        self.title = title.strip()
        self.rating = 400

    def update_rating(self, opponent, outcome):
        self.rating, opponent.rating = self._calculate_elo(self.rating, opponent.rating, outcome)

    def _calculate_elo(self, rating1, rating2, outcome):
        K = 32

        R1 = 10 ** (rating1 / 400)
        R2 = 10 ** (rating2 / 400)

        E1 = R1 / (R1 + R2)
        E2 = R2 / (R1 + R2)

        if outcome == "1":
            S1 = 1
            S2 = 0
        else:
            S1 = 0
            S2 = 1

        new_rating1 = rating1 + K * (S1 - E1)
        new_rating2 = rating2 + K * (S2 - E2)

        return new_rating1, new_rating2


def load_books(file_path):
    with open(file_path, "r") as file:
        return [Book(line) for line in file]


def load_history(file_path, books):
    with open(file_path, "r") as file:
        for line in file:
            round_number, title1, title2, choice = line.strip().split(",")
            book1 = next(book for book in books if book.title == title1)
            book2 = next(book for book in books if book.title == title2)
            book1.update_rating(book2, choice)


def get_matchup(books):
    book1 = random.choice(books)
    book2 = random.choice(books)
    while book1 == book2:
        book2 = random.choice(books)
    return book1, book2

def get_close_matchup(books, tolerance=50):
    book1 = random.choice(books)
    close_books = [book for book in books if book != book1 and abs(book1.rating - book.rating) <= tolerance]
    if not close_books:  # If no close books, fallback to a random choice
        book2 = random.choice([book for book in books if book != book1])
    else:
        book2 = random.choice(close_books)
    return book1, book2

def get_user_choice(book1, book2):
    while True:
        print(f"Choose:\n1. {book1.title}\n2. {book2.title}")
        choice = input().strip()
        if choice in {"1", "2"}:
            return choice
        print("Invalid choice. Please enter 1 or 2.")


def update_history(file_path, round_number, book1, book2, choice):
    with open(file_path, "a") as file:
        file.write(f"{round_number},{book1.title},{book2.title},{choice}\n")


def main():
    books = load_books("BooksList.txt")
    load_history("matches01.csv", books)

    for round_number in range(len(books), len(books) + 200):
        book1, book2 = get_close_matchup(books)
        choice = get_user_choice(book1, book2)
        book1.update_rating(book2, choice)
        update_history("matches01.csv", round_number, book1, book2, choice)

        for book in books:
            print(f"{book.title}: {book.rating}")


if __name__ == "__main__":
    main()
