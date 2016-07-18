<!--<!DOCTYPE html>-->
% include('menu_gral.tpl')

<!--
<div id="AltaUsuario">
<h3><br><font color = "#1E679A">AGREGAR USUARIOS</font></br></h3>
<HR width=40% align="left" color = "#1E679A">
<form style="margin-left:10px" action="/usuarios" method="post">
	<P> Nombre:   <input name="nombre" type="text"/></P>
	<P> Apellido: <input name="apellido" type="text" /></P>
	<P> Email:     <input name="mail" type="text" /></P>
	<P> Tel/Cel: <input name="telefono" type="text" /></P>
	<P> Usuario: <input name="usuario" type="text" /></P>
	<P> Contraseña: <input name="contraseña" type="password" /></P>
	<p>Rol: <select name="rol">
		<option value="administrador">Administrador</option>
		<option value="tecnico">Tecnico</option>
		<option value="usuario">Usuario</option>
		</select>
		</p>
		<input type="submit"value="Agregar"/>
</form>
</div>
-->

<div id="Container" style="position: absolute; left: 10px; top: 150px;">

<div id="AltaUsuario">
<form action="/usuarios" method="post">
  <fieldset>
  <legend><strong/>ALTA DE USUARIO</legend>
    <label for="nombre">Nombre:</label>
    <input type="text" name="nombre" id="nombre" />
    <br />
    <label for="apellido">Apellido:</label>
    <input type="text" name="apellido" id="apellido" />
    <br />
    <label for="mail">E-mail:</label>
    <input type="text" name="mail" id="mail" />
    <br />
    <label for="telefono">Tel/Cel:</label>
    <input type="text" name="telefono" id="telefono" />
    <br />
    <label for="usuario">Usuario:</label>
    <input type="text" name="usuario" id="usuario" size="40" />
    <br />
    <label for="contraseña">Contraseña:</label>
    <input type="password" name="contraseña" id="contraseña" size="20" />
    <br />
    <label for="rol">Rol:</label>
    	<select name="rol">
		<option value="administrador">Administrador</option>
		<option value="tecnico">Tecnico</option>
		<option value="usuario">Usuario</option>
		</select>
		</p>
    <br />
      <input type="submit" value="Agregar"/>
  </fieldset>
</form>
</div>

<div id="ListaUsuarios" style="float:left;">
<h3><br><font color = "#1E679A">USUARIOS REGISTRADOS</font></br></h3>
<table border="1" cellpadding="5" cellspacing="5">
<tr><th>Id</th><th>Nombre</th><th>Apellido</th><th>Email</th><th>Tel</th><th>Usuario</th><th>Clave</th><th>Rol</th></tr>
%for row in rows:
    <tr>
    %for col in row:
        <td>{{col}}</td>
    %end
    </tr>
%end
</table>
</div>

</div>

</body>
</html>
