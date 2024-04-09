$(function () {

    var productosAgregados = {};

    $('#agregar-producto').on('click', function (e) {
        e.preventDefault();
        var productoId = $('#producto').val();
        var productoNombre = $('#producto option:selected').text();
        var productoPrecio = parseInt($('#producto option:selected').data('precio'));
        var cantidad = parseInt($('#cantidad').val());

        if (productosAgregados.hasOwnProperty(productoId)) {
            productosAgregados[productoId].cantidad += cantidad;
            $('#cantidad-' + productoId).text(productosAgregados[productoId].cantidad);
            
        } else {
            productosAgregados[productoId] = {
                nombre: productoNombre,
                precio: productoPrecio,
                cantidad: cantidad,
                subtotal: 0
            };
            var listItem = '';
            listItem += '<li id="producto-'+ productoId +'" class="list-group-item">';
            listItem +=     productoNombre + ' (<span id="cantidad-' + productoId + '">'+ productosAgregados[productoId].cantidad +'</span>)';
            listItem +=     ' --> Subtotal:  <span id="subtotal-' + productoId + '"></span>';
            listItem += '   <input type="hidden" name="productos[]" value="' + productoId + '">';
            listItem += '   <input type="hidden" name="cantidad-'+ productoId +'" value="'+ productosAgregados[productoId].cantidad + '">';
            listItem += '   <button class="btn btn-danger eliminar-producto" type="button" data-producto-id="'+ productoId +'">Eliminar</button>';
            listItem += '   <button class="btn btn-danger eliminar-todos" type="button" data-producto-id="'+ productoId +'">Eliminar todos</button>';
            listItem += '   </li>';
            $('#productos-agregados').append(listItem);
        }

        calcularSubtotal(productoId);
        calcularTotalPedido();
    });

    $(document).on('click', '.eliminar-producto', function () {
        var productoId = $(this).data('producto-id');
        var cantidad = parseInt($('#cantidad').val());

        productosAgregados[productoId].cantidad -= cantidad;
        $('#cantidad-' + productoId).text(productosAgregados[productoId].cantidad);        $('#cantidad-' + productoId).text(productosAgregados[productoId].cantidad);
        if (productosAgregados[productoId].cantidad === 0) {
            delete productosAgregados[productoId];
            $('#producto-' + productoId).remove();
            calcularTotalPedido();
        }

        calcularSubtotal(productoId);
        calcularTotalPedido();
    });

    $(document).on('click', '.eliminar-todos', function() {
        var productoId = $(this).data('producto-id');
        delete productosAgregados[productoId];
        $('#producto-' + productoId).remove();
        calcularTotalPedido();
    });

    function formatoMoneda(valor) {
        return Intl.NumberFormat('es-CL', { style: 'currency', currency: 'CLP' }).format(valor);
    }

    function calcularSubtotal(productoId) {
        var producto = productosAgregados[productoId];
        producto.subtotal = producto.cantidad * producto.precio;
        $('#subtotal-' + productoId).text(formatoMoneda(producto.subtotal));
    }
    
    function calcularTotalPedido() {
        var totalPedido = 0;
        for (var productoId in productosAgregados) {
            var producto = productosAgregados[productoId];
            totalPedido += producto.subtotal;
        }
        if (totalPedido === 0) {
            $('#total-pedido').text('$0')
        } else {
            $('#total-pedido').text(formatoMoneda(totalPedido));
        }
        $('#input-total-pedido').val(totalPedido);
    };
});