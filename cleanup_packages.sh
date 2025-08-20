#!/bin/bash

echo "=== Package Cleanup Script ==="
echo "This will remove packages not in your requirements.txt"
echo ""

# Heavy packages that are not in requirements.txt
PACKAGES_TO_REMOVE=(
    "numpy"
    "scipy" 
    "spacy"
    "spacy-legacy"
    "spacy-loggers"
    "en_core_web_sm"
    "blis"
    "thinc"
    "PyQt5"
    "PyQt5-Qt5"
    "PyQt5_sip"
    "cymem"
    "murmurhash"
    "preshed"
    "srsly"
    "wasabi"
    "weasel"
    "catalogue"
    "confection"
    "typer"
    "shellingham"
    "smart_open"
    "cloudpathlib"
    "langcodes"
    "language_data"
    "marisa-trie"
    "pydantic"
    "pydantic_core"
    "typing-inspection"
)

echo "The following packages will be removed:"
echo "----------------------------------------"
for pkg in "${PACKAGES_TO_REMOVE[@]}"; do
    if pip show "$pkg" &>/dev/null; then
        echo "  - $pkg"
    fi
done

echo ""
read -p "Do you want to proceed with cleanup? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Removing unnecessary packages..."
    for pkg in "${PACKAGES_TO_REMOVE[@]}"; do
        pip uninstall -y "$pkg" 2>/dev/null
    done
    
    echo ""
    echo "Cleanup complete!"
    echo ""
    echo "Running pip check to verify dependencies..."
    pip check
    
    echo ""
    echo "Current package count:"
    pip list --format=freeze | wc -l
else
    echo "Cleanup cancelled."
fi
