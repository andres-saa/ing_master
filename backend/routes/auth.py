from fastapi import FastAPI, Depends, HTTPException, WebSocket, APIRouter,WebSocketDisconnect
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from typing import List, Dict

auth = APIRouter()

# Secret key to sign the JWT token (change this in production)
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

# Model for the site with username and password
class Site:
    def __init__(self, site_id: int, site_name: str,  username: str = "", password: str = ""):
        self.site_id = site_id
        self.site_name = site_name
        self.username = username
        self.password = password

# List of sites with usernames and passwords
sites = [
    
     Site(
        site_id=31,
        site_name="TEZO'S",
        username="tezos_pizza",
        password="tezos_pizza_2024"
    ),
]


# Configuración del esquema de seguridad
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Función para verificar las credenciales del usuario
def verify_user(username: str, password: str):
    for site in sites:
        if site.username == username and site.password == password:
            return site

# Ruta para obtener un token de acceso

@auth.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    site = verify_user(form_data.username, form_data.password)
    if site:
        token_data = {"sub": form_data.username}
        token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
        return {"access_token": token,"site_name":site.site_name, "token_type": "bearer", "username": form_data.username, "site_id": site.site_id}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")


@auth.get("/private-data")
async def get_private_data(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        site = next((s for s in sites if s.username == payload["sub"]), None)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token", headers={"WWW-Authenticate": "Bearer"})
    if site:
        return {"message": "Private Data", "username": payload["sub"], "site_id": site.site_id}
    else:
        raise HTTPException(status_code=401, detail="Invalid token", headers={"WWW-Authenticate": "Bearer"})

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, site_id: int):
        await websocket.accept()
        if site_id not in self.active_connections:
            self.active_connections[site_id] = []
        self.active_connections[site_id].append(websocket)

    def disconnect(self, websocket: WebSocket, site_id: int):
        if site_id in self.active_connections:
            self.active_connections[site_id].remove(websocket)
            if not self.active_connections[site_id]:
                del self.active_connections[site_id]

manager = ConnectionManager()


