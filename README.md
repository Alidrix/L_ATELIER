# 🧱 Architecture globale "local only"

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
  D[(🗄️ PostgreSQL)]:::db

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
  participant D as 🗄️ PostgreSQL

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

## 🔐 Accès Mail "Poste.io"

- Identifiant : `noreply@example.com`
- Mot de passe : `***REDACTED***`

- Identifiant : `fxxxxxxx.mxxxxxxxx@cxxx.fr`
- Mot de passe : `***REDACTED***`


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


### ✉️ Poste.io (webmail) + (NGINX + app + PostgreSQL + menu)

1. Accéder aux interfaces :

| Usage | Lien |
|---|---|
| Webmail | https://mail.local:8443 |
| Webmail - Admin Panel | https://mail.local:8443/admin/login |
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
sudo sh -c 'printf "127.0.0.1 portal-legacy.example.com\n127.0.0.1 mail.local\n" >> /etc/hosts'
```

2. Démarrer la plateforme :

```bash
docker-compose up -d --build && docker-compose -f docker-compose.yml up -d --build
```
