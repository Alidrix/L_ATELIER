# 🎯 Plateforme locale "Mise à jour de sécurité"

Ce dépôt déploie une plateforme locale (100% hors ligne) pour démontrer les flux d'une mise à jour de sécurité.
L'ensemble est orchestré avec Docker Compose et repose sur : NGINX, Poste.io, une application web et SQLITE3.


## 🧱 Architecture globale

```mermaid
flowchart LR
  classDef user fill:#E8F0FE,stroke:#4F83FF,color:#1F2A44;
  classDef mail fill:#F3E8FF,stroke:#9B6BFF,color:#2A1F44;
  classDef web fill:#E8F7FF,stroke:#3FB8FF,color:#1F3A44;
  classDef app fill:#E8FFF1,stroke:#4FD88B,color:#1F442A;
  classDef db fill:#FFF1E8,stroke:#FF9F4F,color:#442A1F;

  U[👤 Utilisateur]:::user
  M[📮 Poste.io Webmail]:::mail
  N[🌐 NGINX Reverse Proxy]:::web
  A[🧩 Application Portail local]:::app
  D[(🗄️ SQLITE 3)]:::db

  U -->|Envoi manuel du message| M
  U -->|Lecture du message| M
  M -->|Clic sur lien local| N
  N -->|Routage HTTP| A
  A -->|Lecture données de démonstration| D
  A -->|Confirmation| U
```



## 🔁 Flux applicatif

```mermaid
sequenceDiagram
  participant U as 👤 Utilisateur
  participant M as 📮 Poste.io
  participant N as 🌐 NGINX
  participant A as 🧩 Application
  participant D as 🗄️ SQLITE 3

  U->>M: Envoi manuel du message
  U->>M: Lecture du message
  Note right of M: Chaîne mail autonome
  M->>N: Accès au lien local
  Note right of N: Centralisation du trafic
  N->>A: Requête HTTP
  Note right of A: Logique métier isolée
  U->>A: Saisie email
  U->>A: Saisie mot de passe
  A->>D: Lecture des données de démonstration
  Note right of D: Données fictives encodées (base64)
  A-->>U: Confirmation visuelle
```



## 🖥️ Portail applicatif

- 🎨 Blanc / gris
- 🧱 Cartes arrondies
- 👁️ Mot de passe masquable
- ⏳ Animation de chargement
- 🔴 Écran de confirmation
- 🔐 Accès admin séparé pour les données de démonstration



## 🔐 Accès GUI BDD

- Identifiant : `alix`
- Mot de passe : `***REDACTED***`



## 🗂️ Arborescence du projet

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
├── docker-compose.yml
├── menu
│   └── menu.sh
├── nginx
│   └── site.conf
└── README.md
```


### 🧱 Stack principale (NGINX + app + PostgreSQL + menu)

1. Accéder aux interfaces :

| Usage | Lien |
|---|---|
| Portail applicatif | (https://portal-legacy.example.com/) |
| Auth Panel - BDD | (https://portal-legacy.example.com/admin) |
| Identifiants - GUI BDD | (https://portal-legacy.example.com/results) |

### ✉️ Poste.io (webmail)

1. Accéder aux interfaces :

| Usage | Lien |
|---|---|
| Webmail | https://mail.local:8443 |
| Admin | https://mail.local:8443/admin/login |



## 🧰 Dépannage rapide

```bash
docker-compose down -v --remove-orphans
```



## 📴 Notes hors ligne

- Aucun service n'effectue d'accès sortant.
- Les images Docker doivent être disponibles localement pour respecter un environnement entièrement déconnecté.



## 🚀 Démarrage de l'infra

1. Ajouter les hôtes locaux (si nécessaire) :

```bash
sudo sh -c 'printf "127.0.0.1 portal-legacy.example.com\n127.0.0.1 mail.local\n" >> /etc/hosts'
```

2. Démarrer la plateforme :

```bash
docker-compose up -d --build && docker-compose -f docker-compose.yml up -d --build
```
