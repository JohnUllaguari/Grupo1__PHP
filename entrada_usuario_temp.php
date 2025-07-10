<?php
$texto = "Hola mundo";  // tipo string

// Asignación compatible
$texto = "Otro texto";  // OK

// Asignación incompatible
$texto = 5 + 7.8;  //  Debe dar incompatible

$numero = 10;
$otro = 20;

// Comparación válida
if ($numero > $otro) {
  echo "OK";
}

// Comparación incompatible
if ($numero > "texto") {  //  Debe dar incompatible
  echo "Comparación rara";
}
?>