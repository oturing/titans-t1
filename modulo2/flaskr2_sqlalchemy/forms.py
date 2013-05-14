#coding: utf-8

from wtforms import Form, TextField, TextAreaField, validators

class ComentarioForm(Form):
    nome = TextField(u'Nome', [validators.Length(min=4, max=32)])
    email = TextField(u'Email', [validators.Email()])
    texto = TextAreaField(u'Comentário',
                    [validators.Length(min=12, max=1000)])

