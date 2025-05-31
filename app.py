import streamlit as st
import sqlite3
import pandas as pd
from datetime import date

# Connexion à la base de données SQLite
conn = sqlite3.connect("hotel.db")
c = conn.cursor()

# Création des tables si elles n'existent pas déjà
def create_tables():
    c.execute('''CREATE TABLE IF NOT EXISTS Client (
        idClient INTEGER PRIMARY KEY AUTOINCREMENT,
        adresse TEXT, ville TEXT, codePostal INTEGER, 
        email TEXT, telephone TEXT, nomComplet TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS Reservation (
        idReservation INTEGER PRIMARY KEY AUTOINCREMENT,
        dateDebut DATE, dateFin DATE, idClient INTEGER,
        FOREIGN KEY(idClient) REFERENCES Client(idClient))''')

    c.execute('''CREATE TABLE IF NOT EXISTS Chambre (
        idChambre INTEGER PRIMARY KEY,
        numero INTEGER, etage INTEGER, estReserve BOOLEAN,
        idType INTEGER, idHotel INTEGER)''')
    conn.commit()

# Afficher les clients
def show_clients():
    clients = pd.read_sql("SELECT * FROM Client", conn)
    st.dataframe(clients)

# Afficher les réservations
def show_reservations():
    reservations = pd.read_sql("SELECT * FROM Reservation", conn)
    st.dataframe(reservations)

# Ajouter un client
def add_client():
    with st.form("Ajouter un client"):
        nom = st.text_input("Nom complet")
        adresse = st.text_input("Adresse")
        ville = st.text_input("Ville")
        code_postal = st.number_input("Code Postal", step=1)
        email = st.text_input("Email")
        telephone = st.text_input("Téléphone")
        submitted = st.form_submit_button("Ajouter")
        if submitted:
            c.execute("INSERT INTO Client (nomComplet, adresse, ville, codePostal, email, telephone) VALUES (?, ?, ?, ?, ?, ?)",
                      (nom, adresse, ville, code_postal, email, telephone))
            conn.commit()
            st.success("Client ajouté avec succès.")

# Ajouter une réservation
def add_reservation():
    clients = pd.read_sql("SELECT idClient, nomComplet FROM Client", conn)
    client_id = st.selectbox("Client", clients["idClient"], format_func=lambda x: clients[clients["idClient"] == x]["nomComplet"].values[0])
    date_debut = st.date_input("Date de début", date.today())
    date_fin = st.date_input("Date de fin", date.today())
    if st.button("Ajouter la réservation"):
        c.execute("INSERT INTO Reservation (dateDebut, dateFin, idClient) VALUES (?, ?, ?)",
                  (date_debut, date_fin, client_id))
        conn.commit()
        st.success("Réservation ajoutée.")

# Liste des chambres disponibles (exemple statique)
def show_available_rooms():
    st.write("Fonction à implémenter : liste des chambres disponibles entre deux dates.")

# Interface Streamlit principale
st.title("Gestion Hôtelière")
menu = st.sidebar.selectbox("Menu", ["Afficher les clients", "Afficher les réservations", "Ajouter un client", "Ajouter une réservation", "Chambres disponibles"])

create_tables()

if menu == "Afficher les clients":
    show_clients()
elif menu == "Afficher les réservations":
    show_reservations()
elif menu == "Ajouter un client":
    add_client()
elif menu == "Ajouter une réservation":
    add_reservation()
elif menu == "Chambres disponibles":
    show_available_rooms()