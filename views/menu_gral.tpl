<html>
<head>
	<title>Datalogger</title>
	<!--
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
	<script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>
	-->
<!--ESTE SCRIPT ES PARA EL BOTON DE SALIR/APAGAR/REINICIAR  -->
	<script>
		function land(ref, target)
		{
		lowtarget=target.toLowerCase();
		if (lowtarget=="_self") {window.location=loc;}
		else {if (lowtarget=="_top") {top.location=loc;}
		else {if (lowtarget=="_blank") {window.open(loc);}
		else {if (lowtarget=="_parent") {parent.location=loc;}
		else {parent.frames[target].location=loc;};
		}}}
		}
		function jump(menu)
		{
		ref=menu.choice.options[menu.choice.selectedIndex].value;
		splitc=ref.lastIndexOf("*");
		target="";
		if (splitc!=-1)
		{loc=ref.substring(0,splitc);
		target=ref.substring(splitc+1,1000);}
		else {loc=ref; target="_self";};
		if (ref != "") {land(loc,target);}
		}
	</script>

<style>
  ul {list-style: none;padding: 0px;margin: 0px;}
  ul li {display: block;position: relative;float: left;border:1px solid #000}
  li ul {display: none;}
  ul li a {display: block;background: #000;padding: 5px 10px 5px 10px;text-decoration: none;
           white-space: nowrap;color: #fff;}
  ul li a:hover {background: #1E679A;}
  li:hover ul {display: block; position: absolute;}
  li:hover li {float: none;}
  li:hover a {background: #50B8F8;}
  li:hover li a:hover {background: #000;}
  #drop-nav li ul li {border-top: 0px;}

  #body { background-color: #E4E2DE;}

 /*Este es un elemento circulo rojo*/ 
 .circleRed {  
	border-radius: 50%;
	width: 30px;
	height: 30px;
    background: red;}
 /*Este es un elemento circulo verde*/
 .circleGreen {
	border-radius: 50%;
	width: 30px;
	height: 30px;
    background: green;}
/*Para el boton de logout*/
Button {
	padding: 5px 10px 7px !important;
	font-size: 12px !important;
	background-color: #48A7DE;
	font-weight: bold;
	/*text-shadow: 1px 1px #57D6C7;*/
	color: #ffffff;
	border-radius: 5px;
	-moz-border-radius: 5px;
	-webkit-border-radius: 5px;
	border: 1px solid #57D6C7;
	cursor: pointer;
	box-shadow: 0 1px 0 rgba(255, 255, 255, 0.5) inset;
	-moz-box-shadow: 0 1px 0 rgba(255, 255, 255, 0.5) inset;
	-webkit-box-shadow: 0 1px 0 rgba(255, 255, 255, 0.5) inset;}

#myform {
    text-align: center;
    padding: 5px;
    border: 1px dotted #ccc;
    margin: 2%;
}
.qty {
    width: 40px;
    height: 25px;
    text-align: center;
}
input.qtyplus { width:25px; height:25px;}
input.qtyminus { width:25px; height:25px;}

/*####### Para el boton Descargar en logs ###########*/
.btn {
  -webkit-border-radius: 12;
  -moz-border-radius: 12;
  border-radius: 12px;
  font-family: Arial;
  color: #ffffff;
  font-size: 14px;
  background: #b8b8b8;
  padding: 1px 7px 3px 9px;
  border: solid #1f628d 2px;
  text-decoration: none;
}

.btn:hover {
  background: #3cb0fd;
  background-image: -webkit-linear-gradient(top, #3cb0fd, #3498db);
  background-image: -moz-linear-gradient(top, #3cb0fd, #3498db);
  background-image: -ms-linear-gradient(top, #3cb0fd, #3498db);
  background-image: -o-linear-gradient(top, #3cb0fd, #3498db);
  background-image: linear-gradient(to bottom, #3cb0fd, #3498db);
  text-decoration: none;
}
/*################ Para el Alta de Usuario ###########################*/
fieldset {
  padding: 1em;
  font:80%/1 sans-serif;
  }
label {
  float:left;
  width:25%;
  margin-right:0.5em;
  padding-top:0.2em;
  text-align:right;
  font-weight:bold;
  }
/*######################################################################*/
</style>
</head>

<body id="body">
<!-- bgcolor="white" text="blue" link="red" vlink="red">-->
<!--### ESTE ES UN RECUADRO DE TEXTO DONDE IRIA LOS DATOS DE LA ESTACION ##-->
<table width=50% cellspacing="1" cellpadding="3" border="0" bgcolor="#1E679A">
<tr>
   <td><font color="#FFFFFF" face="arial, verdana, helvetica">
<b>SISTEMA DE ADQUISICION Y MONITOREO DE DATOS</b>
   </font></td>
</tr>
% import platform
% from time import gmtime, strftime
% diafecha = strftime("%d-%m-%Y", gmtime())
% hostname = platform.node() 

<tr>
   <td bgcolor="#ffffcc">
   <font face="arial, verdana, helvetica">
   <strong>ID:</strong>{{idplaca}} &nbsp;&nbsp;  
   <strong>Fecha:</strong> {{diafecha}} &nbsp;&nbsp;
   <strong>Host:</strong> {{hostname}}
   </font>
   </td>
</tr>
</table> 

<!--MENU -->
<div id=menu>
<ul id="drop-nav">
	<li><a href="/tiemporeal">Estado</a></li>
	<li><a href="/configuracion">Configuracion</a>
		<ul>		
			<li><a href="/sensores">Sensores</a></li>
			<li><a href="/alarmas">Alarmas</a></li>
		</ul>	
	</li>
	<li><a href="/usuarios">Usuarios</a></li>
	<li><a href="/alertas">Alertas</a></li>
	<li><a href="http://192.168.1.250:8080/logs">Logs</a></li>
	<!--
	<li><a href="http://192.168.1.250:8080/historicos">Historicos</a></li>
	-->
</ul>
</div>


<div id="BotonSalida" style="float:left; margin-left:12px; overflow:hidden;"><a href="/logout"><button>Salir</button></a></div>

<!--
<form action="dummy" method="post">
	<select name="choice" size="1" onChange="jump(this.form)">
		<option value="/logout"><button>Salir</button></option>
		<option value="/poweroff"><button>Apagar</button></option>
		<option value="/reboot">Reiniciar</option>
	</select>
</form>
-->

