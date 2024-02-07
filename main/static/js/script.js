 "use strict";
 var W, H;
 var C = {
    x: 0,
    y: 0
 };
 var particles = [],
    touch = false;
 var particleCount = 0; // Initial particle count
 
 const {
    random
 } = Math;
 
 function id(n) {
    return document.getElementById(n);
 }
 
 function handleUpload() {
    // Handle the upload logic here
    alert("Upload button clicked!");
 }
 window.onload=function(){var t=id("drawing-container");function e(){W=t.clientWidth,H=t.clientHeight}function n(t){C.x=t.clientX,C.y=t.clientY,C.x||(C.x=t.touches[0].clientX,C.y=t.touches[0].clientY),touch=!0}function i(){this.x=W*random(),this.y=H*random(),this.dx=1*random()+1,this.dy=0,this.element=document.createElement("div"),this.element.className="cloud-particle",t.appendChild(this.element),this.draw=function(){this.x+=this.dx,this.x>W&&(this.x=-50),this.element.style.left=this.x+"px",this.element.style.top=this.y+"px"}}e(),window.onresize=e,t.addEventListener("touchmove",n),t.addEventListener("touchstart",n),t.addEventListener("touchend",function(){touch=!1}),t.addEventListener("mousedown",function(){t.addEventListener("mousemove",n)}),t.addEventListener("mouseup",function(){t.removeEventListener("mousemove",n),touch=!1}),setInterval(function(){!function(t){for(let e=0;e<t;e++){let t=new i;particles.push(t)}particleCount+=t,particleCount>10&&(particleCount=10)}(1)},2e3),function t(){for(let t of particles)t.draw();window.requestAnimationFrame(t)}()};