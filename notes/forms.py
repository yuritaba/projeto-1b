from django import forms
from .models import Note, Tag


class NoteForm(forms.ModelForm):
    # Adicione um campo para a tag
    tag_name = forms.CharField(max_length=50, required=False)

    class Meta:
        model = Note
        fields = ['title', 'content']

    def save(self, commit=True):
        # Salve a anotação, mas não a insira no banco de dados ainda
        note = super(NoteForm, self).save(commit=False)
        
        # Recupere o nome da tag do formulário
        tag_name = self.cleaned_data.get('tag_name')
        
        if tag_name:
            # Verifique se a tag já existe
            tag, created = Tag.objects.get_or_create(name=tag_name)
            
            # Associe a anotação à tag
            note.tag = tag
        
        if commit:
            # Salve a anotação e a tag associada
            note.save()
        
        return note
