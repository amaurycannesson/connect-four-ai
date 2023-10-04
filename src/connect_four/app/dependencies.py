from .connect_four_service import ConnectFourService

connect_four_service = ConnectFourService()


def get_connect_four_service() -> ConnectFourService:
    return connect_four_service
