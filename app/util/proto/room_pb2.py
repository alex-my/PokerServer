# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: room.proto

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
  name='room.proto',
  package='',
  serialized_pb=_b('\n\nroom.proto\"/\n\nm_3001_tos\x12\x11\n\troom_type\x18\x01 \x02(\r\x12\x0e\n\x06rounds\x18\x02 \x02(\r\"@\n\nm_3001_toc\x12\x0f\n\x07room_id\x18\x01 \x02(\r\x12\x11\n\troom_type\x18\x02 \x02(\r\x12\x0e\n\x06rounds\x18\x03 \x01(\r\"\x1d\n\nm_3002_tos\x12\x0f\n\x07room_id\x18\x01 \x02(\r\"\xd0\x01\n\nm_3002_toc\x12\x0f\n\x07room_id\x18\x01 \x02(\r\x12\x1f\n\tuser_room\x18\x02 \x03(\x0b\x32\x0c.p_user_room\x12\x12\n\nuser_cards\x18\x03 \x03(\r\x12\x1a\n\x12\x65xecute_account_id\x18\x04 \x01(\r\x12\x17\n\x0flast_account_id\x18\x05 \x01(\r\x12\x12\n\nlast_cards\x18\x06 \x03(\r\x12\x0f\n\x07user_id\x18\x07 \x02(\r\x12\x0e\n\x06rounds\x18\x08 \x01(\r\x12\x12\n\nmax_rounds\x18\t \x01(\r\"\xa0\x01\n\x0bp_user_room\x12\x10\n\x08position\x18\x01 \x02(\r\x12\x12\n\naccount_id\x18\x02 \x02(\r\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x12\n\nhead_frame\x18\x04 \x01(\r\x12\x11\n\thead_icon\x18\x05 \x01(\r\x12\x0b\n\x03sex\x18\x06 \x01(\r\x12\n\n\x02ip\x18\x07 \x01(\t\x12\r\n\x05point\x18\x08 \x01(\x05\x12\x0e\n\x06status\x18\t \x01(\r\"\xe0\x02\n\nm_3003_toc\x12\x0f\n\x07room_id\x18\x01 \x02(\r\x12#\n\tuser_room\x18\x02 \x03(\x0b\x32\x10.p_user_mah_room\x12\x12\n\nuser_cards\x18\x03 \x03(\r\x12\x1a\n\x12\x65xecute_account_id\x18\x04 \x01(\r\x12\x17\n\x0flast_account_id\x18\x05 \x01(\r\x12\x12\n\nlast_cards\x18\x06 \x03(\r\x12\x0f\n\x07user_id\x18\x07 \x02(\r\x12\x0e\n\x06rounds\x18\x08 \x01(\r\x12\x12\n\nmax_rounds\x18\t \x01(\r\x12\x1e\n\x16mahjong_start_position\x18\n \x01(\r\x12\x19\n\x11mahjong_start_num\x18\x0b \x01(\r\x12\x1c\n\x14mahjong_end_position\x18\x0c \x01(\r\x12\x17\n\x0fmahjong_end_num\x18\r \x01(\r\x12\x18\n\x10maker_account_id\x18\x0e \x01(\r\"\xd6\x01\n\x0fp_user_mah_room\x12\x10\n\x08position\x18\x01 \x02(\r\x12\x12\n\naccount_id\x18\x02 \x02(\r\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x12\n\nhead_frame\x18\x04 \x01(\r\x12\x11\n\thead_icon\x18\x05 \x01(\r\x12\x0b\n\x03sex\x18\x06 \x01(\r\x12\n\n\x02ip\x18\x07 \x01(\t\x12\r\n\x05point\x18\x08 \x01(\x05\x12\x0e\n\x06status\x18\t \x01(\r\x12\x11\n\tpre_cards\x18\n \x03(\r\x12\x1d\n\x0b\x61ward_cards\x18\x0b \x03(\x0b\x32\x08.p_cards\"\x18\n\x07p_cards\x12\r\n\x05\x63\x61rds\x18\x01 \x03(\r\"-\n\nm_3005_toc\x12\x1f\n\tuser_room\x18\x01 \x02(\x0b\x32\x0c.p_user_room\" \n\nm_3006_toc\x12\x12\n\naccount_id\x18\x01 \x02(\r\"\x1d\n\nm_3101_tos\x12\x0f\n\x07message\x18\x01 \x02(\r\"\x1d\n\nm_3101_toc\x12\x0f\n\x07message\x18\x01 \x02(\r\"1\n\nm_3102_toc\x12\x12\n\naccount_id\x18\x01 \x02(\r\x12\x0f\n\x07message\x18\x02 \x02(\r\"\x1f\n\nm_3103_tos\x12\x11\n\tvoice_url\x18\x01 \x02(\t\"\x1f\n\nm_3103_toc\x12\x11\n\tvoice_url\x18\x01 \x02(\t\"3\n\nm_3104_toc\x12\x12\n\naccount_id\x18\x01 \x02(\r\x12\x11\n\tvoice_url\x18\x02 \x02(\t')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_M_3001_TOS = _descriptor.Descriptor(
  name='m_3001_tos',
  full_name='m_3001_tos',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='room_type', full_name='m_3001_tos.room_type', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='rounds', full_name='m_3001_tos.rounds', index=1,
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
  serialized_start=14,
  serialized_end=61,
)


_M_3001_TOC = _descriptor.Descriptor(
  name='m_3001_toc',
  full_name='m_3001_toc',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='room_id', full_name='m_3001_toc.room_id', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='room_type', full_name='m_3001_toc.room_type', index=1,
      number=2, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='rounds', full_name='m_3001_toc.rounds', index=2,
      number=3, type=13, cpp_type=3, label=1,
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
  serialized_start=63,
  serialized_end=127,
)


_M_3002_TOS = _descriptor.Descriptor(
  name='m_3002_tos',
  full_name='m_3002_tos',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='room_id', full_name='m_3002_tos.room_id', index=0,
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
  serialized_start=129,
  serialized_end=158,
)


_M_3002_TOC = _descriptor.Descriptor(
  name='m_3002_toc',
  full_name='m_3002_toc',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='room_id', full_name='m_3002_toc.room_id', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='user_room', full_name='m_3002_toc.user_room', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='user_cards', full_name='m_3002_toc.user_cards', index=2,
      number=3, type=13, cpp_type=3, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='execute_account_id', full_name='m_3002_toc.execute_account_id', index=3,
      number=4, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='last_account_id', full_name='m_3002_toc.last_account_id', index=4,
      number=5, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='last_cards', full_name='m_3002_toc.last_cards', index=5,
      number=6, type=13, cpp_type=3, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='user_id', full_name='m_3002_toc.user_id', index=6,
      number=7, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='rounds', full_name='m_3002_toc.rounds', index=7,
      number=8, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='max_rounds', full_name='m_3002_toc.max_rounds', index=8,
      number=9, type=13, cpp_type=3, label=1,
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
  serialized_start=161,
  serialized_end=369,
)


_P_USER_ROOM = _descriptor.Descriptor(
  name='p_user_room',
  full_name='p_user_room',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='position', full_name='p_user_room.position', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='account_id', full_name='p_user_room.account_id', index=1,
      number=2, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='name', full_name='p_user_room.name', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='head_frame', full_name='p_user_room.head_frame', index=3,
      number=4, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='head_icon', full_name='p_user_room.head_icon', index=4,
      number=5, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sex', full_name='p_user_room.sex', index=5,
      number=6, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ip', full_name='p_user_room.ip', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='point', full_name='p_user_room.point', index=7,
      number=8, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='status', full_name='p_user_room.status', index=8,
      number=9, type=13, cpp_type=3, label=1,
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
  serialized_start=372,
  serialized_end=532,
)


_M_3003_TOC = _descriptor.Descriptor(
  name='m_3003_toc',
  full_name='m_3003_toc',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='room_id', full_name='m_3003_toc.room_id', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='user_room', full_name='m_3003_toc.user_room', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='user_cards', full_name='m_3003_toc.user_cards', index=2,
      number=3, type=13, cpp_type=3, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='execute_account_id', full_name='m_3003_toc.execute_account_id', index=3,
      number=4, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='last_account_id', full_name='m_3003_toc.last_account_id', index=4,
      number=5, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='last_cards', full_name='m_3003_toc.last_cards', index=5,
      number=6, type=13, cpp_type=3, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='user_id', full_name='m_3003_toc.user_id', index=6,
      number=7, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='rounds', full_name='m_3003_toc.rounds', index=7,
      number=8, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='max_rounds', full_name='m_3003_toc.max_rounds', index=8,
      number=9, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='mahjong_start_position', full_name='m_3003_toc.mahjong_start_position', index=9,
      number=10, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='mahjong_start_num', full_name='m_3003_toc.mahjong_start_num', index=10,
      number=11, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='mahjong_end_position', full_name='m_3003_toc.mahjong_end_position', index=11,
      number=12, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='mahjong_end_num', full_name='m_3003_toc.mahjong_end_num', index=12,
      number=13, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='maker_account_id', full_name='m_3003_toc.maker_account_id', index=13,
      number=14, type=13, cpp_type=3, label=1,
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
  serialized_start=535,
  serialized_end=887,
)


_P_USER_MAH_ROOM = _descriptor.Descriptor(
  name='p_user_mah_room',
  full_name='p_user_mah_room',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='position', full_name='p_user_mah_room.position', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='account_id', full_name='p_user_mah_room.account_id', index=1,
      number=2, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='name', full_name='p_user_mah_room.name', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='head_frame', full_name='p_user_mah_room.head_frame', index=3,
      number=4, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='head_icon', full_name='p_user_mah_room.head_icon', index=4,
      number=5, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sex', full_name='p_user_mah_room.sex', index=5,
      number=6, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ip', full_name='p_user_mah_room.ip', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='point', full_name='p_user_mah_room.point', index=7,
      number=8, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='status', full_name='p_user_mah_room.status', index=8,
      number=9, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='pre_cards', full_name='p_user_mah_room.pre_cards', index=9,
      number=10, type=13, cpp_type=3, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='award_cards', full_name='p_user_mah_room.award_cards', index=10,
      number=11, type=11, cpp_type=10, label=3,
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
  serialized_start=890,
  serialized_end=1104,
)


_P_CARDS = _descriptor.Descriptor(
  name='p_cards',
  full_name='p_cards',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='cards', full_name='p_cards.cards', index=0,
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
  serialized_start=1106,
  serialized_end=1130,
)


_M_3005_TOC = _descriptor.Descriptor(
  name='m_3005_toc',
  full_name='m_3005_toc',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='user_room', full_name='m_3005_toc.user_room', index=0,
      number=1, type=11, cpp_type=10, label=2,
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
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1132,
  serialized_end=1177,
)


_M_3006_TOC = _descriptor.Descriptor(
  name='m_3006_toc',
  full_name='m_3006_toc',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='account_id', full_name='m_3006_toc.account_id', index=0,
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
  serialized_start=1179,
  serialized_end=1211,
)


_M_3101_TOS = _descriptor.Descriptor(
  name='m_3101_tos',
  full_name='m_3101_tos',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='message', full_name='m_3101_tos.message', index=0,
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
  serialized_start=1213,
  serialized_end=1242,
)


_M_3101_TOC = _descriptor.Descriptor(
  name='m_3101_toc',
  full_name='m_3101_toc',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='message', full_name='m_3101_toc.message', index=0,
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
  serialized_start=1244,
  serialized_end=1273,
)


_M_3102_TOC = _descriptor.Descriptor(
  name='m_3102_toc',
  full_name='m_3102_toc',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='account_id', full_name='m_3102_toc.account_id', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='message', full_name='m_3102_toc.message', index=1,
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
  serialized_start=1275,
  serialized_end=1324,
)


_M_3103_TOS = _descriptor.Descriptor(
  name='m_3103_tos',
  full_name='m_3103_tos',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='voice_url', full_name='m_3103_tos.voice_url', index=0,
      number=1, type=9, cpp_type=9, label=2,
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
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1326,
  serialized_end=1357,
)


_M_3103_TOC = _descriptor.Descriptor(
  name='m_3103_toc',
  full_name='m_3103_toc',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='voice_url', full_name='m_3103_toc.voice_url', index=0,
      number=1, type=9, cpp_type=9, label=2,
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
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1359,
  serialized_end=1390,
)


_M_3104_TOC = _descriptor.Descriptor(
  name='m_3104_toc',
  full_name='m_3104_toc',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='account_id', full_name='m_3104_toc.account_id', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='voice_url', full_name='m_3104_toc.voice_url', index=1,
      number=2, type=9, cpp_type=9, label=2,
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
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1392,
  serialized_end=1443,
)

_M_3002_TOC.fields_by_name['user_room'].message_type = _P_USER_ROOM
_M_3003_TOC.fields_by_name['user_room'].message_type = _P_USER_MAH_ROOM
_P_USER_MAH_ROOM.fields_by_name['award_cards'].message_type = _P_CARDS
_M_3005_TOC.fields_by_name['user_room'].message_type = _P_USER_ROOM
DESCRIPTOR.message_types_by_name['m_3001_tos'] = _M_3001_TOS
DESCRIPTOR.message_types_by_name['m_3001_toc'] = _M_3001_TOC
DESCRIPTOR.message_types_by_name['m_3002_tos'] = _M_3002_TOS
DESCRIPTOR.message_types_by_name['m_3002_toc'] = _M_3002_TOC
DESCRIPTOR.message_types_by_name['p_user_room'] = _P_USER_ROOM
DESCRIPTOR.message_types_by_name['m_3003_toc'] = _M_3003_TOC
DESCRIPTOR.message_types_by_name['p_user_mah_room'] = _P_USER_MAH_ROOM
DESCRIPTOR.message_types_by_name['p_cards'] = _P_CARDS
DESCRIPTOR.message_types_by_name['m_3005_toc'] = _M_3005_TOC
DESCRIPTOR.message_types_by_name['m_3006_toc'] = _M_3006_TOC
DESCRIPTOR.message_types_by_name['m_3101_tos'] = _M_3101_TOS
DESCRIPTOR.message_types_by_name['m_3101_toc'] = _M_3101_TOC
DESCRIPTOR.message_types_by_name['m_3102_toc'] = _M_3102_TOC
DESCRIPTOR.message_types_by_name['m_3103_tos'] = _M_3103_TOS
DESCRIPTOR.message_types_by_name['m_3103_toc'] = _M_3103_TOC
DESCRIPTOR.message_types_by_name['m_3104_toc'] = _M_3104_TOC

m_3001_tos = _reflection.GeneratedProtocolMessageType('m_3001_tos', (_message.Message,), dict(
  DESCRIPTOR = _M_3001_TOS,
  __module__ = 'room_pb2'
  # @@protoc_insertion_point(class_scope:m_3001_tos)
  ))
_sym_db.RegisterMessage(m_3001_tos)

m_3001_toc = _reflection.GeneratedProtocolMessageType('m_3001_toc', (_message.Message,), dict(
  DESCRIPTOR = _M_3001_TOC,
  __module__ = 'room_pb2'
  # @@protoc_insertion_point(class_scope:m_3001_toc)
  ))
_sym_db.RegisterMessage(m_3001_toc)

m_3002_tos = _reflection.GeneratedProtocolMessageType('m_3002_tos', (_message.Message,), dict(
  DESCRIPTOR = _M_3002_TOS,
  __module__ = 'room_pb2'
  # @@protoc_insertion_point(class_scope:m_3002_tos)
  ))
_sym_db.RegisterMessage(m_3002_tos)

m_3002_toc = _reflection.GeneratedProtocolMessageType('m_3002_toc', (_message.Message,), dict(
  DESCRIPTOR = _M_3002_TOC,
  __module__ = 'room_pb2'
  # @@protoc_insertion_point(class_scope:m_3002_toc)
  ))
_sym_db.RegisterMessage(m_3002_toc)

p_user_room = _reflection.GeneratedProtocolMessageType('p_user_room', (_message.Message,), dict(
  DESCRIPTOR = _P_USER_ROOM,
  __module__ = 'room_pb2'
  # @@protoc_insertion_point(class_scope:p_user_room)
  ))
_sym_db.RegisterMessage(p_user_room)

m_3003_toc = _reflection.GeneratedProtocolMessageType('m_3003_toc', (_message.Message,), dict(
  DESCRIPTOR = _M_3003_TOC,
  __module__ = 'room_pb2'
  # @@protoc_insertion_point(class_scope:m_3003_toc)
  ))
_sym_db.RegisterMessage(m_3003_toc)

p_user_mah_room = _reflection.GeneratedProtocolMessageType('p_user_mah_room', (_message.Message,), dict(
  DESCRIPTOR = _P_USER_MAH_ROOM,
  __module__ = 'room_pb2'
  # @@protoc_insertion_point(class_scope:p_user_mah_room)
  ))
_sym_db.RegisterMessage(p_user_mah_room)

p_cards = _reflection.GeneratedProtocolMessageType('p_cards', (_message.Message,), dict(
  DESCRIPTOR = _P_CARDS,
  __module__ = 'room_pb2'
  # @@protoc_insertion_point(class_scope:p_cards)
  ))
_sym_db.RegisterMessage(p_cards)

m_3005_toc = _reflection.GeneratedProtocolMessageType('m_3005_toc', (_message.Message,), dict(
  DESCRIPTOR = _M_3005_TOC,
  __module__ = 'room_pb2'
  # @@protoc_insertion_point(class_scope:m_3005_toc)
  ))
_sym_db.RegisterMessage(m_3005_toc)

m_3006_toc = _reflection.GeneratedProtocolMessageType('m_3006_toc', (_message.Message,), dict(
  DESCRIPTOR = _M_3006_TOC,
  __module__ = 'room_pb2'
  # @@protoc_insertion_point(class_scope:m_3006_toc)
  ))
_sym_db.RegisterMessage(m_3006_toc)

m_3101_tos = _reflection.GeneratedProtocolMessageType('m_3101_tos', (_message.Message,), dict(
  DESCRIPTOR = _M_3101_TOS,
  __module__ = 'room_pb2'
  # @@protoc_insertion_point(class_scope:m_3101_tos)
  ))
_sym_db.RegisterMessage(m_3101_tos)

m_3101_toc = _reflection.GeneratedProtocolMessageType('m_3101_toc', (_message.Message,), dict(
  DESCRIPTOR = _M_3101_TOC,
  __module__ = 'room_pb2'
  # @@protoc_insertion_point(class_scope:m_3101_toc)
  ))
_sym_db.RegisterMessage(m_3101_toc)

m_3102_toc = _reflection.GeneratedProtocolMessageType('m_3102_toc', (_message.Message,), dict(
  DESCRIPTOR = _M_3102_TOC,
  __module__ = 'room_pb2'
  # @@protoc_insertion_point(class_scope:m_3102_toc)
  ))
_sym_db.RegisterMessage(m_3102_toc)

m_3103_tos = _reflection.GeneratedProtocolMessageType('m_3103_tos', (_message.Message,), dict(
  DESCRIPTOR = _M_3103_TOS,
  __module__ = 'room_pb2'
  # @@protoc_insertion_point(class_scope:m_3103_tos)
  ))
_sym_db.RegisterMessage(m_3103_tos)

m_3103_toc = _reflection.GeneratedProtocolMessageType('m_3103_toc', (_message.Message,), dict(
  DESCRIPTOR = _M_3103_TOC,
  __module__ = 'room_pb2'
  # @@protoc_insertion_point(class_scope:m_3103_toc)
  ))
_sym_db.RegisterMessage(m_3103_toc)

m_3104_toc = _reflection.GeneratedProtocolMessageType('m_3104_toc', (_message.Message,), dict(
  DESCRIPTOR = _M_3104_TOC,
  __module__ = 'room_pb2'
  # @@protoc_insertion_point(class_scope:m_3104_toc)
  ))
_sym_db.RegisterMessage(m_3104_toc)


# @@protoc_insertion_point(module_scope)
