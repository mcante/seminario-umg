
// SELECT2 PURO
function init_select2() {
    console.log('init_select2');
    //Initialize Select2 Elements
    $('.select2').select2({
        width: 'auto',
        //theme: "classic",
        //theme: "bootstrap-5",
        selectOnClose: false,
    });
};

// SELECT2 CON BOOTSTRAP
function init_select2_bootstrap_4() {
    console.log('init_select2_bootstrap_4');
    //Initialize Select2 Elements
    $('.select2bs4').select2({
        width: 'auto',
        //theme: "classic",
        theme: "bootstrap4",
        selectOnClose: false,
    });
};




function init_datapicker() {
    console.log('init_datapicker');
    //Initialize DataPicker Elements
    $('.datepicker').datepicker({
        format: "dd/mm/yyyy",
        language: "es",
        autoclose: true,
        todayHighlight: true,
        orientation: 'bottom' //Muetra el calendario abajo de la caja de texto
    });
};



function init_datatables_full() {    
    
    if (typeof($.fn.DataTable) === 'undefined') {
        return;
    }
    
    console.log('init_datatables_full');

    var hoy = new Date();
    var hora = hoy.getHours() + ':' + hoy.getMinutes() + ':' + hoy.getSeconds();
    var fecha = hoy.getDate() + '-' + ( hoy.getMonth() + 1 ) + '-' + hoy.getFullYear();
    var fechaYHora = fecha + '--' + hora;

    
    //Función de DataTable para establecer sus parámetros
    $("#dataTablesFull").DataTable({
        
        dom: "Blfrtip",
        buttons: [{
            extend: "copy",
            className: "btn-primary"
        }, {
            text: "Csv",
            extend: "csv",
            charset: 'UTF-8',
            fieldBoundary: '',
            bom: true,
            className: "btn-info",
            filename: "Resultados del reporte " + fechaYHora,
            title: "RESULTADOS DEL REPORTE",
        }, {
            text: "Excel",
            extend: "excelHtml5",
            charset: 'UTF-8',
            fieldBoundary: '',
            className: "btn-success",
            filename: "Resultados del reporte " + fechaYHora,
            title: "RESULTADOS DEL REPORTE",
        }, {
            extend: "pdfHtml5",
            text: 'PDF',
            className: "btn-danger",
            filename: "Resultados del reporte " + fechaYHora,
            messageBottom: "MRCG",
            orientation: "landscape",
            pageSize: "LEGAL",
            title: "RESULTADOS DEL REPORTE",
        } ],
        //Cambiar el idioma, también se puede hacer con un json
        
        language: {
            
            "sProcessing":     "Procesando...",
            "sLengthMenu":     "Mostrar _MENU_ registros",
            "sZeroRecords":    "No se encontraron resultados",
            "sEmptyTable":     "Ningún dato disponible en esta tabla",
            "sInfo":           "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
            "sInfoEmpty":      "Mostrando registros del 0 al 0 de un total de 0 registros",
            "sInfoFiltered":   "(filtrado de un total de _MAX_ registros)",
            "sInfoPostFix":    "",
            "sSearch":         "Buscar:",
            "sUrl":            "",
            "sInfoThousands":  ",",
            "sLoadingRecords": "Cargando...",
            "lengthChange": false,
            "oPaginate": {
                "sFirst":    "Primero",
                "sLast":     "Último",
                "sNext":     "Siguiente",
                "sPrevious": "Anterior"
            },
            "oAria": {
                "sSortAscending":  ": Activar para ordenar la columna de manera ascendente",
                "sSortDescending": ": Activar para ordenar la columna de manera descendente"
            }
        },
        //responsive: true // No permitir que la tabla resultante sea responsive
        //"ordering": false // Deshabilitar las opciones de filtros en las columnas.
        paging: true,
        pagingType: "full_numbers",
        fixedColumns: true,
        "pageLength": 10,
        "order": [[ 0, "desc" ]] // Indicar que se desea ordenar descendentemente la columna 1
    });
    
    
    
    /*
    
    // // Crear una variable de tipo dataTables, es decir del DIV de la tabla para poderla manipular.
    var table = $("#dataTables2").DataTable();
    
    
    // // Aplicar las búsquedas por cada columna.
    table.columns().every( function () {
        var that = this;
        
        //En el tfooter se crearon los campos con th, se aplicada cada filtro a cada campo según su columna.
        $( 'input', this.footer() ).on( 'keyup change', function () {
            if ( that.search() !== this.value ) {
                that
                .search( this.value )
                .draw();
            }
        } );
    });
    */
    
};
