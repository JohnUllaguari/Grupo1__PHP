//Clases, atributos, métodos
#Comentarios de prueba tambien

<?php
class Persona {
    private $nombre;
    private $edad;

    function __construct($nombre, $edad) {
        $this->nombre = $nombre;
        $this->edad = $edad;
    }

    public function saludar() {
        echo "Hola, soy " . $this->nombre . " y tengo " . $this->edad . " años.";
    }
}

$alumno = new Persona("Luis", 20);
$alumno->saludar();
edad = 20;

?>