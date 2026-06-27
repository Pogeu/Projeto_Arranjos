"""Download the externally sourced application images used by the report."""

from __future__ import annotations

import hashlib
import time
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen


FILES = {
    "Phased_array_radar_AN_TPS-59.jpg": "radar_phased_array.jpg",
    "Base_Transceiver_Station_(25578073074).jpg": "wireless_base_station.jpg",
    "Dodecahedral-microphone-array-DHMA.jpg": "acoustic_microphone_array.jpg",
    "Antennes_actives_5G_Ericsson.jpg": "massive_mimo_5g_antennas.jpg",
}


def commons_url(filename: str) -> str:
    digest = hashlib.md5(filename.encode("utf-8")).hexdigest()
    return (
        "https://upload.wikimedia.org/wikipedia/commons/"
        f"{digest[0]}/{digest[:2]}/{quote(filename)}"
    )


def download(url: str, destination: Path) -> None:
    request = Request(url, headers={"User-Agent": "ProjetoArranjos/1.0"})
    with urlopen(request, timeout=60) as response:
        destination.write_bytes(response.read())


def main() -> None:
    output = Path(__file__).resolve().parents[1] / "figures" / "applications"
    output.mkdir(parents=True, exist_ok=True)

    for source_name, local_name in FILES.items():
        download(commons_url(source_name), output / local_name)
        time.sleep(2)

    sonar_name = "Sonar_Principle_EN.svg"
    digest = hashlib.md5(sonar_name.encode("utf-8")).hexdigest()
    sonar_url = (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/"
        f"{digest[0]}/{digest[:2]}/{quote(sonar_name)}/"
        f"1200px-{quote(sonar_name)}.png"
    )
    download(sonar_url, output / "sonar_principle.png")


if __name__ == "__main__":
    main()
