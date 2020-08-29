/* Se crea vista para realizar la consulta de usuarios activos por día y por mes */
 CREATE MATERIALIZED VIEW vista_materializada

   TABLESPACE users_tablespace

   PARALLEL 4

   BUILD IMMEDIATE

   REFRESH COMPLETE ON DEMAND

   AS SELECT usuarios.id, usuarios.nombre, hist_conn.fecha, hist_conn.id

    FROM usuarios , hist_conn

    WHERE usuarios.id = hist_conn.id
	
	exec dbms_mview.refresh( 'vista_materializada', atomic_refresh=>false);