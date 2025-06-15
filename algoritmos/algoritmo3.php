<?php
// Segundo algoritmo para prueba léxica
# Incluye condiciones, bucles y funciones

$contador = 0;
$limite = 5;

function mensaje($nombre) {
    return "Hola, " . $nombre . "!";
}

$nombreUsuario = "Luis";
echo mensaje($nombreUsuario) . "\n";

$pares = array();

while ($contador < $limite) {
    if ($contador % 2 == 0) {
        $pares[] = $contador;
        echo "Par encontrado: " . $contador . "\n";
    } else {
        echo "Impar: " . $contador . "\n";
    }
    $contador++;
}

$sum = 0;
for ($i = 0; $i < count($pares); $i++) {
    $sum += $pares[$i];
}

echo "Suma de pares: " . $sum . "\n";
?>
