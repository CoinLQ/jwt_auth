from json import JSONEncoder
from uuid import UUID
class UUIDEncoder(JSONEncoder):
  def default(self, obj):
     if isinstance(obj, UUID):
         return str(obj)
     return JSONEncoder.default(self, obj)

JSONEncoder.default = UUIDEncoder.default
