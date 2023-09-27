document.addEventListener("DOMContentLoaded", function () {
  const tagInput = document.getElementById('tag_name');
  const tagSuggestions = document.getElementById('tag-suggestions');
  
  tagInput.addEventListener('input', () => {
    const inputText = tagInput.value;
  
    // Enviar uma solicitação AJAX para obter sugestões de tags com base no texto de entrada
    fetch(`/tag-suggestions/?q=${inputText}`)
      .then(response => response.json())
      .then(data => {
        // Limpar sugestões anteriores
        tagSuggestions.innerHTML = '';
  
        // Exibir sugestões
        data.forEach(tag => {
          const suggestion = document.createElement('div');
          suggestion.textContent = tag;
          //suggestion.setAttribute('style', `background-color: {{ color }}`);
          suggestion.classList.add('tag-suggestion'); // Adicione a classe CSS
          suggestion.addEventListener('click', () => {
            // Preencher a textarea da tag com a sugestão
            tagInput.value = tag;
            // Limpar sugestões após escolher uma
            tagSuggestions.innerHTML = '';
          });
          tagSuggestions.appendChild(suggestion);
        });
      });
  });


});