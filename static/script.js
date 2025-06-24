document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('pdf_file');
    const urlInput = document.getElementById('pdf_url');
    const summarizeButton = document.getElementById('summarize_button');
    const summaryOutputDiv = document.getElementById('summary_output');
    const summaryTextDiv = document.getElementById('summary_text');
    const errorMessageDiv = document.getElementById('error_message');
    const errorTextP = document.getElementById('error_text');
    const loadingSpinner = document.getElementById('loading_spinner');
    const buttonText = document.getElementById('button_text');
    const copyButton = document.getElementById('copy_button');
    const copyMessage = document.getElementById('copy_message');

    // Function to hide all messages
    const hideMessages = () => {
        summaryOutputDiv.classList.add('hidden');
        errorMessageDiv.classList.add('hidden');
        copyMessage.classList.add('hidden');
    };

    // Show loading state
    const showLoading = () => {
        buttonText.textContent = 'Summarizing...';
        loadingSpinner.classList.remove('hidden');
        summarizeButton.disabled = true;
        summarizeButton.classList.add('opacity-75', 'cursor-not-allowed');
        hideMessages(); // Hide previous messages when starting new request
    };

    // Hide loading state
    const hideLoading = () => {
        buttonText.textContent = 'Summarize Paper';
        loadingSpinner.classList.add('hidden');
        summarizeButton.disabled = false;
        summarizeButton.classList.remove('opacity-75', 'cursor-not-allowed');
    };

    // Display summary
    const displaySummary = (summary) => {
        summaryTextDiv.textContent = summary;
        summaryOutputDiv.classList.remove('hidden');
    };

    // Display error
    const displayError = (message) => {
        errorTextP.textContent = message;
        errorMessageDiv.classList.remove('hidden');
    };

    summarizeButton.addEventListener('click', async () => {
        hideMessages(); // Clear previous results/errors

        const file = fileInput.files[0];
        const url = urlInput.value.trim();

        if (!file && !url) {
            displayError("Please upload a PDF file or provide a PDF URL.");
            return;
        }
        if (file && url) {
            displayError("Please provide either a PDF file OR a PDF URL, not both.");
            return;
        }

        showLoading();

        const formData = new FormData();
        if (file) {
            formData.append('pdf_file', file);
        } else if (url) {
            formData.append('pdf_url', url);
        }

        try {
            // Updated fetch URL for FastAPI endpoint
            const response = await fetch('/summarize', { 
                method: 'POST',
                body: formData,
            });

            const data = await response.json();

            if (response.ok) {
                displaySummary(data.summary);
            } else {
                displayError(data.detail || data.error || 'An unknown error occurred.'); // FastAPI errors use 'detail'
            }
        } catch (error) {
            console.error('Fetch error:', error);
            displayError('Network error or server unavailable. Please try again.');
        } finally {
            hideLoading();
        }
    });

    // Copy to clipboard functionality (using document.execCommand for wider iframe compatibility)
    copyButton.addEventListener('click', () => {
        const textToCopy = summaryTextDiv.textContent;
        const textarea = document.createElement('textarea');
        textarea.value = textToCopy;
        document.body.appendChild(textarea);
        textarea.select();
        try {
            document.execCommand('copy');
            copyMessage.classList.remove('hidden');
            setTimeout(() => {
                copyMessage.classList.add('hidden');
            }, 2000); // Hide message after 2 seconds
        } catch (err) {
            console.error('Failed to copy text: ', err);
            // Fallback for browsers that don't support execCommand('copy') or in restricted environments
            displayError("Failed to copy. Please manually select and copy the text.");
        } finally {
            document.body.removeChild(textarea);
        }
    });

    // Clear URL input if file is selected, and vice-versa
    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            urlInput.value = ''; // Clear URL if file is chosen
            hideMessages();
        }
    });

    urlInput.addEventListener('input', () => {
        if (urlInput.value.trim() !== '') {
            fileInput.value = ''; // Clear file input if URL is typed
            hideMessages();
        }
    });
});
