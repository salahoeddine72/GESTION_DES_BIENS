from tkinter import *
from tkcalendar import *
from tkinter import ttk, Label, messagebox
import tkinter as tk
import sqlite3

# conn = sqlite3.connect("gestionbien.db")
# sql = 'DELETE FROM Biens'
# cur = conn.cursor()
# cur.execute(sql)
# conn.commit()


tk1 = Tk()
tk1.geometry("400x300")
tk1.title("Gestion de biens ")


########BASE DE DONNEES#########

# fonction d'ajout du bien
def insertMultipleRecords():
    global sqliteConnection
    try:
        sqliteConnection = sqlite3.connect('gestionbien.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        cursor.execute("""
         CREATE TABLE IF NOT EXISTS Biens(
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             type_bien VARCHAR(11) NOT NULL CHECK (type_bien IN ('Maison', 'Appartement')),
             adresse_numero INTEGER NOT NULL CHECK (adresse_numero>0),
             adresse_type VARCHAR(9) NOT NULL CHECK(adresse_type IN ('RUE', 'IMPASSE', 'Avenue', 'Boulevard', 'ALLE',
                                                    'PLACE')) ,
             adresse_nom VARCHAR(255) NOT NULL,
             adresse_code_postal INTEGER NOT NULL CHECK (adresse_code_postal >= 10000 AND adresse_code_postal <=99999),
             adresse_commune VARCHAR(255) NOT NULL,
             superficie_couverte FLOAT NOT NULL,
             superficie_jardin FLOAT DEFAULT 0,
             nombre_pieces INTEGER NOT NULL CHECK (nombre_pieces > 0),
             classe_energetique VARCHAR(1) NOT NULL CHECK(classe_energetique IN ('A', 'B', 'C', 'D')),
             annee_construction INTEGER NOT NULL CHECK (annee_construction >= 1800 AND annee_construction <= 2023),
             nature_gestion VARCHAR(8) NOT NULL CHECK (nature_gestion IN ('Location','Vente')),
             date_mise_sur_marche DATE NOT NULL,
             prix FLOAT NOT NULL)""")

    except sqlite3.Error as error:
        print(error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
##################################


# Partie Recherche
def recherche():
    tk3 = Toplevel(tk1)
    tk3.geometry("1400x550")
    tk3.title("Recherche de biens")
    # annee de construction
    Label(tk3, text="Année de construction :").place(x='50', y='60')
    val12 = tk.StringVar()
    val12.set("texte par défaut")
    cal1 = tk.Entry(tk3, textvariable=val12, width=30)
    cal1.place(x='250', y='60')
    # cal1 = Calendar(tk3, selectmode='day',
    #                 year=2023, month=2,
    #                 day=28)
    # date1 = Label(tk3, text="Date de mise sur le marché :")
    # date1.place(x='50', y='60')
    # cal1.place(x='250', y='10')

    # code postal
    val6 = StringVar()
    cp = Label(tk3, text="Commune : ")
    cp.place(x='50', y='220')
    entree6 = Entry(tk3, textvariable=val6, width=10)
    val6.set("commune")
    entree6.place(x='250', y='220')

    # type de bien
    Label(tk3, text="Nature du bien :").place(x='50', y='270')
    val5 = StringVar()
    Radiobutton(tk3, text="Maison", variable=val5, value="Maison").place(x='250', y='270')
    Radiobutton(tk3, text="Appartement", variable=val5, value="Appartement").place(x='320', y='270')

    # intervalle de prix
    val3 = StringVar()
    val4 = StringVar()
    prixm = Label(tk3, text="Intervalle du Prix : ")
    prixm.place(x='50', y='320')
    entree3 = Entry(tk3, textvariable=val3, width=10)
    entree3.place(x='320', y='320')
    entree4 = Entry(tk3, textvariable=val4, width=10)
    entree4.place(x='250', y='320')

    # intervalle de surface couverte
    val1 = StringVar()
    val2 = StringVar()
    intvsup = Label(tk3, text="Intervalle de superficie : ")
    intvsup.place(x='50', y='370')
    entree1 = Entry(tk3, textvariable=val1, width=10)
    entree1.place(x='250', y='370')
    entree2 = Entry(tk3, textvariable=val2, width=10)
    entree2.place(x='320', y='370')

    # classe energetique
    Label(tk3, text="Classe énergitique :").place(x='50', y='420')
    clsenerg = ttk.Combobox(tk3, width=10)
    clsenerg['values'] = ('A',
                          'B',
                          'C',
                          'D')

    clsenerg.place(x='250', y='420')

    # Nature de gestion
    Label(tk3, text="Nature du bien :").place(x='50', y='470')
    val6 = StringVar()
    Radiobutton(tk3, text="Location", variable=val6, value="Location").place(x='250', y='470')
    Radiobutton(tk3, text="Vente", variable=val6, value="Vente").place(x='320', y='470')

    def conn():
        tk4 = Toplevel(tk3)

        date_mise_sur_marche = cal1.get()
        prix = entree3.get()
        prixm = entree4.get()
        type_bien = val5.get()
        classe_energetique = clsenerg.get()
        adresse_commune = entree6.get()
        nature_gestion = val6.get()
        supermin = entree1.get()
        supermax = entree2.get()

        my_conn = sqlite3.connect('gestionbien.db')

        query = '''SELECT type_bien, adresse_numero,adresse_type,adresse_nom,
     adresse_code_postal,adresse_commune,superficie_couverte, superficie_jardin,
     nombre_pieces,classe_energetique,annee_construction,nature_gestion,
     date_mise_sur_marche,prix from Biens '''

        values = []
        filters = []
        if type_bien:
            filters.append("type_bien LIKE ? ")
            values.append(type_bien)

        if adresse_commune:
            filters.append("adresse_commune LIKE ? ")
            values.append(adresse_commune)

        if date_mise_sur_marche:
            filters.append("annee_construction LIKE ? ")
            values.append(date_mise_sur_marche)

        if classe_energetique:
            filters.append("classe_energetique LIKE ? ")
            values.append(classe_energetique)

        if nature_gestion:
            filters.append("nature_gestion LIKE ? ")
            values.append(nature_gestion)

        if prixm and prix:
            filters.append("prix BETWEEN ? and ? ")
            values.append(float(prixm))
            values.append(float(prix))

        if supermin and supermax:
            filters.append("superficie_couverte BETWEEN ? and ? ")
            values.append(float(supermin))
            values.append(float(supermax))


        if len(filters):
            query += 'WHERE ' + 'AND '.join(filters)

        r_set = my_conn.execute(query, tuple(values))

        e = Label(tk4, width=10, borderwidth=2, relief='ridge', bg='black', fg='white', text="Type de bien", anchor='w')
        e.grid(row=0, column=0)
        e = Label(tk4, width=10, borderwidth=2, relief='ridge', bg='black', fg='white', text="Numero", anchor='w')
        e.grid(row=0, column=1)
        e = Label(tk4, width=10, borderwidth=2, relief='ridge', bg='black', fg='white', text="Type de rue", anchor='w')
        e.grid(row=0, column=2)
        e = Label(tk4, width=10, borderwidth=2, relief='ridge', bg='black', fg='white', text="Adresse", anchor='w')
        e.grid(row=0, column=3)
        e = Label(tk4, width=10, borderwidth=2, relief='ridge', bg='black', fg='white', text="Code Postal", anchor='w')
        e.grid(row=0, column=4)
        e = Label(tk4, width=10, borderwidth=2, relief='ridge', bg='black', fg='white', text="Commune", anchor='w')
        e.grid(row=0, column=5)
        e = Label(tk4, width=10, borderwidth=2, relief='ridge', bg='black', fg='white', text="Superficie du bien",
                  anchor='w')
        e.grid(row=0, column=6)
        e = Label(tk4, width=10, borderwidth=2, relief='ridge', bg='black', fg='white', text="Superficie du jardin",
                  anchor='w')
        e.grid(row=0, column=7)
        e = Label(tk4, width=10, borderwidth=2, relief='ridge', bg='black', fg='white', text="Nombre de pieces",
                  anchor='w')
        e.grid(row=0, column=8)
        e = Label(tk4, width=10, borderwidth=2, relief='ridge', bg='black', fg='white', text="Classe énergetique",
                  anchor='w')
        e.grid(row=0, column=9)
        e = Label(tk4, width=10, borderwidth=2, relief='ridge', bg='black', fg='white', text="Année de construction",
                  anchor='w')
        e.grid(row=0, column=10)
        e = Label(tk4, width=10, borderwidth=2, relief='ridge', bg='black', fg='white', text="Nature de gestion",
                  anchor='w')
        e.grid(row=0, column=11)
        e = Label(tk4, width=10, borderwidth=2, relief='ridge', bg='black', fg='white', text="Date mise sur le marché",
                  anchor='w')
        e.grid(row=0, column=12)
        e = Label(tk4, width=10, borderwidth=2, relief='ridge', bg='black', fg='white', text="Prix du bien", anchor='w')
        e.grid(row=0, column=13)

        i = 1  # row value inside the loop
        for Biens in r_set:
            for j in range(len(Biens)):
                e = Label(tk4, width=10, borderwidth=2, relief='ridge', fg='blue', text=Biens[j], anchor='w')
                e.grid(row=i, column=j)
                e.place()
            i = i + 1

    Button(tk3, text="Retour", command=tk3.destroy).place(x="200", y="520")
    Button(tk3, text="Rechercher", command=conn).place(x="100", y="520")
    tk3.mainloop()


############
############
############
############

# Partie Enregistrement
# fonction pour afficher l'interface de l'enregistrement du bien


def enregistrement():
    # Toplevel object which will
    # be treated as a new window
    tk2 = Toplevel(tk1)
    tk2.geometry("700x700")
    tk2.title("Enregistrement de biens")

    cal = Calendar(tk2, selectmode='day',
                   year=2023, month=2,
                   day=28)
    date = Label(tk2, text="Date de mise sur le marché :")
    date.place(x='50', y='60')
    cal.place(x='250', y='10')

    # SpinBox pour la superficie du bien
    Label(tk2, text="Superficie du bien :").place(x='50', y='220')
    s = tk.Spinbox(tk2, from_=0, to=10000000)
    s.place(x='250', y='220')

    # entrée construction
    Label(tk2, text="Année de construction :").place(x='50', y='270')
    val1 = tk.StringVar()
    val1.set("texte par défaut")
    entree1 = tk.Entry(tk2, textvariable=val1, width=30)
    entree1.place(x='250', y='270')

    # Nature vente ou location
    Label(tk2, text="Nature :").place(x='50', y='320')
    val = StringVar()
    val.set("Vente")
    Radiobutton(tk2, text="Vente", variable=val, value="Vente").place(x='250', y='320')
    Radiobutton(tk2, text="Location", variable=val, value="Location").place(x='320', y='320')

    # nb de pieces
    Label(tk2, text="Nombre de pièces :").place(x='50', y='370')
    val2 = StringVar()
    val2.set("texte par défaut")
    entree2 = Entry(tk2, textvariable=val2, width=30)
    entree2.place(x='250', y='370')

    # ADRESSE
    Label(tk2, text="Adresse :").place(x="50", y="420")
    val3 = StringVar()
    val3.set("code postal")
    entree3 = Entry(tk2, textvariable=val3, width=10)
    entree3.place(x='250', y='420')

    # liste deroulante pour Type de voie
    typrue = ttk.Combobox(tk2, width=10)
    typrue['values'] = ('RUE',
                        'IMPASSE',
                        'Avenue',
                        'Boulevard',
                        'ALLEE',
                        'PLACE')
    typrue.set("RUE")
    typrue.place(x='320', y='420')

    # CODEPOSTALE
    val5 = StringVar()
    val4 = StringVar()
    val6 = StringVar()
    val4.set("Numero")
    entree4 = Entry(tk2, textvariable=val4, width=10)
    entree4.place(x='410', y='420')
    entree5 = Entry(tk2, textvariable=val5, width=10)
    entree5.place(x='480', y='420')
    val5.set("adresse")
    entree6 = Entry(tk2, textvariable=val6, width=10)
    val6.set("commune")
    entree6.place(x="550", y="420")

    # Liste deroulante pour classe energitique
    Label(tk2, text="Classe énergitique :").place(x='50', y='470')
    clsenerg = ttk.Combobox(tk2, width=10)
    clsenerg['values'] = ('A',
                          'B',
                          'C',
                          'D')
    clsenerg.set("A")

    clsenerg.place(x='250', y='470')

    def on_radio_select():
        if val4.get() == "Maison":
            entree7.place(x=500, y=570)
        else:
            entree7.place_forget()

    # Nature du bien
    Label(tk2, text="Nature du bien :").place(x='50', y='520')
    val4 = StringVar()
    val4.set("Maison")
    Radiobutton(tk2, text="Maison", variable=val4, value="Maison", command=on_radio_select).place(x='250', y='520')
    Radiobutton(tk2, text="Appartement", variable=val4, value="Appartement", command=on_radio_select).place(x='320',
                                                                                                            y='520')

    # superficie jardin
    label = Label(tk2, text="Superficie Jardin : ")
    label.place(x=380, y=570)
    val5 = StringVar()
    entree7 = Entry(tk2, textvariable=val5, width=10)
    entree7.place(x=500, y=570)

    def show_hide_label():
        if val4.get() == "Maison":
            label.place(x=380, y=570)
        else:
            label.place_forget()

    # call show_hide_label when the radio button selection changes
    val4.trace("w", lambda *args: show_hide_label())

    # Prix du bien
    Label(tk2, text="Prix du bien : ").place(x=50, y=570)
    val6 = StringVar()
    entree8 = Entry(tk2, textvariable=val6, width=20)
    entree8.place(x=250, y=570)

    def validdata():
        date_mise_sur_marche = cal.get_date()
        prix = entree8.get()
        superficie_jardin = entree7.get()
        type_bien = val4.get()
        classe_energetique = clsenerg.get()
        adresse_numero = entree4.get()
        adresse_nom = entree5.get()
        adresse_commune = entree6.get()
        adresse_type = typrue.get()
        adresse_code_postal = entree3.get()
        nombre_pieces = entree2.get()
        nature_gestion = val.get()
        annee_construction = entree1.get()
        superficie_couverte = s.get()

        my_conn = sqlite3.connect('gestionbien.db')
        my_data = (None, type_bien, adresse_numero, adresse_type, adresse_nom, adresse_code_postal, adresse_commune,
                   superficie_couverte, superficie_jardin, nombre_pieces, classe_energetique, annee_construction,
                   nature_gestion, date_mise_sur_marche, prix)
        my_query = "INSERT INTO Biens values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
        my_conn.execute(my_query, my_data)
        my_conn.commit()
        messagebox.showinfo("Succés", "Le bien est enregistré avec succés")

    b1 = Button(tk2, text="Retour", command=tk2.destroy)
    b1.place(x="400", y="600")
    b2 = Button(tk2, text="Enregistrer", command=validdata)
    b2.place(x="300", y="600")

    tk2.mainloop()


# bouton de sortie
Button(tk1, text="Fermer", command=quit).pack()
tk1['bg'] = 'gray'

# boutton de recherche
Button(tk1, text='Recherche des biens', command=recherche).pack(side=LEFT, padx=5, pady=5)

# boutton d'enregistrement
Button(tk1, text='Enregistrement des biens', command=enregistrement).pack(side=RIGHT, padx=5, pady=5)

tk1.mainloop()
