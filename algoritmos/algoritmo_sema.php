<?php

$notas = array("mate" => 9, "lengua" => 8);

foreach ($notas as $nota) {
    echo $nota;
}

class Persona {
    static function saludar() {
        echo "Hola";
    }
}

$nombre = readline("Ingrese su nombre: ");
echo $nombre;

?>
