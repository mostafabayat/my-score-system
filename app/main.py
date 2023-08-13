from fastapi import Request, FastAPI
import jdatetime

app = FastAPI()
app.score = 0

with open('score', 'r+') as score_file:
    app.score = int(score_file.read())

def log(reason, old_score, dec_or_inc, score):
    log = dict()
    log["date"] = jdatetime.datetime.now().isoformat()
    log["score"] = score
    log["old_score"] = old_score
    log["new_score"] = old_score + score
    log["type"] = dec_or_inc
    log["reason"] = reason
    with open('score.log', 'a+') as score_log:
        score_log.write(str(log) + '\n')


@app.get("/")
async def root():
    return {"score": app.score}

@app.post("/inc/{score_to_increase}")
async def inc(request: Request, score_to_increase):
    req_body = await request.json()
    log(req_body["reason"], app.score, "increase", int(score_to_increase))
    app.score += int(score_to_increase)
    with open('score', 'w+') as score_file:
        score_file.write(str(app.score))
    return {"score": app.score}

@app.post("/dec/{score_to_decrease}")
async def inc(request: Request, score_to_decrease):
    req_body = await request.json()
    log(req_body["reason"], app.score, "decrease", int(score_to_decrease))
    app.score -= int(score_to_decrease)
    with open('score', 'w+') as score_file:
        score_file.write(str(app.score))
    return {"score": app.score}
