import tkinter as tk
import customtkinter as ctk
import random
from collections import deque

# Impostazione del tema globale di CustomTkinter
ctk.set_appearance_mode("system")  # Modalità: system, dark, light
ctk.set_default_color_theme("blue")  # Temi: blue, dark-blue, green

class SlidingTrisGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Tris - Variante 3 Pedine")
        self.root.geometry("520x960")
        self.root.resizable(False, False)

        # Utilizzo di deque per tenere traccia dell'ordine di posizionamento
        self.moves_x = deque()  # Deque per le mosse di X
        self.moves_o = deque()  # Deque per le mosse di O

        self.current_player = "X"
        self.board = [""] * 9
        self.game_over = False

        # Colori del gioco
        self.colors = {
            "X": "#3a7ebf",  # Blu per X
            "O": "#bf3a3a",  # Rosso per O
            "win": "#4CAF50",  # Verde per vincita
            "next_remove_gold": "#FFD700",  # Oro per evidenziare la prossima da rimuovere
            "next_remove": "#333333",  # Oro per evidenziare la prossima da rimuovere
            "bg": "#2b2b2b",  # Sfondo scuro
            "text": "#ffffff"  # Testo chiaro
        }

        # Frame principale
        self.main_frame = ctk.CTkFrame(root)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Titolo del gioco
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="TRIS - VARIANTE 3 PEDINE",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        self.title_label.pack(pady=(15, 5))

        # Descrizione delle regole
        self.rules_label = ctk.CTkLabel(
            self.main_frame,
            text="Ogni giocatore può avere massimo 3 pedine.\nAl quarto posizionamento, la prima pedina viene rimossa.",
            font=ctk.CTkFont(size=14),
            justify="center"
        )
        self.rules_label.pack(pady=(0, 15))

        # Frame per il gioco
        self.game_frame = ctk.CTkFrame(self.main_frame)
        self.game_frame.pack(pady=10)

        # Pulsanti per la griglia di gioco
        self.buttons = []
        for i in range(3):
            for j in range(3):
                btn = ctk.CTkButton(
                    self.game_frame,
                    text="",
                    font=ctk.CTkFont(size=52, weight="bold"),
                    width=100,
                    height=100,
                    fg_color="#3E3E3E",
                    hover_color="#4E4E4E",
                    border_width=2,
                    border_color="#3E3E3E",
                    command=lambda row=i, col=j: self.make_move(row, col)
                )
                btn.grid(row=i, column=j, padx=4, pady=4)
                self.buttons.append(btn)

        # Frame per le info sul gioco
        self.info_frame = ctk.CTkFrame(self.main_frame)
        self.info_frame.pack(pady=20, fill="x")

        # Label per il turno del giocatore
        self.player_frame = ctk.CTkFrame(self.info_frame)
        self.player_frame.pack(pady=10)

        self.player_label = ctk.CTkLabel(
            self.player_frame,
            text="Turn of the player:",
            font=ctk.CTkFont(size=16)
        )
        self.player_label.grid(row=0, column=0, padx=10, pady=10)

        self.current_player_label = ctk.CTkLabel(
            self.player_frame,
            text="X",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.colors["X"]
        )
        self.current_player_label.grid(row=0, column=1, padx=10, pady=10)

        # Contatori pedine
        self.counter_frame = ctk.CTkFrame(self.info_frame)
        self.counter_frame.pack(pady=10)

        self.x_pieces_label = ctk.CTkLabel(
            self.counter_frame,
            text="Stone X: 0/3",
            font=ctk.CTkFont(size=14),
            text_color=self.colors["X"]
        )
        self.x_pieces_label.grid(row=0, column=0, padx=20, pady=5)

        self.o_pieces_label = ctk.CTkLabel(
            self.counter_frame,
            text="Stone O: 0/3",
            font=ctk.CTkFont(size=14),
            text_color=self.colors["O"]
        )
        self.o_pieces_label.grid(row=0, column=1, padx=20, pady=5)

        # Frame per i controlli di gioco
        self.control_frame = ctk.CTkFrame(self.main_frame)
        self.control_frame.pack(pady=10, fill="x")

        # Variabile per la modalità di gioco
        self.game_mode = tk.StringVar(value="player")

        # Radio buttons per selezionare la modalità
        self.mode_label = ctk.CTkLabel(
            self.control_frame,
            text="Modalità di Gioco:",
            font=ctk.CTkFont(size=16)
        )
        self.mode_label.pack(pady=(10, 5))

        self.mode_frame = ctk.CTkFrame(self.control_frame)
        self.mode_frame.pack(pady=5)

        self.two_player_rb = ctk.CTkRadioButton(
            self.mode_frame,
            text="VS Player",
            variable=self.game_mode,
            value="player",
            font=ctk.CTkFont(size=14)
        )
        self.two_player_rb.grid(row=0, column=0, padx=20, pady=10)

        self.vs_computer_rb = ctk.CTkRadioButton(
            self.mode_frame,
            text="VS Computer",
            variable=self.game_mode,
            value="computer",
            font=ctk.CTkFont(size=14)
        )
        self.vs_computer_rb.grid(row=0, column=1, padx=20, pady=10)

        # Pulsante per reset
        self.reset_button = ctk.CTkButton(
            self.control_frame,
            text="New Game",
            command=self.reset_game,
            font=ctk.CTkFont(size=16),
            height=40,
            fg_color="#32a852",  # Verde
            hover_color="#288c44"  # Verde più scuro
        )
        self.reset_button.pack(pady=20, padx=40)

        # Informazioni sullo score
        self.score_frame = ctk.CTkFrame(self.main_frame)
        self.score_frame.pack(pady=10, fill="x")

        self.score_x = 0
        self.score_o = 0
        self.ties = 0

        self.score_label = ctk.CTkLabel(
            self.score_frame,
            text="Score",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.score_label.pack(pady=(10, 5))

        self.score_grid = ctk.CTkFrame(self.score_frame)
        self.score_grid.pack(pady=5)

        # Etichette per lo score
        ctk.CTkLabel(
            self.score_grid,
            text="X:",
            font=ctk.CTkFont(size=16),
            text_color=self.colors["X"]
        ).grid(row=0, column=0, padx=10, pady=5)

        self.score_x_label = ctk.CTkLabel(
            self.score_grid,
            text="0",
            font=ctk.CTkFont(size=16),
            text_color=self.colors["X"]
        )
        self.score_x_label.grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkLabel(
            self.score_grid,
            text="O:",
            font=ctk.CTkFont(size=16),
            text_color=self.colors["O"]
        ).grid(row=0, column=2, padx=10, pady=5)

        self.score_o_label = ctk.CTkLabel(
            self.score_grid,
            text="0",
            font=ctk.CTkFont(size=16),
            text_color=self.colors["O"]
        )
        self.score_o_label.grid(row=0, column=3, padx=10, pady=5)

        ctk.CTkLabel(
            self.score_grid,
            text="Draws:",
            font=ctk.CTkFont(size=16)
        ).grid(row=0, column=4, padx=10, pady=5)

        self.ties_label = ctk.CTkLabel(
            self.score_grid,
            text="0",
            font=ctk.CTkFont(size=16)
        )
        self.ties_label.grid(row=0, column=5, padx=10, pady=5)

    def make_move(self, row, col):
        if self.game_over:
            return

        index = row * 3 + col

        # Controlla se la casella è già occupata
        if self.board[index] == "":
            # Aggiorna la griglia e il bottone
            self.board[index] = self.current_player
            self.buttons[index].configure(
                text=self.current_player,
                text_color=self.colors[self.current_player]
            )

            # Aggiungi la mossa alla coda del giocatore corrente
            if self.current_player == "X":
                self.moves_x.append(index)
                # Se è la quarta mossa, rimuovi la prima
                if len(self.moves_x) > 3:
                    old_index = self.moves_x.popleft()
                    self.board[old_index] = ""
                    self.buttons[old_index].configure(text="", border_color="#3E3E3E")
                # Aggiorna il contatore
                self.x_pieces_label.configure(text=f"Pedine X: {len(self.moves_x)}/3")
                # Evidenzia la prossima pedina da rimuovere
                self.highlight_next_remove()
            else:  # "O"
                self.moves_o.append(index)
                # Se è la quarta mossa, rimuovi la prima
                if len(self.moves_o) > 3:
                    old_index = self.moves_o.popleft()
                    self.board[old_index] = ""
                    self.buttons[old_index].configure(text="", border_color="#3E3E3E")
                # Aggiorna il contatore
                self.o_pieces_label.configure(text=f"Pedine O: {len(self.moves_o)}/3")
                # Evidenzia la prossima pedina da rimuovere
                self.highlight_next_remove()

            # Controlla se la partita è finita
            winner_combo = self.check_winner()
            if winner_combo:
                # Evidenzia la combinazione vincente
                for idx in winner_combo:
                    self.buttons[idx].configure(fg_color=self.colors["win"])

                # Aggiorna il punteggio
                if self.current_player == "X":
                    self.score_x += 1
                    self.score_x_label.configure(text=str(self.score_x))
                else:
                    self.score_o += 1
                    self.score_o_label.configure(text=str(self.score_o))

                # Mostra info sul vincitore
                self.show_game_result(f"Il giocatore {self.current_player} ha vinto!")
                self.game_over = True
                return

            # Cambia giocatore
            self.current_player = "O" if self.current_player == "X" else "X"
            self.current_player_label.configure(
                text=self.current_player,
                text_color=self.colors[self.current_player]
            )

            # Se è il turno del computer e la modalità è contro computer
            if self.current_player == "O" and self.game_mode.get() == "computer" and not self.game_over:
                self.root.after(700, self.computer_move)

    def highlight_next_remove(self):
        # Prima resetta tutti i bordi e colori del testo
        for i, btn in enumerate(self.buttons):
            if self.board[i] != "":
                btn.configure(
                    border_color=self.colors[self.board[i]],
                    text_color=self.colors[self.board[i]]
                )
            else:
                btn.configure(border_color="#3E3E3E")

        # Evidenzia la prossima pedina da rimuovere per X (se ce ne sono 3)
        if len(self.moves_x) == 3:
            next_to_remove_x = self.moves_x[0]
            self.buttons[next_to_remove_x].configure(
                border_color=self.colors["next_remove"],
                text_color=self.colors["next_remove"]  # Cambia anche il colore del testo in oro
            )

        # Evidenzia la prossima pedina da rimuovere per O (se ce ne sono 3)
        if len(self.moves_o) == 3:
            next_to_remove_o = self.moves_o[0]
            self.buttons[next_to_remove_o].configure(
                border_color=self.colors["next_remove"],
                text_color=self.colors["next_remove"]  # Cambia anche il colore del testo in oro
            )

    def computer_move(self):
        if self.game_over:
            return

        # Trova le mosse disponibili
        available_moves = [i for i, val in enumerate(self.board) if val == ""]

        if available_moves:
            move_made = False

            # Strategia per il computer:
            # 1. Se può vincere, lo fa
            # 2. Se deve bloccare l'avversario, lo fa
            # 3. Se il centro è libero, lo prende
            # 4. Altrimenti sceglie una mossa casuale

            # Controlla se può vincere
            for move in available_moves:
                # Simula una mossa
                self.board[move] = "O"

                # Se siamo alla quarta mossa, dobbiamo simulare anche la rimozione
                if len(self.moves_o) >= 3:
                    temp_oldest = self.moves_o[0]
                    old_value = self.board[temp_oldest]
                    self.board[temp_oldest] = ""
                    if self.check_winner(check_only=True):
                        move_made = True
                        # Effettua la mossa vincente
                        self.board[temp_oldest] = old_value  # Ripristina per ora
                        self.make_computer_move(move)
                        break
                    self.board[temp_oldest] = old_value  # Ripristina
                else:
                    if self.check_winner(check_only=True):
                        move_made = True
                        # Effettua la mossa vincente
                        self.make_computer_move(move)
                        break

                # Annulla la simulazione
                self.board[move] = ""

            # Se non può vincere, controlla se deve bloccare
            if not move_made:
                for move in available_moves:
                    # Simula una mossa dell'avversario
                    self.board[move] = "X"

                    # Considera anche la possibile rimozione della prima pedina X
                    if len(self.moves_x) >= 3:
                        temp_oldest = self.moves_x[0]
                        old_value = self.board[temp_oldest]
                        self.board[temp_oldest] = ""
                        if self.check_winner(check_only=True):
                            move_made = True
                            # Blocca la mossa avversaria
                            self.board[temp_oldest] = old_value  # Ripristina
                            self.make_computer_move(move)
                            break
                        self.board[temp_oldest] = old_value  # Ripristina
                    else:
                        if self.check_winner(check_only=True):
                            move_made = True
                            # Blocca la mossa avversaria
                            self.make_computer_move(move)
                            break

                    # Annulla la simulazione
                    self.board[move] = ""

            # Se centro libero, prendilo
            if not move_made and 4 in available_moves:
                self.make_computer_move(4)
            # Altrimenti, mossa casuale
            elif not move_made:
                self.make_computer_move(random.choice(available_moves))

    def make_computer_move(self, index):
        # Esegui la mossa del computer
        self.board[index] = "O"
        self.buttons[index].configure(
            text="O",
            text_color=self.colors["O"]
        )

        # Aggiungi alla coda
        self.moves_o.append(index)

        # Se è la quarta mossa, rimuovi la prima
        if len(self.moves_o) > 3:
            old_index = self.moves_o.popleft()
            self.board[old_index] = ""
            self.buttons[old_index].configure(text="", border_color="#3E3E3E")

        # Aggiorna il contatore
        self.o_pieces_label.configure(text=f"Pedine O: {len(self.moves_o)}/3")

        # Evidenzia la prossima pedina da rimuovere
        self.highlight_next_remove()

        # Controlla se la partita è finita
        winner_combo = self.check_winner()
        if winner_combo:
            for idx in winner_combo:
                self.buttons[idx].configure(fg_color=self.colors["win"])

            self.score_o += 1
            self.score_o_label.configure(text=str(self.score_o))
            self.show_game_result("Il computer ha vinto!")
            self.game_over = True
            return

        # Torna al giocatore umano
        self.current_player = "X"
        self.current_player_label.configure(
            text="X",
            text_color=self.colors["X"]
        )

    def check_winner(self, check_only=False):
        # Combinazioni vincenti
        win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Righe
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Colonne
            [0, 4, 8], [2, 4, 6]              # Diagonali
        ]

        for combo in win_combinations:
            if (self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != ""):
                if check_only:
                    return True
                return combo
        return None

    def show_game_result(self, message):
        # Crea una finestra di dialogo personalizzata
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Partita Terminata")
        dialog.geometry("300x150")
        dialog.resizable(False, False)
        dialog.grab_set()  # Modalità modale

        # Centra la finestra rispetto alla finestra principale
        dialog.geometry(f"+{self.root.winfo_x() + 110}+{self.root.winfo_y() + 250}")

        # Aggiungi il messaggio
        ctk.CTkLabel(
            dialog,
            text=message,
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(20, 10))

        # Pulsante di chiusura
        ctk.CTkButton(
            dialog,
            text="OK",
            command=dialog.destroy,
            width=100
        ).pack(pady=10)

    def reset_game(self):
        self.current_player = "X"
        self.board = [""] * 9
        self.game_over = False

        # Resetta le code delle mosse
        self.moves_x.clear()
        self.moves_o.clear()

        # Resetta tutti i pulsanti
        for btn in self.buttons:
            btn.configure(text="", fg_color="#3E3E3E", border_color="#3E3E3E")

        # Aggiorna l'etichetta del giocatore
        self.current_player_label.configure(
            text="X",
            text_color=self.colors["X"]
        )

        # Aggiorna i contatori delle pedine
        self.x_pieces_label.configure(text="Pedine X: 0/3")
        self.o_pieces_label.configure(text="Pedine O: 0/3")


if __name__ == "__main__":
    root = ctk.CTk()
    app = SlidingTrisGame(root)
    root.mainloop()
