# Vicinex


Plateforme de colocation au Bénin permettant de mettre en relation les personnes qui proposent un logement en colocation avec celles qui en recherchent un — sans inscription requise pour consulter et contacter.

---

## Stack technique

| Couche | Technologie |
|---|---|
| Frontend | Next.js 14 (App Router) + TypeScript |
| Backend | Django REST Framework (Python) |
| Base de données | PostgreSQL |
| Carte interactive | Leaflet.js + OpenStreetMap |
| Stockage photos | Cloudinary |

## Structure du repo

```
vicinex/
├── frontend/       # Application Next.js
├── backend/        # API Django REST Framework
└── .github/
    └── workflows/  # CI/CD GitHub Actions
```

## Démarrage rapide

### Prérequis

- Node.js 20+
- Python 3.12+
- PostgreSQL 16+
- Docker

### Avec Docker (recommandé)

```bash
git clone https://github.com/cheyicarmel/vicinex.git
cd vicinex
cp backend/.env.example backend/.env
docker compose up --build
```

### Sans Docker

Voir les documentations individuels du frontend et du backend (elles sont vides pour l'instant) :
- [`frontend/README.md`](./frontend/README.md)
- [`backend/README.md`](./backend/README.md)

## Branches

| Branche | Rôle |
|---|---|
| `main` | Code stable — reflète la production |
| `develop` | Intégration — fonctionnalités terminées en attente de release |
| `feature/xxx` | Développement d'une fonctionnalité (avancement par phase) |

## Statut du projet

En cours de développement

## Licence

Projet personnel — tous droits réservés.
