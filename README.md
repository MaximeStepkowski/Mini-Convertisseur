# Mini-Convertisseur

### QUESTION DE RÉFLEXION

## 1 - Gestion de version

* Le travail en groupe peut être organisé avec une branche par tâche :
`feature/api-currency`, `feature/new-currency`, `feat/reverse-button`, etc.
Cela permet de séparer les modifications et d’éviter de casser le code des autres.

* Les Pull Requests permettent donc de relire le code, détecter les conflits,
lancer les tests et discuter des changements avant de les fusionner afin
d'éviter les conflits. C’est plus sûr qu’un push direct sur `main`.

## 2 - Qualité et tests

* Un test unitaire vérifie qu’une petite partie du code fonctionne correctement,
par exemple une fonction de conversion. Il est important car il permet de
détecter rapidement les erreurs.

* Automatiser les tests avec GitHub Actions permet de vérifier chaque PR avant
fusion. Cela évite d’intégrer du code qui casse l’application.

## 3 - Refactoring

* Dans le code initial les dettes techniques observées sont :
    * Le code est peu lisible et peu maintenable.
    * Les fonctions sont trop longues et font trop de choses.
    * Les noms de variables et fonctions ne sont pas explicites.
    * Il y a des répétitions de code.
    * Le code n’est pas testé.
    * Les données étaient codées en dur dans le code.

* Les modifications qui ont amélioré la maintenabilité et la lisibilité sont :
    * La séparation entre l’interface Streamlit et la logique métier.
    * La création de fonctions dédiées pour convertir les montants et récupérer les taux.
    * Le remplacement des taux codés en dur par des taux dynamiques via une API.
    * L’ajout de messages d’erreur plus clairs.
    * L’ajout de tests automatisés pour vérifier le bon fonctionnement du code.

## 4 - Maintenance

* Pour les quatre types de maintenance, nos modifications sont classées ainsi :
    * Corrective : correction de bugs et erreurs.
    * Adaptative : adaptation du code à une API externe de taux de change.
    * Perfective : amélioration de la lisibilité, de la maintenabilité et de l’extensibilité du code.
    * Préventive : ajout de tests unitaires pour prévenir les régressions.

* La partie la plus fréquente dans un projet réel semble être la maintenance
corrective, car il est courant de rencontrer des bugs. La maintenance adaptative
est aussi fréquente, car les API et les dépendances évoluent régulièrement.
