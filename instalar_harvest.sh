# 1. Obtener de forma automática la ruta absoluta de donde está guardado este script
DIR_RAIZ="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR_RAIZ"

# 2. Definir el nombre correcto de la carpeta (Asegúrate si es con '-' o '_')
CARPETA_OBJETIVO="harvest"

# 3. Validar si la carpeta no existe para crearla automáticamente
if [ ! -d "$CARPETA_OBJETIVO" ]; then
    echo "📁 Creando la carpeta $CARPETA_OBJETIVO..."
    mkdir "$CARPETA_OBJETIVO"
fi

# 4. Moverse de forma segura a la carpeta
cd "$CARPETA_OBJETIVO"
echo "📍 Ahora estás en: $(pwd)"

# 5. Ejecutar el clonado de CKAN si no se ha clonado antes
if [ ! -d "ckan" ]; then
    echo "📥 Clonando CKAN desde GitHub..."
    git clone https://github.com/ckan/ckan.git
else
    echo "✅ CKAN ya está clonado en esta carpeta."
fi

cd "$DIR_RAIZ"
pip install -r harvest_requeriments.txt
