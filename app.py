from flask import Flask, render_template_string, url_for

app = Flask(__name__)

# ==========================================
# NAVIGATION CODE (Search for these tags):
# [NAV-PYTHON] - Flask Routes & Config
# [NAV-STYLE]  - CSS Global Styles
# [NAV-HTML]   - Game Layout & Screens
# [NAV-JS]     - Core Game Logic & Events
# ==========================================

# [NAV-PYTHON]
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
/* [NAV-STYLE] */
body { margin:0; font-family:Segoe UI; background:#1a1a1a; color:white; overflow:hidden; display:flex; flex-direction:column; }
.player-area { flex:1; display:flex; flex-direction:column; align-items:center; justify-content:center; padding:10px; }
#p2 { transform:rotate(180deg); background:#2c3e50; }
#p1 { background:#2c3e50; }
.q-text { font-size:2.5rem; font-weight:bold; }
.entry { background:white; color:black; width:180px; height:45px; font-size:1.8rem; text-align:center; margin-bottom:10px; border-radius:5px; line-height:45px; }
.dial-pad { display:grid; grid-template-columns:repeat(3,1fr); gap:8px; width:80%; max-width:300px; }
button { padding:12px; font-size:1.2rem; border-radius:8px; border:none; font-weight:bold; }
.submit-btn { grid-column:span 3; background:#27ae60; color:white; }
.score-box { font-size:1.2rem; margin-bottom:5px; color:#f1c40f; }
#overlay, #nameScreen, #rulesScreen { position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.95); color:white; display:flex; flex-direction:column; justify-content:center; align-items:center; z-index:100; }
#overlay, #rulesScreen { display:none; }
/* Timer container removed from view via CSS or hidden */
#timer-container { display: none; } 

@keyframes correctFlash {
    0% { background-color: #2ecc71; }
    50% { background-color: #f1c40f; }
    100% { background-color: #2ecc71; }
}
.flash { animation: correctFlash 0.5s; }
</style>
</head>
<body>

<div id="nameScreen">
<h2>Enter Player Names</h2>
<input id="p1name" placeholder="Player 1 Name" style="padding:10px;font-size:18px;"><br><br>
<input id="p2name" placeholder="Player 2 Name" style="padding:10px;font-size:18px;"><br><br>
<button onclick="showRules()">START GAME</button>
</div>

<div id="rulesScreen">
<h2>Game Rules</h2>
<ul style="text-align:left; font-size:1.2rem; max-width:500px;">
<li>Each player will answer multiplication questions.</li>
<li>Correct answer gives 2 points.</li>
<li>Wrong answer clears your input and freezes your pad for 3 seconds.</li>
<li>Take your time—there is no longer a time limit!</li>
<li>Highest score after 100 rounds wins!</li>
</ul>
<button onclick="startGameFromRules()" style="margin-top:20px; padding:10px 20px; font-size:1rem;">Start Game</button>
</div>

<div id="overlay">
<h1 id="winner-text"></h1>
<p id="final-scores"></p>
<button onclick="location.reload()">RESTART</button>
</div>

<audio id="correctSound" src="{{ url_for('static', filename='correct.mp3') }}"></audio>
<audio id="wrongSound" src="{{ url_for('static', filename='wrong.mp3') }}"></audio>
<audio id="winSound" src="{{ url_for('static', filename='win.mp3') }}"></audio>
<audio id="bgSound" src="{{ url_for('static', filename='background.mp3') }}" loop></audio>

<div id="p2" class="player-area">
<div class="score-box" id="score2">Player 2: 0</div>
<div id="display2" class="entry"></div>
<div class="dial-pad" id="pad2">
<button onclick="addNum(2,'1')">1</button><button onclick="addNum(2,'2')">2</button><button onclick="addNum(2,'3')">3</button>
<button onclick="addNum(2,'4')">4</button><button onclick="addNum(2,'5')">5</button><button onclick="addNum(2,'6')">6</button>
<button onclick="addNum(2,'7')">7</button><button onclick="addNum(2,'8')">8</button><button onclick="addNum(2,'9')">9</button>
<button onclick="addNum(2,'0')">0</button><button onclick="clearN(2)" style="grid-column:span 2;">CLEAR</button>
<button class="submit-btn" id="btn2" onclick="check(2)">SUBMIT</button>
</div>
</div>

<div class="question-bar" style="display:flex; flex-direction:column; height:160px;">
    <div style="flex:1; display:flex; flex-direction:column; justify-content:center; align-items:center; transform:rotate(180deg); background:#34495e; border-bottom:2px solid #fff;">
        <div id="round-text-top" style="color:#f1c40f; font-size:1rem;">Round 1 / 100</div>
        <div class="q-text" id="q-display-top">? × ?</div>
    </div>
    <div style="height:4px; background:white; width:100%;"></div>
    <div style="flex:1; display:flex; flex-direction:column; justify-content:center; align-items:center; background:#2ecc71;">
        <div id="round-text-bottom" style="color:#f1c40f; font-size:1rem;">Round 1 / 100</div>
        <div class="q-text" id="q-display-bottom">? × ?</div>
    </div>
</div>

<div id="p1" class="player-area">
<div id="display1" class="entry"></div>
<div class="score-box" id="score1">Player 1: 0</div>
<div class="dial-pad" id="pad1">
<button onclick="addNum(1,'1')">1</button><button onclick="addNum(1,'2')">2</button><button onclick="addNum(1,'3')">3</button>
<button onclick="addNum(1,'4')">4</button><button onclick="addNum(1,'5')">5</button><button onclick="addNum(1,'6')">6</button>
<button onclick="addNum(1,'7')">7</button><button onclick="addNum(1,'8')">8</button><button onclick="addNum(1,'9')">9</button>
<button onclick="addNum(1,'0')">0</button><button onclick="clearN(1)" style="grid-column:span 2;">CLEAR</button>
<button class="submit-btn" id="btn1" onclick="check(1)">SUBMIT</button>
</div>
</div>

<script>
/* [NAV-JS] */
let ans=0, round=1;
let scores={1:0,2:0};
let inputs={1:"",2:""};
let playerNames={1:"Player 1",2:"Player 2"};
const totalRounds=100;
let rulesTimeout;

function showRules(){
    document.getElementById("nameScreen").style.display = "none";
    document.getElementById("rulesScreen").style.display = "flex";
    playerNames[1]=document.getElementById("p1name").value || "Player 1";
    playerNames[2]=document.getElementById("p2name").value || "Player 2";
    // Auto-start timer removed here as well
}

function startGameFromRules(){
    document.getElementById("rulesScreen").style.display = "none";
    startGame();
}

function startGame(){
    updateScores();
    const bg = document.getElementById("bgSound");
    bg.volume = 0.2;
    bg.play().catch(()=>console.log("Autoplay blocked"));
    nextQ();
}

function updateScores(){
    document.getElementById("score1").innerText=playerNames[1]+": "+scores[1];
    document.getElementById("score2").innerText=playerNames[2]+": "+scores[2];
}

function nextQ(){
    if(round>totalRounds){ showEnd(); return; }
    document.getElementById("round-text-top").innerText="Round "+round+" / "+totalRounds;
    document.getElementById("round-text-bottom").innerText="Round "+round+" / "+totalRounds;
    let a=Math.floor(Math.random()*13);
    let b=Math.floor(Math.random()*13);
    ans=a*b;
    document.getElementById("q-display-top").innerText=a+" × "+b;
    document.getElementById("q-display-bottom").innerText=a+" × "+b;
    clearN(1); clearN(2);
    // startTimer call removed
}

function addNum(p,n){
    if(inputs[p].length<4){ inputs[p]+=n; document.getElementById("display"+p).innerText=inputs[p]; }
}

function clearN(p){ inputs[p]=""; document.getElementById("display"+p).innerText=""; }

function freezePad(p){
    const pad=document.getElementById("pad"+p);
    pad.querySelectorAll("button").forEach(b=>b.disabled=true);
    setTimeout(()=>pad.querySelectorAll("button").forEach(b=>b.disabled=false),3000);
}

function check(p){
    if(parseInt(inputs[p])===ans){
        document.getElementById("correctSound").play();
        document.getElementById("display"+p).classList.add("flash");
        setTimeout(()=>document.getElementById("display"+p).classList.remove("flash"),500);
        scores[p]+=2;
        round++;
        updateScores();
        nextQ();
    } else {
        document.getElementById("wrongSound").play();
        clearN(p);
        freezePad(p);
    }
}

function showEnd(){
    document.getElementById("winSound").play();
    document.getElementById("overlay").style.display="flex";
    let win = scores[1]>scores[2]?playerNames[1]+" Wins!":scores[2]>scores[1]?playerNames[2]+" Wins!":"Draw!";
    document.getElementById("winner-text").innerText=win;
    document.getElementById("final-scores").innerText=playerNames[1]+": "+scores[1]+" | "+playerNames[2]+": "+scores[2];
}
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
