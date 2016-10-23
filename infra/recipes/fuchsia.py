# Copyright 2016 The Fuchsia Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Recipe for building Fuchsia."""

from recipe_engine.recipe_api import Property


DEPS = [
    'infra/goma',
    'infra/jiri',
    'recipe_engine/path',
    'recipe_engine/properties',
    'recipe_engine/step',
]

TARGETS = [ 'arm64', 'x86-64' ]

PROPERTIES = {
    'category': Property(kind=str, help='Build category', default=None),
    'patch_gerrit_url': Property(kind=str, help='Gerrit host', default=None),
    'patch_project': Property(kind=str, help='Gerrit project', default=None),
    'patch_ref': Property(kind=str, help='Gerrit patch ref', default=None),
    'patch_storage': Property(kind=str, help='Patch location', default=None),
    'patch_repository_url': Property(kind=str, help='URL to a Git repository',
                              default=None),
    'manifest': Property(kind=str, help='Jiri manifest to use'),
    'remote': Property(kind=str, help='Remote manifest repository'),
    'target': Property(kind=str, help='Target to build'),
}


def RunSteps(api, category, patch_gerrit_url, patch_project, patch_ref,
             patch_storage, patch_repository_url, manifest, remote, target):
    api.goma.ensure_goma()
    api.jiri.ensure_jiri()

    api.jiri.set_config('fuchsia')

    api.jiri.init()
    api.jiri.clean_project()
    api.jiri.import_manifest(manifest, remote, overwrite=True)
    api.jiri.update(gc=True)
    if patch_ref is not None:
        api.jiri.patch(patch_ref, host=patch_gerrit_url, delete=True, force=True)

    sysroot_target = {'arm64': 'aarch64', 'x86-64': 'x86_64'}[target]

    with api.step.nest('build sysroot'):
        api.step('build',
                 ['scripts/build-sysroot.sh', '-c', '-t', sysroot_target])

    fuchsia_target = {'arm64': 'aarch64', 'x86-64': 'x86-64'}[target]

    with api.step.nest('build Fuchsia'), api.goma.build_with_goma():
        api.step('gen',
                 ['packages/gn/gen.py', '--goma=%s' % api.goma.goma_dir])
        api.step('ninja',
                 ['buildtools/ninja', '-C', 'out/debug-%s' % fuchsia_target])


def GenTests(api):
    yield api.test('scheduler') + api.properties(
        manifest='fuchsia',
        remote='https://fuchsia.googlesource.com/manifest',
        target='x86-64',
    )
    yield api.test('cq') + api.properties.tryserver(
        gerrit_project='fuchsia',
        patch_gerrit_url='fuchsia-review.googlesource.com',
        manifest='fuchsia',
        remote='https://fuchsia.googlesource.com/manifest',
        target='x86-64',
    )
