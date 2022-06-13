
var lg_obj;

function fn_verificar(){

// Paso 1. Verificar llave
    let lv_llave = $("#id_llave_cliente").val();
    
    if(lv_llave == ""){
        alertify.alert("¡Información!", "Debe ingresar su código de cliente.");
        return false;
    }

    $.getJSON(lv_url_key + '?key_access=' + lv_llave,
    function (data) {
        if (data != null){
            

            alertify.success('Código Correcto');

            // Mostrar resultados
            data.forEach(element => {
                document.getElementById("id_nombre_cliente").innerHTML = "<strong> Bienvenido " + element.nombre_empresa + "</strong>"; // Mostrar el nombre del Cliente
                //$("#id_cliente option[value=" + element.id + "]").attr("selected",true); // Seleccionar el cliente
                $("#id_cliente").val(element.id);
                lg_obj = element.id;
                
            });

            document.getElementById("id_form_pedido").style.display = ""; // Mostrar Formulario para el pedido
            document.getElementById("id_form_llave").style.display = "none"; // Ocultar Formulario de validación de llave
        }else{
            alertify.error("El código ingresado no es correcto, verifique e intente de nuevo.");
        }



// Paso 2. Cargar los negocios asociados al cliente

        //console.log($("#id_cliente").val());
    
        $("#id_negocio").empty(); // Limpiar lista de negocios
        $("#id_negocio").append('<option value="" selected disabled> ---- </option>');

        if(lg_obj == ""){
            return false;
        }
        
        $.getJSON(lv_url_negocios + '?cliente=' + lg_obj,
        function (data) {
            $.each(data, function (key, registro) {
                // cargar los negocios sólo a los que el cliente tiene acceso.
                if(registro.negocio ){
                    $("#id_negocio").append('<option value="' + registro.negocio.id + '">' + registro.negocio.nombre_negocio + '</option>');
                }
                
            });
        });


    });

    
}






function fn_verificar_codigo(){

    // Paso 1. Verificar llave
        let lv_llave = $("#id_llave_cliente").val();
        
        if(lv_llave == ""){
            alertify.alert("¡Información!", "Debe ingresar su código de cliente.");
            return false;
        }
    
        $.getJSON(lv_url_key + '?key_access=' + lv_llave,
        function (data) {
            if (data != null){
                
    
                alertify.success('Código Correcto');
    
                // Mostrar resultados
                data.forEach(element => {
                    document.getElementById("id_nombre_cliente").innerHTML = "<strong> Bienvenido " + element.nombre_empresa + "</strong>"; // Mostrar el nombre del Cliente
                    //$("#id_cliente option[value=" + element.id + "]").attr("selected",true); // Seleccionar el cliente

                    // Construir la url para update pasando como parámetro 123 321 y luego reemplazarlo por la llave y el ID
                    lv_url_cliente = lv_url_cliente.replace('123', element.key_access);
                    lv_url_cliente = lv_url_cliente.replace('321', element.id);

                    document.getElementById("id_link_generator").href = lv_url_cliente;

                });
    
                document.getElementById("id_link_access").style.display = ""; // Mostrar Formulario para el pedido
                document.getElementById("id_form_llave").style.display = "none"; // Ocultar Formulario de validación de llave
            }else{
                alertify.error("El código ingresado no es correcto, verifique e intente de nuevo.");
            }
        });
}