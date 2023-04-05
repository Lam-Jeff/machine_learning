# Rapport

## Objectif
Nous avons à notre disposition 4 fichiers.<br/>
Le but de cette étude de cas est de tirer un maximum d'informations.<br/>
Bonus : afficher des graphes, effectuer une prédictions, utilisation d'API etc.

## Contraintes
- 4 fichiers CSV : cities, providers, stations, ticket_data.
- Langage Python.
- Utilisation de la librairie Pandas.

## Structure du projet
- Data contient 2 dossiers : cleaned et raw. <br>
Raw : le dossier contient les fichiers CSV. <br>
Cleaned : le dossier contient les fichiers CSV des données après traitement.
- data_exploratory contient 5 fichiers : 1 pour chaque fichier CSV et 1 dernier "process" qui contient des fonctions.
- html et pdf sont des dossiers contenant des versions html et pdf des scripts python de data_exploratory après exécution.
- tests contient un fichier pour tester les fonctions présente dans "process". Le fichier se lance avec Pytest.
- requirement.txt est un fichier possédant toutes les dépendances.

## Démarche
Chaque fichier exploratory ont la même structure. <br>
On commence par une exploration des données pour tirer un maximum d'informations. <br>
Le type de questions que l'on peut se poser durant la fouille :
- Que représente le fichier ?
- Que représente les attributs ?
- Existe-t-il des valeurs manquantes, nulles, aberrantes ?
- les données sont-elles diversifiées ?
- Doit-on traiter les données ?
- Quels sont les attributs qui pourraient m'aider à répondre à la problématique ?
- Y-a-t-il des données surprenantes ?

Après cette fouille, on peut procéder au traitement des données si nécessaires et si cela est possible avec les ressources à notre disposition. <br>
A cette étape, tous les fichiers ont été sauvegarder sous une version "cleaned". Ces fichiers n'ont pas été utilisé et ne sont la que pour garder une trace du nettoyage de données qui a été effectué. <br>
Une fois que la fouille et le traitement des données ont été faite avec tous les fichiers, on peut passer à la phrase de modélisation. <br>
L'objectif du modèle d'apprentissage est de prédire le prix d'un trajet. Une regression a été faite.<br>
Les étapes sont :
- Split de notre dataset en training / test set. Le training set sera utilisé pour effectuer une cross-validation. Le test set servira à la fin de notre procédure pour évaluer notre modèle.
- Cross-validation : 5 modèles sont évalués avec comme métriques le RSE, MAE et le RMSE.
- Celui qui obtient les meilleurs résultats est sélectionné comme étant le meilleur modèle.
- On passe ensuite au tuning des hyperparamètres de notre modèle.
- Le modèle hyperparamétré et le modèle normale sont évalués avec le RSE, MAE et le RMSE.
- Celui qui obtient les meilleurs résultats devient le modèle finale.
- On effectue une prédiction avec notre test set.

## Observations
Des observations ont été noté dans les scripts. Les observations qui me semble importantes sont :
- Plusieurs langues, alphabets sont utilisés pour nommer les villes et stations. Cela peut entrainer l'apparition de nombreux doublons une fois que l'on compare les coordoonées.
- Le service propose des tickets dont la date de départ est antérieur à celle de la recherche.
- Dans le fichier cities, local_name a le format lieu/région/pays. Lieu est pour certains tuple le nom d'une ville et pour d'autres le nom d'un lieu dans une ville.
- Dans le fichier cities, unique_name formate le nom du lieu en remplaçant les espaces par des tirets et donnant parfois des chaînes de caractères assez particulières.
- Dans le fichier ticket_data, middle_stations possèdent des listes contenant plusieurs fois le même arrêts.

## API
- Geopy : permet de calculer des distances entre 2 points (ici des villes) et avec Nominatim, il est possible de faire du reverse geocoding: à partir des coordonnées GPS, on peut retrouver un lieu.
- mkwikidata : permet d'accéder à la base de données de Wikipédia en utilisant le langage SPARQL. Il permet par exemple de retrouver le nombe d'habitants d'une ville à partir de son nom.

## Critiques et pistes d'améliorations
- Bien que le modèle obtenu offre un bon résultat, il existe peut être un autre modèle plus perfomant. Avec de meilleurs ressources de calculs, on pourrait augmenter le nombre d'hyperparamètres à chercher ou encore tester plus de modèles. On pourrait aussi faire varier le nombre d'attributs utilisés pour la prédiction.
- Geopy et en particulier Nominatim restreint le nombre de requête que l'on peut faire à l'instant t ce qui rend la recherche de la ville lente. Il existe des API tiers plus rapide que l'on peut trouver sur la page wiki de Nominatim. Il y a aussi l'api Google payante.
- La recherche du nombre d'habitants via la base de données de Wikipédia est restreinte par le fait que l'on ne possède parfois pas le nom officiel de la ville. On est souvent obligé de passer par du reverse geocoding pour trouver la ville puis interroger la base de données. 
- La détection de doublons pour les villes et stations peuvent être fait à l'aide des coordonnées plutot que le nom (étant donné qu'il y a plusieurs langues / alphabets). Mais parfois on perd en précision. 2 lieux deviennent un seul lieu.
- Une alternative aux coordonnées et d'utiliser un traducteur puis ensuite de comparer les chaînes de caractères. Cette comparaison peut être faite de manière "traditionnelle" (en utilisant une librairie comme Fuzzywuzzy) ou alors coupler la librairie à du machine learning.