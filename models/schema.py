from pydantic import BaseModel
from typing import List


# Sekarang cuma 1 kolom komentar bebas (evaluasimateri di Laravel),
# aspek TIDAK lagi diketahui dari struktur form -> perlu deteksi otomatis
class PredictRequest(BaseModel):
    komentar: str


class BatchItem(BaseModel):
    komentar: str


class BatchRequest(BaseModel):
    data: List[BatchItem]