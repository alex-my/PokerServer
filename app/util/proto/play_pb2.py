# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: play.proto

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
  name='play.proto',
  package='',
  serialized_pb=_b('\n\nplay.proto\"\x1d\n\nm_4001_tos\x12\x0f\n\x07operate\x18\x01 \x02(\r\"\x1d\n\nm_4001_toc\x12\x0f\n\x07operate\x18\x01 \x02(\r\"1\n\nm_4002_toc\x12\x12\n\naccount_id\x18\x01 \x02(\r\x12\x0f\n\x07operate\x18\x02 \x02(\r\"7\n\nm_4003_toc\x12\x1a\n\x12\x65xecute_account_id\x18\x01 \x02(\r\x12\r\n\x05\x63\x61rds\x18\x02 \x03(\r\"G\n\nm_4004_toc\x12!\n\nclose_info\x18\x01 \x03(\x0b\x32\r.p_close_info\x12\x16\n\x0ewin_account_id\x18\x02 \x02(\r\"6\n\x0cp_close_info\x12\x12\n\naccount_id\x18\x01 \x02(\r\x12\x12\n\ncard_count\x18\x02 \x02(\r')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_M_4001_TOS = _descriptor.Descriptor(
  name='m_4001_tos',
  full_name='m_4001_tos',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='operate', full_name='m_4001_tos.operate', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
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
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=14,
  serialized_end=43,
)


_M_4001_TOC = _descriptor.Descriptor(
  name='m_4001_toc',
  full_name='m_4001_toc',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='operate', full_name='m_4001_toc.operate', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
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
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=45,
  serialized_end=74,
)


_M_4002_TOC = _descriptor.Descriptor(
  name='m_4002_toc',
  full_name='m_4002_toc',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='account_id', full_name='m_4002_toc.account_id', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='operate', full_name='m_4002_toc.operate', index=1,
      number=2, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
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
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=76,
  serialized_end=125,
)


_M_4003_TOC = _descriptor.Descriptor(
  name='m_4003_toc',
  full_name='m_4003_toc',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='execute_account_id', full_name='m_4003_toc.execute_account_id', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='cards', full_name='m_4003_toc.cards', index=1,
      number=2, type=13, cpp_type=3, label=3,
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
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=127,
  serialized_end=182,
)


_M_4004_TOC = _descriptor.Descriptor(
  name='m_4004_toc',
  full_name='m_4004_toc',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='close_info', full_name='m_4004_toc.close_info', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='win_account_id', full_name='m_4004_toc.win_account_id', index=1,
      number=2, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
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
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=184,
  serialized_end=255,
)


_P_CLOSE_INFO = _descriptor.Descriptor(
  name='p_close_info',
  full_name='p_close_info',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='account_id', full_name='p_close_info.account_id', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='card_count', full_name='p_close_info.card_count', index=1,
      number=2, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
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
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=257,
  serialized_end=311,
)

_M_4004_TOC.fields_by_name['close_info'].message_type = _P_CLOSE_INFO
DESCRIPTOR.message_types_by_name['m_4001_tos'] = _M_4001_TOS
DESCRIPTOR.message_types_by_name['m_4001_toc'] = _M_4001_TOC
DESCRIPTOR.message_types_by_name['m_4002_toc'] = _M_4002_TOC
DESCRIPTOR.message_types_by_name['m_4003_toc'] = _M_4003_TOC
DESCRIPTOR.message_types_by_name['m_4004_toc'] = _M_4004_TOC
DESCRIPTOR.message_types_by_name['p_close_info'] = _P_CLOSE_INFO

m_4001_tos = _reflection.GeneratedProtocolMessageType('m_4001_tos', (_message.Message,), dict(
  DESCRIPTOR = _M_4001_TOS,
  __module__ = 'play_pb2'
  # @@protoc_insertion_point(class_scope:m_4001_tos)
  ))
_sym_db.RegisterMessage(m_4001_tos)

m_4001_toc = _reflection.GeneratedProtocolMessageType('m_4001_toc', (_message.Message,), dict(
  DESCRIPTOR = _M_4001_TOC,
  __module__ = 'play_pb2'
  # @@protoc_insertion_point(class_scope:m_4001_toc)
  ))
_sym_db.RegisterMessage(m_4001_toc)

m_4002_toc = _reflection.GeneratedProtocolMessageType('m_4002_toc', (_message.Message,), dict(
  DESCRIPTOR = _M_4002_TOC,
  __module__ = 'play_pb2'
  # @@protoc_insertion_point(class_scope:m_4002_toc)
  ))
_sym_db.RegisterMessage(m_4002_toc)

m_4003_toc = _reflection.GeneratedProtocolMessageType('m_4003_toc', (_message.Message,), dict(
  DESCRIPTOR = _M_4003_TOC,
  __module__ = 'play_pb2'
  # @@protoc_insertion_point(class_scope:m_4003_toc)
  ))
_sym_db.RegisterMessage(m_4003_toc)

m_4004_toc = _reflection.GeneratedProtocolMessageType('m_4004_toc', (_message.Message,), dict(
  DESCRIPTOR = _M_4004_TOC,
  __module__ = 'play_pb2'
  # @@protoc_insertion_point(class_scope:m_4004_toc)
  ))
_sym_db.RegisterMessage(m_4004_toc)

p_close_info = _reflection.GeneratedProtocolMessageType('p_close_info', (_message.Message,), dict(
  DESCRIPTOR = _P_CLOSE_INFO,
  __module__ = 'play_pb2'
  # @@protoc_insertion_point(class_scope:p_close_info)
  ))
_sym_db.RegisterMessage(p_close_info)


# @@protoc_insertion_point(module_scope)
