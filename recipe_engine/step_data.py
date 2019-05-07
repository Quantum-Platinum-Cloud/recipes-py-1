# Copyright 2019 The LUCI Authors. All rights reserved.
# Use of this source code is governed under the Apache License, Version 2.0
# that can be found in the LICENSE file.

"""This module defines `StepData` which is the object returned from executing
a single step (subprocess), usually via the `recipe_engine/step` recipe module.
"""

import attr

from .internal.attr_util import attr_type

from .types import StepPresentation


@attr.s
class _AttributeRaiser(object):
  _step_name = attr.ib(validator=attr_type(basestring))
  _namespace = attr.ib(validator=attr_type(str))
  # `_finalized` doesn't use `attr.s` because of the shenanigans we do with
  # `__getattr__`.

  def __getattr__(self, name):
    raise AttributeError('StepData(%r)%s has no attribute %r.' % (
      self._step_name, self._namespace, name))

  def __setattr__(self, name, value):
    if not hasattr(self, '_finalized') or not self._finalized:
      return object.__setattr__(self, name, value)

    raise AttributeError('Cannot assign to StepData(%r)%s.%s' % (
      self._step_name, self._namespace, name))


@attr.s
class StepData(object):
  """StepData represents the result of running a step.

  For historical reasons, this object has dynamic properties depending on the
  OutputPlaceholders used with the step.

  Every Placeholder has a 'namespace', which is a tuple consisting of the recipe
  module name and function name from however the placeholder was created. For
  example, the namespace of a `api.json.output(...)` placeholder is ('json',
  'output').

  Somewhat confusingly, Placeholders can also have a 'name', which is set by the
  user (like "script_data").

  The namespace and the name are used by the engine to assign the result of the
  Placeholder into this StepData object at a number of places:

    * If the placeholder does not have a name, then the namespace is used to
      assign into the StepData like `StepData.namespace.part = result`. It's not
      valid to have two nameless placeholders with the same namespace.
    * If the placeholder DOES have a name, then it's assigned to (note the `s`
      on `parts`):

      StepData.namespace.parts[name] = result

    * Additionally, if there's exactly one named placeholder, then it's result
      is also assigned to `StepData.namespace.part`.

  # TODO(iannucci): This is all rubbish; change this so that:
  #   * All placeholders are given an explicit name by the caller.
  #   * All placeholder results are mapped to StepData.placeholders[name].
  #   * Remove 'clever' dynamic assignment and _AttributeRaiser.

  Example 1:

      // Input
      api.step('...', ['...', api.json.output()])

      // Output
      StepData.json.output = json.output().result()
      StepData.json.outputs = {}

  Example 2:

      // Input
      api.step('...', ['...', api.json.output(), api.other.placeholder()])

      // Output
      StepData.json.output = json.output().result()
      StepData.json.outputs = {}
      StepData.json.placeholder = other.placeholder().result()
      StepData.json.placeholders = {}

  Example 3:

      // Input
      api.step('...', ['...', api.json.output(), api.json.output()])

      // Invalid; two unnamed placeholders with the same namespace

  Example 4:

      // Input
      api.step('...', ['...', api.json.output(name='bob')])

      // Output
      StepData.json.output = json.output(name='bob').result()
      StepData.json.outputs = {'bob': json.output(name='bob').result()}

  Example 5:

      // Input
      api.step('...', ['...', api.json.output(name='bob'), api.json.output()])

      // Output
      StepData.json.output = json.output().result()
      StepData.json.outputs = {'bob': json.output(name='bob').result()}

  Example 6:

      // Input
      api.step('...', ['...', api.json.output(name='bob'),
                              api.json.output(name='charlie')])

      // Output
      # No 'json.output' because they all have names, and there's more than one
      # with a name.
      StepData.json.outputs = {
        'bob': json.output(name='bob')
        'charlie': json.output(name='charlie')
      }
  """
  # The StepConfig object associated with this step.
  #
  # TODO(iannucci): Almost no code actually relies on this, except for testing
  # code in the recipe engine. Remove this.
  step_config = attr.ib()
  @step_config.validator
  def _step_config_validator(self, attrib, value):
    # TODO(iannucci): This late import will go away in a later CL
    from .internal.engine_step import StepConfig
    attr_type(StepConfig)(self, attrib, value)

  # The returncode of the step.
  retcode = attr.ib(validator=attr_type(int))

  # The StepPresentation object associated with this step.
  presentation = attr.ib(validator=attr_type(StepPresentation))
  @presentation.default
  def _presentation_default(self):
    # TODO(iannucci): move this logic out of StepData and into the engine.
    ret = StepPresentation(self.step_config.name)
    if (self.step_config.ok_ret is self.step_config.ALL_OK
        or self.retcode in self.step_config.ok_ret):
      ret.status = 'SUCCESS'
    else:
      if not self.step_config.infra_step:
        ret.status = 'FAILURE'
      else:
        ret.status = 'EXCEPTION'
    return ret

  # The result of the `stdout` Placeholder, if the step had one.
  #
  # Unless you set the `stdout` kwarg when running the step, this will be None.
  stdout = attr.ib(default=None)

  # The result of the `stderr` Placeholder, if the step had one.
  #
  # Unless you set the `stderr` kwarg when running the step, this will be None.
  stderr = attr.ib(default=None)

  # Bogus fields!
  # Some naughty recipes have taken the liberty in the past of adding arbitrary
  # stuff to the StepData object directly rather than defining and returning
  # their own objects from their methods.
  #
  # You should NOT add new fields to this section. Each field here has an
  # associated bug to remove uses of it and ultimately remove the field
  # entirely.
  BOGUS_FIELDS = frozenset([
    # Written to by the 'build/chromium_swarming' module.
    # FIXME: crbug.com/956698
    'swarming_task',

    # Written to by the 'build/chromium_swarming' module.
    # FIXME: crbug.com/956703
    'isolated_script_results',

    # Written to by the 'build/chromium_swarming' module.
    # FIXME: crbug.com/956705
    'isolated_script_perf_results',

    # Written to by the 'build/chromium_android' module.
    # FIXME: crbug.com/956746
    'test_utils',
  ])

  # Dict[
  #   namespace: Tuple[str],
  #   Dict[
  #     name: str,
  #     result: object]]
  #
  # namespace tuple: the tuple of namespace strings for this placeholder. e.g.
  #   `('json', 'output')`.
  # name: the "name" of the placeholder (within its namespace) or None for
  #   an unnamed placeholder. The name is user-specified to disambiguate between
  #   multiple placeholders in the same namespace on the same step (e.g.
  #   multiple `json.output()`).
  # result: Anything the OutputPlaceholder.result() method returned.
  _staged_placeholders = attr.ib(
      validator=attr_type(dict, type(None)), factory=dict)

  # When set to True, all future assignments to this object are prevented.
  _finalized = attr.ib(validator=attr_type(bool), default=False)

  @property
  def name(self):
    """Returns the build.proto step name (i.e. name_tokens joined with '|')."""
    return '|'.join(self.step_config.name_tokens)

  @property
  def step(self):
    """DEPRECATED: For backward compatibility only. Uses old @@@annotation@@@
    step name.

    Use .step_config.name_tokens or .name instead."""
    # TODO(iannucci): remove this
    return {'name': self.step_config.name}

  def _populate_placeholders(self):
    """
    """
    if self._finalized:
      return

    # Grab all staged placeholders, set _staged_placeholders to None so that no
    # more placeholders could be staged.
    staged = self._staged_placeholders
    self._staged_placeholders = None

    # If we don't have any work, return
    if not staged:
      return

    def _deep_set(namespace, value):
      """Sets `value` at `namespace` on self.

      Populates intermedaite tiers of namespace with _AttributeRaiser objects.

      Args:
        * namespace (Tuple[str]) - A tuple of python identifiers. e.g.
          `('json', 'output')`.
        * value (object) - Arbitrary data to set at the given namespace.
      """
      last_token = namespace[-1]

      obj = self
      namespace_so_far = ''
      for part in namespace[:-1]:
        namespace_so_far += '.%s' % part
        if not hasattr(obj, part):
          subval = _AttributeRaiser(self.name, namespace_so_far)
          setattr(obj, part, subval)
        else:
          subval = getattr(obj, part)
        obj = subval

      setattr(obj, last_token, value)


    # A singleton object used in the loop below to indicate that a data item was
    # not set. Pylint is dumb and doesn't like uppercase function variables.
    UNSET = object()   # pylint: disable=invalid-name

    # For every staged placeholder namespace.
    for namespace, name_to_result in staged.iteritems():
      # The default is defined as the result from the Placeholder with no name
      default = name_to_result.pop(None, UNSET)
      # OR the Placeholder (if there was only one in this namespace)
      if default is UNSET and len(name_to_result) == 1:
        default = name_to_result.values()[0]
      if default is not UNSET:
        # This sets e.g. 'json.output' to `default`
        _deep_set(namespace, default)

      if name_to_result:
        # This sets e.g. 'json.outputs' to
        #   {"user_provided_name": value, "other_name": other_value}
        plural_namespace = namespace[:-1] + (namespace[-1] + 's',)
        _deep_set(plural_namespace, name_to_result)

    # Now set `_finalized` on all _AttributeRaiser objects to prevent further
    # assignments.
    objs = self.__dict__.values()
    while objs:
      obj = objs.pop()
      if not isinstance(obj, _AttributeRaiser):
        continue
      objs.extend(obj.__dict__.values())
      obj._finalized = True   # pylint: disable=protected-access

  def finalize(self):
    """Fills all user-accessible placeholder results, and prevents accidental
    assignment to this StepData.

    Used by the Recipe Engine. You don't need to worry about this :)
    """
    if self._finalized:
      return

    self._populate_placeholders()
    self._finalized = True

  def assign_placeholder(self, placeholder, result):
    """Used by the Recipe Engine to stage placeholder data in this StepData.

    May only be called on a non-finalized StepData instance.

    The placeholder will become user-accessible once this StepData is finalized.

    Args:
      * placeholder (Placeholder) - The placeholder instance to stage. This
        function extracts the namespaces and name.
      * result (object) - The final result of this placeholder.
    """
    if self._finalized:
      raise ValueError(
          'Cannot assign placeholder %r (%r) on finalized StepData from step %r'
          % (placeholder.namespaces, placeholder.name, self.name))
    self._staged_placeholders.setdefault(
        placeholder.namespaces, {})[placeholder.name] = result

  def __setattr__(self, name, value):
    # use hasattr since this logic is called during __init__ and _finalized may
    # not actually exist yet. Calling __getattr__ in this state will fail
    # because it calls `self.name` which ALSO might not exist yet.
    if hasattr(self, '_finalized') and self._finalized:
      if name not in self.BOGUS_FIELDS:
        raise ValueError(
            'Cannot assign to %r on finalized StepData from step %r' %
            (name, self.name))
    return object.__setattr__(self, name, value)

  def __getattr__(self, name):
    try:
      return object.__getattribute__(self, name)
    except AttributeError:
      raise AttributeError(
          'StepData from step %r has no attribute %r.' % (self.name, name))