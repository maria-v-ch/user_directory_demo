document.addEventListener('DOMContentLoaded', function() {
    const colors = [
        'var(--memphis-yellow)',
        'var(--memphis-pink)',
        'var(--memphis-blue)',
        'var(--memphis-purple)',
        'var(--memphis-orange)',
        'var(--memphis-green)'
    ];

    function getRandomColor(seed) {
        const seedRandom = new Math.seedrandom(seed);
        return colors[Math.floor(seedRandom() * colors.length)];
    }

    function applyRandomColors() {
        const seed = document.body.getAttribute('data-color-seed');
        document.querySelectorAll('.memphis-element').forEach(element => {
            element.style.color = getRandomColor(seed + element.textContent);
        });
    }

    applyRandomColors();

    // Reapply colors when navigating between pages
    document.body.addEventListener('htmx:afterSwap', applyRandomColors);
});
