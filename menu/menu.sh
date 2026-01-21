#!/bin/sh

cat <<'MENU'
=========================================
 Plateforme "Mise à jour de sécurité"
=========================================
- Portail applicatif : http://portal-legacy.example.com
- Résultats : http://portal-legacy.example.com/results
- Poste.io (admin & webmail) : http://mail.local:8080
- Poste.io (admin & webmail) : http://localhost:8080

Astuce : ajoutez portal-legacy.example.com à /etc/hosts si besoin.
Astuce : ajoutez mail.local à /etc/hosts pour l'interface Poste.io.
MENU

# Garde le conteneur actif pour afficher le menu.
tail -f /dev/null
