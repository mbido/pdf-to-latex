# PDF to LaTeX Converter

Ce projet convertit des fichiers PDF en LaTeX via Markdown, en utilisant une combinaison de Mistral AI (pour l'OCR et l'extraction du Markdown) et Gemini (pour la conversion Markdown vers LaTeX).

## Prérequis
*   Un compte Mistral AI avec une clé API
*   Une clé API Google Gemini

## Installation

1.  **Clonez le dépôt:**

  ```bash
  git clone git@github.com:mbido/pdf-to-latex.git
  cd pdf-to-latex
  ```

2.  **Installez les dépendances Python:**
Utilisez de préférence un environement virtuel :
  ```bash
  python3 -m venv .venv && source .venv/bin/activate
  ```

  ```bash
  pip install -r requirements.txt
  ```

4.  **Configurez les clés API:**

Enlevez le `.example` du nom du fichier `.env.exemple` et renseignez vos clés d'API
  ```
  MISTRAL_API_KEY=votre_clé_mistral
  GEMINI_API_KEY=votre_clé_gemini
  ```

## Utilisation

1.  **Rendez `exec.sh` exécutable:**

    ```bash
    chmod +x exec.sh
    ```

2.  **Exécutez le script:**

    ```bash
    ./exec.sh <chemin_absolu_vers_votre_fichier.pdf>
    ```

    Le script générera un fichier `.tex` et un fichier `.md` (contenant le Markdown extrait) dans le *même répertoire* que le fichier PDF d'entrée, avec le suffixe `_converted`.

3.  **Créer un alias (recommandé, voir instructions complètes dans le code de `exec.sh`):**
   Ajouter dans votre `.bashrc` (ou `.zshrc` si vous utilisez zsh):
   ```bash
   alias pdf2latex='bash /chemin/absolu/vers/exec.sh'
   ```
   Puis recharger la configuration:
   ```bash
    source ~/.bashrc
    # ou 
    source ~/.zshrc
   ```

## Exemple
```bash
./exec.sh /home/user/Documents/document.pdf
#ou après avoir créé l'alias
pdf2latex /home/user/Documents/document.pdf
```