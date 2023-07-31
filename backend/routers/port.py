from fastapi import APIRouter
import socket

port_router = APIRouter()

# 현재 호스트의 IP 주소와 포트 번호 조회하는 엔드포인트
@port_router.get("/get_host_info/")
async def get_host_info():
    # 호스트 이름 가져오기
    # host_name = socket.gethostname()
    # # 호스트 이름을 IP 주소로 변환
    # host_ip = socket.gethostbyname(host_name)
    # # 서버 포트 번호 가져오기
    # server_info = app.server.base_url
    # port = server_info.port
    return {"host": '34.64.152.76', "port": '30007'}