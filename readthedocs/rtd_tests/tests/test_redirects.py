from django.test import TestCase
from django.test.utils import override_settings

from django_dynamic_fixture import get
from django_dynamic_fixture import fixture

from readthedocs.builds.constants import LATEST
from readthedocs.projects.models import Project
from readthedocs.redirects.models import Redirect

import logging


class RedirectTests(TestCase):
    fixtures = ["eric", "test_data"]

    def setUp(self):
        logging.disable(logging.DEBUG)
        self.client.login(username='eric', password='test')
        self.client.post(
            '/dashboard/import/',
            {'repo_type': 'git', 'name': 'Pip',
             'tags': 'big, fucking, monkey', 'default_branch': '',
             'project_url': 'http://pip.rtfd.org',
             'repo': 'https://github.com/fail/sauce',
             'csrfmiddlewaretoken': '34af7c8a5ba84b84564403a280d9a9be',
             'default_version': LATEST,
             'privacy_level': 'public',
             'version_privacy_level': 'public',
             'description': 'wat',
             'documentation_type': 'sphinx'})
        pip = Project.objects.get(slug='pip')
        pip.versions.create_latest()

    def test_proper_url_no_slash(self):
        r = self.client.get('/docs/pip')
        # This is triggered by Django, so its a 301, basically just
        # APPEND_SLASH
        self.assertEqual(r.status_code, 301)
        self.assertEqual(r['Location'], 'http://testserver/docs/pip/')
        r = self.client.get(r['Location'])
        self.assertEqual(r.status_code, 302)
        r = self.client.get(r['Location'])
        self.assertEqual(r.status_code, 200)

    def test_proper_url(self):
        r = self.client.get('/docs/pip/')
        self.assertEqual(r.status_code, 302)
        self.assertEqual(
            r['Location'], 'http://testserver/docs/pip/en/latest/')
        r = self.client.get(r['Location'])
        self.assertEqual(r.status_code, 200)

    def test_proper_url_with_lang_slug_only(self):
        r = self.client.get('/docs/pip/en/')
        self.assertEqual(r.status_code, 302)
        self.assertEqual(
            r['Location'], 'http://testserver/docs/pip/en/latest/')
        r = self.client.get(r['Location'])
        self.assertEqual(r.status_code, 200)

    def test_proper_url_full(self):
        r = self.client.get('/docs/pip/en/latest/')
        self.assertEqual(r.status_code, 200)

    def test_proper_url_full_with_filename(self):
        r = self.client.get('/docs/pip/en/latest/test.html')
        self.assertEqual(r.status_code, 200)

    # Specific Page Redirects
    def test_proper_page_on_main_site(self):
        r = self.client.get('/docs/pip/page/test.html')
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r['Location'],
                         'http://testserver/docs/pip/en/latest/test.html')
        r = self.client.get(r['Location'])
        self.assertEqual(r.status_code, 200)

    def test_proper_url_with_version_slug_only(self):
        r = self.client.get('/docs/pip/latest/')
        self.assertEqual(r.status_code, 302)
        self.assertEqual(
            r['Location'], 'http://testserver/docs/pip/en/latest/')
        r = self.client.get(r['Location'])
        self.assertEqual(r.status_code, 200)

    # If slug is neither valid lang nor valid version, it should 404.
    # TODO: This should 404 directly, not redirect first
    def test_improper_url_with_nonexistent_slug(self):
        r = self.client.get('/docs/pip/nonexistent/')
        self.assertEqual(r.status_code, 302)
        r = self.client.get(r['Location'])
        self.assertEqual(r.status_code, 404)

    def test_improper_url_filename_only(self):
        r = self.client.get('/docs/pip/test.html')
        self.assertEqual(r.status_code, 404)

    def test_improper_url_dir_file(self):
        r = self.client.get('/docs/pip/nonexistent_dir/bogus.html')
        self.assertEqual(r.status_code, 404)

    def test_improper_url_dir_subdir_file(self):
        r = self.client.get('/docs/pip/nonexistent_dir/subdir/bogus.html')
        self.assertEqual(r.status_code, 404)

    def test_improper_url_lang_file(self):
        r = self.client.get('/docs/pip/en/bogus.html')
        self.assertEqual(r.status_code, 404)

    def test_improper_url_lang_subdir_file(self):
        r = self.client.get('/docs/pip/en/nonexistent_dir/bogus.html')
        self.assertEqual(r.status_code, 404)

    def test_improper_url_dir_subdir_file(self):
        r = self.client.get('/docs/pip/en/nonexistent_dir/subdir/bogus.html')
        self.assertEqual(r.status_code, 404)

    def test_improper_url_version_dir_file(self):
        r = self.client.get('/docs/pip/latest/nonexistent_dir/bogus.html')
        self.assertEqual(r.status_code, 404)

    # Subdomains
    def test_proper_subdomain(self):
        r = self.client.get('/', HTTP_HOST='pip.readthedocs.org')
        self.assertEqual(r.status_code, 302)
        self.assertEqual(
            r['Location'], 'http://pip.readthedocs.org/en/latest/')

    def test_proper_subdomain_with_lang_slug_only(self):
        r = self.client.get('/en/', HTTP_HOST='pip.readthedocs.org')
        self.assertEqual(r.status_code, 302)
        self.assertEqual(
            r['Location'], 'http://pip.readthedocs.org/en/latest/')

    def test_proper_subdomain_and_url(self):
        r = self.client.get('/en/latest/', HTTP_HOST='pip.readthedocs.org')
        self.assertEqual(r.status_code, 200)

    def test_proper_subdomain_and_url_with_filename(self):
        r = self.client.get(
            '/en/latest/test.html', HTTP_HOST='pip.readthedocs.org')
        self.assertEqual(r.status_code, 200)

    # Specific Page Redirects
    def test_proper_page_on_subdomain(self):
        r = self.client.get('/page/test.html', HTTP_HOST='pip.readthedocs.org')
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r['Location'],
                         'http://pip.readthedocs.org/en/latest/test.html')

    # When there's only a version slug, the redirect prepends the lang slug
    def test_proper_subdomain_with_version_slug_only(self):
        r = self.client.get('/1.4.1/', HTTP_HOST='pip.readthedocs.org')
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r['Location'],
                         'http://pip.readthedocs.org/en/1.4.1/')

    def test_improper_subdomain_filename_only(self):
        r = self.client.get('/test.html', HTTP_HOST='pip.readthedocs.org')
        self.assertEqual(r.status_code, 404)


class RedirectUnderscoreTests(TestCase):
    fixtures = ["eric", "test_data"]

    def setUp(self):
        logging.disable(logging.DEBUG)
        self.client.login(username='eric', password='test')
        whatup = Project.objects.create(
            slug='what_up', name='What Up Underscore')

    # Test _ -> - slug lookup
    def test_underscore_redirect(self):
        r = self.client.get('/',
                            HTTP_HOST='what-up.readthedocs.org')
        self.assertEqual(r.status_code, 302)
        self.assertEqual(
            r['Location'], 'http://what-up.readthedocs.org/en/latest/')


class RedirectAppTests(TestCase):
    fixtures = ["eric", "test_data"]

    def setUp(self):
        self.client.login(username='eric', password='test')
        self.client.post(
            '/dashboard/import/',
            {'repo_type': 'git', 'name': 'Pip',
             'tags': 'big, fucking, monkey', 'default_branch': '',
             'project_url': 'http://pip.rtfd.org',
             'repo': 'https://github.com/fail/sauce',
             'csrfmiddlewaretoken': '34af7c8a5ba84b84564403a280d9a9be',
             'default_version': LATEST,
             'privacy_level': 'public',
             'version_privacy_level': 'public',
             'description': 'wat',
             'documentation_type': 'sphinx'})
        self.pip = Project.objects.get(slug='pip')
        self.pip.versions.create_latest()

    @override_settings(USE_SUBDOMAIN=True)
    def test_redirect_root(self):
        Redirect.objects.create(
            project=self.pip, redirect_type='prefix', from_url='/woot/')
        r = self.client.get('/woot/faq.html', HTTP_HOST='pip.readthedocs.org')
        self.assertEqual(r.status_code, 302)
        self.assertEqual(
            r['Location'], 'http://pip.readthedocs.org/en/latest/faq.html')

    @override_settings(USE_SUBDOMAIN=True)
    def test_redirect_page(self):
        Redirect.objects.create(
            project=self.pip, redirect_type='page', from_url='/install.html', to_url='/tutorial/install.html')
        r = self.client.get('/install.html', HTTP_HOST='pip.readthedocs.org')
        self.assertEqual(r.status_code, 302)
        self.assertEqual(
            r['Location'], 'http://pip.readthedocs.org/en/latest/tutorial/install.html')

    @override_settings(USE_SUBDOMAIN=True, PYTHON_MEDIA=True)
    def test_redirect_html(self):
        Redirect.objects.create(
            project=self.pip, redirect_type='sphinx_html')
        r = self.client.get('/en/latest/faq/', HTTP_HOST='pip.readthedocs.org')
        self.assertEqual(r.status_code, 302)
        self.assertEqual(
            r['Location'], 'http://pip.readthedocs.org/en/latest/faq.html')

    @override_settings(USE_SUBDOMAIN=True, PYTHON_MEDIA=True)
    def test_redirect_htmldir(self):
        Redirect.objects.create(
            project=self.pip, redirect_type='sphinx_htmldir')
        r = self.client.get('/en/latest/faq.html', HTTP_HOST='pip.readthedocs.org')
        self.assertEqual(r.status_code, 302)
        self.assertEqual(
            r['Location'], 'http://pip.readthedocs.org/en/latest/faq/')

class RedirectBuildTests(TestCase):
    fixtures = ["eric", "test_data"]

    def setUp(self):
        self.project = get(Project,
                      slug='project-1',
                      documentation_type='sphinx',
                      conf_py_file='test_conf.py',
                      versions=[fixture()])
        self.version = self.project.versions.all()[0]

    def test_redirect_list(self):
        r = self.client.get('/builds/project-1/')
        self.assertEqual(r.status_code, 301)
        self.assertEqual(r['Location'], 'http://testserver/projects/project-1/builds/')

    def test_redirect_detail(self):
        r = self.client.get('/builds/project-1/1337/')
        self.assertEqual(r.status_code, 301)
        self.assertEqual(r['Location'], 'http://testserver/projects/project-1/builds/1337/')

