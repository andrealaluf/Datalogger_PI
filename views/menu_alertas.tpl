% include('menu_gral.tpl')

<div><h3><br><font color = "#1E679A">Historial de alarmas disparadas:</font></br></h3></div>
<div><HR width=50% align="left" color="#1E679A"></div>
<div id="botones" style="float:left"></div>
<div id="Muestra-Log" style="overflow-y:auto; overflow-x:hidden; margin-left:10px; height:400px; width:600px;">
	%for i in range(len(lineas)):
	<div>{{lineas[i]}}</div>
	%end
</div>