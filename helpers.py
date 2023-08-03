import os
import time
import datetime
import operator as op

from typing import Any

from geopy.distance import geodesic

from config import VPS_SERVERS
from dto import GeoVPS, NearVPSResponse, VPSInfo
from fetcher import UserCoordinateFetcher


def get_near_vps(ip: str) -> NearVPSResponse:
    user_info = UserCoordinateFetcher(ip).json()
    user_coordinates = (user_info['longitude'], user_info['latitude'])
    distances = []
    for server in VPS_SERVERS:
        server_coordinates = (VPS_SERVERS[server]["longitude"], VPS_SERVERS[server]["latitude"])
        distances.append(
            GeoVPS(
                distance=geodesic(user_coordinates, server_coordinates).km,
                server_name=server
            )
        )
    near_vps = sorted(distances, key=op.attrgetter('distance'))[0]

    return NearVPSResponse(
        vps=near_vps,
        vps_info=VPSInfo(**VPS_SERVERS[near_vps.server_name])
    )


def timeit(func):
    def inner(*args, **kwargs) -> tuple[Any, float]:
        from datetime import datetime
        start = datetime.now()
        res = func(*args, **kwargs)
        return res, (datetime.now() - start).total_seconds()
    return inner


def gen_filename(url: str) -> str:
    now = datetime.datetime.utcnow().strftime("%y%m%d_%H%M%S")
    filename = os.path.basename(url)
    return "_".join([now, filename])
