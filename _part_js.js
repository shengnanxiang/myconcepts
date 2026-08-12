(function(){
'use strict';
var $=function(id){return document.getElementById(id)};
var cameraClickable=$('cameraClickable'),cameraSvg=$('cameraSvg'),cameraHint=$('cameraHint');
var cameraStateLabel=$('cameraStateLabel');
var lane=$('lane'),judgeText=$('judgeText'),scoreDisplay=$('scoreDisplay');
var progressFill=$('progressFill'),comboDisplay=$('comboDisplay'),comboNum=$('comboNum');
var startOverlay=$('startOverlay'),endOverlay=$('endOverlay');
var startBtn=$('startBtn'),retryBtn=$('retryBtn');
var endScore=$('endScore'),endMaxCombo=$('endMaxCombo'),endAccuracy=$('endAccuracy');
var endTitle=$('endTitle'),endDesc=$('endDesc'),gameScreen=$('gameScreen');

// SVG: 打开状态 — 镜头可见，盖板滑到右侧
var SVG_OPEN='<g>'
+'<rect x="15" y="20" width="190" height="105" rx="16" fill="#2C2C2C" stroke="#1a1a1a" stroke-width="2"/>'
+'<rect x="75" y="10" width="70" height="12" rx="4" fill="#2C2C2C" stroke="#1a1a1a" stroke-width="2"/>'
+'<circle cx="185" cy="30" r="7" fill="#444" stroke="#666" stroke-width="1.5"/>'
+'<circle cx="185" cy="30" r="3" fill="#222"/>'
+'<text x="110" y="115" font-size="7" fill="#555" text-anchor="middle" font-family="monospace" letter-spacing="1">AiKen</text>'
+'<circle cx="110" cy="68" r="34" fill="#1a1a1a" stroke="#333" stroke-width="1"/>'
+'<circle cx="110" cy="68" r="28" fill="#0D0D0D" stroke="#2a2a2a" stroke-width="1"/>'
+'<circle cx="110" cy="68" r="20" fill="#111" stroke="#333" stroke-width="1"/>'
+'<circle cx="110" cy="68" r="12" fill="#080808"/>'
+'<ellipse cx="103" cy="61" rx="7" ry="5" fill="rgba(80,130,180,0.2)"/>'
+'<ellipse cx="103" cy="61" rx="3" ry="2" fill="rgba(150,200,255,0.15)"/>'
+'<circle cx="110" cy="68" r="3" fill="#1a1a1a"/>'
+'<rect x="50" y="42" width="120" height="52" rx="2" fill="none" stroke="rgba(80,80,80,.3)" stroke-width="1" stroke-dasharray="3,2"/>'
+'<rect x="150" y="44" width="28" height="48" rx="5" fill="#3a3a3a" stroke="#555" stroke-width="1.5"/>'
+'<rect x="155" y="50" width="18" height="36" rx="2" fill="#2a2a2a" stroke="#444" stroke-width="1"/>'
+'<text x="164" y="70" font-size="6" fill="#666" text-anchor="middle" font-family="monospace">COVER</text>'
+'<path d="M148 68 L142 68 M145 65 L142 68 L145 71" stroke="rgba(76,175,80,.5)" stroke-width="1.5" fill="none"/>'
+'</g>';

// SVG: 关闭状态 — 盖板覆盖镜头
var SVG_CLOSED='<g>'
+'<rect x="15" y="20" width="190" height="105" rx="16" fill="#2C2C2C" stroke="#1a1a1a" stroke-width="2"/>'
+'<rect x="75" y="10" width="70" height="12" rx="4" fill="#2C2C2C" stroke="#1a1a1a" stroke-width="2"/>'
+'<circle cx="185" cy="30" r="7" fill="#444" stroke="#666" stroke-width="1.5"/>'
+'<circle cx="185" cy="30" r="3" fill="#222"/>'
+'<text x="110" y="115" font-size="7" fill="#555" text-anchor="middle" font-family="monospace" letter-spacing="1">AiKen</text>'
+'<circle cx="110" cy="68" r="34" fill="#1a1a1a" stroke="#333" stroke-width="1"/>'
+'<rect x="50" y="42" width="120" height="52" rx="2" fill="none" stroke="rgba(80,80,80,.3)" stroke-width="1" stroke-dasharray="3,2"/>'
+'<rect x="78" y="44" width="64" height="48" rx="5" fill="#3a3a3a" stroke="#555" stroke-width="1.5"/>'
+'<rect x="83" y="50" width="54" height="36" rx="2" fill="#2a2a2a" stroke="#444" stroke-width="1"/>'
+'<text x="110" y="70" font-size="7" fill="#666" text-anchor="middle" font-family="monospace">CLOSED</text>'
+'<path d="M148 68 L142 68 M145 65 L142 68 L145 71" stroke="rgba(229,57,53,.4)" stroke-width="1.5" fill="none"/>'
+'</g>';

// 游戏状态
var state='idle',notes=[],score=0,combo=0,maxCombo=0,hitCount=0,totalNotes=0;
var startTime=0,rafId=null;
var cameraState='open'; // 初始状态：打开
var isSwitching=false;

// 节奏谱：open 和 close 交替（初始 open，所以第一个提示是 close）
var chart=[
{t:2000,type:'close'},{t:3000,type:'open'},{t:4000,type:'close'},
{t:5000,type:'open'},{t:6000,type:'close'},{t:7000,type:'open'},
{t:8000,type:'close'},{t:9000,type:'open'},{t:10000,type:'close'},
{t:11000,type:'open'},{t:12000,type:'close'},{t:13000,type:'open'},
{t:14000,type:'close'},{t:15000,type:'open'},{t:16000,type:'close'},
{t:17000,type:'open'},{t:18000,type:'close'},{t:19000,type:'open'},
{t:20000,type:'close'},{t:21000,type:'open'},{t:22000,type:'close'},
{t:23000,type:'open'},{t:24000,type:'close'},{t:25000,type:'open'}
];

var NOTE_SPEED=0.25,HIT_WINDOW=350,PERFECT_WINDOW=150,GOOD_WINDOW=280;

// 音频
var audioCtx=null;
function initAudio(){if(!audioCtx){try{audioCtx=new(window.AudioContext||window.webkitAudioContext)()}catch(e){}}}
function playTone(freq,dur,vol){
  if(!audioCtx)return;
  var osc=audioCtx.createOscillator(),gain=audioCtx.createGain();
  osc.frequency.value=freq;osc.type='sine';
  gain.gain.setValueAtTime(vol||0.15,audioCtx.currentTime);
  gain.gain.exponentialRampToValueAtTime(0.001,audioCtx.currentTime+(dur||0.15));
  osc.connect(gain);gain.connect(audioCtx.destination);
  osc.start();osc.stop(audioCtx.currentTime+(dur||0.15));
}
function playHitSound(p){playTone(p?880:660,0.12,0.12);if(p)setTimeout(function(){playTone(1320,0.08,0.08)},30)}
function playMissSound(){playTone(200,0.2,0.1)}
function playUnlockSound(){[523,659,784,1047].forEach(function(f,i){setTimeout(function(){playTone(f,0.3,0.15)},i*120)})}

function createNoteEl(note){
  var el=document.createElement('div');el.className='note '+note.type;
  var a=document.createElement('span');a.className='arrow';
  a.textContent=note.type==='open'?'OPEN':'CLOSE';
  el.appendChild(a);note.el=el;lane.appendChild(el);
}

function startGame(){
  initAudio();
  if(audioCtx&&audioCtx.state==='suspended')audioCtx.resume();
  notes.forEach(function(n){if(n.el)n.el.remove()});
  notes=[];score=0;combo=0;maxCombo=0;hitCount=0;
  scoreDisplay.textContent='0';
  comboDisplay.classList.remove('show');
  progressFill.style.width='0%';
  resetCamera();
  totalNotes=chart.length;
  chart.forEach(function(c){notes.push({t:c.t,type:c.type,hit:false,missed:false,el:null,spawned:false})});
  state='playing';
  startOverlay.classList.add('hidden');
  endOverlay.classList.add('hidden');
  startTime=performance.now();
  rafId=requestAnimationFrame(gameLoop);
}

function gameLoop(now){
  if(state!=='playing')return;
  var elapsed=now-startTime;
  var lastT=chart[chart.length-1].t;
  progressFill.style.width=Math.min(100,(elapsed/(lastT+1000))*100)+'%';
  var laneH=lane.getBoundingClientRect().height;
  var hitY=laneH-24;
  notes.forEach(function(n){
    if(n.spawned)return;
    var t=n.t-elapsed;
    if(t<2000&&t>-HIT_WINDOW){n.spawned=true;createNoteEl(n)}
  });
  notes.forEach(function(n){
    if(!n.spawned||n.hit||n.missed)return;
    var t=n.t-elapsed;
    n.el.style.top=(hitY-t*NOTE_SPEED)+'px';
    if(t<-HIT_WINDOW&&!n.hit){
      n.missed=true;n.el.classList.add('miss-anim');
      (function(m){setTimeout(function(){if(m.el)m.el.remove()},400)})(n);
      combo=0;comboDisplay.classList.remove('show');
      showJudge('miss','MISS');playMissSound();
    }
  });
  var nearHit=notes.some(function(n){return n.spawned&&!n.hit&&!n.missed&&Math.abs(n.t-elapsed)<HIT_WINDOW});
  cameraHint.classList.toggle('active',nearHit);
  if(notes.every(function(n){return n.hit||n.missed})&&elapsed>lastT+500){endGame();return}
  rafId=requestAnimationFrame(gameLoop);
}

function checkHit(){
  if(state!=='playing')return;
  var elapsed=performance.now()-startTime;
  var closest=null,diff=Infinity;
  notes.forEach(function(n){
    if(n.hit||n.missed||!n.spawned)return;
    var d=Math.abs(n.t-elapsed);
    if(d<diff){diff=d;closest=n}
  });
  if(!closest||diff>HIT_WINDOW){
    showJudge('miss','MISS');playMissSound();combo=0;comboDisplay.classList.remove('show');
    return;
  }
  var judge,perfect;
  if(diff<PERFECT_WINDOW){judge='perfect';perfect=true;score+=100}
  else if(diff<GOOD_WINDOW){judge='good';perfect=false;score+=60}
  else{judge='good';perfect=false;score+=30}
  closest.hit=true;hitCount++;combo++;
  if(combo>maxCombo)maxCombo=combo;
  score+=combo*2;
  scoreDisplay.textContent=score;
  comboNum.textContent=combo;
  comboDisplay.classList.add('show');
  showJudge(judge,judge.toUpperCase());
  playHitSound(perfect);
  closest.el.classList.add('hit-anim');
  (function(n){setTimeout(function(){if(n.el)n.el.remove()},300)})(closest);
}

function showJudge(cls,txt){
  judgeText.className='judge-text '+cls;
  judgeText.textContent=txt;
  judgeText.classList.remove('show');
  void judgeText.offsetWidth;
  judgeText.classList.add('show');
}

function endGame(){
  state='ended';
  if(rafId)cancelAnimationFrame(rafId);
  var acc=totalNotes>0?Math.round((hitCount/totalNotes)*100):0;
  endScore.textContent=score;
  endMaxCombo.textContent=maxCombo;
  endAccuracy.textContent=acc+'%';
  if(acc>=80){
    endTitle.textContent='STYLE UNLOCKED';
    endDesc.textContent='Cinestill 800T';
    playUnlockSound();spawnConfetti();
  }else{
    endTitle.textContent='TRY AGAIN';
    endDesc.textContent='准确率 '+acc+'%，需要 80% 以上';
  }
  endOverlay.classList.remove('hidden');
}

function spawnConfetti(){
  var colors=['#E53935','#F6C83C','#4CAF50','#385E77','#F2ECE4'];
  for(var i=0;i<40;i++){
    var c=document.createElement('div');c.className='confetti';
    c.style.background=colors[Math.floor(Math.random()*colors.length)];
    c.style.left=(Math.random()*100)+'%';c.style.top='50%';
    c.style.borderRadius=Math.random()>0.5?'50%':'2px';
    gameScreen.appendChild(c);
    var a=Math.random()*Math.PI*2,v=100+Math.random()*200;
    var vx=Math.cos(a)*v,vy=Math.sin(a)*v-100,st=performance.now();
    (function(c,vx,vy,st){
      requestAnimationFrame(function an(now){
        var dt=(now-st)/1000;
        if(dt>2){c.remove();return}
        var x=vx*dt,y=vy*dt+200*dt*dt;
        c.style.transform='translate('+x+'px,'+y+'px) rotate('+(dt*360)+'deg)';
        c.style.opacity=Math.max(0,1-dt/2);
        requestAnimationFrame(an);
      });
    })(c,vx,vy,st);
  }
}

// ── 相机交互：点击在 open/closed 之间切换 ──
function updateCameraVisual(){
  if(cameraState==='open'){
    cameraSvg.innerHTML=SVG_OPEN;
    cameraStateLabel.textContent='OPEN';
    cameraStateLabel.className='camera-state-label open';
  }else{
    cameraSvg.innerHTML=SVG_CLOSED;
    cameraStateLabel.textContent='CLOSED';
    cameraStateLabel.className='camera-state-label closed';
  }
}

function resetCamera(){
  cameraState='open'; // 初始状态：打开
  isSwitching=false;
  cameraClickable.classList.remove('flash');
  updateCameraVisual();
}

function onCameraClick(){
  if(state!=='playing')return;
  if(isSwitching)return;
  isSwitching=true;
  // 切换状态
  cameraState=cameraState==='open'?'closed':'open';
  updateCameraVisual();
  cameraClickable.classList.add('flash');
  checkHit();
  // 0.3s 后解锁，允许下一次点击
  setTimeout(function(){
    cameraClickable.classList.remove('flash');
    isSwitching=false;
  },300);
}

cameraClickable.addEventListener('click',onCameraClick);
startBtn.addEventListener('click',startGame);
retryBtn.addEventListener('click',startGame);

document.addEventListener('keydown',function(e){
  if(e.code==='Space'&&state==='playing'){
    e.preventDefault();
    onCameraClick();
  }
  if(e.code==='Enter'&&state!=='playing'){startGame()}
});

// 初始化：显示打开状态
updateCameraVisual();
})();
