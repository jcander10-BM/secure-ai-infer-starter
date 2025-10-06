import time
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from .schemas import InferenceIn, InferenceOut
from .security import require_api_key
from .model import predict
from .utils import redact_pii, request_id

REQS = Counter("requests_total", "Total requests")
LAT  = Histogram("request_latency_seconds", "Latency", buckets=(.01,.05,.1,.2,.5,1,2,5))

from collections import defaultdict, deque
from time import time as now
WINDOW, LIMIT = 60, 30
bucket = defaultdict(lambda: deque())
def rate_limit(req: Request):
    key = req.headers.get("x-api-key","anon")
    q = bucket[key]
    t = now()
    while q and t - q[0] > WINDOW: q.popleft()
    if len(q) >= LIMIT:
        return False, int(WINDOW - (t - q[0]))
    q.append(t); return True, 0

app = FastAPI(title="Secure AI Inference")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=False,
    allow_methods=["POST"],
    allow_headers=["x-api-key","content-type"]
)

@app.middleware("http")
async def security_headers(request: Request, call_next):
    start = time.time()
    ok, retry = rate_limit(request)
    if not ok:
        return JSONResponse({"detail":"rate limit exceeded","retry_after":retry}, status_code=429)
    REQS.inc()
    rid = request_id()
    try:
        resp = await call_next(request)
    finally:
        LAT.observe(time.time()-start)
    resp.headers["X-Content-Type-Options"] = "nosniff"
    resp.headers["X-Frame-Options"] = "DENY"
    resp.headers["X-XSS-Protection"] = "0"
    resp.headers["Content-Security-Policy"] = "default-src 'none'"
    resp.headers["X-Request-ID"] = rid
    return resp

@app.get("/healthz")
def healthz(): return {"status":"ok"}

@app.get("/metrics")
def metrics():
    data = generate_latest()
    return JSONResponse(content=data.decode(), media_type=CONTENT_TYPE_LATEST)

@app.post("/predict", response_model=InferenceOut, dependencies=[Depends(require_api_key)])
def classify(inp: InferenceIn, request: Request):
    text = redact_pii(inp.text)
    label, score = predict(text)
    rid = request.headers.get("X-Request-ID","")
    return InferenceOut(label=label, score=score, request_id=rid or request_id())
