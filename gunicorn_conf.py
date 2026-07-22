bind = "127.0.0.1:5000"

# PENTING: sekarang load 2 model IndoBERT sekaligus per worker
# (aspect detection + sentiment classification) -> memori 2x lebih besar
# dari versi sebelumnya. Mulai dari 1 worker dulu kalau RAM terbatas,
# baru naikkan bertahap sambil pantau `free -h` / `htop`.
workers = 2

worker_class = "uvicorn.workers.UvicornWorker"

# Sekarang tiap request = 2x forward pass (aspect detection + sentiment
# per aspek terdeteksi) -> beri timeout lebih longgar dari sebelumnya
timeout = 180
graceful_timeout = 30

# Load kedua model SEKALI di proses master sebelum fork ke worker
preload_app = True

max_requests = 300
max_requests_jitter = 50

accesslog = "-"
errorlog = "-"
loglevel = "info"