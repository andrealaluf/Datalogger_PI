% include('menu_gral.tpl')
<!--
<div style="margin-left:20px;margin-top:50px; width=200px;">
<iframe src="/home/cubie/tesis2015/pygal_2_example.svg" width="500" height="320"> </iframe>
</div>

<iframe width="800" height="600" frameborder="0" seamless="seamless" scrolling="no" src="https://plot.ly/~abhishek.mitra.963/1/.embed?width=800&height=600"></iframe>
-->

<h3><br><font color = "#1E679A">CONFIGURAR SENSORES</font></br></h3>
<HR width=40% align="left" color = "#1E679A">

<table border="1" cellpadding="5" cellspacing="5">
	<tr>
		<td width="150px">Sensor</td>
		<td width="50px">Estado</td>
		<td width="80px">Tiempo</td>
	</tr>

% key = 0
% for key in range(0,5):
	<form action="/historicos" method="post" id="formSensores">
	<tr>
		<td>
			<div id="NombreSensor"><font color="#1E679A">{{key}}</font></div>
		</td>

		<td>
			<div id="SeleccionEstado" style="margin-left:20px; width:150px;">
			<select name="Estado" form="formSensores">
			<option value="Activado">Activado</option>
			<option value="Desactivado">Desactivado</option>
			</select>
			</div>
		</td>
		
		<td>
			<div id="SeleccionTiempo" style="margin-left:30px; width:150px;">
       		<select name="Tiempo">
			<option value="default">Default</option>
			<option value="60">1 min</option>
			<option value="120">2 min</option>
			<option value="300">5 min</option>
			<option value="600">10 min</option>
			<option value="1200">20 min</option>
			<option value="1800">30 min</option>
			</select>
			</div>
		</td>
		
		<td>
			<div id="Seleccion Tiempo3">
			<!--<input name="tiempotexto" type="text"  value="1" size="2" />-->
			<input type="number" name="tiempotexto" value="1" min="1" max="60">
			</div>
		</td>
	</tr>
% end
		<p>
			<input type="submit"value="Guardar"/>
		</p>
</form>
</table>

<!--
<div id="NombreSensor" style="float:left; width:200px;"><font color="#1E679A">{{key}}</font>

<div id="EstadoSensor" style="margin: 10px auto 15px auto ">

	<form action="/sensores" method="post" id="formSensores">
		<p>Estado - Tiempo: <select name="Estado" form="formSensores">
			<option value="Activado">Activado</option>
			<option value="Desactivado">Desactivado</option>
			</select>
			
			<select name="Tiempo">
			<option value="default">Default</option>
			<option value="60">1 min</option>
			<option value="120">2 min</option>
			<option value="300">5 min</option>
			<option value="600">10 min</option>
			<option value="1200">20 min</option>
			<option value="1800">30 min</option>
			</select>
			<!--	
			<input type="checkbox" name="PorDefecto" value="Default">Default<br>
			-->
%#end
<!--
		</p>
	<input type="submit"value="Guardar"/>
	</form>
</div></div>

<form method="GET" id="my_form"></form>
-->
