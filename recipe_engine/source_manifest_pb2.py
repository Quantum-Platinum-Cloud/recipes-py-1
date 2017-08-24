# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: source_manifest.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='source_manifest.proto',
  package='',
  syntax='proto3',
  serialized_pb=_b('\n\x15source_manifest.proto\"\xd8\x04\n\x08Manifest\x12\x0f\n\x07version\x18\x01 \x01(\x05\x12/\n\x0b\x64irectories\x18\x02 \x03(\x0b\x32\x1a.Manifest.DirectoriesEntry\x1aW\n\x0bGitCheckout\x12\x10\n\x08repo_url\x18\x01 \x01(\t\x12\x11\n\tfetch_url\x18\x02 \x01(\t\x12\x10\n\x08revision\x18\x03 \x01(\t\x12\x11\n\tfetch_ref\x18\x04 \x01(\t\x1a\x8f\x01\n\x0b\x43IPDPackage\x12\x17\n\x0f\x63ipd_server_url\x18\x01 \x01(\t\x12\x19\n\x11\x63ipd_package_name\x18\x02 \x01(\t\x12\x1c\n\x14\x63ipd_package_pattern\x18\x03 \x01(\t\x12\x18\n\x10\x63ipd_instance_id\x18\x04 \x01(\t\x12\x14\n\x0c\x63ipd_version\x18\x05 \x01(\t\x1aH\n\x08Isolated\x12\x1b\n\x13isolated_server_url\x18\x01 \x01(\t\x12\x11\n\tnamespace\x18\x02 \x01(\t\x12\x0c\n\x04hash\x18\x03 \x01(\t\x1a\x8b\x01\n\tDirectory\x12+\n\x0cgit_checkout\x18\x01 \x01(\x0b\x32\x15.Manifest.GitCheckout\x12+\n\x0c\x63ipd_package\x18\x02 \x03(\x0b\x32\x15.Manifest.CIPDPackage\x12$\n\x08isolated\x18\x03 \x03(\x0b\x32\x12.Manifest.Isolated\x1aG\n\x10\x44irectoriesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\"\n\x05value\x18\x02 \x01(\x0b\x32\x13.Manifest.Directory:\x02\x38\x01\x62\x06proto3')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_MANIFEST_GITCHECKOUT = _descriptor.Descriptor(
  name='GitCheckout',
  full_name='Manifest.GitCheckout',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='repo_url', full_name='Manifest.GitCheckout.repo_url', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='fetch_url', full_name='Manifest.GitCheckout.fetch_url', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='revision', full_name='Manifest.GitCheckout.revision', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='fetch_ref', full_name='Manifest.GitCheckout.fetch_ref', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=104,
  serialized_end=191,
)

_MANIFEST_CIPDPACKAGE = _descriptor.Descriptor(
  name='CIPDPackage',
  full_name='Manifest.CIPDPackage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='cipd_server_url', full_name='Manifest.CIPDPackage.cipd_server_url', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='cipd_package_name', full_name='Manifest.CIPDPackage.cipd_package_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='cipd_package_pattern', full_name='Manifest.CIPDPackage.cipd_package_pattern', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='cipd_instance_id', full_name='Manifest.CIPDPackage.cipd_instance_id', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='cipd_version', full_name='Manifest.CIPDPackage.cipd_version', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=194,
  serialized_end=337,
)

_MANIFEST_ISOLATED = _descriptor.Descriptor(
  name='Isolated',
  full_name='Manifest.Isolated',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='isolated_server_url', full_name='Manifest.Isolated.isolated_server_url', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='namespace', full_name='Manifest.Isolated.namespace', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='hash', full_name='Manifest.Isolated.hash', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=339,
  serialized_end=411,
)

_MANIFEST_DIRECTORY = _descriptor.Descriptor(
  name='Directory',
  full_name='Manifest.Directory',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='git_checkout', full_name='Manifest.Directory.git_checkout', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='cipd_package', full_name='Manifest.Directory.cipd_package', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='isolated', full_name='Manifest.Directory.isolated', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=414,
  serialized_end=553,
)

_MANIFEST_DIRECTORIESENTRY = _descriptor.Descriptor(
  name='DirectoriesEntry',
  full_name='Manifest.DirectoriesEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='Manifest.DirectoriesEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='value', full_name='Manifest.DirectoriesEntry.value', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=_descriptor._ParseOptions(descriptor_pb2.MessageOptions(), _b('8\001')),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=555,
  serialized_end=626,
)

_MANIFEST = _descriptor.Descriptor(
  name='Manifest',
  full_name='Manifest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='version', full_name='Manifest.version', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='directories', full_name='Manifest.directories', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_MANIFEST_GITCHECKOUT, _MANIFEST_CIPDPACKAGE, _MANIFEST_ISOLATED, _MANIFEST_DIRECTORY, _MANIFEST_DIRECTORIESENTRY, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=26,
  serialized_end=626,
)

_MANIFEST_GITCHECKOUT.containing_type = _MANIFEST
_MANIFEST_CIPDPACKAGE.containing_type = _MANIFEST
_MANIFEST_ISOLATED.containing_type = _MANIFEST
_MANIFEST_DIRECTORY.fields_by_name['git_checkout'].message_type = _MANIFEST_GITCHECKOUT
_MANIFEST_DIRECTORY.fields_by_name['cipd_package'].message_type = _MANIFEST_CIPDPACKAGE
_MANIFEST_DIRECTORY.fields_by_name['isolated'].message_type = _MANIFEST_ISOLATED
_MANIFEST_DIRECTORY.containing_type = _MANIFEST
_MANIFEST_DIRECTORIESENTRY.fields_by_name['value'].message_type = _MANIFEST_DIRECTORY
_MANIFEST_DIRECTORIESENTRY.containing_type = _MANIFEST
_MANIFEST.fields_by_name['directories'].message_type = _MANIFEST_DIRECTORIESENTRY
DESCRIPTOR.message_types_by_name['Manifest'] = _MANIFEST

Manifest = _reflection.GeneratedProtocolMessageType('Manifest', (_message.Message,), dict(

  GitCheckout = _reflection.GeneratedProtocolMessageType('GitCheckout', (_message.Message,), dict(
    DESCRIPTOR = _MANIFEST_GITCHECKOUT,
    __module__ = 'source_manifest_pb2'
    # @@protoc_insertion_point(class_scope:Manifest.GitCheckout)
    ))
  ,

  CIPDPackage = _reflection.GeneratedProtocolMessageType('CIPDPackage', (_message.Message,), dict(
    DESCRIPTOR = _MANIFEST_CIPDPACKAGE,
    __module__ = 'source_manifest_pb2'
    # @@protoc_insertion_point(class_scope:Manifest.CIPDPackage)
    ))
  ,

  Isolated = _reflection.GeneratedProtocolMessageType('Isolated', (_message.Message,), dict(
    DESCRIPTOR = _MANIFEST_ISOLATED,
    __module__ = 'source_manifest_pb2'
    # @@protoc_insertion_point(class_scope:Manifest.Isolated)
    ))
  ,

  Directory = _reflection.GeneratedProtocolMessageType('Directory', (_message.Message,), dict(
    DESCRIPTOR = _MANIFEST_DIRECTORY,
    __module__ = 'source_manifest_pb2'
    # @@protoc_insertion_point(class_scope:Manifest.Directory)
    ))
  ,

  DirectoriesEntry = _reflection.GeneratedProtocolMessageType('DirectoriesEntry', (_message.Message,), dict(
    DESCRIPTOR = _MANIFEST_DIRECTORIESENTRY,
    __module__ = 'source_manifest_pb2'
    # @@protoc_insertion_point(class_scope:Manifest.DirectoriesEntry)
    ))
  ,
  DESCRIPTOR = _MANIFEST,
  __module__ = 'source_manifest_pb2'
  # @@protoc_insertion_point(class_scope:Manifest)
  ))
_sym_db.RegisterMessage(Manifest)
_sym_db.RegisterMessage(Manifest.GitCheckout)
_sym_db.RegisterMessage(Manifest.CIPDPackage)
_sym_db.RegisterMessage(Manifest.Isolated)
_sym_db.RegisterMessage(Manifest.Directory)
_sym_db.RegisterMessage(Manifest.DirectoriesEntry)


_MANIFEST_DIRECTORIESENTRY.has_options = True
_MANIFEST_DIRECTORIESENTRY._options = _descriptor._ParseOptions(descriptor_pb2.MessageOptions(), _b('8\001'))
# @@protoc_insertion_point(module_scope)