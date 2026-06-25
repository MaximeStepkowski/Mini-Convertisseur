# Mini-Convertisseur


### QUESTION DE RÉFLEXION

## 1 - Gestion de version

* Le travail en groupe peut être organisé avec une branche par tâche :
`feature/api-currency`, `feature/new-currency`, `feat/reverse-button`, etc.
Cela permet de séparer les modifications et d’éviter de casser le code des autres.

* Les Pull Requests permettent donc de relire le code, détecter les conflits, lancer les tests et discuter des changements avant de les fusionner afin d'éviter les conflits. C’est plus sûr qu’un push direct sur `main`.

## 2 - Qualité et tests

* Un test unitaire vérifie qu’une petite partie du code fonctionne correctement, par exemple une fonction de conversion. Il est important car il permet de détecter rapidement les erreurs.

* Automatiser les tests avec GitHub Actions permet de vérifier chaque PR avant fusion. Cela évite d’intégrer du code qui casse l’application.

## 3 - Refactoring

* Dans le code initial les dettes techniques observées sont :
    * Le code est peu lisible et peu maintenable.
    * Les fonctions sont trop longues et font trop de choses.
    * Les noms de variables et fonctions ne sont pas explicites.
    * Il y a des répétitions de code.
    * Le code n’est pas testé
    * Les données était codé en dur dans le code.

* (MAXIME REPOND À CA : Quelles modifications ont amélioré la maintenabilité et la lisibilité? )

## 4 - Maintenance

* Pour les quatres types de maintenances nos modifications seront classé de cette manière :
    * Corrective : correction de bugs et erreurs.
    * Adaptative : adaptation du code aux nouvelles versions des API.
    * Perfective : amélioration de la lisibilité, de la maintenabilité et de l’extensibilité du code.
    * Évolutive : inverser les devises, ajouter de nouvelles devises.

* La partie la plus fréquente dans un projet réel semblerait être la maintenance corrective, car il est courant de rencontrer des bugs et des erreurs dans le code. Ou bien la maintenance adaptative, car les API et les dépendances peuvent évoluer rapidement et doivent être mises à jour, nécessitant donc des ajustements dans le code pour rester compatible.
