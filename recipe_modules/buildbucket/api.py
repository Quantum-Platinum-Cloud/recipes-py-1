# Copyright 2017 The LUCI Authors. All rights reserved.
# Use of this source code is governed under the Apache License, Version 2.0
# that can be found in the LICENSE file.

"""API for interacting with the buildbucket service.

Depends on 'buildbucket' binary available in PATH:
https://godoc.org/go.chromium.org/luci/buildbucket/client/cmd/buildbucket
"""

import base64
import json
import re

from recipe_engine import recipe_api

from .proto import build_pb2
from .proto import common_pb2


def _parse_build_set(bs_string):
  """Parses a buildset string to GerritChange or GitilesCommit.

  A port of
  https://chromium.googlesource.com/infra/luci/luci-go/+/fe4e304639d11ca00537768f8bfbf20ffecf73e6/buildbucket/buildset.go#105
  """
  assert isinstance(bs_string, basestring)
  p = bs_string.split('/')
  if '' in p:
    return None

  n = len(p)

  if n == 5 and p[0] == 'patch' and p[1] == 'gerrit':
    return common_pb2.GerritChange(
        host=p[2],
        change=int(p[3]),
        patchset=int(p[4])
    )

  if n >= 5 and p[0] == 'commit' and p[1] == 'gitiles':
    if p[n-2] != '+' or not re.match('^[0-9a-f]{40}$', p[n-1]):
      return None
    return common_pb2.GitilesCommit(
        host=p[2],
        project='/'.join(p[3:n-2]), # exclude plus
        id=p[n-1],
    )

  return None


class BuildbucketApi(recipe_api.RecipeApi):
  """A module for interacting with buildbucket."""

  # Expose protobuf messages to the users of buildbucket module.
  build_pb2 = build_pb2
  common_pb2 = common_pb2

  def __init__(
      self, property, legacy_property, mastername, buildername, buildnumber,
      *args, **kwargs):
    super(BuildbucketApi, self).__init__(*args, **kwargs)
    self._service_account_key = None
    self._host = 'cr-buildbucket.appspot.com'

    legacy_property = legacy_property or {}
    if isinstance(legacy_property, basestring):
      legacy_property = json.loads(legacy_property)
    self._legacy_property = legacy_property

    self._build = build_pb2.Build()
    if property.get('build'):
      self._build.ParseFromString(base64.b64decode(property.get('build')))
    else:
      # Legacy mode.
      build_dict = legacy_property.get('build', {})
      self.build.number = int(buildnumber or 0)
      if 'id' in build_dict:
        self._build.id = int(build_dict['id'])
      _legacy_builder_id(
          build_dict, mastername, buildername, self._build.builder)
      _legacy_build_input(build_dict, self._build.input)
      _legacy_tags(build_dict, self._build)

  def set_buildbucket_host(self, host):
    """Changes the buildbucket backend hostname used by this module.

    Args:
      host (str): buildbucket server host (e.g. 'cr-buildbucket.appspot.com').
    """
    self._host = host

  def use_service_account_key(self, key_path):
    """Tells this module to start using given service account key for auth.

    Otherwise the module is using the default account (when running on LUCI or
    locally), or no auth at all (when running on Buildbot).

    Exists mostly to support Buildbot environment. Recipe for LUCI environment
    should not use this.

    Args:
      key_path (str): a path to JSON file with service account credentials.
    """
    self._service_account_key = key_path

  @property
  def build(self):
    """Returns current build as a buildbucket.v2.Build protobuf message.

    Do not implement conditional logic on returned tags; they are for indexing.
    Use returned build.input instead.

    DO NOT MODIFY the returned value.

    Pure Buildbot support: to simplify transition to buildbucket, returns a
    message even if the current build is not a buildbucket build. Provides as
    much information as possible. If the current build is not a buildbucket
    build, returned build.id is 0.
    """
    return self._build

  @property
  def tags_for_child_build(self):
    """A dict of tags (key -> value) derived from current (parent) build for a
    child build."""
    original_tags = {t.key: t.value for t in self.build.tags}
    new_tags = {'user_agent': 'recipe'}

    # TODO(nodir): switch to ScheduleBuild API where we don't have to convert
    # build input back to tags.
    if self.build.input.HasField('gitiles_commit'):
      c = self.build.input.gitiles_commit
      new_tags['buildset'] = (
          'commit/gitiles/%s/%s/+/%s' % (c.host, c.project, c.id))
      if c.ref:
        new_tags['gitiles_ref'] = c.ref
    elif self.build.input.gerrit_changes:
      cl = self.build.input.gerrit_changes[0]
      new_tags['buildset'] = 'patch/gerrit/%s/%d/%d' % (
          cl.host, cl.change, cl.patchset)
    else:
      buildset = original_tags.get('buildset')
      if buildset:
        new_tags['buildset'] = buildset

    if self.build.number:
      new_tags['parent_buildnumber'] = str(self.build.number)
    if self.build.builder.builder:
      new_tags['parent_buildername'] = str(self.build.builder.builder)
    return new_tags

  # RPCs.

  def put(self, builds, **kwargs):
    """Puts a batch of builds.

    Args:
      builds (list): A list of dicts, where keys are:
        'bucket': (required) name of the bucket for the request.
        'parameters' (dict): (required) arbitrary json-able parameters that a
          build system would be able to interpret.
        'tags': (optional) a dict(str->str) of tags for the build. These will
          be added to those generated by this method and override them if
          appropriate. If you need to remove a tag set by default, set its value
          to None (for example, tags={'buildset': None} will ensure build is
          triggered without 'buildset' tag).

    Returns:
      A step that as its .stdout property contains the response object as
      returned by buildbucket.
    """
    build_specs = []
    for build in builds:
      build_specs.append(self.m.json.dumps({
        'bucket': build['bucket'],
        'parameters_json': self.m.json.dumps(build['parameters']),
        'tags': self._tags_for_build(build['bucket'], build['parameters'],
                                     build.get('tags')),
        'experimental': self.m.runtime.is_experimental,
      }))
    return self._call_service('put', build_specs, **kwargs)

  def cancel_build(self, build_id, **kwargs):
    return self._call_service('cancel', [build_id], **kwargs)

  def get_build(self, build_id, **kwargs):
    return self._call_service('get', [build_id], **kwargs)

  # Internal.

  def _call_service(self, command, args, **kwargs):
    step_name = kwargs.pop('name', 'buildbucket.' + command)
    if self._service_account_key:
      args = ['-service-account-json', self._service_account_key] + args
    args = ['buildbucket', command, '-host', self._host] + args
    kwargs.setdefault('infra_step', True)
    return self.m.step(step_name, args, stdout=self.m.json.output(), **kwargs)

  def _tags_for_build(self, bucket, parameters, override_tags=None):
    new_tags = self.tags_for_child_build
    builder_name = parameters.get('builder_name')
    if builder_name:
      new_tags['builder'] = builder_name
    # TODO(tandrii): remove this Buildbot-specific code.
    if bucket.startswith('master.'):
      new_tags['master'] = bucket[7:]
    new_tags.update(override_tags or {})
    return sorted(
        '%s:%s' % (k, v)
        for k, v in new_tags.iteritems()
        if v is not None)

  # DEPRECATED API.

  @property
  def properties(self):  # pragma: no cover
    """DEPRECATED, use build attribute instead."""
    return self._legacy_property

  @property
  def build_id(self):  # pragma: no cover
    """DEPRECATED, use build.id instead."""
    return self.build.id or None

  @property
  def build_input(self):  # pragma: no cover
    """DEPRECATED, use build.input instead."""
    return self.build.input

  @property
  def builder_id(self):  # pragma: no cover
    """Deprecated. Use build.builder instead."""
    return self.build.builder


# Legacy support.


def _legacy_tags(build_dict, build_msg):
  for t in build_dict.get('tags', []):
    k, v = t.split(':', 1)
    if k =='buildset' and v.startswith(('patch/gerrit/', 'commit/gitiles')):
      continue
    if k in ('build_address', 'builder'):
      continue
    build_msg.tags.add(key=k, value=v)


def _legacy_build_input(build_dict, build_input):
  bs_prefix = 'buildset:'
  ref_prefix = 'gitiles_ref:'
  for t in build_dict.get('tags', []):
    if t.startswith(bs_prefix):
      bs = _parse_build_set(t[len(bs_prefix):])
      if isinstance(bs, common_pb2.GitilesCommit):
        build_input.gitiles_commit.CopyFrom(bs)
      elif isinstance(bs, common_pb2.GerritChange):
        build_input.gerrit_changes.add().CopyFrom(bs)

    elif t.startswith(ref_prefix):
      build_input.gitiles_commit.ref = t[len(ref_prefix):]

  # TODO(nodir): parse repository, branch and revision properties.


def _legacy_builder_id(build_dict, mastername, buildername, builder_id):
  builder_id.project = build_dict.get('project') or ''
  builder_id.bucket = build_dict.get('bucket') or ''

  if builder_id.bucket:
    luci_prefix = 'luci.%s.' % builder_id.project
    if builder_id.bucket.startswith(luci_prefix):
      builder_id.bucket = builder_id.bucket[len(luci_prefix):]
  if not builder_id.bucket and mastername:
    builder_id.bucket = 'master.%s' % mastername

  tags_dict = dict(t.split(':', 1) for t in build_dict.get('tags', []))
  builder_id.builder = tags_dict.get('builder') or buildername or ''
