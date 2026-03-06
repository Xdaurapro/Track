#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from pony.orm import PrimaryKey, Required

from database import db


class PersistedChatState(db.Entity):
    chat_id = PrimaryKey(int, auto=False, size=64)
    payload = Required(str)
    updated_at = Required(datetime, default=lambda: datetime.now())
