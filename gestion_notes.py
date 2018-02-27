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
    :return: ([(str, float)])
    
    CU: Les notes du fichier doivent être de la forme NIP <SEPARATEUR> NOTE
    
    Exemples:
    >>> lire_liste_notes("data\\petite_notes_info.csv")
    [('90000003', 16.0), ('11505350', 14.0), ('11503156', 11.3), ('11503442', 10.2), ('11400130', 0.0), ('11504200', 4.1), ('11403526', 12.3), ('11502148', 11.8), ('11501693', 11.1), ('90000004', 20.0), ('99990125', 12.2), ('99990179', 9.0), ('11402978', 10.4), ('90000002', 0.0)]
    >>> lire_liste_notes("data\\petite_notes_maths.csv")
    [('90000003', 5.5), ('11503156', 15.1), ('11500571', 10.2), ('11402978', 14.2), ('99990125', 11.8), ('11400130', 9.6), ('11403526', 10.3), ('11502148', 10.7), ('99990179', 7.5), ('11503188', 11.2), ('11503442', 8.2), ('11505350', 4.4), ('90000002', 0.0), ('90000004', 20.0)]

    """
    try:
        assert os.path.isfile(fichier), "fichier inexistant"
        with open(fichier, "r") as canal_fichier:
            lignes = [ligne.rstrip("\n") for ligne in canal_fichier.readlines()]
        notes = []
        for ligne in lignes:
            ligne_split = ligne.split(SEPARATEUR)
            notes.append((ligne_split[0], float(ligne_split[1])))
        return notes
    
    except AssertionError as erreur:
        print(erreur)
    except ValueError:
        print("Note du mauvais format (devrait être un nombre à point flottant")
        
        
# On choisit un dictionnaire pour les notes comme cela il est beaucoup plus 
# rapide de se référer à une note précise juste en donnant le nom de l'UE.

def lire_liste_etudiants(fichier):
    """
    Renvoie la liste des étudiants décrits dans ce fichier, chaque étudiant étant représenté par un sextuplet
    :param fichier: (str)
    :return: ([(str, str, str, str, str, dict)]) [(NIP, NOM, PRENOM, PROFIL, GROUPE, NOTES)]
    CU: any
    
    Exemples:
    >>> lire_liste_etudiants("data\\petite_liste_etudiants.csv")
    [('99990179', 'HOUTEKIET', 'THOMAS', 'SESI', '53', {'maths': None, 'info': None}), ('11500571', 'SPROCQ ', 'SIMON', 'SESI', '11', {'maths': None, 'info': None}), ('90000002', 'CALBUTH', 'RAYMOND', 'SESI', '16', {'maths': None, 'info': None}), ('11403526', 'SBAI', 'WISSEM', 'SESI', '14', {'maths': None, 'info': None}), ('11502148', 'WATRELOS ', 'JEREMY', 'SESI', '34', {'maths': None, 'info': None}), ('11402978', 'SOETE', 'CEDRIC', 'SESI', '34', {'maths': None, 'info': None}), ('11505350', 'NGUESSAN', 'MODJUE NOEMIE', 'SESI', '13', {'maths': None, 'info': None}), ('11501693', 'VANOVERBERGHE ', 'CORENTIN', 'SESI', '22', {'maths': None, 'info': None}), ('11503188', 'DELOBELLE TOUSSAINT', 'MATTHIEU', 'PEIP', '15', {'maths': None, 'info': None}), ('11400130', 'SOUAISSA', 'AMZA', 'MASS', '2', {'maths': None, 'info': None}), ('99990125', 'PERON', 'BENJAMIN', 'SESI', '41', {'maths': None, 'info': None}), ('90000004', 'CALBUTH', 'RAYMOND', 'SESI', '15', {'maths': None, 'info': None}), ('90000001', 'CALBUTH', 'RAYMOND', 'LICAM', '1', {'maths': None, 'info': None}), ('11504200', 'GUILLON ', 'DAVID', 'SESI', '22', {'maths': None, 'info': None}), ('90000003', 'CALBUTH', 'MONIQUE', 'PEIP', '12', {'maths': None, 'info': None}), ('11503442', 'BEAU', 'CORENTIN', 'PEIP', '13', {'maths': None, 'info': None}), ('11503156', 'NAGET', 'ARTHUR', 'SESI', '42', {'maths': None, 'info': None})]

    """
    try:
        assert os.path.isfile(fichier), "fichier inexistant"
        with open(fichier, "r") as canal_fichier:
            lignes = [ligne.rstrip("\n") for ligne in canal_fichier.readlines()]
        liste_etudiants = []
        for ligne in lignes:
            ligne_split = ligne.split(SEPARATEUR)
            assert ligne_split[2] in PROFILS, "Profil non reconnu"
            nom, prenom = ligne_split[1].split("- ")
            notes = {}
            for UE in UES:
                notes[UE] = None
            liste_etudiants.append((ligne_split[0], nom, prenom, PROFILS[ligne_split[2]], ligne_split[3], notes))
        return liste_etudiants
    except AssertionError as error:
        print(error)
            

if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS, verbose=False)

    
#print(lire_liste_notes("data\\petite_notes_{0}.csv".format(UES[1])))
#print(lire_liste_etudiants("data\\petite_liste_etudiants.csv"))