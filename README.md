# 🧰 Plateforme locale — Mise à jour de sécurité (Infrastructure Docker)

## 🎯 Objectif du projet
Mettre en place une **plateforme locale complète**, entièrement **hors ligne**, permettant :
- d’analyser un **parcours utilisateur email ➜ portail local**,
- de comprendre **l’architecture technique**, les flux et les interactions entre services,
- de disposer d’un **support clair et professionnel** pour une présentation managériale.

---

## 🧭 Principes clés
- 📴 Fonctionnement **100 % hors ligne**
- 🐳 Orchestration via **Docker Compose**
- 🌐 **NGINX** comme serveur web et reverse proxy
- ✉️ **Mailu** pour la chaîne mail (UI + SMTP/IMAP)
- 🗄️ **PostgreSQL** pour la persistance applicative
- 🎨 Interfaces sobres (blanc / gris)

---

## 🧱 Architecture globale

```mermaid
flowchart LR
  classDef pastel fill:#F2F7FF,stroke:#7AA2F7,color:#1F2A44;
  classDef pastel2 fill:#F7F2FF,stroke:#B38BFF,color:#2A1F44;
  classDef pastel3 fill:#F2FFF7,stroke:#77D9A8,color:#1F442A;
  classDef pastel4 fill:#FFF7F2,stroke:#FFB37A,color:#442A1F;

  U[👤 Utilisateur]:::pastel
  M[📮 Webmail Mailu]:::pastel2
  N[🌐 NGINX]:::pastel
  A[🧩 Application Web]:::pastel3
  D[(🗄️ PostgreSQL)]:::pastel4

  U --> M
  M --> N
  N --> A
  A --> D
  A --> U
```

---

## 🔁 Parcours utilisateur

```mermaid
sequenceDiagram
  participant U as Utilisateur
  participant W as Mailu
  participant N as NGINX
  participant A as Application
  participant D as PostgreSQL

  U->>W: Lecture du message
  W->>N: Accès lien local
  N->>A: Requête HTTP
  U->>A: Saisie email
  U->>A: Saisie mot de passe
  A->>D: Enregistrement
  A-->>U: Confirmation
```

---

## 🧩 Conteneurs

| Conteneur | Rôle |
|---------|------|
| mailu | Chaîne mail |
| nginx | Web |
| app | Applicatif |
| postgres | Base de données |

---

## 🖥️ Portail
- Design blanc / gris
- Champs email + mot de passe (masquable)
- Bouton connexion avec chargement
- Message de confirmation
- Retour à l’accueil

---

## 🚀 Démarrage

```bash
docker compose up -d
```

---

## 📜 Licence
Apache License 2.0
