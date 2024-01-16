####################################################- Importations -####################################################

import csv
import re
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from itertools import cycle
import pandas as pd

"""
################################################- Conversion ics ==> csv -##############################################

from csv_ical import Convert
import csv

convert = Convert()
convert.ICS_FILE_LOCATION = '/home/Etudiants/RT/BUT-RT-1/am620105/SAE 105/ADECal.ics'
convert.CSV_FILE_LOCATION = '/home/Etudiants/RT/BUT-RT-1/am620105/SAE 105/ADECal.csv'

convert.read_ical(convert.ICS_FILE_LOCATION)

convert.make_csv()
convert.save_csv(convert.CSV_FILE_LOCATION)
"""

####################################################- Mise en place -####################################################

####- Dictionaires -####
groupes_TP = {}
groupes_CM = {}
groupes_TD = {}

####- Listes -####
groupes_specifiques = ['RT1Huffman', 'RT1Turing', 'RT1App', 'RT2Hamming', 'RT2Dijkstra', 'RT1Shannon1', 'RT1Shannon2', 'RT2App', 'S1', 'S3', 'LP']
salles_TP = ["RT-Labo Electronique 1", "RT-Labo Electronique 2", "RT-Labo Informatique 1", "RT-Labo Informatique 2", "RT-Labo Informatique 3", "RT-Salle Labo Visio", "RT-Labo reseaux 2", "RT-Labo reseaux 1", "RT-Salle Info CAO", "RT-Labo Telecoms 1", "RT-Labo Telecoms 2", "BIBLIOTHEQUE UNIVERSITAIRE OU TEAMS", "GC-ISAT 111 Info"]
salles_CM = ["RT-Amphi"]
salles_TD = ["RT-Salle-TD1", "RT-Salle-TD2", "RT-Salle-TD3", "RT-Salle-TD4"]
#nous avons mis des listes avec les noms des salles pour pouvoir trier les TD, CM et TP

####################################################- Programme -########################################################

####- Ouverture Fichier -####
chemin_fichier_csv = '/home/Etudiants/RT/BUT-RT-1/am620105/SAE 105/ADECal.csv'
with open(chemin_fichier_csv, newline='') as csvfile:
   reader = csv.reader(csvfile, delimiter=',')


   for row in reader:
####- Vérifier si la ligne contient suffisamment d'informations, cela me permet de pas out of range -####
       if len(row) >= 5:
           heure_debut = datetime.fromisoformat(row[1].replace("Z", "+00:00"))
           heure_fin = datetime.fromisoformat(row[2].replace("Z", "+00:00"))
           groupes = re.findall(r'(\w+)', row[3])
           salle = row[5] if len(row) > 5 else row[4]


####- Calculer la durée du cours en H -####
           
           duree_cours = (heure_fin - heure_debut).seconds / 3600

####- trouver la classe qui appartient a salle pendant le cours -####
           
           classe = ""
           if salle in salles_TP:
               classe = "TP"
           elif salle in salles_CM:
               classe = "CM"
           elif salle in salles_TD:
               classe = "TD"


####- trie, le groupe concerné recois l'heure dans sont dico -####
           for groupe in groupes_specifiques:
               if groupe in groupes:
                   if groupe not in groupes_TP:
                       groupes_TP[groupe] = 0
                   if groupe not in groupes_CM:
                       groupes_CM[groupe] = 0
                   if groupe not in groupes_TD:
                       groupes_TD[groupe] = 0


                   if classe == "TP":
                       groupes_TP[groupe] += duree_cours
                   elif classe == "CM":
                       groupes_CM[groupe] += duree_cours
                   elif classe == "TD":
                       groupes_TD[groupe] += duree_cours

####- affiche les Résultats -####
print("Heures par groupe spécifique:")
for groupe in groupes_specifiques:
   heures_TP = groupes_TP.get(groupe, 0)
   heures_CM = groupes_CM.get(groupe, 0)
   heures_TD = groupes_TD.get(groupe, 0)
   print(f"{groupe}: TP - {heures_TP} heures, CM - {heures_CM} heures, TD - {heures_TD} heures")

####- conversion en CSV pour le CROUS -####
donnees = {
    'Groupe': ['RT1Huffman', 'RT1Turing', 'RT1App', 'RT2Hamming', 'RT2Dijkstra', 'RT1Shannon1', 'RT1Shannon2', 'RT2App', 'S1', 'S3', 'LP'],
    'TP': [346.0, 346.0, 436.5, 207.5, 209.5, 346.0, 346.0, 132.5, 0, 0.25, 146.5],
    'CM': [0, 0, 0.75, 17.0, 17.0, 0, 0, 4.0, 37.75, 8.0, 2.0],
    'TD': [34.0, 34.0, 16.0, 128.0, 126.0, 34.0, 34.0, 139.5, 0, 32.0, 74.25],
}
df = pd.DataFrame(donnees)
df.to_csv('/home/Etudiants/RT/BUT-RT-1/am620105/SAE 105/Resultats_Groupes.csv', index=False)


####################################################- Partie Graphique -########################################################

####- Données pour le Graphique -####
labels = groupes_specifiques
heures_TP = [groupes_TP.get(groupe, 0) for groupe in labels]
heures_CM = [groupes_CM.get(groupe, 0) for groupe in labels]
heures_TD = [groupes_TD.get(groupe, 0) for groupe in labels]

##################- Graphique Barre -##################

####- réglage du tableau (taille, barre, abcisse/ ordonnées, ombres, arrondis, légende, affichage) beaucoup de esthétisme -####
bar_width = 0.25
r1 = np.arange(len(labels))

r2 = [x + bar_width for x in r1]
r3 = [x + bar_width for x in r2]

fig, ax = plt.subplots(figsize=(10, 6))

ax.bar(r1, heures_TP, color='#1f78b4', width=bar_width, edgecolor='grey', label='TP', alpha=0.7)
ax.bar(r2, heures_CM, color='#33a02c', width=bar_width, edgecolor='grey', label='CM', alpha=0.7)
ax.bar(r3, heures_TD, color='#e31a1c', width=bar_width, edgecolor='grey', label='TD', alpha=0.7)

for bar_container in [ax.containers[0], ax.containers[1], ax.containers[2]]:
    for bar in bar_container:
        bar.set_edgecolor('grey')
        bar.set_linewidth(1)
        bar.set_antialiased(True)

plt.xlabel('Groupes spécifiques', fontweight='bold')
plt.xticks([r + bar_width for r in range(len(labels))], labels)
plt.ylabel('Heures de cours')
plt.title('Répartition des heures de cours par groupe spécifique')
plt.legend()

ax.set_facecolor('#f2f2f2')
ax.grid(True, linestyle='--', alpha=0.7)

plt.show()

##################- Graphique camenbert -##################

####- Utilisation de couleurs variées -###
colors = plt.cm.tab20c.colors
explode = (0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)[:len(labels)]  

####- Création des subplots -####
fig, axs = plt.subplots(2, 2, figsize=(15, 12))

####- Graphique pour les heures de TP,CM,TD -####
wedges_tp, texts_tp = axs[0, 0].pie(heures_TP, labels=labels, startangle=90, counterclock=False, wedgeprops=dict(width=0.4), labeldistance=1.05, colors=colors, explode=explode)
axs[0, 0].set_title("Répartition des heures de TP par groupe spécifique")

wedges_cm, texts_cm = axs[0, 1].pie(heures_CM, labels=labels, startangle=90, counterclock=False, wedgeprops=dict(width=0.4), labeldistance=1.05, colors=colors, explode=explode)
axs[0, 1].set_title("Répartition des heures de CM par groupe spécifique")

wedges_td, texts_td = axs[1, 0].pie(heures_TD, labels=labels, startangle=90, counterclock=False, wedgeprops=dict(width=0.4), labeldistance=1.05, colors=colors, explode=explode)
axs[1, 0].set_title("Répartition des heures de TD par groupe spécifique")

####- Graphique vide pour eviter un graphe vide en bas a droite -####
axs[1, 1].axis('off') 

####- Ajout d'ombres, arrondies, étiquettes-####
for wedge in wedges_tp + wedges_cm + wedges_td:
    wedge.set_edgecolor('white')
    wedge.set_linewidth(2)
    wedge.set_antialiased(True)
axs[1, 1].legend(wedges_tp, labels, title='Groupes spécifiques', loc='center left', bbox_to_anchor=(1, 0.5))
plt.show()