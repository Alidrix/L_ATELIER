# Plateforme locale "Mise à jour de sécurité"

Ce dépôt déploie une plateforme locale (100% hors ligne) pour démontrer les flux d'une mise à jour de sécurité.
L'ensemble est orchestré avec Docker Compose et repose sur : NGINX, Mailu, une application web et PostgreSQL.

## Arborescence

```
.
├── app
│   ├── Dockerfile
│   ├── app.py
│   ├── requirements.txt
│   ├── static
│   │   ├── app.js
│   │   └── styles.css
│   └── templates
│       ├── index.html
│       └── results.html
├── db
│   └── init.sql
├── email
│   └── security_update_email.html
├── mailu
│   └── mailu.env
├── menu
│   └── menu.sh
├── nginx
│   └── site.conf
├── docker-compose.yml
└── README.md
```

## Lancement

1. Ajouter l'hôte local (si nécessaire) :

```bash
sudo sh -c 'echo "127.0.0.1 portal-legacy.example.com" >> /etc/hosts'
```

2. Démarrer la plateforme :

```bash
docker compose up --build
```

Le service `menu` affiche directement les liens utiles dans le terminal.

## Vérification rapide

- Portail applicatif : `http://portal-legacy.example.com`
- Résultats : `http://portal-legacy.example.com/results`
- Webmail Mailu : `http://localhost:8081`
- Admin Mailu : `http://localhost:8081/admin`

## Email HTML

Le template HTML de l'email "Mise à jour de sécurité" est disponible dans :
`email/security_update_email.html`.

## Notes hors ligne

- Aucun service n'effectue d'accès sortant.
- Les images Docker doivent être disponibles localement pour respecter un environnement entièrement déconnecté.
