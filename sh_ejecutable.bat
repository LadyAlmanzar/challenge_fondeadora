#!/usr/bin/ksh
# ===========================================================================================
#                                 sh_act_usuario
#
#   Realizar la ejecucion de sp_act_usuario por medio del shell  sh_act_usuario# 
#   para actualizar la información de conexión de los usuarios e identificar los usuarios activos 
#   en la plataforma
#   #   
#   Parametros: Ninguno
#
# ===========================================================================================

echo "\n ========[     INICIA PROCESO   ]======"
echo "\n*--- Inicializa Variables de Trabajo  ---*"

var_fecha3=`sqlplus -s $var_carga<<EOF
set head off pages 0 feed off
quit;
EOF`

echo "*--- PROCESO DE ACTUALIZACION ---*"
echo "*--- PERIODO:  $var_fecha3                 ---*"

echo "\n ========[     INICIA GENERACION Y ACTUALIZACION MV     ]======"
sqlplus $var_carga <<-[] >>$LAR_LOG/sp_act_usuario$var_fecha3.log
start $LAR_SQL/sp_act_usuario.sql $var_fecha3
[]

echo "\n ========[     TERMINA  ACTUALIZACION    ]======"
if [ -s $LAR_DAT/actualizacion_usuario.err ]; then
        echo "\n ========[      Error en proceso de Actualizacion ]========"
        exit 1
fi

echo "\n ========[           PROCESO TERMINADO                  ]========"
