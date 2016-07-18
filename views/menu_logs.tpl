% include('menu_gral.tpl')
<!--Botones de Sensores-->
<!-- Esto es un salto de linea
<br></br> -->

<div><h3><br><font color = "#1E679A">Seleccione el Sensor deseado:</font></br></h3></div>
<div><HR width=50% align="left" color="#1E679A"></div>

<!-- CREA LOS BOTONES DE LOS SENSORES SEGUAN CUAL DETECTA DE UNA
LISTA CREADA DE LOS SENSORES EXISTENTES-->
% import json
% data = open("/home/cubie/tesis2015/modulos/sensores_cfg.json").read()
% j = json.loads(data) #crea a partir de un archivo json una estructura de datos python (un diccionario python)

% for key,value in j.items(): # busca la llave y el valor de ese diccionario	
<div style="margin: 10px auto 15px auto "><a href="/logs/{{key}}"><button>{{key}}</button></a></div>
%end 
<div><HR width=50% align="left" color="#1E679A"></div>

</body>
</html>
