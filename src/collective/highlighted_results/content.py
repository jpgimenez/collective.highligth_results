# -*- coding: utf-8 -*-

from DateTime import DateTime
from zope import schema
from zope.interface import invariant, Invalid

from plone.indexer import indexer
from plone.directives import form, dexterity
from z3c.relationfield.schema import (
    RelationChoice,
    Relation,
)
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.namedfile.field import NamedImage

from plone.app.dexterity import PloneMessageFactory as __
from collective.highlighted_results.config import _


class TargetOrTitle(Invalid):
    """
    """


class Ird(form.Schema):
    """
    """

    # Destino: opcional. Será un campo del tipo "Contenidos relacionados"
    #          pero se podrá elegir un único contenido.
    target = RelationChoice(title=u"Target",
                            source=ObjPathSourceBinder(),
                            required=False,
                            )

    # Título: se mostrará como título en los resultados de búsqueda.
    #         Si no se carga un título se tomará el título del contenido de Destino.
    # Descripción: ídem Título.
    # default fieldset
    title = schema.TextLine(
        title = __(u'label_title', default=u'Title'),
        required = False
        )
        
    description = schema.Text(
        title=__(u'label_description', default=u'Description'),
        description = __(u'help_description', default=u'A short summary of the content.'),
        required = False,
        missing_value = u'',
        )
    
    form.order_before(description = '*')
    form.order_before(title = '*')
    form.order_before(target = '*')
    
    # Link: ídem Título.
    link = schema.TextLine(
        title = _(u'label_link', default=u'Link'),
        required=False,
        )

    # Imagen: ídem Título.
    image = NamedImage(
            title=_(u"Image"),
            required=False,
        )    

    # Comentarios: internos, deberían mostrarse en el área de configuración de RD.
    comments = schema.Text(
        title=_(u'label_comments', default=u'Comments'),
        required = False,
        missing_value = u'',
        )

    # Palabras clave: campo de libre llenado para ingresar varios términos que,
    #                 al ser buscados por un usuario, provocarán que este RD aparezca.
    keywords = schema.Text(
        title=_(u'label_keywords', default=u'Keywords'),
        required = True,
        missing_value = u'',
        )

    # Habilitado: Sí/No. Para controlar si debe o no aparecer el RD.
    enabled = schema.Bool(
        title=_(u"Enabled"),
    )

    @invariant
    def validateTargetOrTitle(data):
        if not data.target and not (data.title and data.link):
            raise TargetOrTitle(_(u"The RD should have a target or a title+link."))


@indexer(Ird)
def ExpirationDateIndexer(obj):
    return DateTime()


@indexer(Ird)
def searchableIndexer(context):
    return context.keywords

@indexer(Ird)
def getRemoteUrl(context):
    return data.link and data.link or data.target.absolute_url()