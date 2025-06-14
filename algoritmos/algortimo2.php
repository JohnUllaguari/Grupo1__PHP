<?php
function saludar($nombre) {
    if ($nombre != "") {
        echo "Hola, " . $nombre;
    } else {
        echo "Nombre vacío";
    }
}

function miFuncion($parametro1, $parametro2) {
  // Bloque de código de la función
  $resultado = $parametro1 + $parametro2;
  return $resultado;
}

$_valor1 = 10;
$_valor2 = 5;
$_resultadoFinal = miFuncion($valor1, $valor2);
echo $_resultadoFinal; // Imprimirá 15

saludar("Joseph");
?>
