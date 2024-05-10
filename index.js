const copyButtons = document.querySelectorAll(".copy-button");

copyButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const targetSelector = button.dataset.copyTarget;
      const target = document.querySelector(targetSelector);
      const text = target.textContent.trim();
      navigator.clipboard
        .writeText(text)
        .then(() => {
          console.log("Text copied to clipboard");
          button.setAttribute("data-bs-original-title", "Copied");
          button.setAttribute("title", "Copied");
          const tooltip = bootstrap.Tooltip.getInstance(button);
          tooltip.show();
        })
        .catch((err) => console.error("Failed to copy: ", err));
    });
  });

  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
});