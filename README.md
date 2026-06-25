# Mini-Convertisseur

## Gestion de version

Pour travailler en groupe, il est conseillé de ne pas modifier directement la
branche principale. Chaque personne crée une branche dédiée à sa tâche :

- `feature/api` pour ajouter la récupération des taux via une API ;
- `feature/new-currency` pour ajouter une nouvelle devise ;
- `bugfix/zero-value` pour corriger le cas des montants nuls ou négatifs.

Cette organisation permet de séparer les changements. Chaque branche contient
un objectif précis, ce qui rend le code plus facile à relire, tester et corriger.

Les Pull Requests sont préférables à un push direct sur `main` car elles
permettent :

- de relire le code avant de l'intégrer ;
- de détecter les conflits avec les autres branches ;
- de lancer les tests automatiquement ;
- de discuter des changements avec l'équipe ;
- de garder un historique clair des évolutions du projet.

Un push direct sur `main` peut casser l'application pour tout le monde. Avec une
Pull Request, le changement est validé avant d'être fusionné.
