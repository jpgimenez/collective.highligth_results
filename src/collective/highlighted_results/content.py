# -*- coding: utf-8 -*-

from DateTime import DateTime
from zope import schema
from zope.interface import invariant, Invalid

from plone.indexer import indexer
from plone.directives import form
from z3c.relationfield.schema import RelationChoice
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
    target = RelationChoice(
        title=_(u"Target"),
        source=ObjPathSourceBinder(),
        required=False,
    )

    # Título: se mostrará como título en los resultados de búsqueda.
    #         Si no se carga un título se tomará el título del contenido de Destino.
    # Descripción: ídem Título.
    # default fieldset
    title = schema.TextLine(
        title=__(u'label_title', default=u'Title'),
        required=False
    )

    description = schema.Text(
        title=__(u'label_description', default=u'Description'),
        required=False,
        default=u'',
        missing_value=u'',
    )

    form.order_before(description='*')
    form.order_before(title='*')
    form.order_before(target='*')

    # Link: ídem Título.
    link = schema.TextLine(
        title=_(u'label_link', default=u'Link'),
        required=False,
    )

    # Imagen: ídem Título.
    image = NamedImage(
        title=_(u"Image"),
        required=False,
    )

    # Palabras clave: campo de libre llenado para ingresar varios términos que,
    #                 al ser buscados por un usuario, provocarán que este RD aparezca.
    keywords = schema.Text(
        title=_(u'label_keywords', default=u'Keywords'),
        required=True,
        default=u'',
        missing_value=u'',
    )

    # Habilitado: Sí/No. Para controlar si debe o no aparecer el RD.
    enabled = schema.Bool(
        title=_(u"Enabled"),
        default=True,
    )

    # Comentarios: internos, deberían mostrarse en el área de configuración de RD.
    comments = schema.Text(
        title=_(u'label_comments', default=u'Comments'),
        required=False,
        default=u'',
        missing_value=u'',
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
def has_image(context):
    return bool(context.image)


@indexer(Ird)
def getRemoteUrl(context):
    return context.link and context.link or context.target.to_object.absolute_url()


@indexer(Ird)
def Title(context):
    return context.title and context.title or context.target.to_object.Title()


@indexer(Ird)
def inactive(context):
    return not bool(context.enabled)
