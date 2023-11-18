from fastapi import Request, FastAPI
import jdatetime
import time

import schema
from schema import Prize, Reward, Penalty
import session

app = FastAPI()

def get_current_score():
    achieved_rewards = sum(reward.score for reward in session.get_achieved(Reward))
    achieved_prizes = sum(prize.score for prize in session.get_achieved(Prize))
    achieved_penalties = sum(penalty.score for penalty in session.get_achieved(Penalty))
    return achieved_rewards - achieved_prizes - achieved_penalties

session.create_tables()

@app.get("/")
@app.get("/get")
async def root():
    return {"score": get_current_score()}

@app.put("/{score_object}")
async def create_score_object(request: Request, score_object: str):
    req_body = await request.json()
    title = req_body["title"]
    score = int(req_body["score"])
    match score_object:
        case "reward":
            reward = Reward(title=title, score=score, creation_date=int(time.time()))
            session.insert(reward)
        case "prize":
            prize = Prize(title=title, score=score, creation_date=int(time.time()))
            session.insert(prize)
        case "penalty":
            penalty = Penalty(title=title, score=score, creation_date=int(time.time()))
            session.insert(penalty)
        case _:
            raise HTTPException(status_code=400, detail="accepted types are reward, prize, penalty!")
    return {"result": "ok!"}

@app.get("/{score_object}")
async def create_score_object(request: Request, score_object: str):
    match score_object:
        case "reward":
            output = [{key: value for key, value in reward.__dict__.items() if key in ["id", "title", "score"]} for reward in session.get_unachieved(Reward)]
        case "prize":
            output = [{key: value for key, value in prize.__dict__.items() if key in ["id", "title", "score"]} for prize in session.get_unachieved(Prize)]
        case "penalty":
            output = [{key: value for key, value in penalty.__dict__.items() if key in ["id", "title", "score"]} for penalty in session.get_unachieved(Penalty)]
        case _:
            raise HTTPException(status_code=400, detail="accepted types are reward, prize, penalty!")
    return output

@app.post("/achieve/{score_object}/{id}")
async def decrease(request: Request, score_object: str, id: int):
    match score_object:
        case "reward":
            session.achieve(Reward, id, int(time.time()))
        case "prize":
            session.achieve(Prize, id, int(time.time()))
        case "penalty":
            session.achieve(Penalty, id, int(time.time()))
        case _:
            raise HTTPException(status_code=400, detail="accepted types are reward, prize, penalty!")
    return {"result": "achieved!"}
