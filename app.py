import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from fastapi import FastAPI

from pymongo import MongoClient
import random
import datetime
import asyncio
from pymongo.errors import ServerSelectionTimeoutError
app = FastAPI()
import requests
url = r'mongodb+srv://projectssayo_db_user:1234@test.mdv08ad.mongodb.net/?retryWrites=true&w=majority&appName=test'

client = MongoClient(
    url,
    serverSelectionTimeoutMS=3000,
    connectTimeoutMS=3000,
    socketTimeoutMS=3000
)

otp_db = client["otp_db"]
otp_table = otp_db["verify_otp"]

user_db = client["users_db"]


user_table = user_db["user_info"]


remember_me_table = user_db["remember_me"]

logged_in_table=user_table["logged_in"]

from fastapi import Request
from fastapi.responses import JSONResponse
from pymongo.errors import ServerSelectionTimeoutError
import socket

@app.exception_handler(ServerSelectionTimeoutError)
async def mongo_timeout_handler(request: Request, exc: ServerSelectionTimeoutError):
    return JSONResponse(
        status_code=200,
        content={
            "success": False,
            "message": "Database unreachable. Please check internet connection."
        }
    )

@app.exception_handler(socket.timeout)
async def socket_timeout_handler(request: Request, exc: socket.timeout):
    return JSONResponse(
        status_code=200,
        content={
            "success": False,
            "message": "Network timeout. Please try again."
        }
    )


@app.get("/")
def test_connectivity():
    try:
        client = MongoClient(url)
        client.admin.command("ping")
        return {
            "status": "Connected to MongoDB successfully" ,
            "/send_otp":"https://zyro-chat.onrender.com/send_otp?email=suyognegi1@gmail.com&mac_id=82c6395286be",
            "/check_otp":"https://zyro-chat.onrender.com/check_otp?email=suyognegi1@gmail.com&mac_id=82c6395286be&input_otp=306741",
            "/set_remember_me":"https://zyro-chat.onrender.com/set_remember_me?mac_id=82c6395286be&remember_me=1&email=suyognegi1@gmail.com",
            "/remember_me":"https://zyro-chat.onrender.com/remember_me?email=suyognegi1@gmail.com&mac_id=82c6395286be",
            "/check_exists":"https://zyro-chat.onrender.com/check_exists?email=suyognegi1@gmail.com",
            "/create_account":"https://zyro-chat.onrender.com/create_account?name=s&email=suyognegi2@gmail.com&password=123&remember_me=true&square_pfp=http://res.cloudinary.com/doeeoa5f1/image/upload/v1771519879/c9jixljhlwkmt7qtzxtv.png&circle_pfp=http://res.cloudinary.com/doeeoa5f1/image/upload/v1771519882/kfmq6endttkglmbsteu9.png&mac_id=b57365813414",
            "/reset_password":"https://zyro-chat.onrender.com/reset_password?email=suyognegi1@gmail.com&password=123456",
            "/login":"https://zyro-chat.onrender.com/login?email=suyognegi1@gmail.com&password=123&mac_id=172382053270683&remember_me=True"
                }

    except ServerSelectionTimeoutError:
        return {"success": False, "message": "Server selection timeout, internet nahi hai gareeb bc"}
    except Exception as e:
        return {"status": "Connection failed", "error": str(e)}




@app.get("/set_logged_in")
def set_logged_in(email:str,mac_id:str):
    try:
        logged_in_table.update_one({"_id":email},{"$set":{"mac_id":mac_id}})
        print(f'user : {email} is set logged in at {mac_id}')
    except ServerSelectionTimeoutError:
        # return {"success": False, "message": "Server selection timeout, internet nahi hai gareeb bc"}
        print('internal server error at set_logged_in')
    except Exception as e:
        # return {"message": str(e), "success": False}
        print('internal server error at set_logged_in error : ',e)




@app.get("/send_otp")
def send_otp(email : str, mac_id : str):
    try:
        otp=random.randint(100_000,999_999)

        data = {"_id" : email,"otp" : otp,"mac_id" : mac_id,"sent_at" : datetime.datetime.now()}

        otp_table.update_one(
            {"_id": email},
            {"$set": data},
            upsert=True
        )
        print(data)
        sender_email = "projects.sayo@gmail.com"
        sender_password = "qwkt wfrd mmon soeg"

        html_message =f"""

<html>
<body style="margin:0; padding:0; background-color:#f2f4f7; font-family: Arial, Helvetica, sans-serif;">

<table width="100%" cellpadding="0" cellspacing="0" style="background:#f2f4f7; padding:20px 0;">
<tr>
<td align="center">

<table width="100%" cellpadding="0" cellspacing="0"
       style="max-width:600px; background:#ffffff; border-radius:10px; overflow:hidden;">

    <!-- Top Banner -->
    <tr>
        <td align="center">
            <img src="https://res.cloudinary.com/dnssyb7hu/image/upload/v1771342930/oik7ztbt79ykygpaoewx.png"
                 width="100%"
                 style="display:block; max-width:600px; height:auto;">
        </td>
    </tr>

    <!-- Main Content -->
    <tr>
        <td style="padding:35px 25px; text-align:center;">

            <h2 style="color:#2c3e50; margin:0 0 15px 0;">
                Verify Your Email Address
            </h2>

            <p style="color:#555555; font-size:14px; margin:0 0 25px 0;">
                Use the One-Time Password below to complete verification.
            </p>

            <div style="display:inline-block;
                        background:#f0f4f8;
                        padding:18px 35px;
                        border-radius:8px;
                        font-size:28px;
                        font-weight:bold;
                        letter-spacing:6px;
                        color:#1f4e79;">
                {otp}
            </div>

            <p style="margin:25px 0 0 0; font-size:13px; color:#777777;">
                This OTP is valid for 5 minutes.
            </p>

            <p style="margin:15px 0 0 0; font-size:12px; color:#999999;">
                If you didn’t request this, you can safely ignore this email.
            </p>

        </td>
    </tr>

    <!-- Divider -->
    <tr>
        <td style="border-top:1px solid #e5e5e5;"></td>
    </tr>

    <!-- Footer -->
    <tr>
        <td style="padding:20px;">

            <table width="100%" cellpadding="0" cellspacing="0">
                <tr>

                    <!-- Logo -->
                    <td width="30%" align="left" style="vertical-align:top;">
                        <img src="https://res.cloudinary.com/dnssyb7hu/image/upload/v1771343726/ev1pgoriwsaixlkmhr1i.png"
                             width="110"
                             style="display:block; max-width:110px; height:auto;">
                    </td>

                    <!-- Footer Text (Tight Spacing) -->
                    <td width="70%" align="right"
                        style="vertical-align:top; font-size:11px; line-height:14px; color:#8a8a8a;">

                        <div style="margin:0;">
                            Please do not reply directly to this email.
                        </div>

                        <div style="margin:0;">
                            © 2026 sayoLabs. All rights reserved.
                        </div>

                        <div style="margin:0;">
                            <a href="https://projectssayo.github.io/a/"
                               style="color:#8a8a8a; text-decoration:none;">
                               Contact Us
                            </a> |
                            <a href="https://projectssayo.github.io/b/"
                               style="color:#8a8a8a; text-decoration:none;">
                               Terms
                            </a> |
                            <a href="https://projectssayo.github.io/b/"
                               style="color:#8a8a8a; text-decoration:none;">
                               Privacy
                            </a>
                        </div>

                    </td>

                </tr>
            </table>

        </td>
    </tr>

</table>

</td>
</tr>
</table>

</body>
</html>

"""

        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Your OTP Code"
        msg["From"] = sender_email
        msg["To"] = email
        msg.attach(MIMEText(html_message, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email,sender_password)
            server.send_message(msg)

        return {"message": "OTP sent successfully", "success" : True}
    except ServerSelectionTimeoutError:
        return {"success": False, "message": "Server selection timeout, internet nahi hai gareeb bc"}
    except Exception as e:
        return {"message": str(e), "success": False}




@app.get("/check_otp")
def check_otp(email:str,mac_id:str,input_otp:str):
    try:


        a=otp_table.find_one({"_id": email})



        print(a) # {'_id': 'suyognegi1@gmail.com', 'mac_id': '82c6395286be', 'otp': 759733, 'sent_at': datetime.datetime(2026, 2, 17, 16, 48, 50, 603000)}
        if not a:
            return {"message": "GAND mara tera se galti hui hai otp bhejne main bcz _id me email exist hi naih karti ", "success": False}
        user_input_otp=input_otp

        print((datetime.datetime.now()-a['sent_at']).total_seconds())
        if int((datetime.datetime.now()-a['sent_at']).total_seconds())>600:
            return {"message":"OTP is has been expired. Retry with new", "success": False}
        if str(a.get("otp"))==str(user_input_otp) and str(a.get("mac_id"))==str(mac_id):
            return {"message": "OTP verifed successfully", "success":True}




        return {"success": False, "data": "wrong otp or try again"}



    except ServerSelectionTimeoutError:
        return {"success": False, "message": "Server selection timeout, internet nahi hai gareeb bc"}
    except Exception as e:
        return {"message": str(e), "success": False}


@app.get("/login")
def login(email:str,password:str,mac_id:str,remember_me:bool):
    try:
        a=user_table.find_one({"_id": email, "password": password})
        print(a)
        del a['password']

        if a:
            if remember_me:

                response = requests.get(
                    "https://zyro-chat.onrender.com/set_remember_me",
                    params={
                        "mac_id": mac_id,
                        "remember_me": 1,
                        "email": email
                    }
                )

                print(response.json())
            try:
                requests.get(
                    f"https://zyro-chat.onrender.com/set_logged_in?email={email}&mac_id={mac_id}",
                    timeout=5
                )
            except:
                pass


                return {"message": "user login cred are verified successfully and remeber me is set", "success":True,'data':a}

            else:
                remember_me_table.delete_one({'_id':email})
                return {"message": "user login cred verfid sucfly", "success":True,'data':a}

        return {"message": "wrong credetials", "success":False}
    except ServerSelectionTimeoutError:
        return {"success": False, "message": "Server selection timeout, internet nahi hai gareeb bc"}
    except Exception as e:
        return {"message": str(e), "success": False}


@app.get("/create_account")
def create_account(name:str,email:str,password:str,remember_me:bool,square_pfp:str, circle_pfp:str,mac_id:str):
    try:
        print(name)
        print(email)
        print(password)
        print(remember_me)
        print(square_pfp)
        print(circle_pfp)
        print(mac_id)

        user_table.insert_one({
            "_id": email,
            "name": name,
            "password": password,
            "square_pfp": square_pfp,
            "circle_pfp": circle_pfp,
            "remember_me": remember_me,
            "created_at": datetime.datetime.now(),
            "last_login": datetime.datetime.now() ,
            "is_online": True,
            "friends_list":[],
            "incoming_list":[],
            "outgoing_list":[],
            "last_pfp_update":datetime.datetime.now(),
            "created_on":mac_id



        })

        try:
            requests.get(
                f"https://zyro-chat.onrender.com/set_logged_in?email={email}&mac_id={mac_id}",
                timeout=5
            )
        except:
            pass


        return {"success":True,"message":"account created successfully !"}



    except ServerSelectionTimeoutError:
        return {"success": False, "message": "Server selection timeout, internet nahi hai gareeb bc"}
    except Exception as e:
        return {"message": str(e), "success": False}


@app.get("/remember_me")
def remember_me(email: str, mac_id: str):
    try:
        a = remember_me_table.find_one({
            "_id": email,
            "mac_id": mac_id,
            "remember_me": 1
        })

        if a:
            return {"success": True, 'message':"user is successfully set on remember me"}

        return {"success": False,"message":"user is for"}
    except ServerSelectionTimeoutError:
        return {"success": False, "message": "Server selection timeout, internet nahi hai gareeb bc"}
    except Exception as e:

        return {"success": False, "message": str(e)}

@app.get("/set_remember_me")
def set_remember_me(mac_id: str, remember_me:int, email:str):
    try:
        remember_me_table.update_one(
            {"_id": email},
            {"$set": {
                "remember_me": remember_me,
                "mac_id": mac_id,
                "updated_at": datetime.datetime.now()
            }},
            upsert=True
        )
        return {"success": True}
    except ServerSelectionTimeoutError:
        return {"success": False, "message": "Server selection timeout, internet nahi hai gareeb bc"}
    except Exception as e:
        return {"message": str(e), "success": False}


@app.get('/check_exists')
def check_exists(email:str):
    try:
        a=user_table.find_one({"_id": email})
        if a:
            return {"success": True, "data": a}
        return {"success": False, "message": "User not found"}


    except ServerSelectionTimeoutError:
        return {"success": False, "message":"Server selection timeout, internet nahi hai gareeb bc"}
    except Exception as e:
        return {"message": str(e), "success": False}



@app.get('/reset_password')
def reset_password(email:str,password:str):
    try:
        user_table.update_one(
            {"_id": email},
            {"$set": {
                "password": password
                }
            }
        )


        return {"success": True,'message':'password reset successfully !'}


    except ServerSelectionTimeoutError:
        return {"success": False, "message":"Server selection timeout, internet nahi hai gareeb bc"}
    except Exception as e:
        return {"message": str(e), "success": False}







# uvicorn api_0223_1058_otp_check_api:app --port 8002
