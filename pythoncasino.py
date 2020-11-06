"""
Pythoncasino projet OUAOTMANE Elias
"""
# import des modules que nous utilisons.
from collections import defaultdict
from random import randrange
import sys
import time
from tkinter import Tk, Button, Label, LabelFrame, PhotoImage
from tkinter import messagebox, DISABLED, NORMAL, Menu, E, W
from tkinter import Toplevel, INSERT, scrolledtext
import webbrowser


class Pok:
    """variables."""
    btn1_held = None
    btn2_held = None
    btn3_held = None
    btn4_held = None
    btn5_held = None

    card_one = 'blank'
    card_two = 'blank'
    card_three = 'blank'
    card_four = 'blank'
    card_five = 'blank'

    high_score = 0

    hold_btn1 = None
    hold_btn2 = None
    hold_btn3 = None
    hold_btn4 = None
    hold_btn5 = None

    no_card_holding = True

    plyr_credits = 100
    plyr_winnings = 0
    plyr_stake = 1

    ranks = ''
    stake_btn = None
    suits = ''
    winning_hand = ''

# Interface.
root = Tk()
root.title('Vidéo Poker')
root.resizable(False, False)

# Fenetre.
pay_table_frame = LabelFrame(root)
pay_table_frame.grid(row=0, column=0)

# Chargement et affichage.
pay_table_lbl = Label(pay_table_frame)
PHOTO = PhotoImage(file=r'cartes/pay-table-bg-386x200.png')
pay_table_lbl.config(image=PHOTO)
pay_table_lbl.grid(row=0, column=0, padx=2, pady=2)
pay_table_lbl.photo = PHOTO

# Fenetre des messages.
msg_frame = LabelFrame(root)
msg_frame.grid(row=1, column=0)

# Message de départ.
msg_lbl = Label(msg_frame, font=('Helvetica', 10, 'bold'),
                text='Choisissez une mise puis cliquez sur Deal')
msg_lbl.grid(row=1, column=0)

# Fenetre pour les images.
cards_frame = LabelFrame(root)
cards_frame.grid(row=2, column=0)

# Fenetre banque.
bank_frame = LabelFrame(root)
bank_frame.grid(row=4, column=0, sticky=W+E)

# Plus haut score.
high_score_frame = LabelFrame(root)
high_score_frame.grid(row=5, column=0, sticky=W+E)

result_frame = LabelFrame(root)
result_frame.grid(row=6, column=0, sticky=W+E)

def logo_result_frame():
    """ Resultat."""
    result_frame_lbl = Label(result_frame)
    PHOTO = PhotoImage(file=r'cartes/result-frame.png')
    result_frame_lbl.config(image=PHOTO)
    result_frame_lbl.grid(row=6, column=0, padx=2, pady=2)
    result_frame_lbl.photo = PHOTO

# Appel du logo.
logo_result_frame()

def show_winner_logo():
    """Affichez l’image de la main."""
    result_frame_lbl = Label(result_frame)
    PHOTO = PhotoImage(file=r'cartes/result-frame-winner.png')
    result_frame_lbl.config(image=PHOTO)
    result_frame_lbl.grid(row=6, column=0, padx=2, pady=2)
    result_frame_lbl.photo = PHOTO

def show_loser_logo():
    """Daffichage graphique de perte de main."""
    result_frame_lbl = Label(result_frame)
    PHOTO = PhotoImage(file=r'cartes/result-frame-loser.png')
    result_frame_lbl.config(image=PHOTO)
    result_frame_lbl.grid(row=6, column=0, padx=2, pady=2)
    result_frame_lbl.photo = PHOTO

def load_high_score():
    """Charger la variable de score élevé à partir du fichier
       et la stocker dans Pok.high_score."""
    with open(r'cartes/high-score.txt', 'r') as contents:
        SAVED_HIGH_SCORE = contents.read()
        if SAVED_HIGH_SCORE > '':
            Pok.high_score = int(SAVED_HIGH_SCORE)

# Appel pour le score le plus haut.
load_high_score()

def game_over():
    """rejouer à la boîte message oui ou non."""
    quest = messagebox.askyesno('Video Poker',
                                'game over, plus de thunes.\n'
                                'Voulez-vous jouer une nouvelle partie?')

    if quest:
        # Nouvelle partie.
        hand = [Pok.card_one, Pok.card_two, Pok.card_three,
                Pok.card_four, Pok.card_five]
        hand_value = check_hand(hand)
        Pok.plyr_credits = 100
        Pok.plyr_winnings = 0
        # ne pas mettre à jour.
        high_score_lbl = Label(high_score_frame, font=('Helvetica', 10, 'bold'),
                               text='Top Score: €'+str(Pok.high_score)+'     ')
        high_score_lbl.grid(row=4, column=0)

        start_game()
        return

    else:
        # Extinction du programme
        root.destroy()
        sys.exit()

def save_high_score():
    """Enregistrer le score actuel dans le fichier s’il bat le score précédent."""
    with open(r'cartes/high-score.txt', 'w') as contents:
        if Pok.plyr_credits < Pok.high_score:
            return

        SAVE_IT = str(Pok.plyr_credits)
        contents.write(SAVE_IT)

def update_high_score():
    """Mettre à jour l’étiquette du score élevé."""
    high_score_lbl = Label(high_score_frame, font=('Helvetica', 10, 'bold'),
                           text='High Score: €'+str(Pok.high_score)+'     ')
    high_score_lbl.grid(row=4, column=0)
    save_high_score()

def update_bank():
    """Mise à jour de la banque."""
    bank_lbl = Label(bank_frame, font=('Helvetica', 10, 'bold'),
                     text='Banque: €'+str(Pok.plyr_credits)+'  ')
    bank_lbl.grid(row=3, column=0)

    # Vérifiez si la banque actuelle bat le score le plus élevé, puis mise à jour.
    if Pok.plyr_credits > Pok.high_score:
        Pok.high_score = Pok.plyr_credits
        update_high_score()

def disable_hold_btns():
    """Désactiver les boutons de verrouillage."""
    Pok.hold_btn1.configure(state=DISABLED)
    Pok.hold_btn2.configure(state=DISABLED)
    Pok.hold_btn3.configure(state=DISABLED)
    Pok.hold_btn4.configure(state=DISABLED)
    Pok.hold_btn5.configure(state=DISABLED)
    Pok.no_card_holding = True

def enable_hold_btns():
    """Activer les boutons de verrouillage."""
    Pok.hold_btn1.configure(state=NORMAL)
    Pok.hold_btn2.configure(state=NORMAL)
    Pok.hold_btn3.configure(state=NORMAL)
    Pok.hold_btn4.configure(state=NORMAL)
    Pok.hold_btn5.configure(state=NORMAL)
    Pok.no_card_holding = False

def hold_card1():
    """Vérifier si peut tenir ou décrocher la carte un, si oui, et mettre à jour."""
    # Aucune retenue autorisée pour l’instant, donc retour.
    if Pok.no_card_holding:
        return

    # Basculer booléen, donc s’il est maintenu, décroché, et vice versa.
    Pok.btn1_held = not Pok.btn1_held

    load_file = 'cartes/hold-btn.png'
    if Pok.btn1_held:
        load_file = 'cartes/held-btn.png'

    Pok.hold_btn1 = Button(cards_frame, width=68, height=35,
                           command=hold_card1)
    hold_image1 = PhotoImage(file=load_file)
    Pok.hold_btn1.config(image=hold_image1)
    Pok.hold_btn1.image = hold_image1
    Pok.hold_btn1.grid(row=1, column=0, padx=2, pady=2)

def hold_card2():
    """Vérifiez si peut tenir ou décrocher la carte 2."""
    if Pok.no_card_holding:
        return

    Pok.btn2_held = not Pok.btn2_held

    load_file = 'cartes/hold-btn.png'
    if Pok.btn2_held:
        load_file = 'cartes/held-btn.png'

    Pok.hold_btn2 = Button(cards_frame, width=68, height=35, command=hold_card2)
    hold_image2 = PhotoImage(file=load_file)
    Pok.hold_btn2.config(image=hold_image2)
    Pok.hold_btn2.image = hold_image2
    Pok.hold_btn2.grid(row=1, column=1, padx=2, pady=2)

def hold_card3():
    """Vérifiez si peut tenir ou décrocher la carte 3."""
    if Pok.no_card_holding:
        return

    Pok.btn3_held = not Pok.btn3_held

    load_file = 'cartes/hold-btn.png'
    if Pok.btn3_held:
        load_file = 'cartes/held-btn.png'

    Pok.hold_btn3 = Button(cards_frame, width=68, height=35, command=hold_card3)
    hold_image3 = PhotoImage(file=load_file)
    Pok.hold_btn3.config(image=hold_image3)
    Pok.hold_btn3.image = hold_image3
    Pok.hold_btn3.grid(row=1, column=2, padx=2, pady=2)

def hold_card4():
    """Vérifiez si peut tenir ou décrocher la carte 4."""
    if Pok.no_card_holding:
        return

    Pok.btn4_held = not Pok.btn4_held

    load_file = 'cartes/hold-btn.png'
    if Pok.btn4_held:
        load_file = 'cartes/held-btn.png'

    Pok.hold_btn4 = Button(cards_frame, width=68, height=35, command=hold_card4)
    hold_image4 = PhotoImage(file=load_file)
    Pok.hold_btn4.config(image=hold_image4)
    Pok.hold_btn4.image = hold_image4
    Pok.hold_btn4.grid(row=1, column=3, padx=2, pady=2)

def hold_card5():
    """Vérifiez si peut tenir ou décrocher la carte 5."""
    if Pok.no_card_holding:
        return

    Pok.btn5_held = not Pok.btn5_held

    load_file = 'cartes/hold-btn.png'
    if Pok.btn5_held:
        load_file = 'cartes/held-btn.png'

    Pok.hold_btn5 = Button(cards_frame, width=68, height=35, command=hold_card5)
    hold_image5 = PhotoImage(file=load_file)
    Pok.hold_btn5.config(image=hold_image5)
    Pok.hold_btn5.image = hold_image5
    Pok.hold_btn5.grid(row=1, column=4, padx=2, pady=2)

def reset_hold_btns():
    """Si des boutons de maintien sont maintenus, les décrocher pour les réinitialiser."""
    if Pok.btn1_held:
        hold_card1()
    if Pok.btn2_held:
        hold_card2()
    if Pok.btn3_held:
        hold_card3()
    if Pok.btn4_held:
        hold_card4()
    if Pok.btn5_held:
        hold_card5()

def display_cards():
    """Affichage des images de cartes à l’aide de boutons."""
    # Définition de la longueur de pause entre les cartes distribuées.
    deal_pause = .10

    # Ne pas faire de pause entre les cartes qui sont distribuées si on traite les cinq premières faces vers le bas.
    if Pok.card_one == 'blank':
        deal_pause = 0

    card1 = Pok.card_one+'.png' # noms des images par cartes.
    card2 = Pok.card_two+'.png'
    card3 = Pok.card_three+'.png'
    card4 = Pok.card_four+'.png'
    card5 = Pok.card_five+'.png'

    # Ne pas montrer la carte de nouveau si elle est conservée, sauf si elle est en blanc.
    if not Pok.btn1_held or deal_pause == 0:
        card1_btn = Button(cards_frame, command=hold_card1)
        PHOTO = PhotoImage(file=r'cartes/'+str(card1))
        card1_btn.config(image=PHOTO)
        card1_btn.grid(row=0, column=0, padx=2, pady=2)
        card1_btn.photo = PHOTO
        time.sleep(deal_pause)
        cards_frame.update()

    if not Pok.btn2_held or deal_pause == 0:
        card2_btn = Button(cards_frame, command=hold_card2)
        PHOTO = PhotoImage(file=r'cartes/'+str(card2))
        card2_btn.config(image=PHOTO)
        card2_btn.grid(row=0, column=1, padx=2, pady=2)
        card2_btn.photo = PHOTO
        time.sleep(deal_pause)
        cards_frame.update()

    if not Pok.btn3_held or deal_pause == 0:
        card3_btn = Button(cards_frame, command=hold_card3)
        PHOTO = PhotoImage(file=r'cartes/'+str(card3))
        card3_btn.config(image=PHOTO)
        card3_btn.grid(row=0, column=2, padx=2, pady=2)
        card3_btn.photo = PHOTO
        time.sleep(deal_pause)
        cards_frame.update()

    if not Pok.btn4_held or deal_pause == 0:
        card4_btn = Button(cards_frame, command=hold_card4)
        PHOTO = PhotoImage(file=r'cartes/'+str(card4))
        card4_btn.config(image=PHOTO)
        card4_btn.grid(row=0, column=3, padx=2, pady=2)
        card4_btn.photo = PHOTO
        time.sleep(deal_pause)
        cards_frame.update()

    if not Pok.btn5_held or deal_pause == 0:
        card5_btn = Button(cards_frame, command=hold_card5)
        PHOTO = PhotoImage(file=r'cartes/'+str(card5))
        card5_btn.config(image=PHOTO)
        card5_btn.grid(row=0, column=4, padx=2, pady=2)
        card5_btn.photo = PHOTO
        time.sleep(deal_pause)
        cards_frame.update()

def check_winnings():
    """Vérifiez combien, le cas échéant, le joueur a gagné."""
    hand_value = check_hand(hand)
    Pok.plyr_credits = Pok.plyr_credits + Pok.plyr_winnings
    update_bank()
    show_winner_logo()

def deal_btn_clkd():
    """Lorsque le bouton Deal est cliqué. Après la configuration initiale du jeu, le programme attend ici
       de sorte que l’enjeu peut être modifié si nécessaire. Lorsque Deal est finalement
       cliqué, nous passons ensuite sur les prises et le tirage."""

    # Assurez-vous que les crédits sont >= à mettre en jeu.
    if Pok.plyr_stake > Pok.plyr_credits:
        messagebox.showinfo('Video Poker', 'Pas assez de thune\n'
                            'pour miser.\n\n'
                            'Veuillez baisser votre mise pour continuer.')
        return
    deal_btn.configure(state=DISABLED)
    Pok.stake_btn.configure(state=DISABLED)
    clear_msg_box()

    disply_blanks()
    time.sleep(0.5)
    # Choisissez 5 cartes puis montrez-les face vers le haut.
    get_rnd_hand()
    display_cards()

    # Configuration interface.
    enable_hold_btns()
    Pok.no_card_holding = False

    # Trouver la meilleur main.
    hand = [Pok.card_one, Pok.card_two, Pok.card_three, Pok.card_four, Pok.card_five]
    hand_value = check_hand(hand)
    best_hand = (hand_dict.get(hand_value))

    if not best_hand:
        best_hand = 'Pas de gagnant'

    # Afficher la meilleure main disponible dans la fenêtre msg.
    msg_lbl = Label(msg_frame, font=('Helvetica', 10, 'bold'),
                    text='Voici votre main: '+str(best_hand))
    msg_lbl.grid(row=1, column=0)

    #Retirer la mise de la banque et mettre à jour le nouveau total.
    Pok.plyr_credits = Pok.plyr_credits - Pok.plyr_stake
    update_bank()

    draw_btn.configure(state=NORMAL)

def clear_msg_box():
    """Efface la boîte msg avec 90 espaces vides."""
    msg_lbl = Label(msg_frame, text=' ' *90)
    msg_lbl.grid(row=1, column=0)

    logo_result_frame()

def winner():
    """Nous avons la main gagnante."""
    added_text = 'Felicitations vous avez gagné €'  \
     +str(Pok.plyr_winnings)+'\nFor '+str(Pok.winning_hand)

    show_winner_logo()
    messagebox.showinfo('Video Poker', added_text)

    disply_blanks()
    reset_hold_btns()
    disable_hold_btns()
    logo_result_frame()

    msg_lbl = Label(msg_frame, font=('Helvetica', 10, 'bold'),
                    text='Choisissez votre mise, et cliqué sur Deal.')
    msg_lbl.grid(row=1, column=0)

    Pok.plyr_winnings = 0

    # Vérifier qu’il y a suffisamment de crédits en banque.
    if Pok.plyr_credits <= 0:
        game_over()
        return

    deal_btn.configure(state=NORMAL)
    Pok.stake_btn.configure(state=NORMAL)

def draw_btn_clkd():
    """Le pari est placé, ainsi maintenant le bouton cliqué."""
    draw_btn.configure(state=DISABLED)
    clear_msg_box()
    get_rnd_card_if_not_held()
    display_cards()

    # Ranger les cinq cartes en main[] liste.
    hand = [Pok.card_one, Pok.card_two, Pok.card_three, Pok.card_four, Pok.card_five]

    # Vérifier les gains dans la main.
    hand_value = check_hand(hand)
    best_hand = (hand_dict.get(hand_value))

    if not best_hand:
        best_hand = 'Pas de gagnant'
    # Affichage de la meilleure main dans la fenêtre msg et verification des gains, le cas échéant.
    msg_lbl = Label(msg_frame, font=('Helvetica', 10, 'bold'),
                    text='Resultat: '+str(best_hand))
    msg_lbl.grid(row=1, column=0)
    check_winnings()

    # Message.
    added_text = 'Pas de gagnant cette fois.\n\nVous avez perdu €'+str(Pok.plyr_stake)+'\n\nEssayez à nouveau!'

    # Si victoire.
    if Pok.plyr_winnings:
        Pok.winning_hand = str((hand_dict.get(hand_value)))
        winner()
        return

    show_loser_logo()

    # Nouvelle main.
    reset_hold_btns()
    disable_hold_btns()

    msg_lbl = Label(msg_frame, font=('Helvetica', 10, 'bold'),
                    text='Choisissez une mise, puis cliquer sur Deal.')
    msg_lbl.grid(row=1, column=0)

    Pok.plyr_winnings = 0

    # verifier argent.
    if Pok.plyr_credits <= 0:
        game_over()
        return

    deal_btn.configure(state=NORMAL)
    Pok.stake_btn.configure(state=NORMAL)

def update_stake():
    """maj des images, 1-5."""
    load_file = 'cartes/stake-btn'+str(Pok.plyr_stake)+'.png'

    Pok.stake_btn = Button(cards_frame, width=68, height=35, command=bet_one)
    stake_image = PhotoImage(file=load_file)
    Pok.stake_btn.config(image=stake_image)
    Pok.stake_btn.image = stake_image
    Pok.stake_btn.grid(row=2, column=0, padx=2, pady=2)

def bet_one():
    """Changer le montant, 1€ a 5€."""
    if Pok.plyr_stake == 5: 
        Pok.plyr_stake = 1
        update_stake()
        return

    Pok.plyr_stake += 1
    update_stake()

def get_rnd_hand():
    """Sélectionnez 5 cartes aléatoires différentes pour un nouveau jeu."""
    Pok.ranks = ['2H', '2D', '2C', '2S', '3H', '3D', '3C', '3S',
                 '4H', '4D', '4C', '4S', '5H', '5D', '5C', '5S',
                 '6H', '6D', '6C', '6S', '7H', '7D', '7C', '7S',
                 '8H', '8D', '8C', '8S', '9H', '9D', '9C', '9S',
                 'TH', 'TD', 'TC', 'TS', 'JH', 'JD', 'JC', 'JS',
                 'QH', 'QD', 'QC', 'QS', 'KH', 'KD',
                 'KC', 'KS', 'AH', 'AD', 'AC', 'AS']

    card_one_rank = randrange(len(Pok.ranks))
    Pok.card_one = (Pok.ranks[card_one_rank])
    del Pok.ranks[card_one_rank]

    card_two_rank = randrange(len(Pok.ranks))
    Pok.card_two = (Pok.ranks[card_two_rank])
    del Pok.ranks[card_two_rank]

    card_three_rank = randrange(len(Pok.ranks))
    Pok.card_three = (Pok.ranks[card_three_rank])
    del Pok.ranks[card_three_rank]

    card_four_rank = randrange(len(Pok.ranks))
    Pok.card_four = (Pok.ranks[card_four_rank])
    del Pok.ranks[card_four_rank]

    card_five_rank = randrange(len(Pok.ranks))
    Pok.card_five = (Pok.ranks[card_five_rank])
    del Pok.ranks[card_five_rank]

    # Vérifiez s’il y a une carte en double, si vous en trouvez une, refaites le lot :get_rnd_hand().
    if Pok.card_one == Pok.card_two or Pok.card_one == Pok.card_three or  \
       Pok.card_two == Pok.card_three or Pok.card_one == Pok.card_four or  \
       Pok.card_two == Pok.card_four or Pok.card_three == Pok.card_four or  \
       Pok.card_one == Pok.card_five or Pok.card_two == Pok.card_five or   \
       Pok.card_three == Pok.card_five or  Pok.card_four == Pok.card_five:
        #check puis appelle
        get_rnd_hand()

def get_rnd_card_if_not_held():
    """If card is not held, and draw is clicked, get new rnd card."""
    if not Pok.btn1_held:
        # Choisissez carte aléa pour la carte un.
        card_one_rank = randrange(len(Pok.ranks))
        Pok.card_one = (Pok.ranks[card_one_rank])

    if not Pok.btn2_held:
        card_two_rank = randrange(len(Pok.ranks))
        Pok.card_two = (Pok.ranks[card_two_rank])

    if not Pok.btn3_held:
        card_three_rank = randrange(len(Pok.ranks))
        Pok.card_three = (Pok.ranks[card_three_rank])

    if not Pok.btn4_held:
        card_four_rank = randrange(len(Pok.ranks))
        Pok.card_four = (Pok.ranks[card_four_rank])

    if not Pok.btn5_held:
        card_five_rank = randrange(len(Pok.ranks))
        Pok.card_five = (Pok.ranks[card_five_rank])

    #Vérifiez s’il y a une carte en double, si vous en trouvez une, refaites le lot:get_rnd_hand()
    if Pok.card_one == Pok.card_two or Pok.card_one == Pok.card_three or  \
        Pok.card_two == Pok.card_three or Pok.card_one == Pok.card_four or  \
        Pok.card_two == Pok.card_four or Pok.card_three == Pok.card_four or  \
        Pok.card_one == Pok.card_five or Pok.card_two == Pok.card_five or   \
        Pok.card_three == Pok.card_five or  Pok.card_four == Pok.card_five:
        get_rnd_card_if_not_held()

# Verification de la main.
def check_royal_flush(hand):
    """Verification de la quinte flush."""
    if check_flush(hand) and check_straight(hand):
        # Check.
        values = [i[0] for i in hand]
        value_counts = defaultdict(lambda: 0)
        for v in values:
            value_counts[v] += 1
            if set(values) == set(['T', 'J', 'Q', 'K', 'A']):
                return True
    else:
        return False

def check_straight_flush(hand):
    """Verification de la flush."""
    if check_flush(hand) and check_straight(hand):
        return True
    else:
        return False

def check_four_of_a_kind(hand):
    """Vérifier pour 4 d’une sorte."""
    values = [i[0] for i in hand]
    value_counts = defaultdict(lambda: 0)
    for v in values:
        value_counts[v] += 1
    if sorted(value_counts.values()) == [1, 4]:
        four_of_a_kind = True
        return True
    return False

def check_full_house(hand):
    """Full house."""
    values = [i[0] for i in hand]
    value_counts = defaultdict(lambda: 0)
    for v in values:
        value_counts[v] += 1
    if sorted(value_counts.values()) == [2, 3]:
        return True
    return False

def check_flush(hand):
    """Flush."""
    Pok.suits = [i[1] for i in hand]
    if len(set(Pok.suits)) == 1:
        return True
    else:
        return False

def check_straight(hand):
    """Straight."""
    values = [i[0] for i in hand]
    value_counts = defaultdict(lambda: 0)
    for v in values:
        value_counts[v] += 1
    rank_values = [card_order_dict[i] for i in values]
    value_range = max(rank_values) - min(rank_values)
    if len(set(value_counts.values())) == 1 and (value_range == 4):
        return True
    else:
        # Vérif.
        if set(values) == set(['A', '2', '3', '4', '5']):
            return True
        return False

def check_three_of_a_kind(hand):
    """3 kind."""
    values = [i[0] for i in hand]
    value_counts = defaultdict(lambda: 0)
    for v in values:
        value_counts[v] += 1
    if set(value_counts.values()) == set([3, 1]):
        return True
    else:
        return False

def check_two_pairs(hand):
    """Double pair."""
    values = [i[0] for i in hand]
    value_counts = defaultdict(lambda: 0)
    for v in values:
        value_counts[v] += 1
    if sorted(value_counts.values()) == [1, 2, 2]:
        return True
    else:
        return False

def check_one_pairs(hand):
    """Vérifier s’il y a une paire de valets, de reines, de rois ou d’as, rejeter les paires inférieures.."""
    # Réinitialiser le contrôle des paires gagnantes.
    pair_aces = 0
    pair_kings = 0
    pair_queens = 0
    pair_jacks = 0

    values = [i[0] for i in hand]

    value_counts = defaultdict(lambda: 0)
    for v in values:
        value_counts[v] += 1

        if v == 'A':
            pair_aces += 1
            if pair_aces == 2:
                return True

        if v == 'K':
            pair_kings += 1
            if pair_kings == 2:
                return True

        if v == 'Q':
            pair_queens += 1
            if pair_queens == 2:
                return True

        if v == 'J':
            pair_jacks += 1
            if pair_jacks == 2:
                return True

    else:
        return False

def check_hand(hand):
    """Vérifier la main pour trouver la meilleure victoire et combien payer."""
    if hand[0] == 'blank':
        return

    if check_royal_flush(hand):
        Pok.plyr_winnings = Pok.plyr_stake *800
        return 10
    if check_straight_flush(hand):
        Pok.plyr_winnings = Pok.plyr_stake *50
        return 9
    if check_four_of_a_kind(hand):
        Pok.plyr_winnings = Pok.plyr_stake *25
        return 8
    if check_full_house(hand):
        Pok.plyr_winnings = Pok.plyr_stake *9
        return 7
    if check_flush(hand):
        Pok.plyr_winnings = Pok.plyr_stake *6
        return 6
    if check_straight(hand):
        Pok.plyr_winnings = Pok.plyr_stake *4
        return 5
    if check_three_of_a_kind(hand):
        Pok.plyr_winnings = Pok.plyr_stake *3
        return 4
    if check_two_pairs(hand):
        Pok.plyr_winnings = Pok.plyr_stake *2
        return 3
    if check_one_pairs(hand):
        Pok.plyr_winnings = Pok.plyr_stake 
        return 2
    else:
        Pok.plyr_winnings = 0
    return 0 

# dictionnaires
card_order_dict = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8,
                   '9':9, 'T':10, 'J':11, 'Q':12, 'K':13, 'A':14}

hand_dict = {10:'Royal Flush', 9:'Straight-Flush', 8:'Four-Of-A-Kind',
             7:'Full-House', 6:'Flush', 5:'Straight',
             4:'Three-Of-A-Kind', 3:'Two-Pairs', 2:'One-Pair', 1:'High-Card'}

# Créez des boutons de mise, de tirage et de distribution.
load_file = 'cartes/stake-btn1.png'

Pok.stake_btn = Button(cards_frame, width=68, height=35, command=bet_one)
stake_image = PhotoImage(file=load_file)
Pok.stake_btn.config(image=stake_image)
Pok.stake_btn.image = stake_image
Pok.stake_btn.grid(row=2, column=0, padx=2, pady=2)

draw_btn = Button(cards_frame, width=68, height=35, command=draw_btn_clkd)
draw_image = PhotoImage(file=r'cartes/draw-btn.png')
draw_btn.config(image=draw_image)
draw_btn.image = draw_image
draw_btn.grid(row=2, column=3, padx=2, pady=2)

deal_btn = Button(cards_frame, width=68, height=35, command=deal_btn_clkd)
deal_image = PhotoImage(file=r'cartes/deal-btn.png')
deal_btn.config(image=deal_image)
deal_btn.image = deal_image
deal_btn.grid(row=2, column=4, padx=2, pady=2)

# Cache
def set_hold_btns():
    """Affichage et chargement des boutons."""
    Pok.hold_btn1 = Button(cards_frame, width=68, height=35, command=hold_card1)
    hold_image1 = PhotoImage(file='cartes/hold-btn.png')
    Pok.hold_btn1.config(image=hold_image1)
    Pok.hold_btn1.image = hold_image1
    Pok.hold_btn1.grid(row=1, column=0, padx=2, pady=2)

    Pok.hold_btn2 = Button(cards_frame, width=68, height=35, command=hold_card2)
    hold_image2 = PhotoImage(file='cartes/hold-btn.png')
    Pok.hold_btn2.config(image=hold_image2)
    Pok.hold_btn2.image = hold_image2
    Pok.hold_btn2.grid(row=1, column=1, padx=2, pady=2)

    Pok.hold_btn3 = Button(cards_frame, width=68, height=35, command=hold_card3)
    hold_image3 = PhotoImage(file='cartes/hold-btn.png')
    Pok.hold_btn3.config(image=hold_image3)
    Pok.hold_btn3.image = hold_image3
    Pok.hold_btn3.grid(row=1, column=2, padx=2, pady=2)

    Pok.hold_btn4 = Button(cards_frame, width=68, height=35, command=hold_card4)
    hold_image4 = PhotoImage(file='cartes/hold-btn.png')
    Pok.hold_btn4.config(image=hold_image4)
    Pok.hold_btn4.image = hold_image4
    Pok.hold_btn4.grid(row=1, column=3, padx=2, pady=2)

    Pok.hold_btn5 = Button(cards_frame, width=68, height=35, command=hold_card5)
    hold_image5 = PhotoImage(file='cartes/hold-btn.png')
    Pok.hold_btn5.config(image=hold_image5)
    Pok.hold_btn5.image = hold_image5
    Pok.hold_btn5.grid(row=1, column=4, padx=2, pady=2)

def disply_blanks():
    """Pour un nouveau départ, montrer les cartes face cachée."""
    Pok.card_one = 'blank'
    Pok.card_two = 'blank'
    Pok.card_three = 'blank'
    Pok.card_four = 'blank'
    Pok.card_five = 'blank'
    display_cards()

def about_menu():
    """information sur le programme."""
    messagebox.showinfo('Information programme', 'Video pokerV1.0\n'
                        'Compatible sur Windows et Linux.\n\n'
                        'Python version 3.\n\n'
                        'Logiciel fait\npar Elias OUAOTMANE.\n\n'
                        '2020')

def visit_blog_menu():
    """python blog."""
    webbrowser.open('https://www.python.org/blogs/')

def contact_menu():
    """email contact."""
    webbrowser.open('e.ouaotmane@ecole-ipssi.net')

def quit_prog():
    """Quitter y-n."""
    ask_yn = messagebox.askyesno('Video Poker',
                                 'Voulez-vous vraiment quitter?')
    if ask_yn:
        root.destroy()
        sys.exit()

# menu.
MENU_BAR = Menu(root)
FILE_MENU = Menu(MENU_BAR, tearoff=0)
MENU_BAR.add_cascade(label='Menu', menu=FILE_MENU)
FILE_MENU.add_command(label='A propos', command=about_menu)
FILE_MENU.add_separator()
FILE_MENU.add_command(label='Contact', command=contact_menu)
FILE_MENU.add_command(label='Visité les blogs python', command=visit_blog_menu)
FILE_MENU.add_separator()
FILE_MENU.add_command(label='Quitter', command=quit_prog)
root.config(menu=MENU_BAR)


#lancement jeu.
def start_game():
    """Commencement."""
    load_high_score()
    disply_blanks()
    set_hold_btns()
    Pok.no_card_holding = True
    draw_btn.configure(state=DISABLED)
    disable_hold_btns()
    update_bank()
    deal_btn.configure(state=NORMAL)


# lancement de la main.
hand = [Pok.card_one, Pok.card_two, Pok.card_three, Pok.card_four, Pok.card_five]
hand_value = check_hand(hand)
high_score_lbl = Label(high_score_frame, font=('Helvetica', 10, 'bold'),
                       text='Top Score: €'+str(Pok.high_score))
high_score_lbl.grid(row=4, column=0)

start_game()

root.mainloop()
