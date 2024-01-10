const contEl = document.querySelector(".cont");

const btnEl = document.querySelector(".btn1");

const popupContEl = document.querySelector(".popup-cont");

const closeIconEl = document.querySelector("#close-icon");

btnEl.addEventListener("click", () => {
  contEl.classList.add("active");
  popupContEl.classList.remove("active");
});

closeIconEl.addEventListener("click", () => {
  contEl.classList.remove("active");
  popupContEl.classList.add("active");
});
