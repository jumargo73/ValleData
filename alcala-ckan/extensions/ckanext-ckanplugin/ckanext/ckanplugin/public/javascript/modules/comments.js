this.ckan.module('dataset-comment-component', function ($, _) {

    return {
        initialize: function () {
            console.log('dataset-comment-component iniciado');
            // 1. Guardamos una referencia al módulo para usarla dentro del evento
            const self = this;

            // 1. Detectar el idioma inicial de la página (buscando el atributo lang de HTML)
            const idiomaInicial = document.documentElement.lang || 'es';

            self.fetchComments(idiomaInicial);

            // 3. Escuchar el evento global de cambio de idioma
            window.addEventListener('cambioDeIdioma', function (event) {
                const nuevoIdioma = event.detail.idioma;
                console.log('Módulo comentario detectó cambio de idioma a:', nuevoIdioma);
                
                // Volvemos a ejecutar la función interna de AJAX con el nuevo idioma
                self.fetchComments(nuevoIdioma);
            });
            // Escuchar el evento submit del formulario dentro del componente
            this.el.on('submit', 'form', $.proxy(this._onSubmit, this));
           
        },
        fetchComments: function (idioma) {

            var datasetId = this.el.data('resource-id');  
            const userId = localStorage.getItem('ratingUserId');             
            const csrfToken = document
                .querySelector('meta[name="_csrf_token"]')
                .getAttribute('content');

            $.ajax({
                url: '/api/3/action/comments_get',
                type: 'POST',
                contentType: 'application/json',
                headers: { 'X-CSRF-Token': csrfToken },
                data: JSON.stringify({
                    dataset_id: datasetId,
                    user_id: userId,
                    lang:idioma
                }) // El paréntesis de JSON.stringify se cierra aquí
            })
            .done(function(res) {
                // jQuery ya parseó el JSON. 'res' es el objeto directo.
                console.log(res)
                var result=res.result
                console.log(result)
                if (result.success && result.comment) { 

                    console.log('Comentario recibido en ' + idioma + ':', result.comment.comment_text);
                    $('#comment_text').val(''); 
                    $("#div_comment").empty(); 

                    var newCommentHtml = `
                        <div class="comment-item" style="background:#f9f9f9; padding:10px; margin-bottom:10px; border-left:4px solid #28a745;">
                            <strong>${result.comment.user_guid ? `Anónimo (${result.comment.user_guid})` : ''}</strong> 
                            <small class="muted" style="float:right;">${result.comment.created}</small>
                            <p style="margin:5px 0 0 0;">${result.comment.comment_text}</p>
                        </div>
                    `;
                    $("#div_comment").append(newCommentHtml);
                } else {
                    console.log('Comentario recibido en ' + idioma + ':', result.message);
                    $('#comment_text').val(''); 
                    $("#div_comment").empty(); 

                    var newCommentHtml = `
                        <div class="comment-item" style="background:#f9f9f9; padding:10px; margin-bottom:10px; border-left:4px solid #28a745;">
                            <p style="margin:5px 0 0 0;">${result.message}</p>
                        </div>
                    `;
                    $("#div_comment").append(newCommentHtml);  
                }
            })
            .fail(function(xhr, status, error) {
                console.error(error);
                alert('Ocurrió un error de red al recibir el comentario.');
            });

        },
        _onSubmit: function (event) {
        event.preventDefault();
        
        var $form = $(event.currentTarget);
        var $textarea = $form.find('textarea[name="comment_text"]');
        var $button = $form.find('button[type="submit"]');
        var $list = this.el.find('.comments-list'); // Contenedor donde se listan
        const csrfToken = document
        .querySelector('meta[name="_csrf_token"]')
        .getAttribute('content');

        var datasetId = $form.data('dataset-id');
        var commentText = $textarea.val().trim();
        const userId = localStorage.getItem('ratingUserId');

        if (!commentText) return;

        // Deshabilitar UI durante el envío
        $button.prop('disabled', true).text('Enviando...');

        // Petición AJAX nativa moderna utilizando fetch
        fetch('/api/3/action/comments_set', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json','X-CSRF-Token': csrfToken},
            body: JSON.stringify({ dataset_id: datasetId, comment_text: commentText,userId:userId })
        })
        .then(response => response.json().then(data => ({ status: response.status, body: data })))
        .then(res => {
            if (res.status === 200 && res.body.success) {
            // Limpiar el campo de texto
            
                this.fetchComments();
            
            } else {
            alert('Error: ' + (res.body.error || 'No se pudo guardar el comentario.'));
            }
        })
        .catch(err => {
            console.error(err);
            alert('Ocurrió un error de red al enviar el comentario.');
        })
        .finally(() => {
            // Restablecer el botón
            $button.prop('disabled', false).text('Enviar Comentario');
        });
    
        }
    };
})  