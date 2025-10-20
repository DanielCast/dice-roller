# 🎲 Multiplayer Dice Roller (FastAPI + WebSockets)

A lightweight multiplayer dice roller built with **FastAPI**, **WebSockets**, and a simple **HTML/JS frontend**.  
Players can connect, pick dice, roll together in real time, and see each other’s results instantly.

![screenshot](static/img/dice-d20.png)

---

Features
- Real‑time multiplayer dice rolling via WebSockets
- Supports standard RPG dice: d4, d6, d8, d10, d12, d20
- Quantum RNG integration (ANU QRNG API) with secure fallback
- Clean UI with dice images, counters, and chat‑style roll history
- Auto‑reset option for quick rolling
- Works over LAN or VPN (e.g. RadminVPN) for remote friends

---

Project Structure

. 

├── main.py          - FastAPI app entrypoint 

├── utils.py         - Dice logic, RNG, history

├── static/

│ ├── index.html     -Frontend UI

│ ├── script.js      -Client logic

│ ├── style.css      -Styling

│ └── img/ - Dice images


1. Clone the repo git clone https://github.com/DanielCast/dice-roller

2. Create and activate a virtual environment 

powershell

python -m venv venv 

On Windows: venv\Scripts\activate.ps1 (if you need permission policy: Set-ExecutionPolicy RemoteSigned -Scope CurrentUser)

On Linux/macOS: source venv/bin/activate

2. bonus actually install python if the python command do not exist

3. Install dependencies 

pip install fastapi uvicorn requests

4. Run the server 

uvicorn app.main:app --host 0.0.0.0 --port 8000

IMPORTANT put the IP you wanna use after host and the port after port (duh?) 
I recommend NOT to use your personal IP unless you really trust who your playing with
so I suggest either put this in a cloud or if you wanna use it locally use something like ngrok, radminVPN hamachi

Also check if you need to open ports on router and firewall

5. Open your browser on http://"the ip you used":"the port you used"

    E.g. http://25.10.26.132:8080

<--------- USAGE --------->

    Click dice to add them to your pool.

    Right‑click dice to remove them.

    Set username in the input box.

    Click Roll to send results to everyone.

    Auto‑reset clears your pool after each roll.

    Reset clears manually.

<--------- RNG NOTES --------->
    Rolls use the ANU Quantum random numbers API but if it's not available or takes too long to reach --↴
    Falls back to Python’s secrets module for secure local randomness.

License

MIT License — feel free to fork, modify, and share.

Credits

    Built with FastAPI + Uvicorn
    Dice icons from open‑source graphics