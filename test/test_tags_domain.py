""" Tests for the tags domain"""

from io import StringIO
from pathlib import Path
import itertools


import pytest
from docutils import nodes
from pycparser.plyparser import parameterized
from sphinx.addnodes import desc_signature

from sphinx.errors import ExtensionError
from sphinx.testing.util import SphinxTestApp
from sphinx.testing.util import assert_node
from sphinx.testing import restructuredtext
from sphinx import addnodes

from sphinx_tags import TagsDomain
from sphinx_tags import TagList

from docs.conf import tags_create_badges
from test.conftest import OUTPUT_ROOT_DIR

OUTPUT_ROOT_DIR = OUTPUT_ROOT_DIR / "general"

@pytest.mark.sphinx('html', testroot='ipynb', confoverrides={'tags_create_tags': True})
def test_tags_domain(app: SphinxTestApp):
    """
    Test that the tags domain inherits the tags
    """
    app.build(force_all=True)
    build_dir = Path(app.srcdir) / "_build" / "text"

    assert 'tags' in app.env.domains
    assert len(app.env.domains['tags'].data['tag_index_pages'])


@pytest.mark.sphinx('html', testroot='ipynb', confoverrides={'tags_create_tags': True})
def test_tags_list(app: SphinxTestApp):
    """
    Assert that the TagList directive returns the expected tags
    """
    app.build(force_all=True)
    build_dir = Path(app.srcdir) / "_build" / "text"

    raw_tag_names = app.env.domains['tags'].data['tag_index_pages'].keys()
    len_tags = len(raw_tag_names)

    # each tag is a reference node and a comma between them
    # ref nodes is the expected set of nodes and nodes.paragraph what has been built
    ref_nodes = [[[nodes.reference, tag_name], [nodes.inline, ', ']] for tag_name in raw_tag_names]
    ref_nodes = tuple(itertools.chain(*ref_nodes))[:-1]

    raw_tag_list_call = ".. taglist::"
    doctree = restructuredtext.parse(app, raw_tag_list_call)
    assert_node(
        doctree[0],
        [nodes.paragraph, ref_nodes]
    )

@pytest.mark.sphinx('html', testroot='ipynb', confoverrides={'tags_create_tags': True, 'tags_create_badges':True})
def test_badged_tags(app: SphinxTestApp):
    """
    Assert that the TagList directive returns the expected tags
    """
    app.build(force_all=True)
    build_dir = Path(app.srcdir) / "_build" / "text"

    raw_tag_names = app.env.domains['tags'].data['tag_index_pages'].keys()

    # each badge has a similar format to the tags, however there is no ',' between the badges
    # also each node has another node for the contents of the badge
    ref_nodes = [[[addnodes.pending_xref, [nodes.inline, tag_name]], [nodes.inline, ' ']] for tag_name in raw_tag_names]
    ref_nodes = tuple(itertools.chain(*ref_nodes))[:-1]

    # additional test to call `taglist` from the domain
    raw_tag_list_call = ".. tags:taglist::"
    doctree = restructuredtext.parse(app, raw_tag_list_call)
    assert_node(
        doctree[0],
        [nodes.paragraph, ref_nodes]
    )

