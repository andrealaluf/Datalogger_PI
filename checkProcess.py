#!/usr/bin/env python
"""
Verifica si un processo esta ejecutandose. Si no, lo 
reinicia.
"""
import os
process_name= "datalogger.py"

#### Inicializador de logger #####
LOG_FILENAME = os.path.join(os.getcwd(),'dataloggerApp.log')
logging.basicConfig(filename=LOG_FILENAME, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)

tmp = os.popen("ps -Af").read()

if process_name not in tmp[:]:
    print "Processo caido. Reiniciandolo..."
    newprocess="python %s &" % (process_name)
    os.system(newprocess)  
else:
    print "Proceso ejecutandose normalmente."

