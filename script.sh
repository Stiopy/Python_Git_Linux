#!/bin/bash

# URL de la page à scraper
URL="https://www.boursorama.com/bourse/matieres-premieres/cours/8xWBS/"

# Chemin du fichier CSV
OUTPUT_FILE="scraping_data.csv"

# Écrire l'en-tête dans le CSV
#echo "Date;Prix">>"$OUTPUT_FILE"

# Récupérer le HTML de la page
HTML=$(curl -s "$URL")

# Obtenir la date et l'heure (tous dans une même chaîne)
DATE=$(date "+%Y-%m-%d %H:%M:%S")

# Extraire UNIQUEMENT la première valeur de prix et nettoyer la chaîne :
EXTRACTED_VALUE=$(echo "$HTML" \
  | grep -oP '<span class="c-instrument c-instrument--last" data-ist-last>[^<]+' \
  | head -n 1 \
  | sed -E 's/.*data-ist-last>([^<]+)/\1/' \
  | sed 's/[^0-9,]//g' \
  | sed 's/,/./g' \
  | sed 's/^\.+//')

# Ajouter la date et le prix dans le fichier CSV (attention, ici on utilise une virgule comme séparateur)
echo "$DATE;$EXTRACTED_VALUE">>"$OUTPUT_FILE"

#echo "Scraped price: $EXTRACTED_VALUE"

#rm temp.html
