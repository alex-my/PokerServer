# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: game_mahjong.proto

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
  name='game_mahjong.proto',
  package='',
  serialized_pb=_b('\n\x12game_mahjong.proto\"i\n\nm_5201_toc\x12\x18\n\x10maker_account_id\x18\x01 \x02(\r\x12\r\n\x05\x63raps\x18\x02 \x03(\r\x12\x19\n\x11mahjong_start_num\x18\x03 \x01(\r\x12\x17\n\x0fmahjong_end_num\x18\x04 \x01(\r\",\n\nm_5202_toc\x12\x0c\n\x04\x63\x61rd\x18\x01 \x02(\r\x12\x10\n\x08operator\x18\x02 \x03(\r\"\x1a\n\nm_5203_tos\x12\x0c\n\x04\x63\x61rd\x18\x01 \x02(\r\"\x0c\n\nm_5203_toc\"r\n\nm_5204_toc\x12\x1a\n\x12\x65xecute_account_id\x18\x01 \x02(\r\x12\x0c\n\x04\x63\x61rd\x18\x02 \x02(\r\x12\x11\n\tcard_list\x18\x03 \x03(\r\x12\x15\n\roperator_able\x18\x04 \x02(\x08\x12\x10\n\x08operator\x18\x05 \x03(\r\"-\n\nm_5205_tos\x12\x10\n\x08operator\x18\x01 \x02(\r\x12\r\n\x05\x63\x61rds\x18\x02 \x03(\r\"I\n\nm_5205_toc\x12\x1a\n\x12\x65xecute_account_id\x18\x01 \x02(\r\x12\x10\n\x08operator\x18\x02 \x02(\r\x12\r\n\x05\x63\x61rds\x18\x03 \x03(\r\"5\n\nm_5206_toc\x12\x15\n\roperator_able\x18\x01 \x02(\x08\x12\x10\n\x08operator\x18\x02 \x03(\r\"@\n\nm_5207_toc\x12 \n\nroom_fulls\x18\x01 \x03(\x0b\x32\x0c.p_room_full\x12\x10\n\x08server_t\x18\x02 \x01(\r\"\xa8\x01\n\x0bp_room_full\x12\x12\n\naccount_id\x18\x01 \x02(\r\x12\x0c\n\x04rank\x18\x02 \x02(\r\x12\x14\n\x0cpoint_change\x18\x03 \x02(\x05\x12\x11\n\tmax_point\x18\x04 \x02(\r\x12\x13\n\x0b\x64rawn_count\x18\x05 \x02(\r\x12\x11\n\twin_count\x18\x06 \x02(\r\x12\x12\n\nlose_count\x18\x07 \x02(\r\x12\x12\n\nhelp_count\x18\x08 \x02(\r\" \n\nm_5208_toc\x12\x12\n\naccount_id\x18\x01 \x02(\r')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_M_5201_TOC = _descriptor.Descriptor(
  name='m_5201_toc',
  full_name='m_5201_toc',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='maker_account_id', full_name='m_5201_toc.maker_account_id', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='craps', full_name='m_5201_toc.craps', index=1,
      number=2, type=13, cpp_type=3, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='mahjong_start_num', full_name='m_5201_toc.mahjong_start_num', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='mahjong_end_num', full_name='m_5201_toc.mahjong_end_num', index=3,
      number=4, type=13, cpp_type=3, label=1,
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
  serialized_start=22,
  serialized_end=127,
)


_M_5202_TOC = _descriptor.Descriptor(
  name='m_5202_toc',
  full_name='m_5202_toc',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='card', full_name='m_5202_toc.card', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='operator', full_name='m_5202_toc.operator', index=1,
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
  serialized_start=129,
  serialized_end=173,
)


_M_5203_TOS = _descriptor.Descriptor(
  name='m_5203_tos',
  full_name='m_5203_tos',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='card', full_name='m_5203_tos.card', index=0,
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
  serialized_start=175,
  serialized_end=201,
)


_M_5203_TOC = _descriptor.Descriptor(
  name='m_5203_toc',
  full_name='m_5203_toc',
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
  serialized_start=203,
  serialized_end=215,
)


_M_5204_TOC = _descriptor.Descriptor(
  name='m_5204_toc',
  full_name='m_5204_toc',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='execute_account_id', full_name='m_5204_toc.execute_account_id', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='card', full_name='m_5204_toc.card', index=1,
      number=2, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='card_list', full_name='m_5204_toc.card_list', index=2,
      number=3, type=13, cpp_type=3, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='operator_able', full_name='m_5204_toc.operator_able', index=3,
      number=4, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='operator', full_name='m_5204_toc.operator', index=4,
      number=5, type=13, cpp_type=3, label=3,
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
  serialized_start=217,
  serialized_end=331,
)


_M_5205_TOS = _descriptor.Descriptor(
  name='m_5205_tos',
  full_name='m_5205_tos',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='operator', full_name='m_5205_tos.operator', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='cards', full_name='m_5205_tos.cards', index=1,
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
  serialized_start=333,
  serialized_end=378,
)


_M_5205_TOC = _descriptor.Descriptor(
  name='m_5205_toc',
  full_name='m_5205_toc',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='execute_account_id', full_name='m_5205_toc.execute_account_id', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='operator', full_name='m_5205_toc.operator', index=1,
      number=2, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='cards', full_name='m_5205_toc.cards', index=2,
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
  serialized_start=380,
  serialized_end=453,
)


_M_5206_TOC = _descriptor.Descriptor(
  name='m_5206_toc',
  full_name='m_5206_toc',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='operator_able', full_name='m_5206_toc.operator_able', index=0,
      number=1, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='operator', full_name='m_5206_toc.operator', index=1,
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
  serialized_start=455,
  serialized_end=508,
)


_M_5207_TOC = _descriptor.Descriptor(
  name='m_5207_toc',
  full_name='m_5207_toc',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='room_fulls', full_name='m_5207_toc.room_fulls', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='server_t', full_name='m_5207_toc.server_t', index=1,
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
  serialized_start=510,
  serialized_end=574,
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
      name='max_point', full_name='p_room_full.max_point', index=3,
      number=4, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='drawn_count', full_name='p_room_full.drawn_count', index=4,
      number=5, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='win_count', full_name='p_room_full.win_count', index=5,
      number=6, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='lose_count', full_name='p_room_full.lose_count', index=6,
      number=7, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='help_count', full_name='p_room_full.help_count', index=7,
      number=8, type=13, cpp_type=3, label=2,
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
  serialized_start=577,
  serialized_end=745,
)


_M_5208_TOC = _descriptor.Descriptor(
  name='m_5208_toc',
  full_name='m_5208_toc',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='account_id', full_name='m_5208_toc.account_id', index=0,
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
  serialized_start=747,
  serialized_end=779,
)

_M_5207_TOC.fields_by_name['room_fulls'].message_type = _P_ROOM_FULL
DESCRIPTOR.message_types_by_name['m_5201_toc'] = _M_5201_TOC
DESCRIPTOR.message_types_by_name['m_5202_toc'] = _M_5202_TOC
DESCRIPTOR.message_types_by_name['m_5203_tos'] = _M_5203_TOS
DESCRIPTOR.message_types_by_name['m_5203_toc'] = _M_5203_TOC
DESCRIPTOR.message_types_by_name['m_5204_toc'] = _M_5204_TOC
DESCRIPTOR.message_types_by_name['m_5205_tos'] = _M_5205_TOS
DESCRIPTOR.message_types_by_name['m_5205_toc'] = _M_5205_TOC
DESCRIPTOR.message_types_by_name['m_5206_toc'] = _M_5206_TOC
DESCRIPTOR.message_types_by_name['m_5207_toc'] = _M_5207_TOC
DESCRIPTOR.message_types_by_name['p_room_full'] = _P_ROOM_FULL
DESCRIPTOR.message_types_by_name['m_5208_toc'] = _M_5208_TOC

m_5201_toc = _reflection.GeneratedProtocolMessageType('m_5201_toc', (_message.Message,), dict(
  DESCRIPTOR = _M_5201_TOC,
  __module__ = 'game_mahjong_pb2'
  # @@protoc_insertion_point(class_scope:m_5201_toc)
  ))
_sym_db.RegisterMessage(m_5201_toc)

m_5202_toc = _reflection.GeneratedProtocolMessageType('m_5202_toc', (_message.Message,), dict(
  DESCRIPTOR = _M_5202_TOC,
  __module__ = 'game_mahjong_pb2'
  # @@protoc_insertion_point(class_scope:m_5202_toc)
  ))
_sym_db.RegisterMessage(m_5202_toc)

m_5203_tos = _reflection.GeneratedProtocolMessageType('m_5203_tos', (_message.Message,), dict(
  DESCRIPTOR = _M_5203_TOS,
  __module__ = 'game_mahjong_pb2'
  # @@protoc_insertion_point(class_scope:m_5203_tos)
  ))
_sym_db.RegisterMessage(m_5203_tos)

m_5203_toc = _reflection.GeneratedProtocolMessageType('m_5203_toc', (_message.Message,), dict(
  DESCRIPTOR = _M_5203_TOC,
  __module__ = 'game_mahjong_pb2'
  # @@protoc_insertion_point(class_scope:m_5203_toc)
  ))
_sym_db.RegisterMessage(m_5203_toc)

m_5204_toc = _reflection.GeneratedProtocolMessageType('m_5204_toc', (_message.Message,), dict(
  DESCRIPTOR = _M_5204_TOC,
  __module__ = 'game_mahjong_pb2'
  # @@protoc_insertion_point(class_scope:m_5204_toc)
  ))
_sym_db.RegisterMessage(m_5204_toc)

m_5205_tos = _reflection.GeneratedProtocolMessageType('m_5205_tos', (_message.Message,), dict(
  DESCRIPTOR = _M_5205_TOS,
  __module__ = 'game_mahjong_pb2'
  # @@protoc_insertion_point(class_scope:m_5205_tos)
  ))
_sym_db.RegisterMessage(m_5205_tos)

m_5205_toc = _reflection.GeneratedProtocolMessageType('m_5205_toc', (_message.Message,), dict(
  DESCRIPTOR = _M_5205_TOC,
  __module__ = 'game_mahjong_pb2'
  # @@protoc_insertion_point(class_scope:m_5205_toc)
  ))
_sym_db.RegisterMessage(m_5205_toc)

m_5206_toc = _reflection.GeneratedProtocolMessageType('m_5206_toc', (_message.Message,), dict(
  DESCRIPTOR = _M_5206_TOC,
  __module__ = 'game_mahjong_pb2'
  # @@protoc_insertion_point(class_scope:m_5206_toc)
  ))
_sym_db.RegisterMessage(m_5206_toc)

m_5207_toc = _reflection.GeneratedProtocolMessageType('m_5207_toc', (_message.Message,), dict(
  DESCRIPTOR = _M_5207_TOC,
  __module__ = 'game_mahjong_pb2'
  # @@protoc_insertion_point(class_scope:m_5207_toc)
  ))
_sym_db.RegisterMessage(m_5207_toc)

p_room_full = _reflection.GeneratedProtocolMessageType('p_room_full', (_message.Message,), dict(
  DESCRIPTOR = _P_ROOM_FULL,
  __module__ = 'game_mahjong_pb2'
  # @@protoc_insertion_point(class_scope:p_room_full)
  ))
_sym_db.RegisterMessage(p_room_full)

m_5208_toc = _reflection.GeneratedProtocolMessageType('m_5208_toc', (_message.Message,), dict(
  DESCRIPTOR = _M_5208_TOC,
  __module__ = 'game_mahjong_pb2'
  # @@protoc_insertion_point(class_scope:m_5208_toc)
  ))
_sym_db.RegisterMessage(m_5208_toc)


# @@protoc_insertion_point(module_scope)
