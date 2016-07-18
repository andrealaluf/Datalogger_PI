% include('menu_gral.tpl')

<!--Botones de Sensores-->
<!--Salto de linea
<br></br> -->
<div><h3><br><font color = "#1E679A">Seleccione el Sensor deseado:</font></br></h3></div>
<div><HR width=50% align="left" color="#1E679A"></div>

<div id="botones" style="float:left">
<!-- CREA LOS BOTONES DE LOS SENSORES SEGUAN CUAL DETECTA DE UNA
LISTA CREADA DE LOS SENSORES EXISTENTES-->
% import json
% data = open("/home/cubie/tesis2015/modulos/sensores_cfg.json").read()
% j = json.loads(data) # genera a partir de un archivo json un diccionario python
% for key,value in j.items(): # busca la llave y el valor de ese diccionario	
<div style="margin: 10px auto 15px auto;"><a href="/logs/{{key}}"><button>{{key}}</button></a></div>
%end 
</div>

<div id="Container-Logs" style="float:left; margin-left:20px; overflow:hidden;">
	<div id="Logs">	
	% 	for i in range(len(archivos)):
	<!--#### MUESTRO LOS NOMBRES DE LOS ARCHIVOS .log DE UN SENSOR DADO #####-->
 		
 		<!--
 		<div><a href="/logs/{{sensorSelected}}/{{archivos[i]}}">{{archivos[i]}}</a></div>
 		-->
 		<table style="width:60%">
 			<tr>
 				<td><a href="/logs/{{sensorSelected}}/{{archivos[i]}}">{{archivos[i]}}</a></td>
 				<!--
 				<td><a href="/download/logs/{{key}}/{{archivos[i]}}"><button onclick="alert('Hello world!')">Descargar</button></a></td>
 				-->
 				<td height="30"><a href="/download/{{sensorSelected}}/{{archivos[i]}}" class='btn'>Descargar</a></td>
 			</tr>
 		</table>
	%end
	</div>

	<div id="Muestra-Log" style="overflow-y:auto; overflow-x:hidden; height:400px; width:400px;">
	<!--#### MUESTRO EL CONTENIDO DEL ARCHIVO .log SELECCIONADO ####-->
	% for i in range(len(logSelected)):
		<div>{{logSelected[i]}}</div>
	%end
	</div>
</div>
<div style="clear:both"><HR width=50% align="left" color="#1E679A"></div>

<!--BOTON PARA REGRESAR A VER CADA SENSOR -->
<div><a href='/logs' class='btn'>Volver</a></div>

</body>
</html>
