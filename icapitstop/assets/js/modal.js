var modal = document.getElementById("myModal");
var btn = document.getElementById("newSupplierBtn");
var span = document.getElementsByClassName("close newSupplier")[0];

btn.onclick = function() {
  modal.style.display = "block";
}
span.onclick = function() {
  modal.style.display = "none";
}
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}
function change_pass(){
  var modal = document.getElementById("myModal");
  var btn = document.getElementById("newSupplierBtn");
  var span = document.getElementsByClassName("close newSupplier")[0];

  btn.onclick = function() {
    modal.style.display = "block";
  }
  span.onclick = function() {
    modal.style.display = "none";
  }
  window.onclick = function(event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  }
}

function update_discount(){
  elem = document.getElementById("update " + id);
  elem.style.display = "block";
  spn = document.getElementsByClassName("close " + id)[0];
  spn.onclick = function(){
    elem.style.display = "none";
  }
  window.onclick = function(event){
    if (event.target == elem){
      elem.style.display = "none";
    }
  }
}

function displayAnswerMsgModal(id){
  elem = document.getElementById("answer " + id);
  elem.style.display = "block";
  spn = document.getElementsByClassName("close " + id)[0];
  spn.onclick = function(){
    elem.style.display = "none";
  }
  window.onclick = function(event){
    if (event.target == elem){
      elem.style.display = "none";
    }
  }
}

function displayReadMsgModal(id){
  elem = document.getElementById("read " + id);
  elem.style.display = "block";
  spn = document.getElementsByClassName("close " + id)[0];
  spn.onclick = function(){
    elem.style.display = "none";
  }
  window.onclick = function(event){
    if (event.target == elem){
      elem.style.display = "none";
    }
  }
}

function displayDetailsMsgModal(id){
  elem = document.getElementById("details " + id);
  elem.style.display = "block";
  spn = document.getElementsByClassName("close " + id)[0];
  spn.onclick = function(){
    elem.style.display = "none";
  }
  window.onclick = function(event){
    if (event.target == elem){
      elem.style.display = "none";
    }
  }
}

function displayMailMsgModal(id){
  elem = document.getElementById("mail " + id);
  elem.style.display = "block";
  spn = document.getElementsByClassName("close " + id)[0];
  spn.onclick = function(){
    elem.style.display = "none";
  }
  window.onclick = function(event){
    if (event.target == elem){
      elem.style.display = "none";
    }
  }
}
