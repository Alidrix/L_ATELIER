#!/bin/sh

cat <<'MENU'
=========================================
 Plateforme "Mise à jour de sécurité"
=========================================
- Portail applicatif : https://portal-legacy.example.com
- Résultats (admin) : https://portal-legacy.example.com/admin
- Poste.io (admin & webmail) : http://mail.example.com:8080
- Poste.io (admin & webmail) : http://localhost:8080

Astuce : ajoutez portal-legacy.example.com à /etc/hosts si besoin.
Astuce : ajoutez mail.example.com à /etc/hosts pour l'interface Poste.io.
MENU

# Garde le conteneur actif pour afficher le menu.
tail -f /dev/null
