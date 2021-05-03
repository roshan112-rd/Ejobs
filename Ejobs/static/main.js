// for the popup msg

let popup = document.querySelector(".popup-msg-text");
let popupCloser = document.querySelector(".popup-close");
popupCloser.addEventListener("click", () => {
  popup.parentNode.parentNode.removeChild(
    popup.parentNode
  );
});

//logout
function openForm() {
  document.getElementById("myForm").style.display = "block";
}

function closeForm() {
  document.getElementById("myForm").style.display = "none";
}