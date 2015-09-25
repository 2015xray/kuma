from django.conf.urls import include, url
from django.views.generic import TemplateView

from kuma.attachments.feeds import AttachmentsFeed

from . import feeds, views
from .constants import DOCUMENT_PATH_RE


# These patterns inherit (?P<document_path>[^\$]+).
document_patterns = [
    url(r'^$',
        views.document.document,
        name='wiki.document'),
    url(r'^\$revision/(?P<revision_id>\d+)$',
        views.revision.revision,
        name='wiki.revision'),
    url(r'^\$history$',
        views.list.revisions,
        name='wiki.document_revisions'),
    url(r'^\$edit$',
        views.edit.edit,
        name='wiki.edit'),
    url(r'^\$edit/(?P<revision_id>\d+)$',
        views.edit.edit,
        name='wiki.new_revision_based_on'),
    url(r'^\$compare$',
        views.revision.compare,
        name='wiki.compare_revisions'),
    url(r'^\$children$',
        views.document.children,
        name='wiki.children'),
    url(r'^\$flag',
        views.misc.flag,
        name='wiki.flag_document'),
    url(r'^\$translate$',
        views.translate.translate,
        name='wiki.translate'),
    url(r'^\$locales$',
        views.translate.select_locale,
        name='wiki.select_locale'),
    url(r'^\$json$',
        views.document.as_json,
        name='wiki.json_slug'),
    url(r'^\$styles$',
        views.document.styles,
        name='wiki.styles'),
    url(r'^\$toc$',
        views.document.toc,
        name='wiki.toc'),
    url(r'^\$move$',
        views.document.move,
        name='wiki.move'),
    url(r'^\$quick-review$',
        views.revision.quick_review,
        name='wiki.quick_review'),
    url(r'^\$samples/(?P<sample_id>.+)/files/(?P<attachment_id>\d+)/(?P<filename>.+)$',
        views.code.raw_code_sample_file,
        name='wiki.raw_code_sample_file'),
    url(r'^\$samples/(?P<sample_id>.+)$',
        views.code.code_sample,
        name='wiki.code_sample'),
    url(r'^\$revert/(?P<revision_id>\d+)$',
        views.delete.revert_document,
        name='wiki.revert_document'),
    url(r'^\$repair_breadcrumbs$',
        views.document.repair_breadcrumbs,
        name='wiki.repair_breadcrumbs'),
    url(r'^\$delete$',
        views.delete.delete_document,
        name='wiki.delete_document'),
    url(r'^\$restore$',
        views.delete.restore_document,
        name='wiki.restore_document'),
    url(r'^\$purge$',
        views.delete.purge_document,
        name='wiki.purge_document'),

    # Un/Subscribe to document edit notifications.
    url(r'^\$subscribe$',
        views.document.subscribe,
        name='wiki.subscribe'),

    # Vote helpful/not helpful
    url(r'^\$vote',
        views.misc.helpful_vote,
        name="wiki.document_vote"),
]

urlpatterns = [
    url(r'^/ckeditor_config.js$',
        views.misc.ckeditor_config,
        name='wiki.ckeditor_config'),

    # internals
    url(r'^.json$',
        views.document.as_json,
        name='wiki.json'),
    url(r'^/preview-wiki-content$',
        views.revision.preview,
        name='wiki.preview'),
    url(r'^/move-requested$',
        TemplateView.as_view(template_name='wiki/move_requested.html'),
        name='wiki.move_requested'),
    url(r'^/get-documents$',
        views.misc.autosuggest_documents,
        name='wiki.autosuggest_documents'),
    url(r'^/load/$',
        views.misc.load_documents,
        name='wiki.load_documents'),

    # Special pages
    url(r'^/templates$',
        views.list.templates,
        name='wiki.list_templates'),
    url(r'^/tags$',
        views.list.tags,
        name='wiki.list_tags'),
    url(r'^/tag/(?P<tag>.+)$',
        views.list.documents,
        name='wiki.tag'),
    url(r'^/new$',
        views.create.create,
        name='wiki.create'),
    url(r'^/all$',
        views.list.documents,
        name='wiki.all_documents'),
    url(r'^/with-errors$',
        views.list.with_errors,
        name='wiki.errors'),
    url(r'^/without-parent$',
        views.list.without_parent,
        name='wiki.without_parent'),
    url(r'^/top-level$',
        views.list.top_level,
        name='wiki.top_level'),
    url(r'^/needs-review/(?P<tag>[^/]+)$',
        views.list.needs_review,
        name='wiki.list_review_tag'),
    url(r'^/needs-review/?',
        views.list.needs_review,
        name='wiki.list_review'),
    url(r'^/localization-in-progress$',
        views.list.with_localization_in_progress,
        name='wiki.list_with_localization_in_progress'),
    url(r'^/category/(?P<category>\d+)$',
        views.list.documents,
        name='wiki.category'),

    # Feeds
    url(r'^/feeds/(?P<format>[^/]+)/all/?',
        feeds.DocumentsRecentFeed(),
        name="wiki.feeds.recent_documents"),
    url(r'^/feeds/(?P<format>[^/]+)/l10n-updates/?',
        feeds.DocumentsUpdatedTranslationParentFeed(),
        name="wiki.feeds.l10n_updates"),
    url(r'^/feeds/(?P<format>[^/]+)/tag/(?P<tag>[^/]+)',
        feeds.DocumentsRecentFeed(),
        name="wiki.feeds.recent_documents"),
    url(r'^/feeds/(?P<format>[^/]+)/category/(?P<category>[^/]+)',
        feeds.DocumentsRecentFeed(),
        name="wiki.feeds.recent_documents_category"),
    url(r'^/feeds/(?P<format>[^/]+)/needs-review/(?P<tag>[^/]+)',
        feeds.DocumentsReviewFeed(),
        name="wiki.feeds.list_review_tag"),
    url(r'^/feeds/(?P<format>[^/]+)/needs-review/?',
        feeds.DocumentsReviewFeed(),
        name="wiki.feeds.list_review"),
    url(r'^/feeds/(?P<format>[^/]+)/revisions/?',
        feeds.RevisionsFeed(),
        name="wiki.feeds.recent_revisions"),
    url(r'^/feeds/(?P<format>[^/]+)/files/?',
        AttachmentsFeed(),
        name="attachments.feeds.recent_files"),

    url(r'^/(?P<document_path>%s)' % DOCUMENT_PATH_RE.pattern,
        include(document_patterns)),
]
