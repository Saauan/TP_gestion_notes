"""
Script python permettant de gérer les notes d'une promo étdudiante

Usage : ./gestion_notes.py <ue1> <ue2> ...
        <ue1> <ue2> ... sont les noms des UE dont il faut reporter les notes.
        
CU : il faut un fichier de nom notes_<ue>.csv par ue présent dans le dossier data
     et un fichier d'étudiants de nom liste_etudiants.csv

:Date: 2018-02-28
:Dernière Révision: 2018-02-28
:Auteurs:
    - Tristan Coignion
    - Logan Becquembois
"""

from functools import cmp_to_key
import sys
import os.path

UES = ["maths", "info"] # Uncomment si on n'utilise pas le script
PROFILS = {'1' : 'SESI',
           '2' : 'PEIP',
           '3' : 'MASS',
           '4' : 'LICAM'}
SEPARATEUR = '|'
MENTIONS = ["Absent", "Ajourné", "Passable", "AB", "B", "TB"]

def lire_liste_notes(fichier):
    """
    Renvoie la liste des notes contenues dans ce fichier, chaque note étant représentée par un couple.
    
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
        if not os.path.isfile(fichier):
            raise FileNotFoundError
        with open(fichier, "r") as canal_fichier:
            lignes = [ligne.rstrip("\n") for ligne in canal_fichier.readlines()]
        notes = []
        for ligne in lignes:
            ligne_split = ligne.split(SEPARATEUR)
            notes.append((ligne_split[0], float(ligne_split[1])))
        return notes
    
    except FileNotFoundError:
        print("Fichier {0} inexistant".format(fichier))
    except ValueError:
        print("Note du mauvais format (devrait être un nombre à point flottant") # On sait JAMAIS
        
        
# On choisit un dictionnaire pour les notes comme cela il est beaucoup plus 
# rapide de se référer à une note précise juste en donnant le nom de l'UE.

def lire_liste_etudiants(fichier):
    """
    Renvoie la liste des étudiants décrits dans ce fichier, chaque étudiant étant représenté par un sextuplet.
    
    :param fichier: (str) le nom ou chemin du fichier
    :return: ([(str, str, str, str, str, dict)]) [(NIP, NOM, PRENOM, PROFIL, GROUPE, NOTES)]
    
    CU: any
    
    Exemples:
    
    >>> lire_liste_etudiants("data\\petite_liste_etudiants.csv")
    [('99990179', 'HOUTEKIET', 'THOMAS', 'SESI', '53', {'maths': None, 'info': None}), ('11500571', 'SPROCQ ', 'SIMON', 'SESI', '11', {'maths': None, 'info': None}), ('90000002', 'CALBUTH', 'RAYMOND', 'SESI', '16', {'maths': None, 'info': None}), ('11403526', 'SBAI', 'WISSEM', 'SESI', '14', {'maths': None, 'info': None}), ('11502148', 'WATRELOS ', 'JEREMY', 'SESI', '34', {'maths': None, 'info': None}), ('11402978', 'SOETE', 'CEDRIC', 'SESI', '34', {'maths': None, 'info': None}), ('11505350', 'NGUESSAN', 'MODJUE NOEMIE', 'SESI', '13', {'maths': None, 'info': None}), ('11501693', 'VANOVERBERGHE ', 'CORENTIN', 'SESI', '22', {'maths': None, 'info': None}), ('11503188', 'DELOBELLE TOUSSAINT', 'MATTHIEU', 'PEIP', '15', {'maths': None, 'info': None}), ('11400130', 'SOUAISSA', 'AMZA', 'MASS', '2', {'maths': None, 'info': None}), ('99990125', 'PERON', 'BENJAMIN', 'SESI', '41', {'maths': None, 'info': None}), ('90000004', 'CALBUTH', 'RAYMOND', 'SESI', '15', {'maths': None, 'info': None}), ('90000001', 'CALBUTH', 'RAYMOND', 'LICAM', '1', {'maths': None, 'info': None}), ('11504200', 'GUILLON ', 'DAVID', 'SESI', '22', {'maths': None, 'info': None}), ('90000003', 'CALBUTH', 'MONIQUE', 'PEIP', '12', {'maths': None, 'info': None}), ('11503442', 'BEAU', 'CORENTIN', 'PEIP', '13', {'maths': None, 'info': None}), ('11503156', 'NAGET', 'ARTHUR', 'SESI', '42', {'maths': None, 'info': None})]

    """
    try:
        if not os.path.isfile(fichier):
            raise FileNotFoundError
        with open(fichier, "r") as canal_fichier:
            lignes = [ligne.rstrip("\n") for ligne in canal_fichier.readlines()]
        liste_etudiants = []
        for ligne in lignes:
            ligne_split = ligne.split(SEPARATEUR)
            if not ligne_split[2] in PROFILS:
                raise NameError
            nom, prenom = ligne_split[1].split("- ")
            notes = {}
            for UE in UES:
                notes[UE] = None
            liste_etudiants.append((ligne_split[0], nom, prenom, PROFILS[ligne_split[2]], ligne_split[3], notes))
        return liste_etudiants
    except FileNotFoundError:
        print("fichier {0} inexistant".format(fichier))
    except NameError:
        print("Le profil n'a pas été reconnu")
            

def reporter_notes1(UE, liste_etudiants, liste_notes):
    """
    Modifie les étudiants de la liste en reportant la note trouvée dans la liste de notes s'ils en ont une.
    Utilise la méthode de recherche séquentielle, sans aucun prétraitement.

    :param UE: (str) l'UE de laquelle on veut reporter les notes
    :param liste_etudiants: (list) une liste d'étudiants valide (NIP, NOM, PRENOM, PROFIL, GROUPE, NOTES)
    :param liste_notes: (list) une liste de notes valide (couples NIP, note) dans une UE
    :return: None
    
    CU: any
    
    Exemple:
    
    >>> liste_etudiants = lire_liste_etudiants("data\\petite_liste_etudiants.csv")
    >>> reporter_notes1(UES[1], liste_etudiants, lire_liste_notes("data\\petite_notes_info.csv"))
    >>> reporter_notes1(UES[0], liste_etudiants, lire_liste_notes("data\\petite_notes_maths.csv"))
    >>> print(liste_etudiants)
    [('99990179', 'HOUTEKIET', 'THOMAS', 'SESI', '53', {'maths': 7.5, 'info': 9.0}), ('11500571', 'SPROCQ ', 'SIMON', 'SESI', '11', {'maths': 10.2, 'info': None}), ('90000002', 'CALBUTH', 'RAYMOND', 'SESI', '16', {'maths': 0.0, 'info': 0.0}), ('11403526', 'SBAI', 'WISSEM', 'SESI', '14', {'maths': 10.3, 'info': 12.3}), ('11502148', 'WATRELOS ', 'JEREMY', 'SESI', '34', {'maths': 10.7, 'info': 11.8}), ('11402978', 'SOETE', 'CEDRIC', 'SESI', '34', {'maths': 14.2, 'info': 10.4}), ('11505350', 'NGUESSAN', 'MODJUE NOEMIE', 'SESI', '13', {'maths': 4.4, 'info': 14.0}), ('11501693', 'VANOVERBERGHE ', 'CORENTIN', 'SESI', '22', {'maths': None, 'info': 11.1}), ('11503188', 'DELOBELLE TOUSSAINT', 'MATTHIEU', 'PEIP', '15', {'maths': 11.2, 'info': None}), ('11400130', 'SOUAISSA', 'AMZA', 'MASS', '2', {'maths': 9.6, 'info': 0.0}), ('99990125', 'PERON', 'BENJAMIN', 'SESI', '41', {'maths': 11.8, 'info': 12.2}), ('90000004', 'CALBUTH', 'RAYMOND', 'SESI', '15', {'maths': 20.0, 'info': 20.0}), ('90000001', 'CALBUTH', 'RAYMOND', 'LICAM', '1', {'maths': None, 'info': None}), ('11504200', 'GUILLON ', 'DAVID', 'SESI', '22', {'maths': None, 'info': 4.1}), ('90000003', 'CALBUTH', 'MONIQUE', 'PEIP', '12', {'maths': 5.5, 'info': 16.0}), ('11503442', 'BEAU', 'CORENTIN', 'PEIP', '13', {'maths': 8.2, 'info': 10.2}), ('11503156', 'NAGET', 'ARTHUR', 'SESI', '42', {'maths': 15.1, 'info': 11.3})]
    """
    for couple_note in liste_notes:
        for etudiant in liste_etudiants:
            if etudiant[0] == couple_note[0]:
                etudiant[5][UE] = couple_note[1]


def reporter_notes2(UE, liste_etudiants, liste_notes):
    """
    Modifie les étudiants de la liste en reportant la note trouvée dans la liste de notes s'ils en ont une. La liste_etudiants est supposée prétriée par ordre de NIP croissants.
    Utilise la recherche par dichotomie.
    
    :param UE: (str) l'UE de laquelle on veut reporter les notes
    :param liste_etudiants: (list) une liste d'étudiants valide (NIP, NOM, PRENOM, PROFIL, GROUPE, NOTES)
    :param liste_notes: (list) une liste de notes valide (couples NIP, note) dans une UE
    :return: None
    
    CU: any
    
    Exemple:
    
    >>> liste_etudiants = lire_liste_etudiants("data\\petite_liste_etudiants.csv")
    >>> liste_etudiants.sort()
    >>> reporter_notes2(UES[1], liste_etudiants, lire_liste_notes("data\\petite_notes_info.csv"))
    >>> reporter_notes2(UES[0], liste_etudiants, lire_liste_notes("data\\petite_notes_maths.csv"))
    >>> print(liste_etudiants)
    [('11400130', 'SOUAISSA', 'AMZA', 'MASS', '2', {'maths': 9.6, 'info': 0.0}), ('11402978', 'SOETE', 'CEDRIC', 'SESI', '34', {'maths': 14.2, 'info': 10.4}), ('11403526', 'SBAI', 'WISSEM', 'SESI', '14', {'maths': 10.3, 'info': 12.3}), ('11500571', 'SPROCQ ', 'SIMON', 'SESI', '11', {'maths': 10.2, 'info': None}), ('11501693', 'VANOVERBERGHE ', 'CORENTIN', 'SESI', '22', {'maths': None, 'info': 11.1}), ('11502148', 'WATRELOS ', 'JEREMY', 'SESI', '34', {'maths': 10.7, 'info': 11.8}), ('11503156', 'NAGET', 'ARTHUR', 'SESI', '42', {'maths': 15.1, 'info': 11.3}), ('11503188', 'DELOBELLE TOUSSAINT', 'MATTHIEU', 'PEIP', '15', {'maths': 11.2, 'info': None}), ('11503442', 'BEAU', 'CORENTIN', 'PEIP', '13', {'maths': 8.2, 'info': 10.2}), ('11504200', 'GUILLON ', 'DAVID', 'SESI', '22', {'maths': None, 'info': 4.1}), ('11505350', 'NGUESSAN', 'MODJUE NOEMIE', 'SESI', '13', {'maths': 4.4, 'info': 14.0}), ('90000001', 'CALBUTH', 'RAYMOND', 'LICAM', '1', {'maths': None, 'info': None}), ('90000002', 'CALBUTH', 'RAYMOND', 'SESI', '16', {'maths': 0.0, 'info': 0.0}), ('90000003', 'CALBUTH', 'MONIQUE', 'PEIP', '12', {'maths': 5.5, 'info': 16.0}), ('90000004', 'CALBUTH', 'RAYMOND', 'SESI', '15', {'maths': 20.0, 'info': 20.0}), ('99990125', 'PERON', 'BENJAMIN', 'SESI', '41', {'maths': 11.8, 'info': 12.2}), ('99990179', 'HOUTEKIET', 'THOMAS', 'SESI', '53', {'maths': 7.5, 'info': 9.0})]

    """
    
    for couple_note in liste_notes:
        a, b = 0, len(liste_etudiants)-1
        while True:
            NIP_etudiant = liste_etudiants[(a+b)//2][0]
            if NIP_etudiant < couple_note[0]:
                a = (a+b)//2 + 1
            elif NIP_etudiant > couple_note[0]:
                b = (a+b)//2 - 1
            else:
                liste_etudiants[(a+b)//2][5][UE] = couple_note[1]
                break

def reporter_notes3(UE, liste_etudiants, liste_notes):
    """
    Modifie les étudiants de la liste en reportant la note trouvée dans la liste de notes s'ils en ont une. La liste_etudiants et la liste_note sont supposés prétriés par ordre de NIP croissants.
    Utilise une méthode d'avancement en parallèle dans chacune des deux listes.
    
    :param UE: (str) l'UE de laquelle on veut reporter les notes
    :param liste_etudiants: (list) une liste d'étudiants valide (NIP, NOM, PRENOM, PROFIL, GROUPE, NOTES)
    :param liste_notes: (list) une liste de notes valide (couples NIP, note) dans une UE
    :return: None
    
    CU: any
    
    Exemple:
    
    >>> liste_etudiants = lire_liste_etudiants("data\\petite_liste_etudiants.csv")
    >>> liste_etudiants.sort()
    >>> reporter_notes3(UES[1], liste_etudiants, sorted(lire_liste_notes("data\\petite_notes_info.csv")))
    >>> reporter_notes3(UES[0], liste_etudiants, sorted(lire_liste_notes("data\\petite_notes_maths.csv")))
    >>> print(liste_etudiants)
    [('11400130', 'SOUAISSA', 'AMZA', 'MASS', '2', {'maths': 9.6, 'info': 0.0}), ('11402978', 'SOETE', 'CEDRIC', 'SESI', '34', {'maths': 14.2, 'info': 10.4}), ('11403526', 'SBAI', 'WISSEM', 'SESI', '14', {'maths': 10.3, 'info': 12.3}), ('11500571', 'SPROCQ ', 'SIMON', 'SESI', '11', {'maths': 10.2, 'info': None}), ('11501693', 'VANOVERBERGHE ', 'CORENTIN', 'SESI', '22', {'maths': None, 'info': 11.1}), ('11502148', 'WATRELOS ', 'JEREMY', 'SESI', '34', {'maths': 10.7, 'info': 11.8}), ('11503156', 'NAGET', 'ARTHUR', 'SESI', '42', {'maths': 15.1, 'info': 11.3}), ('11503188', 'DELOBELLE TOUSSAINT', 'MATTHIEU', 'PEIP', '15', {'maths': 11.2, 'info': None}), ('11503442', 'BEAU', 'CORENTIN', 'PEIP', '13', {'maths': 8.2, 'info': 10.2}), ('11504200', 'GUILLON ', 'DAVID', 'SESI', '22', {'maths': None, 'info': 4.1}), ('11505350', 'NGUESSAN', 'MODJUE NOEMIE', 'SESI', '13', {'maths': 4.4, 'info': 14.0}), ('90000001', 'CALBUTH', 'RAYMOND', 'LICAM', '1', {'maths': None, 'info': None}), ('90000002', 'CALBUTH', 'RAYMOND', 'SESI', '16', {'maths': 0.0, 'info': 0.0}), ('90000003', 'CALBUTH', 'MONIQUE', 'PEIP', '12', {'maths': 5.5, 'info': 16.0}), ('90000004', 'CALBUTH', 'RAYMOND', 'SESI', '15', {'maths': 20.0, 'info': 20.0}), ('99990125', 'PERON', 'BENJAMIN', 'SESI', '41', {'maths': 11.8, 'info': 12.2}), ('99990179', 'HOUTEKIET', 'THOMAS', 'SESI', '53', {'maths': 7.5, 'info': 9.0})]
    """
    last_index = 0
    for couple_note in liste_notes:
        while liste_etudiants[last_index][0] != couple_note[0]:
            last_index += 1
        liste_etudiants[last_index][5][UE] = couple_note[1]
        last_index += 1

def liste_en_dico(liste):
    """
    Renvoie un dictionnaire qui possède comme clé un NIP et comme valeur un tuple de la fiche étudiante qui lui correspond
    
    :param liste: (list) une liste étudiante
    :return: none
    
    Exemple:
    
    >>> liste_etudiants = lire_liste_etudiants("data\\petite_liste_etudiants.csv")
    >>> liste_en_dico(liste_etudiants)
    {'99990179': ('HOUTEKIET', 'THOMAS', 'SESI', '53', {'maths': None, 'info': None}), '11500571': ('SPROCQ ', 'SIMON', 'SESI', '11', {'maths': None, 'info': None}), '90000002': ('CALBUTH', 'RAYMOND', 'SESI', '16', {'maths': None, 'info': None}), '11403526': ('SBAI', 'WISSEM', 'SESI', '14', {'maths': None, 'info': None}), '11502148': ('WATRELOS ', 'JEREMY', 'SESI', '34', {'maths': None, 'info': None}), '11402978': ('SOETE', 'CEDRIC', 'SESI', '34', {'maths': None, 'info': None}), '11505350': ('NGUESSAN', 'MODJUE NOEMIE', 'SESI', '13', {'maths': None, 'info': None}), '11501693': ('VANOVERBERGHE ', 'CORENTIN', 'SESI', '22', {'maths': None, 'info': None}), '11503188': ('DELOBELLE TOUSSAINT', 'MATTHIEU', 'PEIP', '15', {'maths': None, 'info': None}), '11400130': ('SOUAISSA', 'AMZA', 'MASS', '2', {'maths': None, 'info': None}), '99990125': ('PERON', 'BENJAMIN', 'SESI', '41', {'maths': None, 'info': None}), '90000004': ('CALBUTH', 'RAYMOND', 'SESI', '15', {'maths': None, 'info': None}), '90000001': ('CALBUTH', 'RAYMOND', 'LICAM', '1', {'maths': None, 'info': None}), '11504200': ('GUILLON ', 'DAVID', 'SESI', '22', {'maths': None, 'info': None}), '90000003': ('CALBUTH', 'MONIQUE', 'PEIP', '12', {'maths': None, 'info': None}), '11503442': ('BEAU', 'CORENTIN', 'PEIP', '13', {'maths': None, 'info': None}), '11503156': ('NAGET', 'ARTHUR', 'SESI', '42', {'maths': None, 'info': None})}

    """
    dict_etudiants = {}
    for etudiant in liste:
        dict_etudiants[etudiant[0]] = etudiant[1:]
    return dict_etudiants

def reporter_notes4(UE, liste_etudiants, liste_notes):
    """
    Modifie les étudiants de la liste en reportant la note trouvée dans la liste de notes s'ils en ont une.
    Utilise la fonction liste_en_dico.
    
    :param UE: (str) l'UE de laquelle on veut reporter les notes
    :param liste_etudiants: (list) une liste d'étudiants valide (NIP, NOM, PRENOM, PROFIL, GROUPE, NOTES)
    :param liste_notes: (list) une liste de notes valide (couples NIP, note) dans une UE
    :return: None
    
    CU: any
    
    Exemple:
    
    >>> liste_etudiants = lire_liste_etudiants("data\\petite_liste_etudiants.csv")
    >>> reporter_notes4(UES[1], liste_etudiants, lire_liste_notes("data\\petite_notes_info.csv"))
    >>> reporter_notes4(UES[0], liste_etudiants, lire_liste_notes("data\\petite_notes_maths.csv"))
    >>> print(liste_etudiants)
    [('99990179', 'HOUTEKIET', 'THOMAS', 'SESI', '53', {'maths': 7.5, 'info': 9.0}), ('11500571', 'SPROCQ ', 'SIMON', 'SESI', '11', {'maths': 10.2, 'info': None}), ('90000002', 'CALBUTH', 'RAYMOND', 'SESI', '16', {'maths': 0.0, 'info': 0.0}), ('11403526', 'SBAI', 'WISSEM', 'SESI', '14', {'maths': 10.3, 'info': 12.3}), ('11502148', 'WATRELOS ', 'JEREMY', 'SESI', '34', {'maths': 10.7, 'info': 11.8}), ('11402978', 'SOETE', 'CEDRIC', 'SESI', '34', {'maths': 14.2, 'info': 10.4}), ('11505350', 'NGUESSAN', 'MODJUE NOEMIE', 'SESI', '13', {'maths': 4.4, 'info': 14.0}), ('11501693', 'VANOVERBERGHE ', 'CORENTIN', 'SESI', '22', {'maths': None, 'info': 11.1}), ('11503188', 'DELOBELLE TOUSSAINT', 'MATTHIEU', 'PEIP', '15', {'maths': 11.2, 'info': None}), ('11400130', 'SOUAISSA', 'AMZA', 'MASS', '2', {'maths': 9.6, 'info': 0.0}), ('99990125', 'PERON', 'BENJAMIN', 'SESI', '41', {'maths': 11.8, 'info': 12.2}), ('90000004', 'CALBUTH', 'RAYMOND', 'SESI', '15', {'maths': 20.0, 'info': 20.0}), ('90000001', 'CALBUTH', 'RAYMOND', 'LICAM', '1', {'maths': None, 'info': None}), ('11504200', 'GUILLON ', 'DAVID', 'SESI', '22', {'maths': None, 'info': 4.1}), ('90000003', 'CALBUTH', 'MONIQUE', 'PEIP', '12', {'maths': 5.5, 'info': 16.0}), ('11503442', 'BEAU', 'CORENTIN', 'PEIP', '13', {'maths': 8.2, 'info': 10.2}), ('11503156', 'NAGET', 'ARTHUR', 'SESI', '42', {'maths': 15.1, 'info': 11.3})]
    """
    dict_etudiants = liste_en_dico(liste_etudiants)
    for couple_note in liste_notes:
        dict_etudiants[couple_note[0]][4][UE] = couple_note[1]
    # Quand on modifie les valeurs de dict_etudiants, les valeurs associées dans liste_etudiants sont également modifiée
    # Il est alors non nécessaire de transformer dict_etudiants en liste après le report

def resultat(note_etudiant):
    """
    Renvoie un couple (moyenne, mention) correspondant aux notes d'un étudiant
    
    :param note_etudiant: (dict) un dictionnaire contenant les notes d'un étudiant
    :return: ((float, str)) le couple (moyenne, mention)
    
    CU: Utilise la constante MENTIONS
    
    Exemples:
    
    >>> resultat ({'maths': None, 'info': None})
    (None, 'Absent')
    >>> resultat ({'maths': 12, 'info': None})
    (6.0, 'Ajourné')
    >>> resultat ({'maths': None, 'info': 15})
    (7.5, 'Ajourné')
    >>> resultat ({'maths': 9, 'info': 12})
    (10.5, 'Passable')
    >>> resultat ({'maths': 15, 'info': 12})
    (13.5, 'AB')
    >>> resultat ({'maths': 15, 'info': 16})
    (15.5, 'B')
    >>> resultat ({'maths': 18, 'info': 16})
    (17.0, 'TB')
    """
    somme = 0
    liste_notes = []
    for UE in note_etudiant:
        if note_etudiant[UE] != None:
            somme += note_etudiant[UE]
        else:
            liste_notes.append(note_etudiant[UE])
    
    if len(liste_notes) == len(note_etudiant):
        return (None, MENTIONS[0])
    moy = round(somme / len(note_etudiant), 3) # Arrondi 3 chiffres après la virgule 
    if moy < 10:
        mention = MENTIONS[1]
    elif moy < 12:
        mention = MENTIONS[2]
    elif moy < 14:
        mention = MENTIONS[3]
    elif moy < 16:
        mention = MENTIONS[4]
    else:
        mention = MENTIONS[5]

    return moy, mention


def compare_etudiant_admin(etudiant1, etudiant2):
    """
    Compare deux étudiants sur les critères administratifs
    
    Critères
    ========
    
    :premier critère: les étudiants doivent être regroupés par profils. Les profils apparaissent dans l’ordre lexicographique (avec notre exemple doivent figurer en premier les LICAM, puis les MASS, puis les PEIP et enfin les SESI).
    :deuxième critère: au sein d’un profil, les étudiants doivent être classés par ordre lexicographique des noms.
    :troisième critère: en cas d’homonymie (mêmes noms) c’est l’ordre lexicographique des prénoms qui compte.
    :quatrième critère: en cas d’homonymie complète (mêmes noms et prénoms [3]) c’est l’ordre lexicographique des NIP qui compte.

    Paramètres
    ==========
    :param etudiant1: (tuple) Une fiche d'étudiant
    :param etudiant2: (tuple) Une autre fiche d'étudiant
    :return: (int) -1 si etudiant1 est inférieur à étudiant2, 1 sinon. Dans des cas d'ubiquité: 0
    
    Exemple:
    
    >>> liste_etudiants = lire_liste_etudiants("data\\petite_liste_etudiants.csv")
    >>> compare_etudiant_admin(liste_etudiants[0], liste_etudiants[1])
    -1
    """
    if etudiant1[3] < etudiant2[3]: # Profil
        return -1
    if etudiant1[3] > etudiant2[3]:
        return 1
    
    if etudiant1[1] < etudiant2[1]: # Nom
        return -1
    if etudiant1[1] > etudiant2[1]:
        return 1
    
    if etudiant1[1] < etudiant2[1]: # Prénom
        return -1
    if etudiant1[1] > etudiant2[1]:
        return 1
    
    if etudiant1[0] < etudiant2[0]: # Prénom
        return -1
    if etudiant1[0] > etudiant2[0]:
        return 1
    
    return 0 # Identité parfaite. Cette personne est douée du don d'ubiquité

def trie_liste_etudiants(liste_etudiants):
    """
    Trie une liste d'étudiants en fonctions des critères administratifs de compare_etudiant_admin tout en utilisant l'algorithme du Bubble Sort
    
    :param liste_etudiants: (list) une liste de fiches d'étudiants
    :return: None
    
    CU: any
    
    Exemples:
    
    >>> liste_etudiants = lire_liste_etudiants("data\\petite_liste_etudiants.csv")
    >>> trie_liste_etudiants(liste_etudiants)
    >>> print(liste_etudiants)
        [('90000001', 'CALBUTH', 'RAYMOND', 'LICAM', '1', {'maths': None, 'info': None}), ('11400130', 'SOUAISSA', 'AMZA', 'MASS', '2', {'maths': None, 'info': None}), ('11503442', 'BEAU', 'CORENTIN', 'PEIP', '13', {'maths': None, 'info': None}), ('90000003', 'CALBUTH', 'MONIQUE', 'PEIP', '12', {'maths': None, 'info': None}), ('11503188', 'DELOBELLE TOUSSAINT', 'MATTHIEU', 'PEIP', '15', {'maths': None, 'info': None}), ('90000002', 'CALBUTH', 'RAYMOND', 'SESI', '16', {'maths': None, 'info': None}), ('90000004', 'CALBUTH', 'RAYMOND', 'SESI', '15', {'maths': None, 'info': None}), ('11504200', 'GUILLON ', 'DAVID', 'SESI', '22', {'maths': None, 'info': None}), ('99990179', 'HOUTEKIET', 'THOMAS', 'SESI', '53', {'maths': None, 'info': None}), ('11503156', 'NAGET', 'ARTHUR', 'SESI', '42', {'maths': None, 'info': None}), ('11505350', 'NGUESSAN', 'MODJUE NOEMIE', 'SESI', '13', {'maths': None, 'info': None}), ('99990125', 'PERON', 'BENJAMIN', 'SESI', '41', {'maths': None, 'info': None}), ('11403526', 'SBAI', 'WISSEM', 'SESI', '14', {'maths': None, 'info': None}), ('11402978', 'SOETE', 'CEDRIC', 'SESI', '34', {'maths': None, 'info': None}), ('11500571', 'SPROCQ ', 'SIMON', 'SESI', '11', {'maths': None, 'info': None}), ('11501693', 'VANOVERBERGHE ', 'CORENTIN', 'SESI', '22', {'maths': None, 'info': None}), ('11502148', 'WATRELOS ', 'JEREMY', 'SESI', '34', {'maths': None, 'info': None})]

    """
    swaped = True
    while swaped:
        swaped = False
        for i in range(len(liste_etudiants)-1):
            if compare_etudiant_admin(liste_etudiants[i], liste_etudiants[i+1]) == 1:
                liste_etudiants[i], liste_etudiants[i+1] = liste_etudiants[i+1], liste_etudiants[i]
                swaped = True
                
def ecrire_notes(liste_etudiants_triee):
    """
    Ecrit les notes dans un fichier "notes_etudiants.csv"
    
    :param liste_etudiants_triee: (list) une liste de fiches d'étudiants supposée triée (selon les critères administratifs)
    :return: None
    
    CU: any
    """
    with open("notes_etudiants.csv", "w") as canal_notes:
        for etudiant in liste_etudiants_triee:
            notes = [etudiant[5][UE] for UE in etudiant[5]]
            for i, note in enumerate(notes):
                if note == None:
                    notes[i] = ""
                notes[i] = str(notes[i])
            moyenne, mention = resultat(etudiant[5])
            if moyenne == None:
                moyenne = ""
            moyenne = str(moyenne)
            
            ligne = "|".join(etudiant[:5] + tuple(notes) + (moyenne, mention))
            canal_notes.write(ligne + "\n")

def usage():
    """
    Imprime une aide à l'utilisation du script

    CU: Le fichier usage.txt doit se trouver dans le même dossier que gestion_notes.py
    """
    with open("usage.txt", "r", encoding = "latin-1") as usage:
        for ligne in usage:
            print(ligne, end="")    

if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS, verbose=False)


if len(sys.argv) == 1:
    usage()
else:
    UES = []
    for i in range(1, len(sys.argv)):
        UES.append(sys.argv[i])
        
    try:
        if not os.path.isfile("data\\liste_etudiants.csv"):
            raise FileNotFoundError("data\\liste_etudiants.csv")
        liste_etudiants = lire_liste_etudiants("data\\liste_etudiants.csv")
        trie_liste_etudiants(liste_etudiants)
        for UE in UES:
            if not os.path.isfile("data\\notes_{0}.csv".format(UE)):
                raise FileNotFoundError("data\\notes_{0}.csv".format(UE))
            reporter_notes4(UE, liste_etudiants, lire_liste_notes("data\\notes_{0}.csv".format(UE)))
        ecrire_notes(liste_etudiants)
    except FileNotFoundError as fichier:
        print("Le fichier {0} n'existe pas !".format(fichier))