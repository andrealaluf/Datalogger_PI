<!--<!DOCTYPE html>-->
<html>
<head>
	<title>Datalogger</title>
</head>

<style type="text/css">
  ul {list-style: none;padding: 0px;margin: 0px;}
  ul li {display: block;position: relative;float: left;border:1px solid #000}
  li ul {display: none;}
  ul li a {display: block;background: #000;padding: 5px 10px 5px 10px;text-decoration: none;
           white-space: nowrap;color: #fff;}
  ul li a:hover {background: #f00;}
  li:hover ul {display: block; position: absolute;}
  li:hover li {float: none;}
  li:hover a {background: #f00;}
  li:hover li a:hover {background: #000;}
  #drop-nav li ul li {border-top: 0px;}
  <!--Color del fondo de la pagina-->
  #body { background-color: #C0C0C0;}
</style>

<body>
<!--### ESTE ES UN RECUADRO DE TEXTO DONDE IRIA LOS DATOS DE LA ESTACION ##-->
<table width="640" cellspacing="1" cellpadding="3" border="0" bgcolor="#1E679A">
<tr>
   <td><font color="#FFFFFF" face="arial, verdana, helvetica">
<b>ESTACION</b>
   </font></td>
</tr>
<tr>
   <td bgcolor="#ffffcc">
   <font face="arial, verdana, helvetica">
   Id: {{idplaca}} | Estacion: {{idescuela}}
   </font>
   </td>
</tr>
</table> 

<!--MENU -->
<ul id="drop-nav">
  <li><a href="http://192.168.1.199:8080/tiemporeal">Tiempo Real</a></li>
  <li><a href="http://192.168.1.199:8080/configuracion">Configuracion</a></li>
<!--    <ul>
      <li><a href="#">HTML</a></li>
      <li><a href="#">CSS</a></li>
      <li><a href="#">JavaScript</a></li>
    </ul>
  </li> -->
  <li><a href="http://192.168.1.199:8080/alertas">Alertas</a>
<!--    <ul>
      <li><a href="#">Joomla</a></li>
      <li><a href="#">Drupal</a></li>
      <li><a href="#">WordPress</a></li>
      <li><a href="#">Concrete 5</a></li>
    </ul> -->
  </li>
  <li><a href="http://192.168.1.199:8080/logs">Logs</a></li>
  <li><a href="http://192.168.1.199:8080/historicos">Historicos</a></li>
</ul>
</body>
</html>
