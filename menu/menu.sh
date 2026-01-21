#!/bin/sh

cat <<'MENU'
=========================================
 Plateforme "Mise à jour de sécurité"
=========================================
- Portail applicatif : http://portal-legacy.example.com
- Résultats : http://portal-legacy.example.com/results
- Mailu (webmail) : http://webmailu:8081
- Mailu (admin)   : http://webmailu:8081/admin

Astuce : ajoutez portal-legacy.example.com à /etc/hosts si besoin.
MENU

# Garde le conteneur actif pour afficher le menu.
tail -f /dev/null
