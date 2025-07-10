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

// Definición de listas (arrays)
$numeros = array(1, 2, 3);
$palabras = array("hola", "mundo");

// Estructura de control if-else con expresión booleana
if ($numeros[0] > 0) {
  echo "Primer número es positivo";
} else {
  echo "Primer número no es positivo";
}

// Declaración de función con retorno y variable
function saludar($nombre) {
  return "Hola, " . $nombre;
}
echo saludar("Joseph");

// Expresión aritmética correcta
$suma = 5 + 3;

// Expresión aritmética incompatible: sumando número con string
$suma_error = 5 + "texto";

// Asignación incompatible: variable string recibe número
$mensaje = "Hola mundo";
$mensaje = 5;

// Operación inválida: sumar lista con número
$resultado_error = $numeros + 5;

?>