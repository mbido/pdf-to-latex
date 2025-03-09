#!/bin/bash

# Vérifie si un argument (chemin du fichier PDF) a été fourni
if [ $# -eq 0 ]; then
  echo "Usage: $0 <chemin_absolu_du_fichier_pdf>"
  exit 1
fi

# Récupère le chemin absolu du fichier PDF
pdf_path="$1"

# Vérifie si le fichier PDF existe
if [ ! -f "$pdf_path" ]; then
  echo "Erreur : Le fichier PDF spécifié n'existe pas."
  exit 1
fi

# Récupère le répertoire du fichier PDF
pdf_dir=$(dirname "$pdf_path")
# Récupère le nom de base du fichier PDF (sans extension)
pdf_basename=$(basename "$pdf_path" .pdf)

# Définit le chemin du fichier de sortie LaTeX et du fichier Markdown final (avec _converted)
latex_file="$pdf_dir/$pdf_basename-converted.tex"
final_markdown_file="$pdf_dir/$pdf_basename-converted.md"

# Récupère le répertoire où se trouve le script exec.sh
script_dir=$(dirname "$(readlink -f "$0")")

# Définit le chemin du répertoire src et du fichier Markdown temporaire
src_dir="$script_dir/src"
temp_markdown_file="$src_dir/converting.md"

# Active l'environnement virtuel
if [ -f "$script_dir/.venv/bin/activate" ]; then
    echo "Activation de l'environnement virtuel..."
    source "$script_dir/.venv/bin/activate"
else
    echo "Erreur : L'environnement virtuel n'a pas été trouvé."
    exit 1
fi

# Étape 1 : Extraction du Markdown à partir du PDF avec extract_markdown.py
echo "Extraction du Markdown depuis $pdf_path..."
python3 "$src_dir/extract_markdown.py" "$pdf_path" -o "$temp_markdown_file"
if [ $? -ne 0 ]; then
    echo "Erreur lors de l'exécution de extract_markdown.py."
    deactivate
    exit 1
fi

# Étape 2 : Conversion du Markdown en LaTeX avec markdown_to_latex.py
echo "Conversion du Markdown en LaTeX..."
python3 "$src_dir/markdown_to_latex.py" > "$latex_file"
if [ $? -ne 0 ]; then
    echo "Erreur lors de l'exécution de markdown_to_latex.py."
    deactivate
    exit 1
fi

# Renommer le fichier Markdown temporaire vers le répertoire final
echo "Déplacement du fichier Markdown vers $final_markdown_file..."
mv "$temp_markdown_file" "$final_markdown_file"
if [ $? -ne 0 ]; then
    echo "Erreur lors du renommage/déplacement du fichier Markdown."
    deactivate
    exit 1
fi

# Désactive l'environnement virtuel
deactivate

# Affiche un message de succès
echo "Conversion terminée. Les fichiers sont :"
echo "  LaTeX : $latex_file"
echo "  Markdown : $final_markdown_file"

exit 0