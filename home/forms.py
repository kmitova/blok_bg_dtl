from django import forms

from home.models import Post, Comment, Reply, Announcement, SupportPost


class PostBaseForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('publication_date', 'user')
        labels = {
            'content': 'Текст',
            'photo': 'Снимка'
        }


class PostCreateForm(PostBaseForm):
    pass


class PostDeleteForm(PostBaseForm):
    def save(self, commit=True):
        if commit:
            SupportPost.objects.filter(id=self.instance.id).delete()
            Comment.objects.filter(post_id=self.instance.id).delete()

            self.instance.delete()
        else:
            pass
        return self.instance


class CommentDeleteForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

    def save(self, commit=True):
        if commit:
            Reply.objects.filter(comment=self.instance.id).delete()

            self.instance.delete()
        else:
            pass
        return self.instance


class ReplyDeleteForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

    def save(self, commit=True):
        if commit:
            self.instance.delete()
        else:
            pass
        return self.instance


class PostEditForm(PostBaseForm):
    pass


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.TextInput(
                attrs={
                    'placeholder': 'Кометирай...',
                }
            )}


class CommentEditForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class ReplyEditForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ('text',)


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ('text',)
        widgets = {
            'text': forms.TextInput(
                attrs={
                    'placeholder': 'Отговори...',
                }
            )}


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ('title', 'content')
        labels = {
            'title': 'Заглавие',
            'content': 'Текст'
        }
