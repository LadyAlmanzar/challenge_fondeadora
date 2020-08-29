CREATE OR REPLACE procedure SP_ACT_USUARIO (par_fecha date, V_MSG_ERROR OUT VARCHAR2) AS
/*
   Procedimiento Almacenado: SP_ACT_USUARIO
   Descripcion:  Se realiza procedimiento almacenado para realizar la actualización de información de usuarios registrados
   Parametros:   par_fecha.- Fecha de corte
                               Ejemplo: '20201001'
*/
v_fh_actual    date;
cursor c1 is
SELECT    A.rowid            row_id
    ,A.id
	,A.nombre
	,A.correo
      FROM    usuarios A
    ,(select max(hist_conn.fecha)
        from hist_conn) B 
WHERE    v_fh_actual = B.hist_conn.fecha
   and    A.usuarios.id        = B.hist_conn.id(+)
   
;
v_cont number:=0;
v_cont2 number:=0;
begin
    
    for r1 in c1 loop
        begin
            update usuarios 
               set    id = r1.usuario_activo
             where rowid = r1.row_id
            ;
            if SQL%FOUND = TRUE then
                    v_cont2 := v_cont2 + SQL%ROWCOUNT;
                end if;
            end if;
            if SQL%FOUND = TRUE then
                v_cont := v_cont + SQL%ROWCOUNT;
            end if;
            if mod(c1%rowcount,10000) = 0 then
                commit;
            end if;
        exception
            when no_data_found then
                dbms_output.put_line('===============================================================================');
                dbms_output.put_line('Error: No hay registros en el cursor.');
                dbms_output.put_line('===============================================================================');
                V_MSG_ERROR := sqlerrm;
            when others then
                dbms_output.put_line('===============================================================================');
                dbms_output.put_line('Error: '|| sqlerrm);
                dbms_output.put_line('===============================================================================');
                V_MSG_ERROR := sqlerrm;
                ROLLBACK;
        end;
    end loop;
    commit;
    SP_ANALIZA_TABLA('usuarios');
    V_MSG_ERROR :=sqlerrm;
    dbms_output.put_line('SP_ACT_USUARIO-Registros actualizados= '||v_cont);
    dbms_output.put_line('[SP_ACT_USUARIO]-Registros con usuarios no activos = '||v_cont2);
exception
    when others then
        dbms_output.put_line('===============================================================================');
        dbms_output.put_line('Error: '|| sqlerrm);
        dbms_output.put_line('===============================================================================');
        V_MSG_ERROR := sqlerrm;
        ROLLBACK;
end;
/