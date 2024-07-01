// Declare various document elements
const feedbackForm = document.querySelector('.feedback-form');
const feedbackButton = document.querySelector('.feedback-btn');

// Event listener for feedback button, toggles feedback form
feedbackButton.addEventListener('click', (event) => {
    if (feedbackForm.style.display === 'none' 
        || feedbackForm.style.display === '') {
        feedbackForm.style.display = 'flex';
    } 
    else 
    {
        feedbackForm.style.display = 'none';
  
    }
    
});