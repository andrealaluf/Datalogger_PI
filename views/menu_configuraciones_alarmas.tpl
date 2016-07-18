% include('menu_gral.tpl')

% import json
% data = open("/home/cubie/tesis2015/modulos/sensores_cfg.json").read()
% nombreSensores = json.loads(data) #crea a partir de un archivo json una estructura de datos python (un diccionario python)

<h3><br><font color = "#1E679A">CONFIGURAR ALARMAS DE SENSORES</font></br></h3>

<table border="1" cellpadding="5" cellspacing="5">

  <tr bgcolor="#1E679A">
    <td rowspan="2" width="150px" align="center"><strong><font color="white"/>Sensor</strong></td>
    <td colspan="4" width="20px" align="center"><strong><font color="white"/>Alarmas Mínimo</strong></td>
    <td colspan="4" width="60px" align="center"><strong><font color="white"/>Alarmas Máximo</strong></td>
  </tr>

  <tr bgcolor="#1E679A">
    <td width="20px" align="center"><strong><font color="white"/>Baja</strong></td>
    <td width="60px" align="center"><strong><font color="white"/>Media</strong></td>
    <td widht="20px" align="center"><strong><font color="white"/>Alta</strong></td>
    <td widht="50px" align="center"><strong><font color="white"/>Urgente</strong></td>
    <td widht="50px" align="center"><strong><font color="white"/>Baja</strong></td>
    <td widht="50px" align="center"><strong><font color="white"/>Media</strong></td>
    <td widht="50px" align="center"><strong><font color="white"/>Alta</strong></td>
    <td widht="50px" align="center"><strong><font color="white"/>Urgente</strong></td>
  </tr>

<!-- CREA FORMULARIO PARA ACTIVAR O DESACTIVAR SENSORES-->
% for key,value in sorted(nombreSensores.items()): # busca la llave y el valor de ese diccionario 

  <form action="/alarmas" method="post" id="formAlarmas">
  <tr>
    <td>
      <div id="NombreSensor"><font color="#1E679A">{{key}}</font></div>
    </td>

    <td align="center">
		  <select name="AlarmaMinBaja-{{key}}" form="formAlarmas">
      %for i in listaFunciones:
      <option value='{{i}}'>{{i}}</option>
      %end
      </select>
    </td>

    <td align="center">
    <select name="AlarmaMinMedia-{{key}}" form="formAlarmas">
    %for i in listaFunciones:
    <option value='{{i}}'>{{i}}</option>
    %end
    </select>
    </td>

	<td align="center">
    <select name="AlarmaMinAlta-{{key}}" form="formAlarmas">
    %for i in listaFunciones:
    <option value='{{i}}'>{{i}}</option>
    %end
    </select>
    </td>

    <td align="center">
		<select name="AlarmaMinUrg-{{key}}" form="formAlarmas">
    %for i in listaFunciones:
    <option value='{{i}}'>{{i}}</option>
    %end
    </select>
    </td>

    <td align="center">
    <select name="AlarmaMaxBaja-{{key}}" form="formAlarmas">
    %for i in listaFunciones:
    <option value='{{i}}'>{{i}}</option>
    %end
    </select>
    </td>

    <td align="center">
    <select name="AlarmaMaxMedia-{{key}}" form="formAlarmas">
    %for i in listaFunciones:
    <option value='{{i}}'>{{i}}</option>
    %end
    </select>
    </td>

    <td align="center">
    <select name="AlarmaMaxAlta-{{key}}" form="formAlarmas">
    %for i in listaFunciones:
    <option value='{{i}}'>{{i}}</option>
    %end
    </select>
    </td>

    <td align="center">
    <select name="AlarmaMaxUrg-{{key}}" form="formAlarmas">
    %for i in listaFunciones:
    <option value='{{i}}'>{{i}}</option>
    %end
    </select>
    </td>

</tr>
% end
	<tr bgcolor="#2AFFBF">
		<td align="center" colspan="9"> <!--colspam es para que ocupe N cantidad de columnas. Seria un combinar celdas -->
    	<p>
      		<input type="submit" value="Guardar"/>
    	</p>
    	</td>
    </tr>
</form>
</table>



