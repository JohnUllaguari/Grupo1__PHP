<?php
// === Prueba de función anónima ===
$saludo = function($nombre) {
    return "Hola " . $nombre;
};

// === Prueba de array multidimensional ===
$matriz = [[1, 2], [3, 4], [5, 6]];

// === Prueba de estructura de control: while ===
$i = 0;
while ($i < 3) {
    echo $saludo("Steeven") . "\n";
    $i++;
}
?>
