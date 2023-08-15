from fastapi import Request, FastAPI
import jdatetime

app = FastAPI()
app.score = 0

with open('score', 'r+') as score_file:
    app.score = int(score_file.read())

def log(reason, old_score, dec_or_inc, score):
    log = dict()
    log["date"] = jdatetime.datetime.now().isoformat()
    log["type"] = dec_or_inc
    log["score"] = score
    log["old_score"] = old_score
    log["new_score"] = old_score + score if dec_or_inc == "increase" else old_score - score
    log["reason"] = reason
    with open('score.log', 'a+') as score_log:
        score_log.write(str(log) + '\n')


@app.get("/")
@app.get("/get")
async def root():
    return {"score": app.score}

@app.post("/increase/{score_to_increase}")
async def increase(request: Request, score_to_increase):
    req_body = await request.json()
    log(req_body["reason"], app.score, request.url.path.split("/")[1], int(score_to_increase))
    app.score += int(score_to_increase)
    with open('score', 'w+') as score_file:
        score_file.write(str(app.score))
    return {"score": app.score}

@app.post("/spend/{score_to_decrease}")
@app.post("/decrease/{score_to_decrease}")
async def decrease(request: Request, score_to_decrease):
    req_body = await request.json()
    log(req_body["reason"], app.score, request.url.path.split("/")[1], int(score_to_decrease))
    app.score -= int(score_to_decrease)
    with open('score', 'w+') as score_file:
        score_file.write(str(app.score))
    return {"score": app.score}
