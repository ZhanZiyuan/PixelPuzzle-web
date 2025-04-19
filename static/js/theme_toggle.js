document.addEventListener("DOMContentLoaded", function () {
    const toggleButton = document.getElementById("theme-toggle");
    const githubIcon = document.getElementById("github-icon");
    const currentTheme = localStorage.getItem("theme") || "light";
    document.body.classList.add(currentTheme + "-mode");

    // Set GitHub icon based on theme
    const updateGithubIcon = () => {
        const theme = document.body.classList.contains("light-mode")
            ? "light"
            : "dark";
        if (theme === "light") {
            githubIcon.src = "../static/images/github-mark.svg";
        } else {
            githubIcon.src = "../static/images/github-mark-white.svg";
        }
    };

    // Initial GitHub icon update
    updateGithubIcon();

    toggleButton.addEventListener("click", function () {
        const newTheme = document.body.classList.contains("light-mode")
            ? "dark"
            : "light";
        document.body.classList.remove("light-mode", "dark-mode");
        document.body.classList.add(newTheme + "-mode");
        localStorage.setItem("theme", newTheme);
        updateGithubIcon(); // Update the GitHub icon after theme change
    });

    // GitHub icon click to redirect to GitHub repository
    githubIcon.addEventListener("click", function () {
        window.open("https://github.com/ZhanZiyuan/PixelPuzzle", "_blank");
    });
});
