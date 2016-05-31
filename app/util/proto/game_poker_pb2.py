# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: game_poker.proto

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
  name='game_poker.proto',
  package='',
  serialized_pb=_b('\n\x10game_poker.proto\"\x1b\n\nm_5101_tos\x12\r\n\x05\x63\x61rds\x18\x01 \x03(\r\"\x0c\n\nm_5101_toc\"P\n\nm_5102_toc\x12\x1a\n\x12\x65xecute_account_id\x18\x01 \x02(\r\x12\x17\n\x0fnext_account_id\x18\x02 \x02(\r\x12\r\n\x05\x63\x61rds\x18\x03 \x03(\r\"/\n\nm_5103_toc\x12\x12\n\naccount_id\x18\x01 \x02(\r\x12\r\n\x05point\x18\x02 \x02(\r\"4\n\nm_5104_toc\x12\x12\n\naccount_id\x18\x01 \x02(\r\x12\x12\n\ncard_count\x18\x02 \x02(\r\"@\n\nm_5105_toc\x12 \n\nroom_fulls\x18\x01 \x03(\x0b\x32\x0c.p_room_full\x12\x10\n\x08server_t\x18\x02 \x01(\r\"\x93\x01\n\x0bp_room_full\x12\x12\n\naccount_id\x18\x01 \x02(\r\x12\x0c\n\x04rank\x18\x02 \x02(\r\x12\x14\n\x0cpoint_change\x18\x03 \x02(\x05\x12\x11\n\twin_count\x18\x04 \x02(\r\x12\x12\n\nlose_count\x18\x05 \x02(\r\x12\x12\n\nbomb_count\x18\x06 \x02(\r\x12\x11\n\tmax_point\x18\x07 \x02(\r')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_M_5101_TOS = _descriptor.Descriptor(
  name='m_5101_tos',
  full_name='m_5101_tos',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='cards', full_name='m_5101_tos.cards', index=0,
      number=1, type=13, cpp_type=3, label=3,
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
  serialized_start=20,
  serialized_end=47,
)


_M_5101_TOC = _descriptor.Descriptor(
  name='m_5101_toc',
  full_name='m_5101_toc',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
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
  serialized_start=49,
  serialized_end=61,
)


_M_5102_TOC = _descriptor.Descriptor(
  name='m_5102_toc',
  full_name='m_5102_toc',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='execute_account_id', full_name='m_5102_toc.execute_account_id', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='next_account_id', full_name='m_5102_toc.next_account_id', index=1,
      number=2, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='cards', full_name='m_5102_toc.cards', index=2,
      number=3, type=13, cpp_type=3, label=3,
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
  serialized_start=63,
  serialized_end=143,
)


_M_5103_TOC = _descriptor.Descriptor(
  name='m_5103_toc',
  full_name='m_5103_toc',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='account_id', full_name='m_5103_toc.account_id', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='point', full_name='m_5103_toc.point', index=1,
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
  serialized_start=145,
  serialized_end=192,
)


_M_5104_TOC = _descriptor.Descriptor(
  name='m_5104_toc',
  full_name='m_5104_toc',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='account_id', full_name='m_5104_toc.account_id', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='card_count', full_name='m_5104_toc.card_count', index=1,
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
  serialized_start=194,
  serialized_end=246,
)


_M_5105_TOC = _descriptor.Descriptor(
  name='m_5105_toc',
  full_name='m_5105_toc',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='room_fulls', full_name='m_5105_toc.room_fulls', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='server_t', full_name='m_5105_toc.server_t', index=1,
      number=2, type=13, cpp_type=3, label=1,
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
  serialized_start=248,
  serialized_end=312,
)


_P_ROOM_FULL = _descriptor.Descriptor(
  name='p_room_full',
  full_name='p_room_full',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='account_id', full_name='p_room_full.account_id', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='rank', full_name='p_room_full.rank', index=1,
      number=2, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='point_change', full_name='p_room_full.point_change', index=2,
      number=3, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='win_count', full_name='p_room_full.win_count', index=3,
      number=4, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='lose_count', full_name='p_room_full.lose_count', index=4,
      number=5, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bomb_count', full_name='p_room_full.bomb_count', index=5,
      number=6, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='max_point', full_name='p_room_full.max_point', index=6,
      number=7, type=13, cpp_type=3, label=2,
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
  serialized_start=315,
  serialized_end=462,
)

_M_5105_TOC.fields_by_name['room_fulls'].message_type = _P_ROOM_FULL
DESCRIPTOR.message_types_by_name['m_5101_tos'] = _M_5101_TOS
DESCRIPTOR.message_types_by_name['m_5101_toc'] = _M_5101_TOC
DESCRIPTOR.message_types_by_name['m_5102_toc'] = _M_5102_TOC
DESCRIPTOR.message_types_by_name['m_5103_toc'] = _M_5103_TOC
DESCRIPTOR.message_types_by_name['m_5104_toc'] = _M_5104_TOC
DESCRIPTOR.message_types_by_name['m_5105_toc'] = _M_5105_TOC
DESCRIPTOR.message_types_by_name['p_room_full'] = _P_ROOM_FULL

m_5101_tos = _reflection.GeneratedProtocolMessageType('m_5101_tos', (_message.Message,), dict(
  DESCRIPTOR = _M_5101_TOS,
  __module__ = 'game_poker_pb2'
  # @@protoc_insertion_point(class_scope:m_5101_tos)
  ))
_sym_db.RegisterMessage(m_5101_tos)

m_5101_toc = _reflection.GeneratedProtocolMessageType('m_5101_toc', (_message.Message,), dict(
  DESCRIPTOR = _M_5101_TOC,
  __module__ = 'game_poker_pb2'
  # @@protoc_insertion_point(class_scope:m_5101_toc)
  ))
_sym_db.RegisterMessage(m_5101_toc)

m_5102_toc = _reflection.GeneratedProtocolMessageType('m_5102_toc', (_message.Message,), dict(
  DESCRIPTOR = _M_5102_TOC,
  __module__ = 'game_poker_pb2'
  # @@protoc_insertion_point(class_scope:m_5102_toc)
  ))
_sym_db.RegisterMessage(m_5102_toc)

m_5103_toc = _reflection.GeneratedProtocolMessageType('m_5103_toc', (_message.Message,), dict(
  DESCRIPTOR = _M_5103_TOC,
  __module__ = 'game_poker_pb2'
  # @@protoc_insertion_point(class_scope:m_5103_toc)
  ))
_sym_db.RegisterMessage(m_5103_toc)

m_5104_toc = _reflection.GeneratedProtocolMessageType('m_5104_toc', (_message.Message,), dict(
  DESCRIPTOR = _M_5104_TOC,
  __module__ = 'game_poker_pb2'
  # @@protoc_insertion_point(class_scope:m_5104_toc)
  ))
_sym_db.RegisterMessage(m_5104_toc)

m_5105_toc = _reflection.GeneratedProtocolMessageType('m_5105_toc', (_message.Message,), dict(
  DESCRIPTOR = _M_5105_TOC,
  __module__ = 'game_poker_pb2'
  # @@protoc_insertion_point(class_scope:m_5105_toc)
  ))
_sym_db.RegisterMessage(m_5105_toc)

p_room_full = _reflection.GeneratedProtocolMessageType('p_room_full', (_message.Message,), dict(
  DESCRIPTOR = _P_ROOM_FULL,
  __module__ = 'game_poker_pb2'
  # @@protoc_insertion_point(class_scope:p_room_full)
  ))
_sym_db.RegisterMessage(p_room_full)


# @@protoc_insertion_point(module_scope)
