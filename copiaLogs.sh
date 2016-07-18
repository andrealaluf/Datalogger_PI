#!/bin/sh

#DIR1="/var/tmp/*"
DIR1="/tmp/*"
DIR2="/home/cubie/tesis2015/logs/"

cp -r $DIR1 $DIR2

# Capaz me conviene mas hacer un rsync por cuestiones de que cuando se
# añadan archivos nuevos me va a borrar los que hay en la carpeta de destino. 
# Para un archivo en ese dia no habría problema el tema es que pasa cuando 
# registro varios dias
rsync -avzh $DIR1 $DIR2
