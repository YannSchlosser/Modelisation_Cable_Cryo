Développement en Python de la modélisation de la chute d'un cable.

##### Précision du modèle sans frottement

En suivant l'évolution de l'énergie du système (cinématique + potentielle gravitationelle) on se rend compte que le modèle a des fluctuations d'énergie.

- Certaines sont explicables : les "pertes" d'énergies doivent être dues a leur conversion en potentiel mécanique des liens entre les points (les liens sont considérés comme des ressorts a forte raideur). Cela se confirme si l'on augmente la constante de raideur des liens cela réduit immédiatement les "pertes" d'énergies.

- On se rend aussi compte que le modèle rend trop d'énergie dans le cas test du pendule double. Même si cet excès est modéré est corélé avec le pas de temps (i.e. un pas de temps faible réduit les imprécisions), on cherchera a améliorer le modèle pour optimiser le ratio : précision / temps de calcul
Data sur le cas test Pendule double :
    - dt = 0.01s --> énergie initiale : 654 J, énergie max enregistrée : 656.25 J (excès de 0.34%)
    - dt = 0.001s --> énergie initiale : 654 J, énergie max enregistrée : 654.2 J (excès de 0.03%)
    - dt = 0.0001s --> énergie initiale : 654 J, énergie max enregistrée : 654.0115 J (excès de 0.0018%)


##### Développements futur du modèle

- Ajout d'autre visualisation pour vérifier le bon fonctionnement du modèle et apporter plus de data.
- Etude de la performance du modèle pour un grand nombre de point.
- 

##### Optimisation des calculs

- Une proposition est de faire les calculs avec numpy pour limiter le nombre d'iteration.