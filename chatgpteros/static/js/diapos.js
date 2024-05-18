document.addEventListener('DOMContentLoaded', function() {
    var formset = document.getElementById('formset-container');
    var totalForms = document.getElementById('id_diapositiva_set-TOTAL_FORMS');
    var addButton = document.getElementById('agregar-diapositiva');

    /*
    // Funcionalidad de editor de texto: color de texto
    */
    function addColorPicker(simplemde, textarea) {
        var toolbar = textarea.parentElement.getElementsByClassName('editor-toolbar')[0];
        if (!toolbar) {
            console.error("Toolbar not found for the textarea");
            return;
        }
        var colorPickerInput = document.createElement("input");
        colorPickerInput.type = "color";
        colorPickerInput.title = "Cambiar color del texto";
        toolbar.appendChild(colorPickerInput);

        colorPickerInput.addEventListener("change", function() {
            var selectedColor = colorPickerInput.value;
            var selectedText = simplemde.codemirror.getSelection();
            if (selectedText) {
                var newText = `<span style='color:${selectedColor}'>${selectedText}</span>`;
                simplemde.codemirror.replaceSelection(newText);
            }
        });
    }

    function initializeSimpleMDE(textarea) {
        var simplemde = new SimpleMDE({ element: textarea, spellChecker: false });
        addColorPicker(simplemde, textarea);
    }

    function createNewForm(index) {
        var newForm = document.createElement('div');
        newForm.className = 'formset-row';
        newForm.innerHTML = `
            <p><label for="id_diapositiva_set-${index}-subtitulo">Subtítulo (opcional):</label>
            <input type="text" id="id_diapositiva_set-${index}-subtitulo" name="diapositiva_set-${index}-subtitulo"></p>
            <p><label for="id_diapositiva_set-${index}-contenido">Contenido:</label>
            <textarea id="id_diapositiva_set-${index}-contenido" name="diapositiva_set-${index}-contenido" class="markdown-editor"></textarea></p>
        `;
        formset.appendChild(newForm);
        initializeSimpleMDE(newForm.querySelector('.markdown-editor'));
    }

    function addNewSlide() {
        var formIndex = parseInt(totalForms.value);
        createNewForm(formIndex);
        totalForms.value = formIndex + 1;
    }

    addButton.addEventListener('click', addNewSlide);

    document.querySelectorAll('.markdown-editor').forEach(initializeSimpleMDE);
});
