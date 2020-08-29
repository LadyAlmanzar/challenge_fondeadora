/* Definición Tabla Usuario
ID	INT64
NOMBRE	VARCHAR(30)
APELLIDO	VARCHAR(30)
CORREO	VARCHAR(30)
TELEFONO	INT
NOMBRE_SHOW  VARCHAR(30)
______________________

Definición Tabla hist_conn
ID INT64
FECHA   DATE 
TIEMPO_CONN  TIMESTAMP 
*/

 
CREATE VIEW AGGREGATEVIEW (Nombre,show, tiempo_conn) AS
        SELECT usuarios.nombre, usuarios.nombre_show , hist_conn.tiempo_conn
		FROM usuarios , hist_conn
		WHERE usuarios.id = hist_conn.id
		
	
	exec dbms_mview.refresh( 'vista_materializada', atomic_refresh=>false);