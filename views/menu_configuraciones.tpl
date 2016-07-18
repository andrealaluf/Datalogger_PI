<!--<!DOCTYPE html>-->
% include('menu_gral.tpl')


<br />
<h3><br><font color = "#1E679A">CONFIGURACIONES GENERALES</font></br></h3>
<HR width=40% align="left" color = "#1E679A">

<form action="/configuracion/reporte" method="post">
  <fieldset>
  <legend><h3><strong><font color = "#1E679A">REPORTES Y NOTIFICACIONES</font></strong></h3></legend>
    <label for="nombre">Cantidad de días de almacenamiento de logs:</label>
    	<!--<input style="align:center; width:50px" type="number" name="cantDias" value="1" min="1" max="31"/>-->
      <input style="align:center; width:50px" type="number" name="cantDias" value={{reportdays}} min="1" max="31"/>
    <br />
    <br><br>
    <label for="apellido">Intervalo de envío de notificaciones:</label>
    	<!--<input style="align:center; width:50px" type="number" name="intervaloNotif" value="1" min="1" max="60"/>-->
      <input style="align:center; width:50px" type="number" name="intervaloNotif" value={{notific}} min="1" max="60"/>
    	<select name="unidadTiempo_not">
      		<option value="seg">seg</option>
      		<option value="min">min</option>
      		<option value="horas">hs</option>
      		<option value="dias">dias</option>
          <option value={{unit}} selected>{{unit}}</option>
      	</select>
    <br />
    <br /> 
    <HR width=100% align="left" color = "#1E679A">
    <legend><h3><strong><font color = "#1E679A">CONECTIVIDAD</font></strong></h3></legend>
    <label for="nombre">Seleccione el medio de comunicación:</label>
      <select name="modo_com">
    <option value="3G">3G</option>
    <option value="UHF">UHF</option>
    <option value={{viacom}} selected>{{viacom}}</option>
    </select>
    <br />
    <br /> 
      <input type="submit" value="Guardar"/>
  </fieldset>
 
</form>

<!--FORMULARIO PARA CAMBIO DE NOMBRE DE ESTACION-->
<form action="/configuracion/nombre" method="post">
  <fieldset>
  <legend><h3><strong><font color = "#1E679A">CAMBIO DE NOMBRE DE ESTACION</font></strong></h3></legend>
    <label for="nombre">Introduzca un nuevo nombre:</label>
      <input type="text" name="nombre_estacion" maxlength="30" value="Nombre">
      <br><br>
      <input type="submit" value="Cambiar">
    <br />
    <br />
  </fieldset>
</form>
</body> 
</html>

