"""
Script python permettant de gérer les notes d'une promo étdudiante
Usage:

Auteurs: Tristan Coignion Logan Becquembois
"""

from functools import cmp_to_key
import os.path

UES = ["maths", "info"]
PROFILS = {'1' : 'SESI',
           '2' : 'PEIP',
           '3' : 'MASS',
           '4' : 'LICAM'}
SEPARATEUR = '|'
MENTIONS = ["Absent", "Ajourné", "Passable", "AB", "B", "TB"]

def lire_liste_notes(fichier):
    """
    Renvoie la liste des notes contenues dans ce fichier, chaque note étant représentée par un couple
    :param fichier: (str) le nom du fichier
    :return: ((str, float))
    
    CU: Les notes du fichier doivent être de la forme NIP <SEPARATEUR> NOTE
    
    Exemples:
    """
    try:
        assert os.path.isfile(fichier), "fichier inexistant"
        with open(fichier,"r") as canal_fichier:
            lignes = [ligne.rstrip("\n") for ligne in canal_fichier.readlines()]
            print(lignes)
        notes = []
        for ligne in lignes:
            ligne_split = ligne.split(SEPARATEUR)
            notes.append((ligne_split[0], float(ligne_split[1])))
        return notes
    except AssertionError as erreur:
        print(erreur)
    except ValueError:
        print("Note du mauvais format (devrait être un nombre à point flottant")
        
print(lire_liste_notes("data\\petite_notes_info_wrong.csv"))
        