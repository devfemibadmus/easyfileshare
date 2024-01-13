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
 
 window.onload = function () {
    var drawingContainer = id("drawing-container");
 
    function init() {
       W = drawingContainer.clientWidth;
       H = drawingContainer.clientHeight;
    }
    init();
    window.onresize = init;
 
    function move(e) {
       C.x = e.clientX;
       C.y = e.clientY;
       if (!C.x) {
          C.x = e.touches[0].clientX;
          C.y = e.touches[0].clientY;
       }
       touch = true;
    }
    drawingContainer.addEventListener("touchmove", move);
    drawingContainer.addEventListener("touchstart", move);
    drawingContainer.addEventListener("touchend", function () {
       touch = false;
    });
    drawingContainer.addEventListener("mousedown", function () {
       drawingContainer.addEventListener("mousemove", move);
    });
    drawingContainer.addEventListener("mouseup", function () {
       drawingContainer.removeEventListener("mousemove", move);
       touch = false;
    });
 
    function CloudParticle() {
       this.x = W * random();
       this.y = H * random();
       this.dx = 1 * random() + 1; // Cloud particle speed
       this.dy = 0;
       this.element = document.createElement("div");
       this.element.className = "cloud-particle";
       drawingContainer.appendChild(this.element);
 
       this.draw = function () {
          this.x += this.dx;
 
          if (this.x > W) {
             this.x = -50; // Move cloud particle to the left when it goes off the screen
          }
 
          this.element.style.left = this.x + "px";
          this.element.style.top = this.y + "px";
       };
    }
 
    function addCloudParticles(count) {
       for (let i = 0; i < count; i++) {
          let cloud = new CloudParticle();
          particles.push(cloud);
       }
       particleCount += count;
       if (particleCount > 10) {
          particleCount = 10;
       }
    }
 
    function animate() {
       for (let cloud of particles) {
          cloud.draw();
       }
       window.requestAnimationFrame(animate);
    }
 
    // Add cloud particles every 2 seconds
    setInterval(function () {
       addCloudParticles(1);
    }, 2000);
 
    animate();
 };