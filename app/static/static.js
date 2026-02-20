document.querySelectorAll(".delete").forEach(button => {
    button.addEventListener("click", function(event) {
        if (!confirm("Are you sure you want to delete this product?")) {
            event.preventDefault();
        }
    });
});
document.querySelectorAll(".delete").forEach(button => {
    button.addEventListener("click", function(event) {
        if (!confirm("Are you sure you want to delete this product?")) {
            event.preventDefault();
        }
    });
});
