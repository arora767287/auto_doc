// Listen for specific events or data collection triggers
document.addEventListener('DOMContentLoaded', () => {
    // Collect page metadata
    const metadata = {
        url: window.location.href,
        title: document.title,
        timestamp: Date.now()
    };
    
    // Send to background script
    chrome.runtime.sendMessage({
        action: "pageVisited",
        data: metadata
    });
});
