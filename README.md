# 🧱 Architecture globale

```mermaid
flowchart LR
  classDef user fill:#E8F0FE,stroke:#4F83FF,color:#1F2A44;
  classDef web fill:#E8F7FF,stroke:#3FB8FF,color:#1F3A44;
  classDef app fill:#E8FFF1,stroke:#4FD88B,color:#1F442A;
  classDef db fill:#FFF1E8,stroke:#FF9F4F,color:#442A1F;

  U[👤 Utilisateur]:::user
  N[🌐 NGINX Reverse Proxy]:::web
  A[🧩 Application Portail]:::app
  D[(🗄️ PostgreSQL)]:::db

  U -->|Accès web| N
  N -->|Routage HTTP| A
  A -->|Enregistrement identifiants| D
  A -->|Confirmation| U
```


## 🔁 Flux applicatif

```mermaid
sequenceDiagram
  participant U as 👤 Utilisateur
  participant N as 🌐 NGINX
  participant A as 🧩 Application
  participant D as 🗄️ PostgreSQL

  U->>N: Accès au portail
  N->>A: Requête HTTP
  U->>A: Saisie email
  U->>A: Saisie mot de passe
  A->>D: Enregistrement des identifiants
  A-->>U: Confirmation visuelle
```


## 🖥️ Portail applicatif

- 🎨 Blanc / gris
- 🧱 Cartes arrondies
- 👁️ Mot de passe masquable
- ⏳ Animation de chargement
- 🔴 Écran de confirmation
- 🔐 Accès admin séparé pour les identifiants


## 🔐 Accès GUI BDD

- Identifiant : `alix`
- Mot de passe : `***REDACTED***`


## 🗂️ Arborescence du projet

```
.
├── app
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── static
│   │   ├── app.js
│   │   ├── illustration-login.svg
│   │   ├── rubix-favicon.svg
│   │   └── styles.css
│   └── templates
│       ├── admin_login.html
│       ├── index.html
│       └── results.html
├── db
│   └── init.sql
├── docker-compose.yml
├── email
│   ├── install_notifications.sh
│   ├── notify-mail.service
│   ├── notify-mail.timer
│   ├── notify_new_mail.py
│   ├── security_update_email.html
│   └── send_security_update.py
├── nginx
│   ├── Dockerfile
│   ├── entrypoint.sh
│   ├── site.conf
│   └── ssl
│       ├── portal.example.crt
│       └── portal.example.key
└── README.md
```


### ✅ Interfaces disponibles

| Usage | Lien |
|---|---|
| Portail applicatif | https://portal-legacy.example.com |
| Auth Panel - BDD | https://portal-legacy.example.com/admin |
| Identifiants - GUI BDD | https://portal-legacy.example.com/results |


## 🧰 Dépannage rapide

```bash
docker-compose down -v --remove-orphans
```


## 🚀 Démarrage de l'infra

1. Ajouter les hôtes locaux (si nécessaire) :

```bash
sudo sh -c 'printf "127.0.0.1 portal-legacy.example.com\n" >> /etc/hosts'
```

2. Démarrer la plateforme :

```bash
docker-compose up -d --build
```
