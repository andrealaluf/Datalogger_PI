% include('menu_gral.tpl')

<!--Comienzo de variables-->
<br></br> <!--Salto de linea-->

<h3><br><font color = "#1E679A">SENSORES DISPONIBLES</font></br></h3>
<HR width=50% align="left" color = "#1E679A"> 
<!--VERIFICO SI EXISTE EL ARCHIVO DE ESTADO,TIEMPO DE LOS SENSORES, SINO AVISO QUE PRIMERO CONFIGURE
LOS SENSORES -->
%if checkFile == 0: # Archivo no existe, aviso
<p>Por favor, primero configure los sensores!!!</p>
<a href="/sensores"><button>Configurar</button></a>

% else: # Archivo si existe
% for key,value in sensores.items(): # busca la llave y el valor de ese diccionario
%	print key, value
<div id="nombreSensores">

% if value[0]=='Activado': # para saber si el sensor esta o no activo
<div style="float:left; width:220px">{{key}} &nbsp;</div> 
 <div style="margin: 10px auto 15px auto "><font color = "green">ACTIVO</font></div>

% else:
<div style="float:left; width:220px">{{key}} &nbsp;<br></div> 
<div style="margin: 10px auto 15px auto "><font color = "red">NO ACTIVO</font></div>
</div>
% end
% end

<HR width=50% align="left" color ="#1E679A">

</body>
</html>
