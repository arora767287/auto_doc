let historyData = [];

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "collectHistory") {
        chrome.history.search({
            text: '',
            startTime: Date.now() - (7 * 24 * 60 * 60 * 1000),  // Last 7 days
            maxResults: 1000
        }, (data) => {
            historyData = data;
            sendResponse({status: "success", data: historyData});
        });
        return true;
    }
});

// Sync history periodically
setInterval(() => {
    if (historyData.length > 0) {
        fetch('http://localhost:5000/api/sync-history', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({history: historyData})
        });
    }
}, 3600000); // Every hour
