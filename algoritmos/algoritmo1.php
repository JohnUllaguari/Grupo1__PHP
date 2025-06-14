<?php
function obtenerPromedio($notas) {
    $total = 0;
    foreach ($notas as $nota) {
        $total += $nota;
    }
    return $total / count($notas);
}

$notas = array(8, 7.5, 9);
$promedio = obtenerPromedio($notas);

if ($promedio >= 7) {
    echo "Aprobado";
} else {
    echo "Reprobado";
}
?>
