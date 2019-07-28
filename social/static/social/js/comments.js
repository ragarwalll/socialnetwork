$(".profile--wrapper").on("click", ".post--comment", function() {
  $(this)
    .parent()
    .next()
    .next()
    .next()
    .toggleClass("open");
});
