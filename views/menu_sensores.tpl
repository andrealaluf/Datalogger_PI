% include('menu_gral.tpl')

% import json
% data = open("/home/cubie/tesis2015/modulos/sensores_cfg.json").read()
% nombreSensores = json.loads(data) #crea a partir de un archivo json una estructura de datos python (un diccionario python)

<h3><br><font color = "#1E679A">CONFIGURAR SENSORES</font></br></h3>

<table border="1" cellpadding="5" cellspacing="5" >
  <tr bgcolor="#1E679A">
    <th width="150px" align="center" rowspan="2"><strong><font color="white"/>Sensor</strong></th>
    <th width="80px" align="center" rowspan="2"><strong><font color="white"/>Estado</strong></th>
    <th width="60px" align="center" rowspan="2"><strong><font color="white"/>Tiempo</strong></th>
    <th widht="20px" align="center" rowspan="2"><strong><font color="white"/>Unidad</strong></th>
    <th widht="20px" align="center" colspan="8"><strong><font color="white"/>ALARMAS</strong></th>
 </tr>
 <tr bgcolor="#1E679A">
	 <td widht="40px" align="center" bgcolor="#34ff34" vertical-align=top>MinBaja</strong></td>
	 <td widht="50px" align="center" bgcolor="#fcff2f" vertical-align=top>MinMed</strong></td>
	 <td widht="50px" align="center" bgcolor="#f8a102" vertical-align=top>MinAlta</strong></td>
	 <td widht="50px" align="center" bgcolor="#fe0000" vertical-align=top>MinUrg</strong></td>
    <td widht="50px" align="center" bgcolor="#34ff34" vertical-align=top>MaxBaja</td>
    <td widht="50px" align="center" bgcolor="#fcff2f" vertical-align=top>MaxMed</td>
    <td widht="50px" align="center" bgcolor="#f8a102" vertical-align=top>MaxAlta</td>
    <td widht="50px" align="center" bgcolor="#fe0000" vertical-align=top>MaxUrg</td>
  </tr>


<!-- CREA FORMULARIO PARA ACTIVAR O DESACTIVAR SENSORES-->
% for key,value in sorted(nombreSensores.items()): # busca la llave y el valor de ese diccionario 

  <form action="/sensores" method="post" id="formSensores">
  <tr>
    <td>
      <div id="NombreSensor"><font color="#1E679A">{{key}}</font></div>
    </td>

    <td>
      <div id="SeleccionEstado">
      <select name="Estado" form="formSensores" style="align:center; width:100px;">
      <option value="Activado">Activado</option>
      <option value="Desactivado">Desactivado</option>
      </select>
      </div>
    </td>

    <td align="center">
      <div id="Seleccion Tiempo3">
      <input style="align:center; width:50px" type="number" name="cantidadTiempo" value="1" min="1" max="60">
      <!--<input type="range" name="points" min="0" max="10">-->
      </div>
    </td>

    <td align="center">
      <select name="unidadTiempo" form="formSensores">
      <option value="seg">seg</option>
      <option value="min">min</option>
      <option value="hs">hs</option>
      </select>
    </td>

  <td align="center">
    <div id="AlarmaUnderBaja">
    <input style="align:center; width:60px" type="number" name="minBaja" min="-60" max="100" value="0" step="0.1">
    </div>
  </td>

    <td align="center">
    <div id="AlarmaUnderMedia">
    <input style="align:center; width:60px" type="number" name="minMed" min="-60" max="100" value="0" step="0.1">
    </div>
    </td>

   <td align="center">
    <div id="AlarmaUnderAlta">
    <input style="align:center; width:60px" type="number" name="minAlta" min="-60" max="100" value="0" step="0.1">
    </div>
    </td>

    <td align="center">
    <div id="AlarmaUnderUrg">
    <input style="align:center; width:60px" type="number" name="minUrg" min="-60" max="100" value="0" step="0.1">
    </div>
    </td>

    <td align="center">
    <div id="AlarmaOverBaja">
    <input style="align:center; width:60px" type="number" name="maxBaja" min="-60" max="100" value="0" step="0.1">
    </div>
    </td>


    <td align="center">
    <div id="AlarmaOverMed">
    <input style="align:center; width:60px" type="number" name="maxMed" min="-60" max="100" value="0" step="0.1">
    </div>
    </td>


    <td align="center">
    <div id="AlarmaOverAlta">
    <input style="align:center; width:60px" type="number" name="maxAlta" min="-60" max="100" value="0" step="0.1">
    </div>
    </td>

 

    <td align="center">
    <div id="AlarmaOverUrg">
    <input style="align:center; width:60px" type="number" name="maxUrg" min="-60" max="100" value="0" step="0.1">
    </div>
    </td>

    </tr>
% end
  <tr bgcolor="#2AFFBF">
    <td align="center" colspan="12"> <!--colspam es para que ocupe N cantidad de columnas. Seria un combinar celdas -->
      <p>
          <input type="submit"value="Guardar"/>
      </p>
      </td>
    </tr>

</form>
</table>

<br/>
<p>Por favor configure las alarmas de los sensores</p>






