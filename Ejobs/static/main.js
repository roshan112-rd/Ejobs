// for the popup msg

let popup = document.querySelector(".popup-msg-text");
let popupCloser = document.querySelector(".popup-close");
popupCloser.addEventListener("click", () => {
  popup.parentNode.parentNode.removeChild(
    popup.parentNode
  );
});
