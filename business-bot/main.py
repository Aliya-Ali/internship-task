# main.py

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

from bot.google_sheets import connect_to_sheet, get_vertical_business_data, update_submission
from bot.instagram import login_instagram, update_full_profile, get_profile_url, post_image
from bot.image import get_random_image_from_folder

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "message": "", "profile_url": ""})

@app.post("/", response_class=HTMLResponse)
async def submit_form(request: Request, action: str = Form(...)):
    message = ""
    profile_url = ""

    try:
        username = "WspAli1"
        sheet = connect_to_sheet("Cut Cost Roofing Info")
        data = get_vertical_business_data(sheet)
        password = data['Password']

        cl = login_instagram(username, password)
        if not cl:
            message = "❌ Login failed"
        else:
            image_path = get_random_image_from_folder("images")
            if action == "update_profile":
                update_full_profile(cl, data, image_path)
                profile_url = get_profile_url(username)
                update_submission(sheet, 1, profile_url)
                message = "✅ Profile updated successfully!"
            elif action == "post_feed":
                caption = f"{data['Name']}\n{data['Address']}\n📞 {data['Phone Number']}\n🌐 {data.get('Website', '')}"
                post_url = post_image(cl, image_path, caption)
                update_submission(sheet, 1, post_url)
                message = "✅ Post uploaded!"
                profile_url = post_url

    except Exception as e:
        message = f"❌ Error: {e}"

    return templates.TemplateResponse("index.html", {"request": request, "message": message, "profile_url": profile_url})
